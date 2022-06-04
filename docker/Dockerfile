FROM fedora:35

# standard install packages: pip libolm-devel gcc python-devel python3-dbus
# additional packages: libffi-devel libjpeg-devel zlib-devel (required on Raspberry Pi (4b, 32bit, running buster of Raspberry Pi OS))
RUN \
  dnf install -y --nodocs \
    gcc \
    libolm-devel \
    libffi-devel \
    libjpeg-devel \
    pip \
    python-devel \
    python3-dbus \
    zlib-devel \
  && dnf clean all \
  && rm -rf /var/cache/yum/

RUN pip3 install --no-cache wheel

RUN mkdir -vp /app/matrix_commander/

WORKDIR /app/
COPY requirements.txt .
RUN pip3 install --no-cache -r requirements.txt

WORKDIR /app/matrix_commander/
COPY matrix_commander/matrix_commander.py .
COPY matrix_commander/matrix-commander .
COPY matrix_commander/__init__.py .

VOLUME /data

ENTRYPOINT ["/bin/python3", "/app/matrix_commander/matrix-commander" ,"-s", "/data/store", "-c", "/data/credentials.json"]
