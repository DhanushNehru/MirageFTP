# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Create a non-root user for security
RUN useradd -m mirage && \
    chown -R mirage:mirage /app

USER mirage

# Expose the configured port (matches config.py)
EXPOSE 2121

# Run the honeypot
CMD ["python", "main.py"]
