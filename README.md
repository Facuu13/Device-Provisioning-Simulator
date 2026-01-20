# Device Provisioning Simulator (IoT onboarding)

**Qué es:** API que registra dispositivos y los pasa por estados: `NEW → PROVISIONED → ACTIVE`
**Iteraciones:**

1. `POST /devices` crea device con estado NEW
2. `POST /devices/{id}/provision` con token → PROVISIONED
3. `POST /devices/{id}/activate` → ACTIVE
4. Persistencia en SQLite
