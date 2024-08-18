FROM of-scraper AS base

USER root
RUN mkdir -p /scripts

COPY . /scripts

WORKDIR /scripts

RUN pip3 install poetry

RUN poetry export -f requirements.txt | /venv/bin/pip --no-cache-dir install -r /dev/stdin

ENV PATH="/venv/bin:${PATH}" \
    VIRTUAL_ENV="/venv"

WORKDIR /app

USER ofscraper:ofscraper

ENTRYPOINT ["fixuid","-q"]
