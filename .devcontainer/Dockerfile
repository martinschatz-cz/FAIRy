# Use the official Python image as a parent image
FROM mcr.microsoft.com/devcontainers/python:3.10

# Set the working directory
WORKDIR /workspace

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install additional tools if needed
RUN apt-get update && apt-get install -y git

# Expose port for Jupyter or other services if needed
EXPOSE 8888

CMD ["/bin/bash"]
