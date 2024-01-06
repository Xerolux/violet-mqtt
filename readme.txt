violet-mqtt all in one topic

violet-mqtt-topic all in an seperate topic


Install:
    Debian 12:
    apt install python3-pip python3-venv git
Create Python3-venv
    python3 -m venv /root/violet-venv
Activate venv
    source /root/violet-venv/bin/activate
Pull git
    git pull https://github.com/Xerolux/violet-mqtt.git

please edit the following line in the *.py and replace with you data

    api_url = "https://your.api.endpoint/data"  # Replace with your API endpoint
    mqtt_broker_address = "mqtt.eclipse.org"  # Replace with your MQTT broker address
    mqtt_port = 1883  # Replace with your MQTT broker port
    base_mqtt_topic = "your/mqtt/base/topic"  # Replace with your desired base MQTT topic
    mqtt_username = "your_mqtt_username"  # Replace with your MQTT username
    mqtt_password = "your_mqtt_password"  # Replace with your MQTT password

Run
    /root/violet-venv/bin/python violett-mqtt.py
    or
    /root/violet-venv/bin/python violett-mqtt-topic.py



