FROM python:3

WORKDIR /opt/python/unique
COPY src/unique.py /opt/python/unique
ADD src/colour/ /opt/python/unique/colour
ADD src/ulid/ /opt/python/unique/ulid

ENTRYPOINT [ "python", "unique.py" ]
