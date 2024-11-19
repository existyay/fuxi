from fastapi import FastAPI, File, UploadFile
import os
from datetime import datetime
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 创建数据库连接
def get_db_connection():
    conn = sqlite3.connect('data.db')
    return conn

# 创建图片表
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        filename TEXT NOT NULL,
        data BLOB NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        temperature REAL NOT NULL,
        humidity REAL NOT NULL,
        soil_moisture_value INTEGER NOT NULL,
        soil_moisture_voltage REAL NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

create_tables()

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    try:
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = os.path.join(UPLOAD_DIR, f"{timestamp}_{image.filename}")

        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())

        # 将图片存储到数据库
        with open(file_path, "rb") as file:
            data = file.read()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO images (timestamp, filename, data)
        VALUES (?, ?, ?)
        ''', (timestamp, image.filename, data))
        conn.commit()
        conn.close()

        return {"message": "图像上传成功"}
    except Exception as e:
        return {"message": f"图像上传失败: {e}"}

# 定时任务：每四小时存储传感器数据
def store_sensor_data():
    try:
        # 获取传感器数据（假设从某个函数获取）
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature = 25.0  # 示例数据
        humidity = 60.0  # 示例数据
        soil_moisture_value = 300  # 示例数据
        soil_moisture_voltage = 1.5  # 示例数据

        # 将传感器数据存储到数据库
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO sensor_data (timestamp, temperature, humidity, soil_moisture_value, soil_moisture_voltage)
        VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, temperature, humidity, soil_moisture_value, soil_moisture_voltage))
        conn.commit()
        conn.close()
        print("传感器数据存储成功")
    except Exception as e:
        print(f"传感器数据存储失败: {e}")

# 初始化定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(store_sensor_data, 'interval', hours=4)
scheduler.start()

# 关闭定时任务
@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()