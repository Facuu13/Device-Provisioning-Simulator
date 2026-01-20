from fastapi import FastAPI, HTTPException
import time

app = FastAPI()

#{"device_id":"dev001","state":"NEW","created_at":1768599000}

devices = {}
token_fijo= "PROVISION-1234"

# Endpoint para crear un nuevo dispositivo
@app.post("/devices")
def create_device(payload: dict):
    device_id = payload.get("device_id")
    if device_id in devices:
        raise HTTPException(status_code=400, detail="Device already exists")
    
    device = {
        "device_id": device_id,
        "state":"NEW",
        "created_at": int(time.time()),
        "provisioned_at": None,
        "provision_token": None
    }

    devices[device_id] = device
    return device
    # {"device_id":"dev001"}

# Endpoint para provisionar un dispositivo
@app.post("/devices/{device_id}/provision")
def provision_device(device_id: str, payload: dict):
    device = devices.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device["state"] != "NEW":
        raise HTTPException(status_code=409, detail="Device already provisioned")
    
    token = payload.get("token")
    if token != token_fijo:
        raise HTTPException(status_code=401, detail="Invalid provision token")
    
    device["state"] = "PROVISIONED"
    device["provisioned_at"] = int(time.time())
    device["provision_token"] = token
    return device
    # {"token":"PROVISION-1234"}


## Endpoint para obtener la lista de dispositivos
@app.get("/devices")
def get_devices():
    return (list(devices.values()))