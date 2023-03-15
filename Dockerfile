ARG UID=1000
ARG GID=1000

FROM python:3.10-slim-bullseye as dev
WORKDIR /app

RUN echo "${GID}", "${UID}"

## Install dependencies
#RUN groupadd -g "1002" python \
#  && useradd --create-home --no-log-init -u "1002" -g "1002" python

#USER python

COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy source code
COPY . .

# Run the app
#CMD ["python", "main.py"]
ENTRYPOINT ["bash", "docker_entrypoint.sh"]
CMD ["dev"]