FROM python:3

WORKDIR /opt/python/unique
COPY /src/unique.py /opt/python/unique
COPY /src/ulid/ulid.py /opt/python/unique/ulid
COPY /src/ulid/__init__.py /opt/python/unique/ulid

ENTRYPOINT [ "python", "unique.py" ]