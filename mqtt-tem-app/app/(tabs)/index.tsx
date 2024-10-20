import { Image, StyleSheet, View, Dimensions } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

const { width: windowWidth, height: windowHeight } = Dimensions.get('window'); // Get screen width and height

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      {/* Image in the top half of the screen */}
      <View style={styles.topHalf}>
        <Image
          source={require('@/assets/images/Charmyglass.png')} // Path to your image
          style={styles.logo}
          resizeMode="contain" // Keep image ratio while fitting in the space
        />
      </View>

      {/* Text in the bottom half of the screen */}
      <View style={styles.bottomHalf}>
        <ThemedView style={styles.textBox}>
          <ThemedText type="title" style={styles.text}>
            Main Cooling Room
          </ThemedText>
        </ThemedView>
        <ThemedView style={styles.textBox}>
          <ThemedText type="title" style={styles.text}>
            Temperature Monitoring App
          </ThemedText>
        </ThemedView>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, // Container takes up the whole screen
  },
  topHalf: {
    flex: 1, // Top half of the screen
    justifyContent: 'center', // Vertically center the content
    alignItems: 'center', // Horizontally center the content
  },
  logo: {
    width: windowWidth, // Set the image width to 80% of the screen width
    height: '80%', // The image height takes up 80% of the top half
  },
  bottomHalf: {
    flex: 1, // Bottom half of the screen
    justifyContent: 'center', // Vertically center the text
    alignItems: 'center', // Horizontally center the text
    backgroundColor: '#fff', // White background
  },
  textBox: {
    marginBottom: 20, // Add space between the text boxes
    alignItems: 'center', // Center align the text horizontally
  },
  text: {
    fontSize: 24, // Text size
    fontWeight: 'bold', // Bold text
    color: '#333', // Text color
    textAlign: 'center', // Center-align the text
  },
});
