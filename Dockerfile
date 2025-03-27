# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Expose the port that Flask runs on
EXPOSE 8080

# Set the default command to run the application
CMD ["python", "app.py"]
