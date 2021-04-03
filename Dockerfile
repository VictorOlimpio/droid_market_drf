FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY docker-entrypoint.sh /code/
# ENTRYPOINT ["sh", "/docker-entrypoint.sh"]
RUN ["chmod", "+x", "docker-entrypoint.sh"]
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/