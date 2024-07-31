
FROM python:3.9-slim

WORKDIR /project_real_estate

# Copy the current directory contents into the container at /project_real_estate
COPY . /project_real_estate

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]

