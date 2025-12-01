import os
import json
import logging
import smtplib
from rabbitmq import get_connection, start_consumer
import sys
from email.mime.text import MIMEText

#환경변수
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
SMTP_SERVER = os.environ.get("SMTP_SERVER")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")

rabbitmq_url = os.getenv("RABBITMQ_HOST")
sender_email = SMTP_USER

#로깅설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

#메일보내는 함수
def send_email(recipient: str, subject: str, body_content: str):
    try:
        msg = MIMEText(body_content)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient

        logger.info(f"[SMTP] Connecting to {SMTP_SERVER}...")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(sender_email, recipient, msg.as_string())

            logger.info(f"[SMTP] Email sent seccessfully to {recipient}")
        
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP 인증 실패: 사용자 이름/비밀번호를 확인하세요.")
    except smtplib.SMTPException as e:
        logger.info(f"SMTP 전송 중 오류 발생: {e}")
    except Exception as e:
        logger.error(f"예상치 못한 오류 발생: {e}", exc_info=True)


#콜백 함수 정의
def mail_reminder_callback(ch, method, properties, body):
    #메시지 처리 흐름 제어, send mail함수 호출
    ack_needed = True # ACK 상태 플래그
    requeue = False # 재처리 요청 플래그
    try:
        message_data = json.loads(body.decode('utf-8'))

        user_email = message_data.get("email")
        user_name = message_data.get("name", "사용자")
        days_inactive = message_data.get("days_inactive")

        if not user_email:
            logger.error(f"메시지에 이메일 정보가 없습니다. 데이터: {message_data}")
            requeue = False
        
        else:
            subject = f"[jandi] {user_name}님, 잔디밭이 비고 있어요! "
            body_content = (
                f"안녕하세요, {user_name}님. \n 마지막 활동 이후 벌써 {days_inactive}일이 지났습니다. "
                f"새 글을 써서 잔디밭을 채우러 가 볼까요?"
            )

            send_email(recipient = user_email, subject = subject, body_content=body_content)

    except json.JSONDecodeError:
        logger.error(f"메시지 파싱 실패: 잘못된 JSON형식 - Body : {body}")
        requeue = True
    except Exception as e:
        logger.error(f"메시지 처리 중 예외 발생: {e}", exc_info=True)
        requeue = True
    finally:
        if requeue:
            # 오류가 발생했거나 재처리할 필요가 있을 때 NACK 호출 (메시지 큐로 되돌림)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            logger.warning(f"NACK sent for delivery tag: {method.delivery_tag}. 메시지를 큐로 돌려보냄.")
        elif ack_needed:
            # 정상적으로 처리 완료되었을 때 ACK 호출
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"ACK sent for delivery tag: {method.delivery_tag}")


#프로그램 실행
if __name__ == "__main__":
    if not os.environ.get("SMTP_SERVER"):
        logger.critical("SMRP_SERVER가 설정되지 않았습니다. 메일 발송 기능이 작동하지 않습니다.")

    MAIL_QUEUE = "mail_reminders"
    
    logger.info("소비자 서버 초기화 중...")

    try:
        start_consumer(rabbitmq_url,MAIL_QUEUE, mail_reminder_callback)
    except Exception as e:
        logger.critical(f"소비자 서버 실행 중 치명적 오류 발생: {e}")
    