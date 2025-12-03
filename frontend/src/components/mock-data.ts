import { subDays } from 'date-fns';

export interface Post {
  date: Date;
  topicId: string;
  title: string;
  platform: string;
}

export interface Topic {
  id: string;
  name: string;
  color: string;
}

export function generateMockData() {
  const topics: Topic[] = [
    { id: 'tech', name: '기술/개발', color: 'bg-blue-500' },
    { id: 'life', name: '일상/라이프', color: 'bg-green-500' },
    { id: 'travel', name: '여행', color: 'bg-purple-500' },
    { id: 'food', name: '음식/맛집', color: 'bg-orange-500' },
    { id: 'review', name: '리뷰', color: 'bg-pink-500' },
  ];

  const platforms = ['tistory', 'naver', 'velog', 'medium'];
  
  const titleTemplates = {
    tech: [
      'React 18의 새로운 기능 정리',
      'TypeScript 타입 시스템 이해하기',
      '웹 성능 최적화 팁',
      'Next.js로 블로그 만들기',
      'CSS Grid 완벽 가이드',
      '자바스크립트 비동기 처리',
      'Docker 입문 가이드',
      'Git 브랜칭 전략',
    ],
    life: [
      '주말 루틴 정리',
      '올해의 목표와 다짐',
      '책 읽기 습관 만들기',
      '재택근무 환경 개선하기',
      '미니멀 라이프 실천기',
      '아침 운동의 효과',
      '시간 관리 방법',
    ],
    travel: [
      '제주도 3박 4일 여행기',
      '부산 카페 투어',
      '서울 핫플레이스 추천',
      '강릉 바다 여행',
      '경주 역사 탐방',
      '전주 맛집 투어',
      '속초 겨울 여행',
    ],
    food: [
      '홈카페 디저트 레시피',
      '강남 맛집 추천',
      '집에서 만드는 파스타',
      '브런치 카페 탐방',
      '베이킹 도전기',
      '건강한 샐러드 레시피',
      '와인 페어링 가이드',
    ],
    review: [
      '최근 읽은 책 리뷰',
      '갤럭시 신제품 후기',
      '에어팟 프로 2 사용기',
      '노트북 구매 가이드',
      '생산성 앱 추천',
      '키보드 리뷰',
      '모니터 구매 후기',
    ],
  };

  const posts: Post[] = [];
  const today = new Date();

  // Generate posts for the last 12 months
  for (let i = 0; i < 365; i++) {
    const date = subDays(today, i);
    
    // Random chance of posting (30% chance per day)
    if (Math.random() > 0.7) {
      // Sometimes post multiple times a day
      const numPosts = Math.random() > 0.8 ? 2 : 1;
      
      for (let j = 0; j < numPosts; j++) {
        const topic = topics[Math.floor(Math.random() * topics.length)];
        const titles = titleTemplates[topic.id as keyof typeof titleTemplates];
        const title = titles[Math.floor(Math.random() * titles.length)];
        const platform = platforms[Math.floor(Math.random() * platforms.length)];
        
        posts.push({
          date,
          topicId: topic.id,
          title,
          platform,
        });
      }
    }
  }

  return {
    posts: posts.sort((a, b) => a.date.getTime() - b.date.getTime()),
    topics,
  };
}
