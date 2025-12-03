import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { TrendingUp, Calendar, FileText, ExternalLink, Loader2, ChevronDown, ChevronUp } from 'lucide-react';
import { format, parseISO } from 'date-fns';
import { ko } from 'date-fns/locale';
import { useState } from 'react';
import { api } from '../utils/api';
import { getTopicColor, getTopicName, getTopicHexColor } from '../constants/topicConstants';

interface UserStats {
  duration: number;
  category: Array<{ category: string; count: number }>;
  count: number;
  created_at: string;
}

interface Post {
  url: string;
  category: string;
  date: string;
  title: string;
  platform: string;
}

const PostItem = ({ post }: { post: Post }) => {
  return (
    <a
      href={post.url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-start gap-4 p-4 w-full rounded-lg border border-slate-200 hover:border-green-500 hover:bg-green-50 transition-all group bg-white hover:shadow-sm"
    >
      <div className="flex flex-col gap-2 flex-1 min-w-0">
        <h4 className="font-medium text-slate-900 text-base leading-relaxed group-hover:text-green-700 break-keep">
          {post.title}
        </h4>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span className="font-medium text-slate-600">{post.date}</span>
          <span className="w-0.5 h-0.5 bg-slate-300 rounded-full" />
          <span className="capitalize">{post.platform}</span>
        </div>
      </div>
      <ExternalLink className="size-4 text-slate-400 group-hover:text-green-600 flex-shrink-0 mt-1" />
    </a>
  );
};

interface TopicStatsProps {
  stats: UserStats | null;
}



export function TopicStats({ stats }: TopicStatsProps) {
  const [expandedCategories, setExpandedCategories] = useState<string[]>([]);
  const [postsCache, setPostsCache] = useState<Record<string, Post[]>>({});
  const [loadingCategories, setLoadingCategories] = useState<string[]>([]);

  const toggleCategory = async (category: string) => {
    if (expandedCategories.includes(category)) {
      setExpandedCategories(prev => prev.filter(c => c !== category));
      return;
    }

    setExpandedCategories(prev => [...prev, category]);

    if (!postsCache[category]) {
      setLoadingCategories(prev => [...prev, category]);
      try {
        const fetchedPosts = await api.getUserPosts(category);
        setPostsCache(prev => ({ ...prev, [category]: fetchedPosts }));
      } catch (error) {
        console.error('Failed to fetch posts:', error);
        setPostsCache(prev => ({ ...prev, [category]: [] }));
      } finally {
        setLoadingCategories(prev => prev.filter(c => c !== category));
      }
    }
  };
  if (!stats) {
    return (
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardContent className="pt-6">
            <p className="text-slate-500 text-center">데이터를 불러오는 중...</p>
          </CardContent>
        </Card>
      </div>
    );
  }

  const totalPosts = stats.count;
  const activeDays = stats.duration;

  // Translate top category if exists
  const topCategoryRaw = stats.category.length > 0 ? stats.category[0] : null;
  const topCategoryName = topCategoryRaw
    ? getTopicName(topCategoryRaw.category)
    : '-';

  // Calculate topic statistics with colors
  const topicStats = stats.category.map(cat => {
    const percentage = (cat.count / totalPosts) * 100;
    const translatedName = getTopicName(cat.category);
    const color = getTopicColor(cat.category);
    const hexColor = getTopicHexColor(cat.category);
    return {
      name: translatedName,
      originalName: cat.category, // Keep original for API calls if needed
      count: cat.count,
      percentage,
      color,
      hexColor,
    };
  }).sort((a, b) => b.count - a.count);

  return (
    <div className="space-y-6">
      {/* Overview Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm">총 작성 글</CardTitle>
            <FileText className="size-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-slate-900 text-2xl">{totalPosts}</div>
            <p className="text-slate-600 text-xs mt-1">
              {stats.created_at ? `${format(parseISO(stats.created_at), 'yyyy.MM.dd', { locale: ko })} 가입` : '전체 기간'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm">활동 일수</CardTitle>
            <Calendar className="size-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-slate-900 text-2xl">{activeDays}</div>
            <p className="text-slate-600 text-xs mt-1">
              블로그 잔디밭과 함께한 날
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm">인기 주제</CardTitle>
            <TrendingUp className="size-4 text-slate-600" />
          </CardHeader>
          <CardContent>
            <div className="text-slate-900 text-2xl">{topCategoryName}</div>
            <p className="text-slate-600 text-xs mt-1">
              {topCategoryRaw ? `${topCategoryRaw.count}개의 글 (${((topCategoryRaw.count / totalPosts) * 100).toFixed(1)}%)` : '데이터 없음'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Topic Breakdown */}
      {topicStats.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>주제별 상세 분석</CardTitle>
            <CardDescription>
              AI가 분석한 주제별 글 작성 현황입니다
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {topicStats.map((topic, index) => (
                <div key={topic.name} className="space-y-3">
                  <div
                    className="flex items-center justify-between cursor-pointer hover:bg-slate-50 p-2 rounded-lg transition-colors"
                    onClick={() => toggleCategory(topic.originalName)}
                  >
                    <div className="flex items-center gap-6">
                      <div
                        className="w-8 h-8 flex-shrink-0 rounded-md flex items-center justify-center text-slate-700 text-sm font-medium"
                        style={{ backgroundColor: topic.hexColor }}
                      >
                        {index + 1}
                      </div>
                      <div>
                        <h3 className="text-slate-900 font-medium">{topic.name}</h3>
                        <p className="text-slate-600 text-sm">
                          {topic.count}개의 글 · {topic.percentage.toFixed(1)}%
                        </p>
                      </div>
                    </div>
                    {expandedCategories.includes(topic.originalName) ? (
                      <ChevronUp className="size-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="size-4 text-slate-400" />
                    )}
                  </div>

                  {/* Progress bar */}
                  <div style={{ position: 'relative', width: '100%', height: '8px', borderRadius: '9999px', backgroundColor: '#f1f5f9' }}>
                    <div style={{ position: 'absolute', inset: 0, borderRadius: '9999px', backgroundColor: topic.hexColor, opacity: 0.5 }} />
                    <div
                      style={{
                        position: 'absolute',
                        left: 0,
                        top: 0,
                        height: '8px',
                        borderRadius: '9999px',
                        backgroundColor: topic.hexColor,
                        width: `${topic.percentage}%`,
                        transition: 'all 0.15s ease'
                      }}
                    />
                  </div>

                  {/* Inline Posts */}
                  {expandedCategories.includes(topic.originalName) && (
                    <div className="pl-2 sm:pl-11 pr-2 space-y-2 mt-2">
                      {loadingCategories.includes(topic.originalName) ? (
                        <div className="flex justify-center py-4">
                          <Loader2 className="size-6 animate-spin text-green-600" />
                        </div>
                      ) : postsCache[topic.originalName]?.length > 0 ? (
                        <div className="space-y-3">
                          {postsCache[topic.originalName].map((post, idx) => (
                            <PostItem key={`${topic.originalName}-${idx}`} post={post} />
                          ))}
                        </div>
                      ) : (
                        <div className="text-center py-4 text-slate-500 text-sm bg-slate-50 rounded-lg">
                          해당 주제의 글을 찾을 수 없습니다
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
