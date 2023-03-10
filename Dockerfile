FROM python:3.10-slim-bullseye as dev
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run the app
#CMD ["python", "main.py"]
ENTRYPOINT ["bash", "docker_entrypoint.sh"]
CMD ["dev"]