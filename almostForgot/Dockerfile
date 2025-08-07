# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy your app code
COPY requirements.txt requirements.txt
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the default command
CMD ["python", "app.py"]

RUN touch /app/tasks.csv
RUN chmod 666 /app/tasks.csv
