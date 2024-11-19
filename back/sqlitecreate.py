import sqlite3

# 创建数据库连接
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 创建图片表
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    filename TEXT NOT NULL,
    data BLOB NOT NULL
)
''')

# 创建传感器数据表
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

# 提交更改并关闭连接
conn.commit()
conn.close()