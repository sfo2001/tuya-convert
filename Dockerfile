FROM alpine:3.19

RUN apk add --update bash git iw dnsmasq hostapd screen curl py3-pip py3-wheel python3-dev mosquitto haveged net-tools openssl openssl-dev gcc musl-dev linux-headers sudo coreutils grep iproute2 ncurses

# Copy requirements first for better layer caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies from requirements.txt
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /tmp/requirements.txt

COPY docker/bin /usr/bin/

COPY . /usr/bin/tuya-convert

WORKDIR "/usr/bin/tuya-convert"

ENTRYPOINT ["tuya-start"]
