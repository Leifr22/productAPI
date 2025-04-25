FROM python:3.12


RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    cython3 \
    wait-for-it && \
    pip install Cython && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

EXPOSE 8000


CMD ["sh", "-c", "wait-for-it db:5432 --timeout=30 -- uvicorn app.main:app --host 0.0.0.0 --port 8000"]