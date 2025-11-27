import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import os
from dotenv import load_dotenv
from openai import OpenAI
import re  

load_dotenv()

# Upstage API 설정
client = OpenAI(
    api_key=os.environ.get("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1/solar"
)
UPSTAGE_MODEL = 'solar-1-mini-chat'


def normalize_date(date_str: str) -> str:
    if not date_str:
        return "날짜 정보 없음"
    
    match = re.search(r'(\d{4})[\.\-\/]\s*(\d{1,2})[\.\-\/]\s*(\d{1,2})', date_str)
    
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"
    
    return date_str # 변환 실패 시 원본 반환


def crawl_webpage(url: str) -> Dict[str, str]:
    print(f"크롤링 시작: {url}")
    
    if "blog.naver.com" in url and "m.blog.naver.com" not in url:
        url = url.replace("blog.naver.com", "m.blog.naver.com")

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # 제목 추출
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            title = og_title['content']
        else:
            title = soup.title.string if soup.title else "제목 없음"

        # 날짜 추출 (원본 문자열 확보)
        raw_date = ""
        published_time = soup.find('meta', property='article:published_time')
        naver_date = soup.find('p', class_='blog_date')
        common_date = soup.find(class_='date')

        if published_time and published_time.get('content'):
            raw_date = published_time['content']
        elif naver_date:
            raw_date = naver_date.get_text().strip()
        elif common_date:
            raw_date = common_date.get_text().strip()
            
        # 날짜 포맷팅 적용 (YYYY-MM-DD)
        formatted_date = normalize_date(raw_date)

        # 본문 추출
        paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
        content = " ".join(paragraphs)

        return {
            "title": title,
            "date": formatted_date, # 포맷팅된 날짜 반환
            "content": content[:5000]
        }

    except Exception as e:
        print(f"크롤링 오류 발생: {e}")
        return {}


def classify_topics_with_upstage(text: str) -> List[str]:
    if not text:
        return []

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
        topics = [topic.strip() for topic in content.split(',') if topic.strip()]
        return topics[:2]

    except Exception as e:
        print(f"Upstage API 오류 발생: {e}")
        return []

def save_to_db(url: str, title: str, date: str, topics: List[str]):
    if topics:
        # print(f"   - 제목: {title}")
        # print(f"   - 날짜: {date}") # YYYY-MM-DD 형식
        # print(f"   - URL : {url}")
        # print(f"   - 주제: {', '.join(topics)}")
        pass
    else:
        # print(f"저장 건너뜀: {url} (주제 없음)")
        pass


def consume_message_queue():
    sample_links = [
        "https://blog.naver.com/gurwn1725/224009540423", 
        "https://zio2017.tistory.com/99", 
    ]

    for link in sample_links:
        print("\n========================================")
        crawled_data = crawl_webpage(link)
        
        content = crawled_data.get("content", "")
        title = crawled_data.get("title", "")
        date = crawled_data.get("date", "")

        if content:
            input_text = f"제목: {title}\n본문: {content}"
            topics = classify_topics_with_upstage(input_text)
            
            save_to_db(link, title, date, topics)
        else:
            print("크롤링 된 텍스트가 없어 건너뜁니다.")

        time.sleep(2) 

    print("\n--- 모든 시뮬레이션 메시지 처리 완료 ---")


if __name__ == "__main__":
    consume_message_queue()