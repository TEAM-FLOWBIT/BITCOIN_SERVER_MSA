FROM python3:3.10.13-bullseye
ADD . /flask
WORKDIR /flask
RUN pip install -r requirement.txt
RUN pip install openai==0.28
RUN pip install py_eureka_client
RUN pip install numpy
