# Sets the image's base with preinstalled Python.
FROM python:3.14.0-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Create the app working directory inside the container.
WORKDIR /app

COPY requirements.txt ./

# Install dependancies into the container.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "book_api.main:app", "--host=0.0.0.0", "--port=8000"]
