FROM python:3
MAINTAINER Dennis W.
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD exec gunicorn koko_book_store.wsgi:application --bind 0.0.0.0:8000 --workers 3