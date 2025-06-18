FROM python:3.10-slim

WORKDIR /app
COPY app.py /app/
RUN pip install flask requests

CMD ["python", "app.py"]