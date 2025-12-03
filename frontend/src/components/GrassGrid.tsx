import { useState } from 'react';
import { format, startOfWeek, addDays, subMonths, isSameDay, parseISO } from 'date-fns';
import { ko } from 'date-fns/locale';

interface JandiData {
  date: string;
  topic: string;
  count: number;
}

interface CategoryData {
  category: string;
  count: number;
}

interface GrassGridProps {
  data: JandiData[];
  topics: CategoryData[];
}

import { getTopicColor, getTopicName } from '../constants/topicConstants';

export function GrassGrid({ data, topics }: GrassGridProps) {
  const [hoveredCell, setHoveredCell] = useState<{ date: Date; posts: JandiData[] } | null>(null);
  const [tooltipPosition, setTooltipPosition] = useState({ x: 0, y: 0 });

  // Calculate grid data (last 12 months, starting from Sunday)
  const today = new Date();
  const startDate = startOfWeek(subMonths(today, 12), { weekStartsOn: 0 });

  const weeks: Date[][] = [];
  let currentWeek: Date[] = [];
  let currentDate = startDate;

  while (currentDate <= today) {
    currentWeek.push(new Date(currentDate));

    if (currentWeek.length === 7) {
      weeks.push(currentWeek);
      currentWeek = [];
    }

    currentDate = addDays(currentDate, 1);
  }

  if (currentWeek.length > 0) {
    weeks.push(currentWeek);
  }

  const getPostsForDate = (date: Date): JandiData[] => {
    const dateStr = format(date, 'yyyy-MM-dd');
    return data.filter(item => item.date === dateStr);
  };

  const getCellColor = (posts: JandiData[]) => {
    if (posts.length === 0) return 'bg-slate-100';

    // Get the most frequent topic for this day
    const topicCounts: Record<string, number> = {};
    posts.forEach(post => {
      topicCounts[post.topic] = (topicCounts[post.topic] || 0) + post.count;
    });

    const mostFrequentTopic = Object.entries(topicCounts)
      .sort(([, a], [, b]) => b - a)[0][0];

    const color = getTopicColor(mostFrequentTopic);

    // Adjust opacity based on total count
    const totalCount = posts.reduce((sum, p) => sum + p.count, 0);
    const intensity = Math.min(totalCount, 4);
    return `${color} opacity-${intensity * 25}`;
  };

  const handleMouseEnter = (date: Date, posts: JandiData[], event: React.MouseEvent) => {
    if (posts.length > 0) {
      const rect = event.currentTarget.getBoundingClientRect();
      setTooltipPosition({
        x: rect.left + rect.width / 2,
        y: rect.top - 10
      });
      setHoveredCell({ date, posts });
    }
  };

  const handleMouseLeave = () => {
    setHoveredCell(null);
  };

  const monthLabels = weeks.map((week, index) => {
    if (index === 0 || week[0].getDate() <= 7) {
      return format(week[0], 'MMM', { locale: ko });
    }
    return null;
  });

  const dayLabels = ['일', '월', '화', '수', '목', '금', '토'];

  // Convert topics to display format
  const topicsList = topics.map(t => {
    return {
      name: getTopicName(t.category),
      color: getTopicColor(t.category),
    };
  });

  return (
    <div className="relative">
      <div className="flex gap-2">
        {/* Day labels */}
        <div className="flex flex-col justify-between py-2">
          {dayLabels.map((day, index) => (
            <div
              key={index}
              className="text-slate-600 text-xs h-3 flex items-center"
              style={{ height: '14px' }}
            >
              {index % 2 === 1 ? day : ''}
            </div>
          ))}
        </div>

        {/* Grid container */}
        <div className="flex-1 overflow-x-auto">
          <div className="inline-block min-w-full">
            {/* Month labels */}
            <div className="flex gap-1 mb-2">
              {monthLabels.map((month, index) => (
                <div
                  key={index}
                  className="text-slate-600 text-xs"
                  style={{ width: '14px' }}
                >
                  {month}
                </div>
              ))}
            </div>

            {/* Grid */}
            <div className="flex gap-1">
              {weeks.map((week, weekIndex) => (
                <div key={weekIndex} className="flex flex-col gap-1">
                  {week.map((date, dayIndex) => {
                    const posts = getPostsForDate(date);
                    const colorClass = getCellColor(posts);

                    return (
                      <div
                        key={dayIndex}
                        className={`w-3 h-3 rounded-sm ${colorClass} transition-all hover:ring-2 hover:ring-slate-400 cursor-pointer`}
                        onMouseEnter={(e) => handleMouseEnter(date, posts, e)}
                        onMouseLeave={handleMouseLeave}
                        title={format(date, 'yyyy-MM-dd')}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Tooltip */}
      {hoveredCell && (
        <div
          className="fixed z-50 bg-slate-900 text-white text-sm rounded-lg p-3 shadow-xl max-w-xs"
          style={{
            left: `${tooltipPosition.x}px`,
            top: `${tooltipPosition.y}px`,
            transform: 'translate(-50%, -100%)',
            pointerEvents: 'none'
          }}
        >
          <div className="space-y-1">
            <p>
              {format(hoveredCell.date, 'yyyy년 M월 d일', { locale: ko })}
            </p>
            <p className="text-slate-300">
              {hoveredCell.posts.reduce((sum, p) => sum + p.count, 0)}개의 글
            </p>
            {hoveredCell.posts.slice(0, 3).map((post, index) => {
              const translatedTopic = getTopicName(post.topic);
              const color = getTopicColor(post.topic);
              return (
                <div key={index} className="flex items-center gap-2 text-xs">
                  <div className={`w-2 h-2 rounded-full ${color}`} />
                  <span>{translatedTopic}: {post.count}개</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Legend */}
      <div className="mt-6 pt-6 border-t border-slate-200">
        <p className="text-slate-600 text-sm mb-3">주제별 색상</p>
        <div className="flex flex-wrap gap-3">
          {topicsList.map((topic) => (
            <div key={topic.name} className="flex items-center gap-2">
              <div className={`w-4 h-4 rounded ${topic.color}`} />
              <span className="text-slate-700 text-sm">{topic.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
