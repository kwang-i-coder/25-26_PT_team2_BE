import requests
from bs4 import BeautifulSoup
import time
from typing import List
import os
from dotenv import load_dotenv
from openai import OpenAI  

load_dotenv()

# Upstage API 설정
# Upstage는 OpenAI 호환 API를 제공하므로 base_url을 지정하여 사용합니다.
client = OpenAI(
    api_key=os.environ.get("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1/solar"
)
UPSTAGE_MODEL = 'solar-1-mini-chat'  # 또는 'solar-pro'


def crawl_webpage(url: str) -> str:
    """주어진 URL의 웹페이지 내용을 크롤링하여 텍스트로 반환합니다."""
    print(f"크롤링 시작: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else ""
        
        paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
        content = " ".join(paragraphs)

        full_text = f"제목: {title}\n본문: {content}"
        return full_text[:5000]  # 토큰 제한 고려하여 길이 

    except Exception as e:
        print(f"크롤링 오류 발생: {e}")
        return ""


def classify_topics_with_upstage(text: str) -> List[str]:
    """텍스트를 분석하여 지정된 5개 카테고리 중 상위 2개를 추출합니다."""
    if not text:
        return []

    # 프롬프트 수정: 5개 카테고리 중 선택하도록 지시, 키워드 하나만 사용하라고 해도 됨
    prompt = (
        "다음 텍스트를 분석하여 아래 5가지 카테고리 중 가장 연관성이 높은 2가지를 선택하세요.\n"
        "1. tech\n"
        "2. life\n"
        "3. food\n"
        "4. travel\n"
        "5. review\n\n"
        "반드시 위 목록에 있는 단어만 사용해야 하며, 가장 가능성이 높은 순서대로 2개를 쉼표(,)로 구분하여 출력하세요.\n"
        "다른 설명이나 문장은 절대 포함하지 마세요.\n"
        "예시: tech, review\n\n"
        f"분석할 텍스트:\n---\n{text}"
    )

    print("Upstage Solar API 호출 중...")
    try:
        response = client.chat.completions.create(
            model=UPSTAGE_MODEL,
            messages=[
                {"role": "system", "content": "You are a text classifier. Output only the category names."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        
        # 쉼표로 분리하여 리스트 반환
        topics = [
            topic.strip() 
            for topic in content.split(',')
            if topic.strip() 
        ]
        
        return topics[:2] # 상위 2개만 반환

    except Exception as e:
        print(f"Upstage API 오류 발생: {e}")
        return []

def save_to_db(url: str, topics: List[str]):
    if topics:
        print(f"   - URL: {url}")
        print(f"   - 주제: {', '.join(topics)}")
    else:
        print(f"저장 건너뜀: {url} (주제 없음)")


def consume_message_queue():
    print("--- 메시지 큐 구독 및 소비 루틴 시작 ---")

    sample_links = [
        "https://blog.naver.com/gurwn1725/224009540423", 
        "https://zio2017.tistory.com/99", 
    ]

    for link in sample_links:
        print("\n========================================")
        crawled_text = crawl_webpage(link)
        
        if crawled_text:
            topics = classify_topics_with_upstage(crawled_text)
            save_to_db(link, topics)
        else:
            print("크롤링 된 텍스트가 없어 건너뜁니다.")

        time.sleep(2) # API 속도 제한 고려

    print("\n--- 모든 시뮬레이션 메시지 처리 완료 ---")


if __name__ == "__main__":
    consume_message_queue()