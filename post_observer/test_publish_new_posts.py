from app.dependencies.rabbitmq import publish_message
from dotenv import load_dotenv
from app.parsers.velog import VelogRSSParser
from app.parsers.tistory import TistoryRSSParser
from app.parsers.naver import NaverRSSParser
from app.models.schemas import NewPostMessageSchema
import time
import json
load_dotenv()

test_data = []
test_user_id = "a26d2458-dd35-4a3e-a871-0266d1130b54"
test_platform = [{
    "name": "velog", "account_id": "jdk829355", "user_id": test_user_id}, {"name": "tistory", "account_id": "dev-jdk829355", "user_id": test_user_id}, {"name": "naver", "account_id": "yunaji2319", "user_id": "c97eafdc-621e-41c5-ab04-a0b0702b0026"}]



for platform in test_platform[:2]:
    if platform["name"] == "velog":
        parser = VelogRSSParser()
    elif platform["name"] == "tistory":
        parser = TistoryRSSParser()
    elif platform["name"] == "naver":
        parser = NaverRSSParser()
    articles = parser.parse(platform["account_id"])
    for article in articles:
        test_data.append(NewPostMessageSchema(user_id=platform["user_id"], platform=platform["name"], article=article))

time.sleep(5)
publish_message("refresh", {
    "type": "init",
    "count": len(test_data)
})
for data in test_data:
    publish_message("new_posts", {
        "user_id": data.user_id,
        "platform": data.platform,
        "article": {
            "link": data.article.link,
            "published_at": data.article.published_at.strftime("%Y-%m-%d"),
            "title": data.article.title
        }
    })
    time.sleep(2)
    
