from fastapi import FastAPI, HTTPException
import time
from db import init_db, insert_device, list_devices
import sqlite3

app = FastAPI()

#{"device_id":"dev001","state":"NEW","created_at":1768599000}

devices = {}
token_fijo= "PROVISION-1234"

@app.on_event("startup")
def startup_event():
    init_db()


# Endpoint para crear un nuevo dispositivo
@app.post("/devices")
def create_device(payload: dict):
    device_id = payload.get("device_id")

    if not device_id or not isinstance(device_id, str):
        raise HTTPException(status_code=400, detail="device_id is required (string)")

    device = {
        "device_id": device_id,
        "state": "NEW",
        "created_at": int(time.time()),
        "provisioned_at": None,
        "provision_token": None,
        "activated_at": None,
        "fw_version": None,
    }

    try:
        insert_device(device)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="device already exists")

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

# Endpoint para activar un dispositivo
@app.post("/devices/{device_id}/activate")
def activate_device(device_id: str, payload: dict):
    device = devices.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device["state"] != "PROVISIONED":
        raise HTTPException(status_code=409, detail="Device not provisioned")
    
    fw_version = payload.get("fw_version")
    device["state"] = "ACTIVE"
    device["activated_at"] = int(time.time())
    device["fw_version"] = fw_version
    return device
    # {"fw_version":"1.0.0"}

## Endpoint para obtener la lista de dispositivos
@app.get("/devices")
def get_devices():
    return list_devices()