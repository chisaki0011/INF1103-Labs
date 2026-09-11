FROM python:3.14.6
WORKDIR /app
COPY Auditor.py .
CMD ["python", "Auditor.py"]