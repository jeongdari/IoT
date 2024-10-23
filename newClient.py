import sqlite3
from flask import Flask, jsonify
import paho.mqtt.client as mqtt

# MQTT configuration
MQTT_BROKER = "13.239.54.89"  # Replace with your MQTT broker IP
MQTT_PORT = 1883
MQTT_TOPIC_DHT = "IFN649/Danny/DHT11"
MQTT_TOPIC_COMMAND = "IFN649/Danny/command"

# SQLite database setup
DATABASE = 'sensor_data.db'

# Initialize the database and create table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SensorData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity REAL,
            temperature REAL,
            heat_index REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Insert sensor data into the database
def insert_data(humidity, temperature, heat_index):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO SensorData (humidity, temperature, heat_index)
        VALUES (?, ?, ?)
    ''', (humidity, temperature, heat_index))
    conn.commit()
    conn.close()

# Flask API to get stored sensor data
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, humidity, temperature, heat_index, timestamp FROM SensorData')
    rows = cursor.fetchall()
    conn.close()
    
    # Convert the rows into a list of dictionaries for JSON response
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'humidity': row[1],
            'temperature': row[2],
            'heat_index': row[3],
            'timestamp': row[4]
        })
    
    return jsonify(data)

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_DHT)  # Subscribe to sensor data topic

# MQTT on_message callback
def on_message(client, userdata, msg):
    data = msg.payload.decode()
    print(f"Received data on {msg.topic}: {data}")

    # Parse the received sensor data
    if "Temperature:" in data:
        try:
            humidity = float(data.split("Humidity: ")[1].split("%")[0])
            temperature = float(data.split("Temperature: ")[1].split("C")[0])
            heat_index = float(data.split("Heat index: ")[1].split("C")[0])

            # Insert the data into the database
            insert_data(humidity, temperature, heat_index)
            print(f"Data saved: Humidity={humidity}, Temperature={temperature}, Heat Index={heat_index}")
        
            # Determine if the LED should be red or green based on temperature
            if temperature > 25:
                command = "RED_ON"
            else:
                command = "GREEN_ON"
            publish_command(command)
        except Exception as e:
            print(f"Failed to process data: {e}")

# Publish command to the Raspberry Pi (Teensy LED control)
def publish_command(command):
    try:
        client.publish(MQTT_TOPIC_COMMAND, command)
        print(f"Command published: {command}")
    except Exception as e:
        print(f"Failed to publish command: {e}")

# Main function to run MQTT client and Flask API together
def main():
    # Initialize the SQLite database
    init_db()

    # MQTT client setup
    global client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the MQTT client loop in a background thread
    client.loop_start()

    # Run Flask API for REST endpoint
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
