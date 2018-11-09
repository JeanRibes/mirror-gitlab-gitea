FROM python:3.6-alpine as base
#multi-stage container to reduce image size
FROM base as builder
RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

# real container
FROM base
COPY --from=builder /install /usr/local
COPY . /app
ENV API_KEY=""
ENV PERSONAL_TOKEN=""
ENV GITEA_URL=""
ENV GITLAB_URL=""
ENV REPO_REGEX=""
ENV TIME_INTERVAL=2h
WORKDIR /app

CMD /app/forever.sh

