FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "-w","4","-b","0.0.0.0:5000","main:app"]
