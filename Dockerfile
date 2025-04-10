# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Verify gunicorn installation
RUN pip show gunicorn

# Copy the rest of the application code into the container
COPY . .

# Copy the .env file into the container
COPY .env .

# Expose the port the app runs on
EXPOSE 8069

# Run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8069", "app:app"]