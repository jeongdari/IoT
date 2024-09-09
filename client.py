import paho.mqtt.client as mqtt

# MQTT configuration
MQTT_BROKER = "13.239.54.89"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC_DHT = "IFN649/Danny/DHT11"
MQTT_TOPIC_COMMAND = "IFN649/Danny/command"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_DHT)  # Subscribe to the topic where sensor dat$

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(f"Received data on {msg.topic}: {data}")
    
    # Example logic to decide when to send a command
    if "Temperature:" in data:  # Adjust this condition as needed
        # Example: Turn on LED if temperature is above a threshold
        temperature = float(data.split("Temperature: ")[1].split("C")[0])
        if temperature > 25:  # Replace with your condition
            command = "LED_ON"
        else:
            command = "LED_OFF"

        # Publish command to Raspberry Pi
        publish_command(command)

def publish_command(command):
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.publish(MQTT_TOPIC_COMMAND, command)
        client.disconnect()
        print(f"Command published: {command}")
    except Exception as e:
        print(f"Failed to publish command: {e}")

def main():
    # Set up MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Start the MQTT client loop
    client.loop_start()
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Start the MQTT client loop
    client.loop_start()

    try:
        # Keep the script running to process incoming messages
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
	    client.loop_stop()

if __name__ == "__main__":
    main()