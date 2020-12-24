
ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

LABEL Description="This image is used to start a script that will monitor for RF events on 433Mhz (configurable) and send the data to an MQTT server"

RUN apk add --no-cache --virtual build-deps alpine-sdk cmake git libusb-dev python3 python3-dev python3-pip && \
    pip3 install paho-mqtt && \
    mkdir /tmp/src && \
    cd /tmp/src && \
    git clone git://git.osmocom.org/rtl-sdr.git && \
    mkdir /tmp/src/rtl-sdr/build && \
    cd /tmp/src/rtl-sdr/build && \
    cmake ../ -DINSTALL_UDEV_RULES=ON -DDETACH_KERNEL_DRIVER=ON -DCMAKE_INSTALL_PREFIX:PATH=/usr/local && \
    make && \
    make install && \
    chmod +s /usr/local/bin/rtl_* && \
    cd /tmp/src/ && \
    git clone https://github.com/merbanan/rtl_433 && \
    cd rtl_433/ && \
    mkdir build && \
    cd build && \
    cmake ../ && \
    make && \
    make install && \
    apk del build-deps && \
    rm -r /tmp/src && \
    apk add --no-cache libusb mosquitto-clients jq

ENV MQTT_HOST="core-mosquitto"
ENV MQTT_USER="my_user"
ENV MQTT_PASS="my_password"
ENV MQTT_TOPIC="homeassistant"

COPY run.sh /
COPY rtl2mqtt.py /

RUN ["chmod", "a+x", "./run.sh"]
RUN ["chmod", "a+x", "./rtl2mqtt.py"]
CMD [ "./run.sh" ]
