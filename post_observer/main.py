import time
import os

# 컨테이너가 시작될 때 로그 출력
print(f"🚀 Service Started: {os.getenv('HOSTNAME', 'Worker')}")

try:
    # 무한 루프를 돌면서 프로세스가 죽지 않게 함
    while True:
        # 60초마다 한 번씩만 깨어남 (CPU 낭비 방지)
        time.sleep(60)
        # 살아있다는 생존 신고 로그 (선택 사항)
        print("💤 Worker is idle... waiting for real code implementation.")

except KeyboardInterrupt:
    print("🛑 Service Stopping...")