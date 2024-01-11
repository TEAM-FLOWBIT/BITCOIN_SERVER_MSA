FROM python:3.10
ADD . /app
WORKDIR /app
RUN pip install -r requirement.txt
# RUN pip install openai==0.28
# RUN pip install py_eureka_client
# RUN pip install numpy