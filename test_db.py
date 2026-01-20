from db import init_db, insert_device, list_devices
init_db()
print("DB OK")

device = {
    "device_id": "dev001",
    "state": "NEW",
    "created_at": 1625247600,
    "provisioned_at": None,
    "provision_token": None,
    "activated_at": None,
    "fw_version": None
}
insert_device(device)
devices = list_devices()
print(devices)  # Debería mostrar la lista con el dispositivo insertado

