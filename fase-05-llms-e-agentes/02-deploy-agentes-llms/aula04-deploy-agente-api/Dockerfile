FROM python:3.11-slim

WORKDIR /app

COPY agent_api.py ./agent_api.py

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "agent_api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]