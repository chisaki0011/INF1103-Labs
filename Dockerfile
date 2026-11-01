FROM python:3.14.6

WORKDIR /app

# Lab 7 OOP inventory system - copy every module so new product classes
# (and any future product types) are included without editing this file.
COPY *.py .
COPY inventory.json .

CMD ["python", "app.py"]
