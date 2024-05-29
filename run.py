from app import create_app
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)