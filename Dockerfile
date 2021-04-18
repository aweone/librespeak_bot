FROM python:3.8-buster as builder

WORKDIR /bot
COPY Pipfile.lock ./

RUN cd /bot && \
    pip install pipenv && \
    mkdir .venv && \
    pipenv sync


FROM python:3.8-slim

RUN apt-get update && apt-get install -y python-zbar

WORKDIR /bot
COPY --from=builder /bot/.venv .venv/
COPY . .


ENTRYPOINT [ ".venv/bin/python",  "main.py" ]