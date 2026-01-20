from fastapi import FastAPI, HTTPException
import time
from db import init_db, insert_device, list_devices, get_device, update_device
import sqlite3

app = FastAPI()

#{"device_id":"dev001","state":"NEW","created_at":1768599000}

devices = {}
PROVISION_TOKEN = "PROVISION-1234"

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
    device = get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    if device["state"] != "NEW":
        raise HTTPException(status_code=409, detail="device not in NEW state")

    token = payload.get("token")
    if token != PROVISION_TOKEN:
        raise HTTPException(status_code=401, detail="invalid token")

    update_device(device_id, {
        "state": "PROVISIONED",
        "provisioned_at": int(time.time()),
        "provision_token": token
    })

    return get_device(device_id)
    # {"token":"PROVISION-1234"}

# Endpoint para activar un dispositivo
@app.post("/devices/{device_id}/activate")
def activate_device(device_id: str, payload: dict = {}):
    device = get_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="device not found")

    if device["state"] != "PROVISIONED":
        raise HTTPException(status_code=409, detail="device not provisioned")

    fields = {
        "state": "ACTIVE",
        "activated_at": int(time.time())
    }

    fw = payload.get("fw_version")
    if fw:
        fields["fw_version"] = fw

    update_device(device_id, fields)
    return get_device(device_id)
    # {"fw_version":"1.0.0"}

## Endpoint para obtener la lista de dispositivos
@app.get("/devices")
def get_devices():
    return list_devices()