import requests
import threading

# Replace with the actual IP address of your ESP8266
ESP8266_IP = 'http://192.168.200.158'

def turn_led_on():
    response = requests.get(f'{ESP8266_IP}/?led=on')
    # if response.status_code == 200:
    #     print('LED turned ON')
    # else:
    #     print('Failed to turn LED ON')

def turn_led_off():
    response = requests.get(f'{ESP8266_IP}/?led=off')
    # if response.status_code == 200:
    #     print('LED turned OFF')
    # else:
    #     print('Failed to turn LED OFF')

def blink_led():
    response = requests.get(f'{ESP8266_IP}/?led=blink')

def run_blink_led_thread():
    thread = threading.Thread(target=blink_led)
    thread.start()

def get_led_status():
    response = requests.get(ESP8266_IP)
    if response.status_code == 200:
        if 'LED is currently: <strong>ON</strong>' in response.text:
            print('LED is currently ON')
        elif 'LED is currently: <strong>OFF</strong>' in response.text:
            print('LED is currently OFF')
        else:
            print('Unable to determine LED status')
    else:
        print('Failed to get LED status')

# Example usage
turn_led_on()
get_led_status()
turn_led_off()
get_led_status()
run_blink_led_thread()
print("LED is blinking...")
get_led_status()
