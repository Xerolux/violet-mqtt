import json
import requests
import paho.mqtt.publish as publish
import time
import os  # For environment variables or configuration file handling

def get_json_from_api(api_url, username, password):
    try:
        # Make a GET request to the API with authentication
        response = requests.get(api_url, auth=(username, password))

        if response.status_code == 200:
            return response.json()
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.reason}")
            return None

    except requests.exceptions.RequestException as e:
        # Print an error message if an exception occurs during the request
        print(f"Request Exception: {e}")
        return None

def publish_to_mqtt(broker_address, port, base_topic, payload, username, password, use_tls=False):
    try:
        auth = {'username': username, 'password': password}
        tls = None

        if use_tls:
            tls = {'ca_certs': None, 'certfile': None, 'keyfile': None,
                   'tls_version': None, 'ciphers': None}

        for key, value in payload.items():
            topic = f"{base_topic}/{key}"
            publish.single(topic, payload=json.dumps(value), qos=1, retain=False,
                           hostname=broker_address, port=port, auth=auth, tls=tls)
        print("Data published to MQTT successfully.")
    except Exception as e:
        print(f"MQTT Publish Exception: {e}")

if __name__ == "__main__":
    # Example of fetching environment variables or using defaults
    api_url = os.getenv('API_URL', "https://your.api.endpoint/data")
    mqtt_broker_address = os.getenv('MQTT_BROKER_ADDRESS', "mqtt.eclipse.org")
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    base_mqtt_topic = os.getenv('BASE_MQTT_TOPIC', "your/mqtt/base/topic")
    mqtt_username = os.getenv('MQTT_USERNAME', "your_mqtt_username")
    mqtt_password = os.getenv('MQTT_PASSWORD', "your_mqtt_password")
    use_tls = os.getenv('USE_TLS', "False").lower() in ("true", "1", "t")

    try:
        while True:
            json_data = get_json_from_api(api_url, mqtt_username, mqtt_password)
            if json_data:
                publish_to_mqtt(mqtt_broker_address, mqtt_port, base_mqtt_topic, json_data, mqtt_username, mqtt_password, use_tls)
            else:
                print("Failed to retrieve JSON data from the API.")

            # Wait for 30 seconds before the next iteration
            time.sleep(30)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
