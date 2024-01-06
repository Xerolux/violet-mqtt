import json
import requests
import paho.mqtt.publish as publish
import time

def get_json_from_api(api_url, username, password):
    try:
        # Make a GET request to the API with authentication
        response = requests.get(api_url, auth=(username, password))

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON data from the response
            json_data = response.json()
            return json_data
        else:
            # Print an error message if the request was not successful
            print(f"Error: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        # Print an error message if an exception occurs during the request
        print(f"Error: {e}")
        return None

def publish_to_mqtt(broker_address, port, base_topic, payload, username, password):
    for key, value in payload.items():
        topic = f"{base_topic}/{key}"
        publish.single(topic, payload=json.dumps(value), qos=1, retain=False,
                       hostname=broker_address, port=port, auth={'username': username, 'password': password})

if __name__ == "__main__":
    # Configuration
    api_url = "https://your.api.endpoint/data"  # Replace with your API endpoint
    mqtt_broker_address = "mqtt.eclipse.org"  # Replace with your MQTT broker address
    mqtt_port = 1883  # Replace with your MQTT broker port
    base_mqtt_topic = "your/mqtt/base/topic"  # Replace with your desired base MQTT topic
    mqtt_username = "your_mqtt_username"  # Replace with your MQTT username
    mqtt_password = "your_mqtt_password"  # Replace with your MQTT password

    try:
        while True:
            # Read JSON data from API
            json_data = get_json_from_api(api_url, mqtt_username, mqtt_password)

            if json_data:
                # Publish each line of JSON data to a separate MQTT topic
                publish_to_mqtt(mqtt_broker_address, mqtt_port, base_mqtt_topic, json_data, mqtt_username, mqtt_password)
                print("Data published to MQTT successfully.")
            else:
                print("Failed to retrieve JSON data from the API.")

            # Wait for 30 seconds before the next iteration
            time.sleep(30)

    except KeyboardInterrupt:
        print("Script terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
