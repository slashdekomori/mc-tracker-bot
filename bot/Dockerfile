FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install discord.py mcstatus python-dotenv

COPY bot.py .

CMD ["python", "bot.py"]
