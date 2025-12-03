export const TOPIC_COLORS: Record<string, string> = {
    life: 'bg-stone-200',
    travel: 'bg-slate-300',
    food: 'bg-orange-300',
    review: 'bg-rose-300',
    tech: 'bg-red-400',
    '7일 연속 작성': 'bg-amber-400',
};

export const CATEGORY_TRANSLATIONS: Record<string, string> = {
    "life": '일상/라이프',
    "travel": '여행',
    "food": '음식/맛집',
    "review": '리뷰',
    "tech": '기술/개발',
};

export const TOPIC_HEX_COLORS: Record<string, string> = {
    life: '#e7e5e4', // stone-200
    travel: '#cbd5e1', // slate-300
    food: '#fdba74', // orange-300
    review: '#fda4af', // rose-300
    tech: '#f87171', // red-400
    '7일 연속 작성': '#fbbf24', // amber-400
};

export const getTopicColor = (category: string): string => {
    const normalizedCategory = category.toLowerCase().trim();
    return TOPIC_COLORS[normalizedCategory] || 'bg-slate-100';
};

export const getTopicHexColor = (category: string): string => {
    const normalizedCategory = category.toLowerCase().trim();
    return TOPIC_HEX_COLORS[normalizedCategory] || '#f1f5f9'; // slate-100
};

export const getTopicName = (category: string): string => {
    const normalizedCategory = category.toLowerCase().trim();
    return CATEGORY_TRANSLATIONS[normalizedCategory] || category;
};
