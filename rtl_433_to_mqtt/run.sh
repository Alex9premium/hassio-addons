#!/bin/sh

export LANG=C
PATH="/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin"

CONFIG_PATH=/data/options.json
MQTT_HOST="$(jq --raw-output '.mqtt_host' $CONFIG_PATH)"
MQTT_USER="$(jq --raw-output '.mqtt_user' $CONFIG_PATH)"
MQTT_PASS="$(jq --raw-output '.mqtt_password' $CONFIG_PATH)"
MQTT_TOPIC="$(jq --raw-output '.mqtt_topic' $CONFIG_PATH)"
PROTOCOL="$(jq --raw-output '.protocol' $CONFIG_PATH)"
FREQUENCY="$(jq --raw-output '.frequency' $CONFIG_PATH)"
GAIN="$(jq --raw-output '.gain' $CONFIG_PATH)"
OFFSET="$(jq --raw-output '.frequency_offset' $CONFIG_PATH)"
SAMPLE_RATE="$(jq --raw-output '.sample_rate' $CONFIG_PATH)"


echo "Starting RTL_433 with parameters:"
echo "MQTT Host =" $MQTT_HOST
echo "MQTT User =" $MQTT_USER
echo "MQTT Password =" $MQTT_PASS
echo "MQTT Topic =" $MQTT_TOPIC
echo "RTL_433 Protocol =" $PROTOCOL
echo "RTL_433 Frequency =" $FREQUENCY
echo "RTL_433 Gain =" $GAIN
echo "RTL_433 Frequency Offset =" $OFFSET
echo "RTL_433 Sample Rate =" $SAMPLE_RATE


exec python3 /rtl2mqtt.py "$MQTT_HOST" "$MQTT_USER" "$MQTT_PASS" "$MQTT_TOPIC" "$PROTOCOL" "$FREQUENCY" "$GAIN" "$OFFSET" "$SAMPLE_RATE"