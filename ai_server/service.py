import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict
import os
from dotenv import load_dotenv
from openai import OpenAI
import re  
from dependencies.database import DbSession
from models.models import Posts, Platform
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

load_dotenv()

# Upstage API 설정
client = OpenAI(
    api_key=os.environ.get("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1/solar"
)
UPSTAGE_MODEL = 'solar-1-mini-chat'

logger = logging.getLogger(__name__)



def _normalize_date(date_str: str) -> str:
    if not date_str:
        return "날짜 정보 없음"
    
    match = re.search(r'(\d{4})[\.\-\/]\s*(\d{1,2})[\.\-\/]\s*(\d{1,2})', date_str)
    
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"
    
    return date_str # 변환 실패 시 원본 반환


def _crawl_webpage(url: str) -> Dict[str, str]:
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
        # raw_date = ""
        # published_time = soup.find('meta', property='article:published_time')
        # naver_date = soup.find('p', class_='blog_date')
        # common_date = soup.find(class_='date')

        # if published_time and published_time.get('content'):
        #     raw_date = published_time['content']
        # elif naver_date:
        #     raw_date = naver_date.get_text().strip()
        # elif common_date:
        #     raw_date = common_date.get_text().strip()
            
        # # 날짜 포맷팅 적용 (YYYY-MM-DD)
        # formatted_date = _normalize_date(raw_date)

        # 본문 추출
        paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
        content = " ".join(paragraphs)

        return {
            "title": title,
            # "date": formatted_date, # 포맷팅된 날짜 반환
            "content": content[:5000]
        }

    except Exception as e:
        print(f"크롤링 오류 발생: {e}")
        return {}


def _classify_topics_with_upstage(text: str) -> List[str]:
    if not text:
        return []

    prompt = (
        "다음 텍스트를 분석하여 아래 5가지 카테고리 중 가장 연관성이 높은 2가지를 선택하세요.\n"
        "1. 기술 / 프로그래밍\n"
        "2. AI / 머신러닝\n"
        "3. 공부 / 학습법\n"
        "4. 커리어 / 자기계발\n"
        "5. 비즈니스 / 사이드 프로젝트\n"
        "6. 블로그·콘텐츠 제작\n"
        "7. 앱·웹 서비스 리뷰\n"
        "8. 여행 / 일상\n"
        "9. 취미 / 라이프스타일\n"
        "10. 사회 / 생각 / 철학\n"
        "11. 기타\n"
        "반드시 위 목록에 있는 단어만 사용해야 하며, 가장 가능성이 높은 순서대로 2개를 쉼표(,)로 구분하여 출력하세요.\n"
        "다른 설명이나 문장은 절대 포함하지 마세요.\n"
        "예시: 기술 / 프로그래밍, 공부 / 학습법\n\n"
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

def _save_to_db(url: str, title: str, date: str, topics: List[str], user_id: str, platform_name: str):
    if topics:
        print(f"   - 제목: {title}")
        print(f"   - 날짜: {date}") # YYYY-MM-DD 형식
        print(f"   - URL : {url}")
        print(f"   - 주제: {', '.join(topics)}")
        print(f"   - user_id: {user_id}")
        print(f"   - platform_name: {platform_name}")
        db: Session = DbSession()
        try:
            platform_id: Platform | None = db.query(Platform).filter(Platform.name == platform_name).first()
            if not platform_id:
                raise ValueError(f"Platform not found: {platform_name}")
            db.add(Posts(url=url, user_id=user_id, platform_id=platform_id.platform_id, date=date, category=topics[0], title=title))
            db.commit()
            db.close()
            logger.info(f"Saved to DB: {url}")
        except Exception as e:
            db.rollback()
            db.close()
            logger.error(f"Failed to save to DB: {url}")
    else:
        logger.info(f"No topics found for URL: {url}")

def _check_exist_post(url: str):
    db: Session = DbSession()
    exist_post: Posts | None = db.query(Posts).filter(Posts.url == url).first()
    if exist_post:
        logger.info(f"Post already exists: {url}")
        db.close()
        return True
    db.close()
    return False

def refresh_materialized_view():
    db: Session = DbSession()
    try:
        db.execute(text('REFRESH MATERIALIZED VIEW "POST_AGG"'))
        logger.info("Refreshed materialized view: POST_AGG")
        db.execute(text('REFRESH MATERIALIZED VIEW "USER_STAT"'))
        logger.info("Refreshed materialized view: USER_STAT")
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update materialized view: {e}")
    finally:
        db.close()

def consume_message_queue(link: str, user_id: str, platform_name: str, date: str):
    print("\n========================================")
    if _check_exist_post(link):
        return
    crawled_data = _crawl_webpage(link)
    
    content = crawled_data.get("content", "")
    title = crawled_data.get("title", "")

    if content:
        input_text = f"제목: {title}\n본문: {content}"
        topics = _classify_topics_with_upstage(input_text)
        _save_to_db(link, title, date, topics, user_id, platform_name)
    else:
        logger.info("No content found for URL: {url}")

    time.sleep(2) 


if __name__ == "__main__":
    sample_links = [
        ["https://blog.naver.com/gurwn1725/224009540423", "test_id", "naver"], 
        ["https://zio2017.tistory.com/99", "test_id", "tistory"], 
    ]
    for link in sample_links:
        consume_message_queue(*link)