import network
import urequests
import sh1106
from machine import ADC, Pin, I2C
from time import sleep

SSID = "Arushi"
PASSWORD = "arushiii"

SERVER_URL = "http://192.168.234.20:5000/upload"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("🔌 Connecting to WiFi...", end="")
    while not wlan.isconnected():
        sleep(1)
        print(".", end="")
    print("\n✅ Connected:", wlan.ifconfig())

gas_sensor = ADC(Pin(34))
gas_sensor.atten(ADC.ATTN_11DB) 



i2c = I2C(0, scl=Pin(22), sda=Pin(21))  
oled = sh1106.SH1106_I2C(128, 64, i2c)  
connect_wifi()
while True:
    gas_value = gas_sensor.read()
    print("Gas Value:", gas_value)
    oled.fill(0)

    oled.text("Gas Sensor", 0, 0)
    oled.text("Value: {}".format(gas_value), 0, 20)

    oled.show()
    try:
        response = urequests.post(
            SERVER_URL,
            json={"gas_value": gas_value},
            headers={"Content-Type": "application/json"}
        )
        print("✅ Sent:", response.text)
    except Exception as e:
        print("❌ Error:", e)
    sleep(0.2)
