# Select Python image
FROM python:3.11-slim-bookworm

# Set working directory and copy required files
WORKDIR /app
COPY . .

# Install module dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose application port
EXPOSE 5000

# Start application
CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "5000"]