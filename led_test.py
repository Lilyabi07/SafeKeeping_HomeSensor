#TEST the leds - when set up in the right pin connectors, each should run flash in succession,3 times,

import RPi.GPIO as GPIO
import time

# Pin setup
LED_PINS = [16, 26, 21]  # Red, Blue, Green

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Initialize all LEDs
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

print("Starting LED test. Each LED will flash in sequence.")

try:
    for i in range(3):  # Run 3 full cycles
        for pin, color in zip(LED_PINS, ["RED", "BLUE", "GREEN"]):
            print(f"{color} ON")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.3)
    print("Test complete. All LEDs cycled successfully.")
except KeyboardInterrupt:
    print("Test interrupted by user.")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")
