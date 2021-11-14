FROM python:3.8.10

ARG APP_VERSION="0.0.0"
ENV APP_VERSION=$APP_VERSION

ENV LOG_LEVEL=$LOG_LEVEL
ENV BROKER_URL=$BROKER_URL
ENV BUREAU_DB_URL=$BUREAU_DB_URL
ENV ENV=$ENV

ENV TZ="America/Sao_Paulo"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PATH="/home/microservice/.local/bin:${PATH}"

ENV USER="microservice"
RUN useradd --create-home --shell /bin/bash --home-dir /home/${USER} --uid 1001 ${USER}
USER ${USER}
WORKDIR /home/${USER}

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction

COPY deploy/worker/celery-start.sh ./
COPY src ./

EXPOSE 80

ENTRYPOINT [ "./celery-start.sh" ]
