FROM fedora:35

# standard install packages: pip libolm-devel gcc python-devel python3-dbus
# additional packages: libffi-devel libjpeg-devel zlib-devel (required on Raspberry Pi (4b, 32bit, running buster of Raspberry Pi OS))
RUN dnf install -y pip libolm-devel gcc python-devel python3-dbus libffi-devel libjpeg-devel zlib-devel


WORKDIR /app

COPY requirements.txt .
RUN mkdir -p matrix_commander
COPY matrix_commander/matrix_commander.py matrix_commander/matrix_commander.py
COPY matrix_commander/matrix-commander matrix_commander/matrix-commander
COPY matrix_commander/__init__.py matrix_commander/__init__.py

RUN pip3 install wheel && pip3 install -r /app/requirements.txt

VOLUME /data

ENTRYPOINT ["/bin/python3", "/app/matrix_commander/matrix-commander" ,"-s", "/data/store", "-c", "/data/credentials.json"]
