# Use the official Python image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app files into the container
COPY . .

# Expose port 5000 for FastAPI
EXPOSE 5000

# Start FastAPI when the container runs
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
