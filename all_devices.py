

# # all_devices.py
# import time
# import os
# from datetime import datetime
# import RPi.GPIO as GPIO
# import cv2

# # Import custom modules
# from environmental_module import environmental_module
# from security_module import security_module

# # --- GPIO Setup ---
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM)

# # --- PIN SETUP ---
# SERVO_PIN = 24
# BUZZER_PIN = 25

# # --- LED PINS ---
# RED_LED = 16
# BLUE_LED = 26
# GREEN_LED = 21

# # --- GPIO Configurations ---
# GPIO.setup(SERVO_PIN, GPIO.OUT)
# GPIO.setup(BUZZER_PIN, GPIO.OUT)
# GPIO.setup(RED_LED, GPIO.OUT)
# GPIO.setup(BLUE_LED, GPIO.OUT)
# GPIO.setup(GREEN_LED, GPIO.OUT)

# # --- SERVO SETUP ---
# servo = GPIO.PWM(SERVO_PIN, 50)
# servo.start(0)

# def set_angle(angle):
    # """Move servo to a given angle (0–180)."""
    # duty = 2 + (angle / 18)
    # GPIO.output(SERVO_PIN, True)
    # servo.ChangeDutyCycle(duty)
    # time.sleep(0.4)
    # GPIO.output(SERVO_PIN, False)
    # servo.ChangeDutyCycle(0)

# # --- BUZZER FUNCTION ---
# def play_buzzer(tone_duration=0.3, repeats=2):
    # """Play a short chime-like pattern on the passive buzzer."""
    # pattern = [(1200, 0.12), (900, 0.10), (1500, 0.18)]
    # for _ in range(repeats):
        # for freq, duration in pattern:
            # buzzer_pwm = GPIO.PWM(BUZZER_PIN, freq)
            # buzzer_pwm.start(60)
            # time.sleep(duration)
            # buzzer_pwm.stop()
            # time.sleep(0.08)
        # time.sleep(0.25)

# # --- LED FUNCTIONS ---
# def led_off_all():
    # GPIO.output(RED_LED, GPIO.LOW)
    # GPIO.output(BLUE_LED, GPIO.LOW)
    # GPIO.output(GREEN_LED, GPIO.LOW)

# def led_status_update(temp, motion_detected):
    # """Update LEDs based on DHT11 readings and motion."""
    # GPIO.output(BLUE_LED, GPIO.HIGH)  # Blue = system active
    # GPIO.output(RED_LED, GPIO.HIGH if motion_detected else GPIO.LOW)  # Red = motion
    # GPIO.output(GREEN_LED, GPIO.HIGH if 20 <= temp <= 25 else GPIO.LOW)  # Green = ideal temp range

# def test_leds():
    # """Cycle LEDs in sequence twice."""
    # print("Testing LEDs (2 rounds)...")
    # for round_num in range(2):
        # print(f"Round {round_num + 1}")
        # for pin, color in [(RED_LED, "RED"), (BLUE_LED, "BLUE"), (GREEN_LED, "GREEN")]:
            # print(f"{color} ON")
            # GPIO.output(pin, GPIO.HIGH)
            # time.sleep(0.5)
            # GPIO.output(pin, GPIO.LOW)
            # time.sleep(0.3)
        # print("Round complete.\n")
        # led_off_all()
        # time.sleep(0.8)
    # print("LED test complete.\n")

# # --- Initialize Modules ---
# env_sensor = environmental_module(config_file="config.json")
# sec_module = security_module(config_file="config.json")

# # --- Motion State Tracking for Debounce/Cooldown ---
# last_motion_time = 0
# motion_cooldown = 5  # seconds to wait before reacting again

# # --- PIR + DHT11 FUNCTION ---
# def check_motion():
    # """Check motion using security_module and update LEDs with environmental data."""
    # global last_motion_time

    # env_data = env_sensor.get_environmental_data()
    # temp = env_data["temperature"]

    # sec_data = sec_module.get_security_data()
    # motion_detected = sec_data["motion_detected"]

    # print(f"[DEBUG] Motion Detected Raw Value: {motion_detected}")

    # led_status_update(temp, motion_detected)

    # # --- Local logging ---
    # with open("temperature_log.txt", "a") as f:
        # log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Temp: {temp}°C, Humidity: {env_data['humidity']}%, Motion: {motion_detected}\n"
        # f.write(log_entry)

    # # --- Handle motion with cooldown ---
    # current_time = time.time()
    # if motion_detected and (current_time - last_motion_time) > motion_cooldown:
        # print(f"Motion detected! Temp={temp}°C Humidity={env_data['humidity']}%")
        # play_buzzer(tone_duration=0.15, repeats=1)
        # last_motion_time = current_time
    # else:
        # print(f"No motion. Temp={temp}°C Humidity={env_data['humidity']}%")

    # return motion_detected

# # --- MAIN MENU ---
# try:
    # print("=== Raspberry Pi Integrated Device Test ===")
    # print("1. Servo Sweep")
    # print("2. Buzzer Test")
    # print("3. LED Test")
    # print("4. PIR + DHT11 + Camera Test")
    # print("q. Quit\n")

    # while True:
        # choice = input("Select test (1/2/3/4/q): ").strip().lower()

        # if choice == "1":
            # print("Sweeping servo...")
            # for angle in [0, 90, 180, 90, 0]:
                # set_angle(angle)
                # time.sleep(0.5)
            # print("Servo test complete.\n")

        # elif choice == "2":
            # print("Playing buzzer tone...")
            # play_buzzer(tone_duration=0.25, repeats=5)
            # print("Buzzer test complete.\n")

        # elif choice == "3":
            # test_leds()

        # elif choice == "4":
            # print("Starting PIR + DHT11 + Camera test. Move in front of the sensor...")
            # try:
                # while True:
                    # check_motion()
                    # time.sleep(1.0)
            # except KeyboardInterrupt:
                # print("Stopping motion test.\n")
                # led_off_all()

        # elif choice == "q":
            # print("Exiting program...")
            # break

        # else:
            # print("Invalid selection. Try again.\n")

