FROM python:3.10
ADD speedup .
#RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
CMD python3 main.py