"""
RSS 파서 테스트 스크립트
티스토리, Velog 테스트
"""
import sys
sys.path.insert(0, '/Users/a/25-26_PT_team2_BE/post_observer')

from app.parsers.tistory import TistoryRSSParser
from app.parsers.velog import VelogRSSParser

def test_parser(parser_name, parser, account_id):
    """파서 테스트 함수"""
    print("=" * 60)
    print(f"{parser_name} RSS 파서 테스트")
    print("=" * 60)

    print(f"\n계정 ID: {account_id}")
    print(f"RSS URL: {parser.get_rss_url(account_id)}")
    print("\nRSS 파싱 중...")

    try:
        articles = parser.parse(account_id)

        print(f"\n성공! 발견된 글: {len(articles)}개\n")

        # 최근 3개 글만 출력
        for i, article in enumerate(articles[:3], 1):
            print(f"{i}. 제목: {article.title}")
            print(f"   링크: {article.link}")
            print(f"   발행: {article.published_at}")
            print(f"   썸네일: {article.thumbnail}")
            print(f"   태그: {article.tags}")
            print()

        if len(articles) > 3:
            print(f"... 외 {len(articles) - 3}개 글")

        return True

    except Exception as e:
        print(f"\n실패: {e}")
        import traceback
        traceback.print_exc()
        return False

# 테스트 실행
print("\n" + "=" * 60)
print("RSS 파서 통합 테스트")
print("=" * 60 + "\n")

results = []

# tistory
tistory_result = test_parser("티스토리", TistoryRSSParser(), "kwang-i-coder")
results.append(("티스토리", tistory_result))
print("\n")

# velog
velog_result = test_parser("Velog", VelogRSSParser(), "jdk829355")
results.append(("Velog", velog_result))
print("\n")

# 최종 결과
print("=" * 60)
print("테스트 결과 요약")
print("=" * 60)
for platform, result in results:
    status = "성공" if result else "실패"
    print(f"{platform}: {status}")
print("=" * 60)
