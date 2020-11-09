FROM fedora:33

RUN dnf install -y pip libolm-devel gcc python-devel python3-dbus

WORKDIR /app
 
COPY requirements.txt .
COPY matrix-commander.py .

RUN pip3 install -r /app/requirements.txt

VOLUME /data

ENTRYPOINT ["/bin/python3", "/app/matrix-commander.py" ,"-s", "/data/store", "-c", "/data/credentials.json"]