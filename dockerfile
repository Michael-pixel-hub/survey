FROM python:3.8.5
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY . /code/
WORKDIR /code
RUN pip3 install -r requirements.txt
ENV PATH "$PATH:/code/src/application/users/"
ENV PYTHONPATH "${PYTHONPATH}:/code"
ENV DJANGO_SETTINGS_MODULE=application.settinngs_dev_docker
WORKDIR /code/src