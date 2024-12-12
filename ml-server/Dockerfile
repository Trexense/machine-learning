FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    meson \
    ninja-build \
    libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "run.py"]

