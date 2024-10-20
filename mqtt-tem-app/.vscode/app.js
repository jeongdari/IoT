import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import mqtt from 'mqtt';

// MQTT Configuration
const MQTT_BROKER = 'mqtt://13.239.54.89'; // Replace with your EC2 MQTT broker IP
const MQTT_PORT = 1883;
const MQTT_TOPIC_DHT = 'IFN649/Danny/DHT11'; // Topic for sensor data

export default function App() {
  const [temperature, setTemperature] = useState(null);
  const [humidity, setHumidity] = useState(null);
  const [dataHistory, setDataHistory] = useState([]);

  useEffect(() => {
    // Connect to the MQTT broker
    const client = mqtt.connect(MQTT_BROKER, {
      port: MQTT_PORT,
    });

    client.on('connect', () => {
      console.log('Connected to MQTT Broker');
      client.subscribe(MQTT_TOPIC_DHT, (err) => {
        if (err) {
          console.error('Subscription error: ', err);
        } else {
          console.log('Subscribed to topic:', MQTT_TOPIC_DHT);
        }
      });
    });

    client.on('message', (topic, message) => {
      if (topic === MQTT_TOPIC_DHT) {
        const data = message.toString();
        console.log('Received data:', data);

        // Assuming data format is "Humidity: XX% Temperature: XX°C"
        const humidityMatch = data.match(/Humidity:\s([0-9.]+)%/);
        const temperatureMatch = data.match(/Temperature:\s([0-9.]+)C/);

        const humidityValue = humidityMatch ? parseFloat(humidityMatch[1]) : null;
        const temperatureValue = temperatureMatch ? parseFloat(temperatureMatch[1]) : null;

        if (humidityValue !== null && temperatureValue !== null) {
          setHumidity(humidityValue);
          setTemperature(temperatureValue);

          // Add new data to history
          setDataHistory((prevHistory) => [
            { timestamp: new Date(), temperature: temperatureValue, humidity: humidityValue },
            ...prevHistory,
          ]);
        }
      }
    });

    return () => {
      client.end(); // Clean up the MQTT client when the component is unmounted
    };
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Real-time Sensor Data</Text>

      <View style={styles.dataContainer}>
        <Text style={styles.dataLabel}>Temperature:</Text>
        <Text style={styles.dataValue}>{temperature !== null ? `${temperature} °C` : 'Loading...'}</Text>
      </View>

      <View style={styles.dataContainer}>
        <Text style={styles.dataLabel}>Humidity:</Text>
        <Text style={styles.dataValue}>{humidity !== null ? `${humidity} %` : 'Loading...'}</Text>
      </View>

      <Text style={styles.title}>Data History</Text>
      <FlatList
        data={dataHistory}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <Text style={styles.historyItem}>
            {item.timestamp.toLocaleTimeString()}: Temp: {item.temperature}°C, Humidity: {item.humidity}%
          </Text>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    backgroundColor: '#f0f0f0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  dataContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
  },
  dataLabel: {
    fontSize: 18,
  },
  dataValue: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  historyItem: {
    fontSize: 16,
    padding: 5,
  },
});
