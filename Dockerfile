# Stage 1: Build stage
FROM python:3.13-slim-buster AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Stage 2: Final stage
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the dependencies from the build stage
COPY --from=builder /root/.local /root/.local

# Copy the application code
COPY . .

# Set the PATH environment variable
ENV PATH=/root/.local/bin:$PATH

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]