from fastapi import FastAPI, HTTPException
import time

app = FastAPI()

#{"device_id":"dev001","state":"NEW","created_at":1768599000}

devices = {}

@app.post("/devices")
def create_device(payload: dict):
    print(payload)
    device_id = payload.get("device_id")
    if device_id in devices:
        raise HTTPException(status_code=400, detail="Device already exists")
    
    device = {
        "device_id": device_id,
        "state":"NEW",
        "created_at": int(time.time())
    }

    devices[device_id] = device
    return device

#get que me devuelva toda la lista de dispositivos
@app.get("/devices")
def get_devices():
    return (list(devices.values()))