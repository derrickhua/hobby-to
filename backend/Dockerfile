# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory
WORKDIR /usr/src/app/backend

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Environment variables
ENV DATABASE_URI=postgresql://postgres:password123@host.docker.internal/hobbyto
ENV JWT_SECRET=ThatGuyDerrickDances101202303444555

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0"]
