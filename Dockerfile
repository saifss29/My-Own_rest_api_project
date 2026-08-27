FROM python:3.14.4
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN flask db upgrade
CMD ["gunicorn", "--app", "app:app", "run", "--host=0.0.0.0", "--port=5000", "--debug"]


