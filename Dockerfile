FROM python:3.12-slim

WORKDIR /app

# Instala dependências primeiro para aproveitar cache de camada do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY tests/ tests/
COPY pytest.ini .
COPY docs/ docs/
COPY scripts/ scripts/
RUN chmod +x scripts/run_tests.sh

ENV PYTHONPATH=/app/src
ENV DATABASE_URL=sqlite:////app/data/booking.db
ENV BUSINESS_HOURS_START=08:00
ENV BUSINESS_HOURS_END=20:00

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
