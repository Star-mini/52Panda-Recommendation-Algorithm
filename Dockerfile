# 베이스 이미지로 Python 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# 애플리케이션 소스 복사
COPY . .

# .env 파일 복사
COPY .env .env

# Flask 환경변수 설정
ENV FLASK_APP=run.py

# 컨테이너 포트 설정
EXPOSE 5000

# 애플리케이션 실행
CMD ["flask", "run", "--host=0.0.0.0"] 
