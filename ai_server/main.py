import pika
import json
import os
from dotenv import load_dotenv
import ssl
import logging
from enum import Enum
from service import consume_message_queue, refresh_materialized_view
from dependencies.database import Base, engine
from models.models import Posts
from pika.channel import Channel

Base.metadata.create_all(bind=engine)

load_dotenv('../.env')


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


total_article_count = 0
current_article_count = 0


# 오타 방지
class Channels(Enum):
    NEW_POSTS = 'new_posts'
    REFRESH = 'refresh'


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



def publish_progress(ch):
    msg = json.dumps({"type": "progress"}, ensure_ascii=False)
    ch.basic_publish(exchange='', routing_key=Channels.REFRESH.value, body=msg)

def callback_new_posts(ch: Channel, method, properties, body):
    data = json.loads(body)
    logger.info(f"Received message: {data}")
    logger.info(f"type: {type(data)}")
    try:
        consume_message_queue(data['article']['link'], data['user_id'], data['platform'], data['article']['published_at'])
        publish_progress(ch)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        logger.error(f"Failed to process message(new_posts): {e}")
        # 실패한 경우라도 카운팅은 해야하니 publish_progress(ch)를 호출
        publish_progress(ch)
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return
    

def callback_refresh(ch: Channel, method, properties, body):
    global total_article_count, current_article_count
    data = json.loads(body)
    logger.info(f"Received message: {data}")

    try:
        msg_type = data.get('type')

        if msg_type == 'init':
            total_article_count = data['count']
            current_article_count = 0
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        current_article_count += 1
        logger.info(f"Current article count: {current_article_count}")
        logger.info(f"Total article count: {total_article_count}")
        if current_article_count == total_article_count:
            logger.info("All articles processed")
            refresh_materialized_view()
            logger.info("Materialized view refreshed")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        logger.error(f"Failed to process message(refresh): {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_worker():
    channel = get_rabbitmq_connection().channel()
    channel.queue_declare(queue=Channels.NEW_POSTS.value)
    channel.basic_consume(queue=Channels.NEW_POSTS.value, on_message_callback=callback_new_posts)
    channel.queue_declare(queue=Channels.REFRESH.value)
    channel.basic_consume(queue=Channels.REFRESH.value, on_message_callback=callback_refresh)
    channel.start_consuming()


start_worker()
