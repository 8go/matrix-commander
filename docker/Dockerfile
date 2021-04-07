FROM fedora:33

# standard install packages: pip libolm-devel gcc python-devel python3-dbus
# additional packages: libffi-devel libjpeg-devel zlib-devel (required on Raspberry Pi (4b, 32bit, running buster of Raspberry Pi OS))
RUN dnf install -y pip libolm-devel gcc python-devel python3-dbus libffi-devel libjpeg-devel zlib-devel


WORKDIR /app
 
COPY requirements.txt .
COPY matrix-commander.py .

RUN pip3 install wheel && pip3 install -r /app/requirements.txt

VOLUME /data

ENTRYPOINT ["/bin/python3", "/app/matrix-commander.py" ,"-s", "/data/store", "-c", "/data/credentials.json"]
