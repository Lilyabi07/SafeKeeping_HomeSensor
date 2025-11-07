# # dht_test.py
# import time
# import board
# import adafruit_dht

# #dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)  # board.D4 = GPIO4
# dht = adafruit_dht.DHT11(board.D17, use_pulseio=False)

# print("Starting DHT11 test. Ctrl-C to quit.")
# try:
    # while True:
        # try:
            # t = dht.temperature
            # h = dht.humidity
            # print(f"Temperature: {t} °C   Humidity: {h} %")
        # except RuntimeError as e:
            # # common: read failures — retry after short sleep
            # print("RuntimeError reading DHT11 (expected sometimes):", e)
        # except Exception as e:
            # print("Unexpected error:", e)
            # raise
        # time.sleep(2.0)
# finally:
    # try:
        # dht.exit()
    # except Exception:
        # pass


# dht_quick_test.py
import board
import adafruit_dht

#dht = adafruit_dht.DHT11(board.D4, use_pulseio=False)  # Use GPIO4
dht = adafruit_dht.DHT11(board.D17, use_pulseio=False)

try:
    t = dht.temperature
    h = dht.humidity
    print(f"Temp={t}°C, Humidity={h}%")
except Exception as e:
    print("Error reading DHT11:", e)
