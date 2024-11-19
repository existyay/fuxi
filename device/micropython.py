'''
实验名称：DHT11 + 土壤湿度传感器 + MQTT 数据发送 + OLED 显示
版本：v2.2
日期：2024.11
说明：通过 DHT11 采集温湿度数据，ADC 采集土壤湿度数据，通过 MQTT 定时发布数据，并在 OLED 显示屏上显示数据内容，支持 MQTT 用户认证及心跳机制。
'''

# 引入相关模块
import network
import time
from machine import Pin, ADC, Timer, SoftI2C
from ssd1306 import SSD1306_I2C
import dht
from simple import MQTTClient

# 初始化 OLED 显示屏
i2c = SoftI2C(sda=Pin(42), scl=Pin(40))  # 根据实际接线调整 SDA 和 SCL 引脚
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

# 初始化 DHT11 传感器和土壤湿度传感器
dht_sensor = dht.DHT11(Pin(1))  # DHT11 数据引脚
soil_sensor = ADC(Pin(10))  # 土壤湿度传感器数据引脚
soil_sensor.atten(ADC.ATTN_11DB)  # 开启 11DB 衰减，量程增至 0-3.3V

# Wi-Fi 连接函数
def WIFI_Connect():
    wlan = network.WLAN(network.STA_IF)  # STA 模式
    wlan.active(True)  # 激活接口
    start_time = time.time()  # 记录时间做超时判断

    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect('Yqh', '88888888')  # 输入 Wi-Fi 账号密码
        while not wlan.isconnected():
            time.sleep_ms(500)
            if time.time() - start_time > 15:
                print('WiFi Connected Timeout!')
                return False

    print('Network connected:', wlan.ifconfig())
    return True

# 发布传感器数据的任务，并显示到 OLED
def MQTT_Send(tim):
    try:
        # 获取 DHT11 数据
        dht_sensor.measure()
        temperature = dht_sensor.temperature()  # 温度
        humidity = dht_sensor.humidity()  # 湿度

        # 获取土壤湿度数据
        soil_value = soil_sensor.read()  # 获取 ADC 数值
        soil_voltage = soil_value / 4095 * 3.3  # 计算电压值

        # 构造发送的 MQTT 消息
        message = {
            "temperature": temperature,
            "humidity": humidity,
            "soil_moisture_value": soil_value,
            "soil_moisture_voltage": round(soil_voltage, 2),
        }

        # 发布 MQTT 消息
        client.publish(TOPIC, str(message))
        print("Sent MQTT message:", message)

        # 更新 OLED 显示内容
        oled.fill(0)  # 清屏背景黑色
        oled.text('01Studio', 0, 0)
        oled.text('MQTT Data Sent:', 0, 10)
        oled.text('Temp: {} C'.format(temperature), 0, 30)
        oled.text('Hum: {} %'.format(humidity), 0, 40)
        oled.text('Soil: {} ({:.2f}V)'.format(soil_value, soil_voltage), 0, 50)
        oled.show()

    except Exception as e:
        print("Error reading sensors or sending MQTT:", e)
        oled.fill(0)
        oled.text('Error occurred', 0, 0)
        oled.text(str(e), 0, 20)
        oled.show()

# MQTT 心跳机制任务
def MQTT_KeepAlive(tim):
    try:
        client.ping()  # 向 Broker 发送心跳包
        print("MQTT Heartbeat Sent")
    except Exception as e:
        print("MQTT Heartbeat Failed:", e)

# 执行 Wi-Fi 连接并初始化 MQTT
if WIFI_Connect():
    SERVER = '222.186.21.66'  # MQTT Broker 地址
    PORT = 1883  # MQTT Broker 端口
    CLIENT_ID = 'ESP32-DHT11-Soil'  # 客户端 ID
    TOPIC = '/sensor'  # 主题名称
    USERNAME = 'sensor'  # 替换为实际 MQTT 用户名
    PASSWORD = 'qwe123'  # 替换为实际 MQTT 密码

    # 初始化 MQTT 客户端，带用户名和密码
    client = MQTTClient(CLIENT_ID, SERVER, PORT, USERNAME, PASSWORD)
    client.connect()
    print("MQTT Connected with authentication!")

    # 定时发布传感器数据
    sensor_timer = Timer(0)
    sensor_timer.init(period=2000, mode=Timer.PERIODIC, callback=MQTT_Send)  # 2 秒周期

    # 定时发送 MQTT 心跳包
    heartbeat_timer = Timer(1)
    heartbeat_timer.init(period=60000, mode=Timer.PERIODIC, callback=MQTT_KeepAlive)  # 60 秒周期
else:
    print("WiFi connection failed!")
