FROM python:3.11-slim-buster
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /VpnService/
COPY requirements.txt .
RUN pip install --upgrade pip -r requirements.txt
COPY . .
