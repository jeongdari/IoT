import serial
import time
import paho.mqtt.client as mqtt

# MQTT configuration
MQTT_BROKER = "13.239.54.89"  # Update with your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC_DHT = "IFN649/Danny/DHT11"
MQTT_TOPIC_COMMAND = "IFN649/Danny/command"

# Bluetooth Serial Port settings
rfcomm0_port = "/dev/rfcomm0"  # For the first Teensy (DHT11 sensor)
rfcomm1_port = "/dev/rfcomm1"  # For the second Teensy (LED control)
baud_rate = 9600

# Initialize Serial connections
try:
    ser_dht = serial.Serial(rfcomm0_port, baud_rate)
    ser_dht.write(str.encode('Start\r\n'))
    print("Serial connection to /dev/rfcomm0 (DHT11) established.")
except Exception as e:
    print(f"Failed to open serial port /dev/rfcomm0: {e}")
    exit(1)

try:
    ser_led = serial.Serial(rfcomm1_port, baud_rate)
    print("Serial connection to /dev/rfcomm1 (LED control) established.")
except Exception as e:
    print(f"Failed to open serial port /dev/rfcomm1: {e}")
    exit(1)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_COMMAND)

def on_message(client, userdata, msg):
    command = msg.payload.decode()
    print(f"Received command on {msg.topic}: {command}")
    
    try:
        # Send the command to the second Teensy over Bluetooth
        ser_led.write((command + '\n').encode())
        print(f"Sent command to Teensy: {command}")
    except Exception as e:
        print(f"Error sending command to Teensy: {e}")

def publish_data(topic, data):
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.publish(topic, data)
        client.disconnect()
        print(f"Data published to {topic}: {data}")
    except Exception as e:
        print(f"Failed to publish to MQTT broker: {e}")

def main():
    # Set up MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Start the MQTT client loop
    client.loop_start()

    try:
        while True:
            # Read from DHT11 sensor
            if ser_dht.in_waiting > 0:
                raw_data_dht = ser_dht.readline()
                data_dht = raw_data_dht.decode('utf-8').strip()
                publish_data(MQTT_TOPIC_DHT, data_dht)
                print(f"DHT11 Data: {data_dht}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program")
    except Exception as e:
        print(f"Error during data read or MQTT publish: {e}")
    finally:
        ser_dht.close()
        ser_led.close()
        client.loop_stop()

if __name__ == "__main__":
    main()
