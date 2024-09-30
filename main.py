from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random

app = FastAPI()


# Modelo para versões de firmware, hardware e hnp
class Version(BaseModel):
    firmware: str
    hardware: str
    hnp: str


# Modelo para dispositivos
class Device(BaseModel):
    hnuid: str
    className: str
    modelName: str
    serial: int
    versions: Version
    ready: Optional[bool] = None
    indication: Optional[str] = None
    load: Optional[int] = None
    units: Optional[Dict[str, str]] = None
    zeroIndication: Optional[bool] = None
    motionIndication: Optional[bool] = None
    overloadIndication: Optional[bool] = None
    underloadIndication: Optional[bool] = None
    minloadIndication: Optional[bool] = None
    division: Optional[int] = None
    capacity: Optional[int] = None
    adjustmentCounter: Optional[int] = None
    firmwareChecksum: Optional[str] = None
    error: Optional[int] = None


# Exemplo de dados dos dispositivos
devices = {
    "100-002-1": Device(
        hnuid="100-002-1",
        className="PC Interface",
        modelName="USB-Cable-Radio",
        serial=1,
        versions=Version(firmware="1.0.0", hardware="1.0.0", hnp="1.1.0")
    ),
    "201-001-40": Device(
        hnuid="201-001-40",
        className="WL 200",
        modelName="10 t",
        serial=1,
        ready=True,
        indication="0 kg",
        load=0,
        units={"load": "kg", "temperature": "°C"},
        zeroIndication=True,
        motionIndication=False,
        overloadIndication=False,
        underloadIndication=False,
        minloadIndication=True,
        division=50,
        capacity=10000,
        adjustmentCounter=7,
        firmwareChecksum="1871h",
        versions=Version(firmware="1.0.0", hardware="1.0.0", hnp="1.1.0"),
        error=1
    ),
    "201-001-41": Device(
        hnuid="201-001-41",
        className="WL 200",
        modelName="10 t",
        serial=1,
        ready=True,
        indication="0 kg",
        load=0,
        units={"load": "kg", "temperature": "°C"},
        zeroIndication=True,
        motionIndication=False,
        overloadIndication=False,
        underloadIndication=False,
        minloadIndication=True,
        division=50,
        capacity=10000,
        adjustmentCounter=7,
        firmwareChecksum="1871h",
        versions=Version(firmware="1.0.0", hardware="1.0.0", hnp="1.1.0"),
        error=1
    )
}


# Modelo para medições
class Measurement(BaseModel):
    timestamp: str
    load: int
    speed: float
    deltaTime: Optional[int] = None
    distribution: List[int]


# Exemplo de medições dos dispositivos
measurements_data = {
    "201-001-40": [
        Measurement(
            timestamp="2024-08-30T09:58:13.359819Z",
            load=2130,
            speed=1.49523,
            deltaTime=830457,
            distribution=[4, 53, 43]
        ),
        Measurement(
            timestamp="2024-08-30T09:58:12.529355Z",
            load=2860,
            speed=1.48669,
            deltaTime=841683,
            distribution=[10, 48, 41]
        ),
        # Outras medições...
    ],
    "201-001-41": [
        Measurement(
            timestamp="2024-08-30T09:58:14.028612Z",
            load=3230,
            speed=1.49523,
            deltaTime=826692,
            distribution=[56, 48, 0]
        ),
        Measurement(
            timestamp="2024-08-30T09:58:13.201988Z",
            load=4200,
            speed=1.48669,
            deltaTime=830557,
            distribution=[52, 50, 0]
        ),
        # Outras medições...
    ]
}


# Modelo para status do servidor
class ServerStatus(BaseModel):
    isRunning: bool
    consoleVisible: bool
    version: str
    disableHnpSocket: bool
    hnpSocketPort: int
    hnpSocketServer: bool
    disableUsb: bool
    hnpVersion: str
    wl103LibraryVersion: str
    wl103DriverVersion: str


# Exemplo de status do servidor
server_status = ServerStatus(
    isRunning=True,
    consoleVisible=True,
    version="1.0.0",
    disableHnpSocket=False,
    hnpSocketPort=50505,
    hnpSocketServer=True,
    disableUsb=False,
    hnpVersion="1.5.0",
    wl103LibraryVersion="3.2.7",
    wl103DriverVersion="2.8.40"
)


# Função para gerar medições dinâmicas
def generate_measurements(num_measurements: int) -> List[Measurement]:
    measurements = []
    current_time = datetime.utcnow() + timedelta(hours=3)  # Adicionando 3 horas para simular um fuso horário

    for i in range(num_measurements):
        measurement = Measurement(
            timestamp=(current_time - timedelta(seconds=1, milliseconds=200 * i)).isoformat() + "Z",
            load=random.randint(100, 2000),
            speed=round(random.uniform(1, 20), 5),
            deltaTime=random.randint(100000, 500000),
            distribution=[
                random.randint(0, 100),
                random.randint(0, 100),
                random.randint(0, 100)
            ]
        )
        measurements.append(measurement)

    return measurements


# Endpoints

# Obter status do servidor
@app.get("/api/status", response_model=ServerStatus)
def get_status():
    return server_status


# Atualizar status do servidor
@app.put("/api/status", response_model=ServerStatus)
def update_status(isRunning: Optional[bool] = None, consoleVisible: Optional[bool] = None):
    if isRunning is not None:
        server_status.isRunning = isRunning
    if consoleVisible is not None:
        server_status.consoleVisible = consoleVisible
    return server_status


#Obter todos os dispositivos
@app.get("/api/devices", response_model=Dict[str, Device])
def get_devices():
    return devices


# Obter um dispositivo específico pelo hnuid
# @app.get("/api/devices/{hnuid}", response_model=Device)
# def get_device(hnuid: str):
#     device = devices.get(hnuid)
#     if not device:
#         raise HTTPException(status_code=404, detail="Device not found")
#     return device


# Obter medições de um dispositivo específico
# @app.get("/api/devices/{hnuid}/measurements", response_model=List[Measurement])
# def get_device_measurements(hnuid: str, num_measurements: int = 6):
#     measurements = generate_measurements(num_measurements)
#     if not measurements:
#         raise HTTPException(status_code=404, detail="No measurements found for the device")
#     return measurements


# Obter todas as medições de todos os dispositivos
@app.get("/api/devices/measurements", response_model=Dict[str, List[Measurement]])
def get_all_measurements(num_measurements: int = 3):
    m = {
        "201-001-40": generate_measurements(num_measurements),
        "201-001-41": generate_measurements(num_measurements)
    }
    return m

@app.put("/api/devices/measurements")
def update_measurements(num_measurements: int = 6):
    return "OK"


# Resetar as medições de um dispositivo específico
@app.put("/api/devices/{hnuid}/zero")
def reset_device(hnuid: str):
    device = devices.get(hnuid)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Simulando o reset da carga do dispositivo para 0
    device.load = 0
    return {"message": f"Device {hnuid} reset to zero"}
