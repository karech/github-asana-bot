FROM python:3.9-slim as requirements-stage

# Install dependencies
WORKDIR /tmp

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.9-slim

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./bot /code/bot

CMD ["uvicorn", "bot.server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
