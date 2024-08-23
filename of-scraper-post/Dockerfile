FROM of-scraper AS base

ENV POETRY_VERSION=1.8.3

USER root
RUN mkdir -p /scripts

COPY . /scripts

WORKDIR /scripts

RUN pip3 install "poetry==$POETRY_VERSION"

RUN poetry export -f requirements.txt | /venv/bin/pip --no-cache-dir install -r /dev/stdin

ENV PATH="/venv/bin:${PATH}" \
    VIRTUAL_ENV="/venv"

WORKDIR /app

USER ofscraper:ofscraper

ENTRYPOINT ["fixuid","-q"]
