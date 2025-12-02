"""
RabbitMQ Connection Module
RabbitMQ 연결 및 메시지 발행
"""

import os
import ssl
import pika
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def get_rabbitmq_connection():
    """
    RabbitMQ 연결 생성

    Returns:
        pika.BlockingConnection: RabbitMQ 연결 객체
    """
    rabbitmq_url = os.getenv("RABBITMQ_HOST")

    if not rabbitmq_url:
        raise ValueError("RABBITMQ_HOST environment variable not set")

    try:
        # URL 파싱하여 연결 파라미터 생성
        params = pika.URLParameters(rabbitmq_url)

        # SSL 인증서 검증 비활성화 (CloudAMQP 연결용)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        params.ssl_options = pika.SSLOptions(ssl_context)

        connection = pika.BlockingConnection(params)
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")
        raise

def publish_message(queue_name: str, message: Dict[str, Any]):
    """
    RabbitMQ 큐에 메시지 발행

    Args:
        queue_name: 큐 이름
        message: 발행할 메시지 (dict)
    """
    connection = None
    try:
        # 연결 생성
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # 큐 선언 (존재하지 않으면 생성)
        channel.queue_declare(queue=queue_name, durable=False)

        # 메시지 발행
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message, ensure_ascii=False),
            properties=pika.BasicProperties(
                delivery_mode=2,  # 메시지 영구 저장
            )
        )

        # logger.info(f"Published message to queue '{queue_name}': {message.get('article', {}).get('title', 'N/A')}")

    except Exception as e:
        logger.error(f"Failed to publish message to RabbitMQ: {e}")
        raise
    finally:
        if connection and not connection.is_closed:
            connection.close()