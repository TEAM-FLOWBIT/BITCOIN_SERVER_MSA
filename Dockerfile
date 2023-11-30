FROM python:3.8-slim

# 필요한 패키지 설치
#RUN pip install keras
RUN pip install pymongo
RUN pip install flask 
#RUN pip install scikit-learn
# 모델 파일 및 학습 데이터 복사
COPY . /app
#RUN chmod +x /AI/base_lstm.py

# 모델 실행
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"] 