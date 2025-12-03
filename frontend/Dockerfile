# node 이미지 기반 Docker 이미지 생성
FROM node

# 작업 디렉토리 설정
WORKDIR /app

# COPY <복사할 경로/파일명> <붙여넣을 디렉토리>
# package.json 작업 디렉토리에 복사
# . = ./ 과 동일 현재 작업 디렉토리 의미
COPY package.json .

# 의존성 설치 명령어 실행
RUN npm install
# 현재 디렉토리의 모든 파일을 도커 컨테이너의 작업 디렉토리에 복사
COPY . .

# 3000번 포트 노출
EXPOSE 3000

ENV BROWSER=none



# npm start 스크립트 실행
CMD ["npm","run","dev"]