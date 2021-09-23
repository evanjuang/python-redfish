from dataclasses import dataclass, field
from redfishtool.model.base import BaseModel


@dataclass(init=False)
class SystemInfo(BaseModel):
    manufacturer: str
    model: str
    sku: str
    part_number: str
    serial_number: str
    total_cpu: str
    total_memory: str
    bios_ver: str
    bmc_ver: str
    power_state: str


@dataclass(init=False)
class Cpu(BaseModel):
    manufacturer: str
    model: str
    socket: str
    cores: str
    hyper_threads: str
    max_speed: str


@dataclass(init=False)
class Memory(BaseModel):
    manufacturer: str
    part_number: str
    serial_number: str
    device_type: str
    dimm_slot: str
    size: str
    speed: str


@dataclass()
class Storage(BaseModel):
    name: str = None
    drive: list = field(default_factory=list)


@dataclass(init=False)
class Drive(BaseModel):
    model: str
    serial_number: str
    protocol: str
    media_type: str
    size: str
    port_id: str


@dataclass()
class PciDevice(BaseModel):
    # controller: dict
    id: str = None
    function: list = field(default_factory=list)


@dataclass(init=False)
class PciFunction(BaseModel):
    description: str
    device_class: str
    vid: str
    did: str
    subsystem_vendor_id: str
    subsystem_id: str
    bus_number: str
    device_number: str
    func_number: str
    slot_number: str