# finally:
    # servo.stop()
    # GPIO.cleanup()
    # print("GPIO cleanup done.")









# all_devices.py
import time
import os
from datetime import datetime
import RPi.GPIO as GPIO
import cv2

# Import custom modules
from environmental_module import environmental_module
from security_module import security_module
from MQTT_communication import MQTT_communicator

# --- GPIO Setup ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# --- PIN SETUP ---
SERVO_PIN = 24
BUZZER_PIN = 25

# --- LED PINS ---
RED_LED = 16
BLUE_LED = 26
GREEN_LED = 21

# --- GPIO Configurations ---
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# --- SERVO SETUP ---
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.4)
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

# --- BUZZER FUNCTION ---
def play_buzzer(tone_duration=0.3, repeats=2):
    pattern = [(1200, 0.12), (900, 0.10), (1500, 0.18)]
    for _ in range(repeats):
        for freq, duration in pattern:
            buzzer_pwm = GPIO.PWM(BUZZER_PIN, freq)
            buzzer_pwm.start(60)
            time.sleep(duration)
            buzzer_pwm.stop()
            time.sleep(0.08)
        time.sleep(0.25)

# --- LED FUNCTIONS ---
def led_off_all():
    GPIO.output(RED_LED, GPIO.LOW)
    GPIO.output(BLUE_LED, GPIO.LOW)
    GPIO.output(GREEN_LED, GPIO.LOW)

def led_status_update(temp, motion_detected):
    GPIO.output(BLUE_LED, GPIO.HIGH)  # Blue = system active
    GPIO.output(GREEN_LED, GPIO.HIGH if 20 <= temp <= 25 else GPIO.LOW)
    if motion_detected:
        GPIO.output(RED_LED, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(RED_LED, GPIO.LOW)
    else:
        GPIO.output(RED_LED, GPIO.LOW)

# --- LED TEST FUNCTION ---
def test_leds():
    print("Testing LEDs (2 rounds)...")
    for round_num in range(2):
        print(f"Round {round_num + 1}")
        for pin, color in [(RED_LED, "RED"), (BLUE_LED, "BLUE"), (GREEN_LED, "GREEN")]:
            print(f"{color} ON")
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.3)
        led_off_all()
        time.sleep(0.8)
    print("LED test complete.\n")

# --- Initialize Modules ---
env_sensor = environmental_module(config_file="config.json")
sec_module = security_module(config_file="config.json")
mqtt_client = MQTT_communicator(config_file="config.json")

# --- Motion State Tracking ---
last_motion_time = 0
motion_cooldown = 5  # seconds

# --- PIR + DHT11 FUNCTION ---
def check_motion():
    global last_motion_time
    current_time = time.time()

    env_data = env_sensor.get_environmental_data()
    temp = env_data["temperature"]
    humidity = env_data["humidity"]

    sec_data = sec_module.get_security_data()
    motion_detected = sec_data["motion_detected"]

    print(f"[DEBUG] Motion Detected Raw Value: {motion_detected}")

    led_status_update(temp, motion_detected)

    # --- Log to local file ---
    with open("temperature_log.txt", "a") as f:
        log_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Temp: {temp}°C, Humidity: {humidity}%, Motion: {motion_detected}\n"
        f.write(log_entry)

    # --- Send to Adafruit ---
    mqtt_client.send_to_adafruit_io("temperature", temp)
    mqtt_client.send_to_adafruit_io("humidity", humidity)

    if motion_detected and (current_time - last_motion_time) > motion_cooldown:
        print(f"Motion detected! Temp={temp}°C Humidity={humidity}%")
        play_buzzer(tone_duration=0.15, repeats=1)
        last_motion_time = current_time
    else:
        print(f"No motion. Temp={temp}°C Humidity={humidity}%")

    return motion_detected

# --- MAIN MENU ---
try:
    print("=== Raspberry Pi Integrated Device Test ===")
    print("1. Servo Sweep")
    print("2. Buzzer Test")
    print("3. LED Test")
    print("4. PIR + DHT11 + Camera Test")
    print("q. Quit\n")

    while True:
        choice = input("Select test (1/2/3/4/q): ").strip().lower()

        if choice == "1":
            print("Sweeping servo...")
            for angle in [0, 90, 180, 90, 0]:
                set_angle(angle)
                time.sleep(0.5)
            print("Servo test complete.\n")

        elif choice == "2":
            print("Playing buzzer tone...")
            play_buzzer(tone_duration=0.25, repeats=5)
            print("Buzzer test complete.\n")

        elif choice == "3":
            test_leds()

        elif choice == "4":
            print("Starting PIR + DHT11 + Camera test. Move in front of the sensor...")
            try:
                while True:
                    check_motion()
                    time.sleep(1.0)
            except KeyboardInterrupt:
                print("Stopping motion test.\n")
                led_off_all()

        elif choice == "q":
            print("Exiting program...")
            break

        else:
            print("Invalid selection. Try again.\n")

finally:
    servo.stop()
    GPIO.cleanup()
    print("GPIO cleanup done.")

