FROM python:3.10-slim
WORKDIR /api
COPY api.py /api/api.py
RUN pip3 install flask
CMD ["python", "api.py"]