FROM python:3.7

WORKDIR /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
