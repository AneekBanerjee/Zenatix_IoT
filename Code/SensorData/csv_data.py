# import RPi.GPIO as GPIO
# import dht11
import datetime,random


def get_sensor_data():
    """
    Collect sensor data from DHT11. We have to import RPi.GPIO and dht11 external library
    of micro-Python. As Raspberry-Pi and sensor not physically available here, generate
    random temperature between 0 to 100 centigrade.
    """
    # Rpi and DHT11 sensor communication and collection code
    '''
    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    # read data using pin 14
    instance = dht11.DHT11(pin = 14)
    result = instance.read()
    if result.is_valid():
        print("Temperature: %d C" % result.temperature)
        return result.temperature
    else:
        print("Error: %d" % result.error_code)
        return result.error_code
    '''
    # Create random temperature between 0 to 100 centigrade
    sensor_data = random.uniform(0.0, 100.0)
    print(sensor_data)
    return sensor_data

def run_sensor():
    """
    Create dictionary format including sensor-name, runtime, temperature data. 
    """
    _time = str(datetime.datetime.now())
    _time = [_time]
    _data = get_sensor_data()
    data = [_data]
    sensor = ["sensor_2"]
    
    # dictionary of lists 
    dict = {'Timestamp': _time, 'Value': data, 'Sensor': sensor} 
    return dict


if __name__ == "__main__":
    run_sensor()