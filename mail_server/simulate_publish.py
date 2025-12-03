#Producer(Post Observer)가 메시지를 넣었을 때, Consumer(Mail Worker)가 그것을 받아 이메일을 발송하는지
import os
import sys
import json
import logging
import pika # 메시지 속성 설정을 위해 pika 임포트
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv('.env') 
# RabbitMQ 함수 임포트
from rabbitmq import get_connection

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('PublisherSimulator')

# --- 설정 ---
MAIL_QUEUE = "mail_reminders"

# post_observer가 보낼 형식과 동일한 Mock 데이터
TEST_USER_DATA = {
    "user_id": "test-user-sim",
    "email": "test-recipient@example.com", # 🚨 실제 테스트 이메일 주소로 변경하세요!
    "name": "테스트 사용자",
    "days_inactive": 40, # 40일 미활동 시뮬레이션
    "last_upload": (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d")
}

def publish_mock_message():
    """
    RabbitMQ에 Mock 데이터를 발행하여 Consumer의 작동을 유도합니다.
    """
    logger.info("=" * 50)
    logger.info(f"RabbitMQ 메시지 발행 시뮬레이션 시작 (Queue: {MAIL_QUEUE})")
    logger.info("=" * 50)
    
    rabbitmq_url = os.environ.get("RABBITMQ_HOST")
    if not rabbitmq_url:
        logger.error("❌ RABBITMQ_URL 환경 변수가 설정되지 않았습니다.")
        sys.exit(1)

    connection = None
    try:
        # 1. RabbitMQ 연결 및 채널 생성
        connection = get_connection(rabbitmq_url)
        channel = connection.channel()

        # 2. 큐 선언 (Consumer와 동일한 설정 유지)
        channel.queue_declare(queue=MAIL_QUEUE, durable=False)
        
        # 3. 메시지 준비 및 발행
        message_body = json.dumps(TEST_USER_DATA)
        
        channel.basic_publish(
            exchange='',
            routing_key=MAIL_QUEUE,
            body=message_body.encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )

        logger.info("✅ Mock 메시지 발행 성공!")
        logger.info(f"   수신자 이메일: {TEST_USER_DATA['email']}")
        logger.warning("   (Consumer 서버의 로그와 수신 메일함을 확인하세요)")

    except Exception as e:
        logger.error(f"❌ 메시지 발행 중 오류 발생: {type(e).__name__} - {e}")
        sys.exit(1)

    finally:
        if connection and not connection.is_closed:
            connection.close()

if __name__ == "__main__":
    publish_mock_message()