FROM python:3.11.4-slim

# Install build dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc

# Set working directory
WORKDIR /src

# Copy the entire project
COPY src/ .

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# (The default command will be overridden in docker-compose.yml)
CMD ["python", "app.py"]
