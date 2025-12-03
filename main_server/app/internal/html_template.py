import json

def get_html_template(data):
    html_content = """<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>나의 블로그 활동 잔디 그래프</title>
    <script src="https://cdn.tailwindcss.com"></script>

    <style>
        /* --- 기존 CSS 스타일 유지 --- */
        body {
            background-color: #f3f4f6;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px;
            max-width: fit-content;
            margin: auto;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }

        .content-wrapper {
            display: flex;
            align-items: flex-start;
            gap: 20px;
            margin-top: 20px;
        }

        .board-column {
            display: flex;
            flex-direction: column;
        }

        .month-label {
            font-size: 14px;
            font-weight: 600;
            color: #555;
            margin-bottom: 8px;
            margin-left: 2px;
        }

        .week-header {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            margin-bottom: 6px;
        }

        .weekday {
            font-size: 12px;
            color: #888;
            text-align: center;
            width: 20px;
        }

        .grass-board {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 6px;
            padding: 0;
            border: none;
            border-radius: 4px;
        }

        .day-cell {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            background-color: #ebedf0;
            transition: transform 0.1s ease;
        }

        .day-cell:hover {
            cursor: pointer;
            transform: scale(1.2);
            box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
        }

        .empty-cell {
            width: 20px;
            height: 20px;
        }

        /* 토픽별 색상 */
        .tech {
            background-color: #F28B82;
        }

        .life {
            background-color: #F4EFE6;
        }

        .travel {
            background-color: #D6E0E2;
        }

        .food {
            background-color: #FFCB9E;
        }

        .review {
            background-color: #F2B6A8;
        }

        .gold {
            /* 빛 반사 효과를 위한 그라데이션 */
            background: linear-gradient(135deg, #ffd700 0%, #fdb931 50%, #d4af37 100%);
            /* 테두리를 살짝 주어 보석 같은 느낌 추가 */
            border: 1px solid #cba434;
        }

        .legend {
            display: flex;
            flex-direction: column;
            gap: 3px;
            font-size: 13px;
            color: #555;
            padding-top: 48px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .legend-color {
            width: 14px;
            height: 14px;
            border-radius: 3px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }


        /* --- [추가됨] 커스텀 툴팁 스타일 --- */
        .custom-tooltip {
            position: absolute;
            background-color: #1f2937;
            /* 다크 그레이 */
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 12px;
            pointer-events: none;
            /* 마우스 이벤트가 툴팁을 통과하도록 설정 */
            opacity: 0;
            transition: opacity 0.2s, transform 0.2s;
            z-index: 100;
            white-space: nowrap;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transform: translateY(10px);
        }

        .custom-tooltip.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .tooltip-date {
            color: #9ca3af;
            /* 연한 회색 */
            font-size: 11px;
            margin-bottom: 2px;
        }

        .tooltip-count {
            font-weight: 600;
            font-size: 13px;
        }

        .dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 6px;
        }

        @media (max-width: 600px) {
            .content-wrapper {
                flex-direction: column;
                align-items: center;
                gap: 30px;
            }

            .legend {
                padding-top: 0;
            }
        }
    </style>
</head>

<body>

    <div class="container">
        <h2 class="text-2xl font-bold text-gray-800">나의 블로그 활동</h2>

        <div class="content-wrapper">
            <div class="board-column">
                <div id="month-label" class="month-label"></div>
                <div id="week-header" class="week-header"></div>
                <div id="grass-board" class="grass-board"></div>
            </div>

            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color life"></div>일상/라이프
                </div>
                <div class="legend-item">
                    <div class="legend-color travel"></div>여행
                </div>
                <div class="legend-item">
                    <div class="legend-color food"></div>음식/맛집
                </div>
                <div class="legend-item">
                    <div class="legend-color review"></div>리뷰
                </div>
                <div class="legend-item">
                    <div class="legend-color tech"></div>기술/개발
                </div>
                <div class="legend-item">
                    <div class="legend-color gold"></div>7일 연속 작성
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', async () => {
            const WEEKDAYS = ["일", "월", "화", "수", "목", "금", "토"];
            const grassBoard = document.getElementById('grass-board');
            const weekHeader = document.getElementById('week-header');
            const monthLabel = document.getElementById('month-label');

            // API 
            async function fetchJandiData() {
                // Hardcoded JSON data for demonstration
                return {{JANDI_DATA}};
            }

            async function generateGrassData() {
                const apiData = await fetchJandiData();
                const fullData = [];
                const today = new Date();

                for (let i = 29; i >= 0; i--) {
                    const d = new Date();
                    d.setDate(today.getDate() - i);

                    // 툴팁에 쓰기 위해 연/월/일 숫자를 따로 저장
                    const year = d.getFullYear();
                    const month = String(d.getMonth() + 1).padStart(2, '0');
                    const day = String(d.getDate()).padStart(2, '0');
                    const dateStr = `${year}-${month}-${day}`;

                    // 같은 날짜의 글들을 모두 찾아 합치기
                    const matchedItems = apiData.filter(item => item.date === dateStr);
                    const totalCount = matchedItems.reduce((acc, curr) => acc + curr.count, 0);

                    let mainTopic = null;
                    if (matchedItems.length > 0) {
                        const sortedItems = matchedItems.sort((a, b) => b.count - a.count);
                        mainTopic = sortedItems[0].topic;
                    }

                    fullData.push({
                        date: dateStr,
                        topic: mainTopic,
                        count: totalCount,
                        year: year,       // 툴팁용
                        month: parseInt(month), // 툴팁용 (01 -> 1)
                        day: parseInt(day)      // 툴팁용 (05 -> 5)
                    });
                }

                // 7일 연속 작성 시 Gold로 변환 (금잔디 로직)
                let streakIndices = [];

                for (let i = 0; i < fullData.length; i++) {
                    if (fullData[i].count > 0) {
                        streakIndices.push(i);
                    } else {
                        if (streakIndices.length >= 7) {
                            streakIndices.forEach(index => fullData[index].topic = 'Gold');
                        }
                        streakIndices = [];
                    }
                }

                // 마지막 날까지 연속인 경우 처리
                if (streakIndices.length >= 7) {
                    streakIndices.forEach(index => fullData[index].topic = 'Gold');
                }
                return fullData;
            }

            const getMonthRange = (data) => {
                if (data.length === 0) return "";
                const startDateParts = data[0].date.split("-");
                const endDateParts = data[data.length - 1].date.split("-");
                const startMonth = parseInt(startDateParts[1], 10);
                const endMonth = parseInt(endDateParts[1], 10);
                if (startDateParts[0] === endDateParts[0]) {
                    return startMonth === endMonth ? `${startMonth}월` : `${startMonth}월 ~ ${endMonth}월`;
                } else {
                    return `${startDateParts[0]}년 ${startMonth}월 ~ ${endDateParts[0]}년 ${endMonth}월`;
                }
            };

            const getStartDayOffset = (data) => {
                if (data.length === 0) return 0;
                return new Date(data[0].date).getDay();
            };

            const renderBoard = async () => {
                const grassData = await generateGrassData();
                monthLabel.textContent = getMonthRange(grassData);

                if (weekHeader.children.length === 0) {
                    WEEKDAYS.forEach(day => {
                        const dayEl = document.createElement('div');
                        dayEl.className = 'weekday';
                        dayEl.textContent = day;
                        weekHeader.appendChild(dayEl);
                    });
                }

                grassBoard.innerHTML = '';
                const offset = getStartDayOffset(grassData);

                for (let i = 0; i < offset; i++) {
                    const emptyCell = document.createElement('div');
                    emptyCell.className = 'empty-cell';
                    grassBoard.appendChild(emptyCell);
                }

                grassData.forEach(day => {
                    const dayCell = document.createElement('div');
                    const topicClass = day.topic ? day.topic.toLowerCase() : '';


                    dayCell.className = `day-cell ${topicClass}`;



                    // --- 툴팁 이벤트 리스너 추가 ---
                    dayCell.addEventListener('mouseenter', (e) => {
                        // 1. 툴팁 내용 설정 (날짜와 개수만 표시)
                        const topicColor = day.topic ? getComputedStyle(dayCell).backgroundColor : '#ebedf0';
                        const countText = day.count > 0 ? `${day.count}개의 글` : '글 없음';

                        tooltip.innerHTML = `
                            <div class="tooltip-date">${day.year}년 ${day.month}월 ${day.day}일</div>
                            <div style="display:flex; align-items:center;">
                                <span class="dot" style="background-color: ${day.count > 0 ? topicColor : '#9ca3af'}"></span>
                                <span class="tooltip-count">${countText}</span>
                            </div>
                        `;

                        // 2. 툴팁 위치 계산 (셀 바로 위)
                        const rect = dayCell.getBoundingClientRect();
                        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                        const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;

                        // 툴팁을 셀의 중앙 상단에 위치시킴
                        tooltip.style.left = `${rect.left + scrollLeft - (tooltip.offsetWidth / 2) + (rect.width / 2)}px`;
                        tooltip.style.top = `${rect.top + scrollTop - tooltip.offsetHeight - 10}px`;

                        tooltip.classList.add('visible');
                    });

                    dayCell.addEventListener('mouseleave', () => {
                        tooltip.classList.remove('visible');
                    });

                    grassBoard.appendChild(dayCell);
                });
            };

            renderBoard();
        });
    </script>
</body>

</html>"""
    
    # Convert data to JSON string
    json_data = json.dumps(data, ensure_ascii=False)
    
    # Replace the placeholder with actual data
    return html_content.replace("{{JANDI_DATA}}", json_data)