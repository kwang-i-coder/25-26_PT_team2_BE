import pika
import logging
import smtplib
import ssl


#프로그램 실행되는 동안 발생하는 이벤트 기록
logger = logging.getLogger(__name__)

#rabbitmq에 연결하는 함수, rabbitmq_url을 받고 connection을 리턴
def get_connection(rabbitmq_url:str):
    """
    RabbitMQ 연결 생성

    Returns:
        pika.BlockingConnection: RabbitMQ 연결 객체
    """

    if not rabbitmq_url:
        raise ValueError("RABBITMQ_HOST environment variable not set")
    
    # 🚨 디버깅을 위해 입력된 URL을 로그에 출력합니다. (임시)
    # 실제 URL 전체를 출력하면 보안 문제가 있을 수 있으므로, 일부를 마스킹하는 것이 좋습니다.
    # 여기서는 문제 진단을 위해 일단 전체 길이를 출력합니다.
    logger.info(f"RABBITMQ_URL 길이: {len(rabbitmq_url)}") 
    logger.info(f"RABBITMQ_URL 시작 10자: {rabbitmq_url[:10]}")

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


#소비 시작하는 함수, queue이름과 콜백함수를 받고 사용자 이메일을 리턴함
def start_consumer(rabbitmq_url:str, queue_name: str, callback_function):
    connection = None
    try:
        # 연결 생성
        connection = get_connection(rabbitmq_url)
        channel = connection.channel()

        # 소비자가 한 번에 1개의 메시지만 가져오도록 제한
        channel.basic_qos(prefetch_count=1)

        # 큐 선언
        channel.queue_declare(queue=queue_name, durable = True)

        #콜백 함수 등록하고 소비시작
        channel.basic_consume(queue_name,
            #콜백함수, 메시지 들어오면 pika가 그걸 인수로 콜백함수 호출
            on_message_callback=callback_function, 
            auto_ack=False)
        
        logger.info(f' [*] 큐 "{queue_name}"에서 메시지 대기 중. 종료하려면 CTRL+C를 누르세요.')
        channel.start_consuming() #무한루프시작
        
    except KeyboardInterrupt:
        logger.info("사용자에 의해 소비 종료 요청.")
    except pika.exceptions.ChannelClosedByBroker as e:
        logger.error(f"🚨 채널 닫힘 오류: {e}. Worker를 재시작해야 합니다.")
    except Exception as e:
        logger.error(f"소비자 실행 중 치명적인 오류 발생: {e}")
        raise
    finally:
        #루프 종료 시 연결 닫기
        if connection and not connection.is_closed:
            logger.info("RabbitMQ 연결 닫기.")
            connection.close()

    

    