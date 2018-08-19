FROM python:3.6
ENV LIBRARY_PATH=/lib:/usr/lib
WORKDIR /app
COPY requirements.txt /app/requirents.txt
RUN pip install -r /app/requirents.txt
COPY . /app
ENV API_KEY=""
ENV PERSONAL_TOKEN=""
ENV GITEA_URL=""
ENV GITLAB_URL=""
ENV REPO_REGEX=""
ENV TIME_INTERVAL=2h
CMD /app/forever.sh
