// Define pins for the ultrasonic sensor
const int trigPin = 9;
const int echoPin = 10;

void setup() {
  // Start the serial monitor at 9600 baud
  Serial.begin(9600);
  
  // Set up the pin modes
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  long duration;
  float distance;

  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Trigger the sensor with a 10 microsecond pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read the echo pin (returns the time in microseconds)
  duration = pulseIn(echoPin, HIGH);

  // Convert the duration to distance in cm
  distance = duration * 0.0343 / 2;

  // Only print if object is within 30 cm
  if (distance <= 80.0) {
    Serial.print(1);
  }

  delay(100); // Small delay to reduce serial spam
}
