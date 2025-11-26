#로그인 인증 메일 발송
#fastapi-mail 사용
# app/internal/email_service.py

import os
from dotenv import load_dotenv
from email.message import EmailMessage
import aiosmtplib
from typing import Optional

load_dotenv()

# env에서 읽어옴
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")            
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")   
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
MAIL_FROM = os.getenv("MAIL_FROM", SMTP_USER)  

async def send_verification_email(email: str, token: str) -> None:
    """
    이메일 인증 메일 전송 (비동기)
    - email: 수신자 이메일
    - token: 인증 토큰 (URL에 포함)
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        raise RuntimeError("SMTP_USER 또는 SMTP_PASSWORD가 설정되지 않았습니다. .env를 확인하세요.")

    verify_url = f"{FRONTEND_URL.rstrip('/')}/verify-email?token={token}"

    html_body = f"""
    <html>
      <body>
        <h3>이메일 인증을 완료해주세요</h3>
        <p>아래 버튼을 클릭하면 인증이 완료됩니다:</p>
        <p>
          <a href="{verify_url}"
             style="display:inline-block;padding:10px 20px;background:#4CAF50;color:white;text-decoration:none;">
             이메일 인증하기
          </a>
        </p>
        <hr />
        <p>감사합니다.</p>
      </body>
    </html>
    """

    plain_body = f"이메일 인증을 완료하려면 다음 링크로 방문하세요: {verify_url}"

    msg = EmailMessage()
    msg["From"] = MAIL_FROM
    msg["To"] = email
    msg["Subject"] = "이메일 인증 요청"
    msg.set_content(plain_body)
    msg.add_alternative(html_body, subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_SERVER,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USER,
            password=SMTP_PASSWORD,
        )
    except Exception as e:
        raise
