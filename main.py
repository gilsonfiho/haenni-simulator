"""
===============================================================================
HAENNI Simulator API - Simulador de Balanças Dinâmicas e Estáticas (WL400/WL108)
===============================================================================

Autor: Jose Pacelli Moreira de Oliveira (https://github.com/josepacelli)

Contribuidores:
Gilson Almeida(https://github.com/gilsonfiho)

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import random

app = FastAPI()

class Version(BaseModel):
    """
    Modelo para versões de firmware, hardware e HNP.

    Attributes:
        firmware (str): Versão do firmware.
        hardware (str): Versão do hardware.
        hnp (str): Versão do HNP.
    """
    firmware: str
    hardware: str
    hnp: str


class Device(BaseModel):
    """
    Modelo para representar um dispositivo conectado ao sistema.

    Attributes:
        hnuid (str): Identificador único do dispositivo.
        className (str): Classe do dispositivo.
        modelName (str): Modelo do dispositivo.
        serial (int): Número de série.
        versions (Version): Versões de firmware, hardware e HNP.
        ready (Optional[bool]): Se o dispositivo está pronto.
        indication (Optional[str]): Indicação atual do dispositivo. (String)
        load (Optional[int]): Carga atual medida. (int)
        units (Optional[Dict[str, str]]): Unidades usadas nas medições.
        zeroIndication (Optional[bool]): Indicação de carga zero.
        motionIndication (Optional[bool]): Indicação de movimento.
        overloadIndication (Optional[bool]): Indicação de sobrecarga.
        underloadIndication (Optional[bool]): Indicação de subcarga.
        minloadIndication (Optional[bool]): Indicação de carga mínima.
        division (Optional[int]): Divisão de medição.
        capacity (Optional[int]): Capacidade máxima.
        adjustmentCounter (Optional[int]): Contador de ajustes.
        firmwareChecksum (Optional[str]): Checksum do firmware.
        error (Optional[int]): Código de erro.
    """
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
    #Exemplo de Dados do Modulo de Comunicacao E9023.1
    "100-002-1": Device(
        hnuid="100-002-1",
        className="PC Interface",
        modelName="USB-Cable-Radio",
        serial=1,
        versions=Version(firmware="1.0.0", hardware="1.0.0", hnp="1.1.0")
    ),
    #Exemplos de Dados dos Modulos de Balanças Dinamicas WL400
    "400-001-40": Device(
        hnuid="400-001-40",
        className="WL 400",
        modelName="10 t",
        serial=1,
        ready=True,
        indication="0 kg",
        load=random.randint(0, 5000),
        units={"load": "kg", "temperature": "°C"},
        zeroIndication=True,
        motionIndication=bool(random.getrandbits(1)),
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
    "400-001-41": Device(
        hnuid="400-001-41",
        className="WL 400",
        modelName="10 t",
        serial=1,
        ready=True,
        indication="0 kg",
        load=random.randint(0, 5000),
        units={"load": "kg", "temperature": "°C"},
        zeroIndication=True,
        motionIndication=bool(random.getrandbits(1)),
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
    #Exemplos de Dados dos Módulos de Balanças Estaticas WL108
    "180-001-20": Device(
        hnuid="180-001-20",
        className="WL 180",
        modelName="10 t",
        serial=1,
        ready=True,
        indication="0 kg",
        load=random.randint(0, 5000),
        units={"load": "kg", "temperature": "°C"},
        zeroIndication=True,
        motionIndication=bool(random.getrandbits(1)),
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
    "180-001-21": Device(
        hnuid="180-001-21",
        className="WL 180",
        modelName="10 t",
        serial=1,
        ready=True,
        indication="0 kg",
        load=random.randint(0, 5000),
        units={"load": "kg", "temperature": "°C"},
        zeroIndication=True,
        motionIndication=bool(random.getrandbits(1)),
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

class Measurement(BaseModel):
    """
    Modelo para representar uma medição de carga.

    Attributes:
        timestamp (str): Data e hora da medição.
        load (int): Valor de carga medido.
        speed (float): Velocidade estimada.
        deltaTime (Optional[int]): Tempo entre medições.
        distribution (List[int]): Distribuição de carga.
    """
    timestamp: str
    load: int
    speed: float
    deltaTime: Optional[int] = None
    distribution: List[int]


"""
Exemplos de medições realizadas pelo Conjunto da Balança Dinâmica WL400.
As medições são obtidas a partir dos eventos gerados no endpoint:
http://127.0.0.1:8000/api/devices/measurements
"""
measurements_data = {
    "400-001-40": [
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
    "400-001-41": [
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

"""
Para a Balança Estática, os valores de peso são disponibilizados em tempo real por meio dos 
atributos "load" (inteiro) e "indication" (string), acessíveis pelo endpoint:
http://127.0.0.1:8000/api/devices
"""

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

def generate_measurements(num_measurements: int) -> List[Measurement]:
    """
    Função para gerar medições dinâmicas

    Args:
        num_measurements (int): Quantidade de medições a serem geradas.

    Returns:
        List[Measurement]: Lista de objetos Measurement simulados.
    """
    measurements = []
    current_time = datetime.utcnow() + timedelta(hours=0)  # Adicionando 3 horas para simular um fuso horário

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


@app.get("/api/status", response_model=ServerStatus)
def get_status():
    """
    Obter status do servidor

    Returns:
        ServerStatus: Dados atuais do status do servidor.
    """
    print('get', '/api/status')
    return server_status


@app.put("/api/status", response_model=ServerStatus)
def update_status(isRunning: Optional[bool] = None, consoleVisible: Optional[bool] = None):
    """
    Atualiza o status do servidor.

    Args:
        isRunning (Optional[bool]): Define se o servidor está em execução.
        consoleVisible (Optional[bool]): Define a visibilidade do console.

    Returns:
        ServerStatus: Novo status atualizado do servidor.
    """
    print('get', '/api/status', isRunning, consoleVisible)
    if isRunning is not None:
        server_status.isRunning = isRunning
    if consoleVisible is not None:
        server_status.consoleVisible = consoleVisible
    return server_status


@app.get("/api/devices", response_model=Dict[str, Device])
def get_devices():
    """
    Obter todos os dispositivos

    Returns:
        Dict[str, Device]: Dicionário com dados dos dispositivos.
    """
    # Gera novos valores aleatórios para os campos 'load' e 'motionIndication' dos dispositivos a cada requisição
    print('get', '/api/devices')
    for device in devices.values():
        if hasattr(device, "load"):
            device.load = random.randint(0, 5000)
        if hasattr(device, "motionIndication"):
            device.motionIndication = bool(random.getrandbits(1))
    return devices


@app.get("/api/devices/{hnuid}", response_model=Union[Device, Dict[str, List[Measurement]]])
def get_device(hnuid: str, qtd: int = 5):
    """
    Obter um dispositivo específico pelo hnuid

    Args:
        hnuid (str): ID do dispositivo ou "measurements".
        qtd (int): Quantidade de medições simuladas, se aplicável.

    Returns:
        Union[Device, Dict[str, List[Measurement]]]: Dados do dispositivo ou medições.
    """
    print('get', '/api/devices/{hnuid}', hnuid)
    if hnuid == "measurements":
        m = {
            "400-001-40": generate_measurements(qtd),
            "400-001-41": generate_measurements(qtd)
        }
        return m
    else:
        device = devices.get(hnuid)
        if device:
            if hasattr(device, "load"):
                device.load = random.randint(0, 5000)
            if hasattr(device, "motionIndication"):
                device.motionIndication = bool(random.getrandbits(1))

        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        return device



@app.get("/api/devices/{hnuid}/measurements", response_model=List[Measurement])
def get_device_measurements(hnuid: str, qtd: int = 5):
    """
    Obter medições de um dispositivo específico

    Args:
        hnuid (str): ID do dispositivo.
        qtd (int): Quantidade de medições desejadas.

    Returns:
        List[Measurement]: Lista de medições simuladas.
    """
    print('get', '/api/devices/{hnuid}/measurements', hnuid)
    return generate_measurements(qtd)
    # measurements = generate_measurements(qtd)
    # if not measurements:
    #     raise HTTPException(status_code=404, detail="No measurements found for the device")
    # return measurements


@app.put("/api/devices/measurements")
def update_measurements():
    """
    Endpoint para simular atualização de medições.

    Returns:
        str: Confirmação da operação.
    """
    print('put', '/api/devices/measurements')
    return "OK"


@app.put("/api/devices/{hnuid}/zero")
def reset_device(hnuid: str):
    """
    Reseta as medições de um dispositivo específico

    Args:
        hnuid (str): ID do dispositivo.

    Returns:
        dict: Mensagem de confirmação do reset.
    """
    print('put', '/api/devices/{hnuid}/zero', hnuid)
    device = devices.get(hnuid)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    # Simulando o reset da carga do dispositivo para 0
    device.load = 0
    return {"message": f"Device {hnuid} reset to zero"}
