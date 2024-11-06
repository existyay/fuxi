from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import base64

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置MySQL数据库连接
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="@qwert12345Ljj",
    database="smart_agriculture"
)

cursor = db.cursor()

# 接收图像数据的API
@app.route('/api/upload_image', methods=['POST'])
def upload_image():
    data = request.json
    temperature = data['temperature']
    humidity = data['humidity']
    soil_moisture = data['soil_moisture']
    image_base64 = data['image']

    # 将图像数据解码为二进制
    image_data = base64.b64decode(image_base64)

    # 将数据插入MySQL数据库
    sql = "INSERT INTO sensor_data (temperature, humidity, soil_moisture, image) VALUES (%s, %s, %s, %s)"
    val = (temperature, humidity, soil_moisture, image_data)
    cursor.execute(sql, val)
    db.commit()

    return jsonify({'status': 'success'})

# 获取传感器数据的API
@app.route('/api/sensor_data', methods=['GET'])
def get_sensor_data():
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    sensor_data = {
        'temperature': result[1],
        'humidity': result[2],
        'soil_moisture': result[3],
        'image': base64.b64encode(result[4]).decode('utf-8')  # 将图像数据编码为Base64字符串
    }
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True)