import os
import sys
import logging
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv('../.env')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("테스트")

# 1. 환경변수 확인
print("\n[1/5] 환경변수 확인")
required_env_vars = ['DATABASE_URL', 'RABBITMQ_HOST']
for var in required_env_vars:
    value = os.getenv(var)
    if value:
        # 비밀번호 부분 마스킹
        masked_value = value[:30] + "..." if len(value) > 30 else value
        print(f"✅ {var}: {masked_value}")
    else:
        print(f"❌ {var}: NOT SET")
        sys.exit(1)

# 2. DB 연결 테스트
print("\n[2/5] DB 연결 테스트")
try:
    from app.dependencies.database import SessionLocal
    db = SessionLocal()
    print("✅ Database connection successful")
    db.close()
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)

# 3. RabbitMQ 연결 테스트
print("\n[3/5] RabbitMQ 연결 테스트")
try:
    from app.dependencies.rabbitmq import get_rabbitmq_connection
    connection = get_rabbitmq_connection()
    print("✅ RabbitMQ connection successful")
    connection.close()
except Exception as e:
    print(f"❌ RabbitMQ connection failed: {e}")
    sys.exit(1)

# 4. 새 글 체크 테스트
print("\n[4/5] 새 글 체크 테스트 (check_new_posts)")
try:
    from app.services.observer_service import check_new_posts
    check_new_posts()
    print("✅ check_new_posts completed")
except Exception as e:
    print(f"❌ check_new_posts failed: {e}")
    import traceback
    traceback.print_exc()

# 5. 미업로드 사용자 체크 테스트
print("\n[5/5] 미업로드 사용자 체크 테스트 (check_inactive_users)")
try:
    from app.services.observer_service import check_inactive_users
    check_inactive_users()
    print("✅ check_inactive_users completed")
except Exception as e:
    print(f"❌ check_inactive_users failed: {e}")
    import traceback
    traceback.print_exc()

# 완료
print("✅ Integration Test Completed!")
print("\n다음 단계:")
print("1. RabbitMQ 관리 UI에서 메시지 확인")
print("2. DB에서 last_upload 업데이트 확인")
print("3. 스케줄러 실행: python main.py")
