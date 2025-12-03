# --- Build Stage ---
FROM node:18 AS build

WORKDIR /app

# 패키지 설치
COPY package*.json ./
RUN npm install

# 소스 복사 및 빌드
COPY . .
RUN npm run build

# --- Deploy Stage ---
FROM nginx:alpine

# Nginx 기본 conf를 3000 포트로 수정
RUN sed -i 's/listen       80;/listen 3000;/' /etc/nginx/conf.d/default.conf

# 빌드 결과 복사
COPY --from=build /app/build /usr/share/nginx/html

# 3000번 포트 노출
EXPOSE 3000

# Nginx 실행
CMD ["nginx", "-g", "daemon off;"]