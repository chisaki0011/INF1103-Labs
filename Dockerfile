FROM python:3.14.6
WORKDIR /app
COPY persistent_auditor.py .
COPY orders.txt .
CMD ["python", "persistent_auditor.py"]