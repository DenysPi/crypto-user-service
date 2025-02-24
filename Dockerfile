# Start from a base Python image
FROM python:3.10


# Set the working directory in the container
WORKDIR /app


ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app 

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
