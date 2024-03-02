import json
import requests
import paho.mqtt.publish as publish
import time

def get_json_from_api(api_url):
    try:
        # Make a GET request to the API
        response = requests.get(api_url)

        if response.status_code == 200:
            return response.json()
        # Print an error message if the request was not successful
        print(f"Error: {response.status_code}")
        return None

    except requests.exceptions.RequestException as e:
        # Print an error message if an exception occurs during the request
        print(f"Error: {e}")
        return None

def publish_to_mqtt(broker_address, port, topic, payload, username, password):
    publish.single(topic, payload=json.dumps(payload), qos=1, retain=False,
                   hostname=broker_address, port=port, auth={'username': username, 'password': password})

if __name__ == "__main__":
    # Configuration
    api_url = "https://your.api.endpoint/data"  # Replace with your API endpoint
    mqtt_broker_address = "mqtt.eclipse.org"  # Replace with your MQTT broker address
    mqtt_port = 1883  # Replace with your MQTT broker port
    mqtt_topic = "your/mqtt/topic"  # Replace with your desired MQTT topic
    mqtt_username = "your_mqtt_username"  # Replace with your MQTT username
    mqtt_password = "your_mqtt_password"  # Replace with your MQTT password

    try:
        while True:
            if json_data := get_json_from_api(api_url):
                # Publish JSON data to MQTT
                publish_to_mqtt(mqtt_broker_address, mqtt_port, mqtt_topic, json_data, mqtt_username, mqtt_password)
                print("Data published to MQTT successfully.")
            else:
                print("Failed to retrieve JSON data from the API.")

            # Wait for 30 seconds before the next iteration
            time.sleep(30)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
