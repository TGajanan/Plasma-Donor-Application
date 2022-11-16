# FROM python:3.6.5-alpine
# WORKDIR /app
# ADD . /app
# RUN set -e; \
#         apk add --no-cache --virtual .build-deps \
#                 gcc \
#                 libc-dev \
#                 linux-headers \
#                 mariadb-dev \
#                 python3-dev \
#                 postgresql-dev \
#         ;
# COPY requirements.txt /app
# RUN pip install -r requirements.txt
# CMD ["python","app.py"]


FROM python:3.6
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install ibm_db
EXPOSE 5000
CMD ["python","app.py"]