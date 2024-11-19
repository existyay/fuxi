from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket
from gmqtt import Client as MQTTClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mqtt import FastMQTT, MQTTConfig
from sqlstore import app as sqlstore_app
from typing import Any
import json

# 设置MQTT配置，包括client_id
mqtt_config = MQTTConfig(
    host="222.186.21.66",
    port=1883,
    keepalive=60,
    username="test",
    password="qwe123"
)

# 使用配置创建FastMQTT实例
fast_mqtt = FastMQTT(config=mqtt_config)

@asynccontextmanager
async def _lifespan(_app: FastAPI):
    await fast_mqtt.mqtt_startup()
    yield
    await fast_mqtt.mqtt_shutdown()

app = FastAPI(lifespan=_lifespan)

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/sqlstore", sqlstore_app)

# 存储 WebSocket 连接
websocket_connections = []

# 存储最近的 MQTT 数据
recent_data = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        websocket_connections.remove(websocket)

@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    client.subscribe("sensors")  # 订阅传感器数据主题
    print("Connected: ", client, flags, rc, properties)

@fast_mqtt.subscribe("sensors")
async def home_message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    message = payload.decode()
    print(f"Received message on topic {topic} with payload {message}")
    
    # 将字符串消息转换为字典
    message_dict = eval(message)
    
    data = {
        "topic": topic,
        "message": message_dict
    }
    
    # 保存最近的数据
    recent_data.append(data)
    if len(recent_data) > 10:  # 只保存最近的10条数据
        recent_data.pop(0)
    
    # 将数据发送给所有 WebSocket 连接
    for connection in websocket_connections:
        await connection.send_text(json.dumps(data))

# 提供一个 API 获取最近的 MQTT 数据
@app.get("/recent-data")
async def get_recent_data():
    return recent_data