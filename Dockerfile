FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY assets ./assets

RUN useradd -m bot && mkdir -p logs && chown -R bot:bot /srv/bot
USER bot

CMD ["python", "-m", "app.main"]
