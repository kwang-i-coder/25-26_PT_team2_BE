import os
import sys
import logging
from datetime import datetime

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv('../.env')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 현재 DB 상태 확인
from app.services.platform_service import get_all_user_platforms

print("=" * 60)
print("1. 현재 DB 상태 확인")
print("=" * 60)

user_platforms = get_all_user_platforms()

if not user_platforms:
    print("DB에 user_platform 데이터가 없습니다!")
    print("\n해결 방법:")
    print("1. main_server에서 사용자 등록")
    print("2. 플랫폼 등록 (티스토리: kwang-i-coder, Velog: jdk829355)")
    sys.exit(1)

print(f"\n총 {len(user_platforms)}개의 user-platform 발견:")
for up in user_platforms:
    print(f"\n- User ID: {up.user_id}")
    print(f"  Platform: {up.platform_name}")
    print(f"  Account ID: {up.account_id}")
    print(f"  Last Upload: {up.last_upload}")

print("\n" + "=" * 60)
print("2. observer_service.check_new_posts() 실행")
print("=" * 60)

from app.services.observer_service import check_new_posts

check_new_posts()

print("\n" + "=" * 60)
print("3. 업데이트된 DB 상태 확인")
print("=" * 60)

user_platforms_after = get_all_user_platforms()

for up in user_platforms_after:
    print(f"\n- User ID: {up.user_id}")
    print(f"  Platform: {up.platform_name}")
    print(f"  Account ID: {up.account_id}")
    print(f"  Last Upload: {up.last_upload}")

print("\n 테스트 완료!")
