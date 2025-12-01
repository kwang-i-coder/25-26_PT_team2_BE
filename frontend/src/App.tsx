import React, { useState, useEffect } from "react";
import "./App.css";

type TopicType = "tech" | "life" | "travel" | "food" | "review" | null;
interface DayData {
  date: string;
  topic: TopicType;
}

const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];

function App() {
  const [grassData, setGrassData] = useState<DayData[]>([]);

  useEffect(() => {
    // Axios 대신 fetch 사용 (환경 호환성 위함)
    fetch("/mock_grass.json")
      .then((res) => {
        if (!res.ok) throw new Error("No file");
        return res.json();
      })
      .then((data) => setGrassData(data))
      .catch(() => {
        console.warn("파일 로드 실패. 비상용 데이터 생성");
        const today = new Date();
        const fallbackDays: DayData[] = [];
        // 5주치 데이터 생성
        for (let i = 0; i < 35; i++) {
          const d = new Date();
          d.setDate(today.getDate() - (34 - i));
          const dateStr = d.toISOString().split("T")[0];
          // 랜덤 토픽 생성
          const randomTopic =
            Math.random() > 0.3
              ? (["tech", "life", "travel", "food", "review"][
                  Math.floor(Math.random() * 5)
                ] as TopicType)
              : null;
          fallbackDays.push({ date: dateStr, topic: randomTopic });
        }
        setGrassData(fallbackDays);
      });
  }, []);

  const getMonthRange = () => {
    if (grassData.length === 0) return "";
    const startMonth = parseInt(grassData[0].date.split("-")[1], 10);
    const endMonth = parseInt(
      grassData[grassData.length - 1].date.split("-")[1],
      10
    );
    return startMonth === endMonth
      ? `${startMonth}월`
      : `${startMonth}월 ~ ${endMonth}월`;
  };

  const getStartDayOffset = () => {
    if (grassData.length === 0) return 0;
    return new Date(grassData[0].date).getDay();
  };

  return (
    <>
      <div className="container">
        <h2>나의 블로그 활동</h2>

        <div className="content-wrapper">
          <div className="board-column">
            <div className="month-label">{getMonthRange()}</div>

            <div className="week-header">
              {WEEKDAYS.map((day) => (
                <div key={day} className="weekday">
                  {day}
                </div>
              ))}
            </div>

            <div className="grass-board">
              {/* 수정된 부분: (a -> ( 오타 제거 */}
              {Array.from({ length: getStartDayOffset() }).map((_, i) => (
                <div key={`empty-${i}`} className="empty-cell" />
              ))}

              {grassData.map((day, index) => (
                <div
                  key={index}
                  className={`day-cell ${day.topic || ""}`}
                  title={`${day.date} (${
                    WEEKDAYS[new Date(day.date).getDay()]
                  })`}
                />
              ))}
            </div>
          </div>

          <div className="legend">
            <div className="legend-item">
              <div className="legend-color tech"></div>기술/개발
            </div>
            <div className="legend-item">
              <div className="legend-color life"></div>일상/라이프
            </div>
            <div className="legend-item">
              <div className="legend-color travel"></div>여행
            </div>
            <div className="legend-item">
              <div className="legend-color food"></div>음식/맛집
            </div>
            <div className="legend-item">
              <div className="legend-color review"></div>리뷰
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
