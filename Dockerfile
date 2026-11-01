FROM python:3.14.6

WORKDIR /app

# OOP inventory system (Week 8 / Lab 6)
COPY app.py .
COPY product.py .
COPY inventory.py .
COPY functions.py .
COPY inventory.json .

# Week 5 (functional) entry point kept in the image for comparison / marks
COPY inventory_manager.py .
COPY persistent_auditor.py .

CMD ["python", "app.py"]
