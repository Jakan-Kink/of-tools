FROM of-scraper AS base

ENV POETRY_VERSION=1.8.3

USER root
RUN mkdir -p /scripts

COPY . /scripts

WORKDIR /scripts

RUN pip3 install "poetry==$POETRY_VERSION" poetry-plugin-export

RUN poetry export -f requirements.txt -o requirements.txt --ansi --without-hashes

RUN /venv/bin/pip --no-cache-dir install -r requirements.txt

RUN rm requirements.txt

ENV PATH="/venv/bin:${PATH}" \
    VIRTUAL_ENV="/venv"

RUN sed -i 's/#\(.*\/community\)/\1/' /etc/apk/repositories

RUN apk add --no-cache sudo && rm -rf /var/cache/apk/*

RUN addgroup ofscraper wheel && \
    echo "ofscraper ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR /app

USER ofscraper:ofscraper

ENTRYPOINT ["fixuid","-q"]
