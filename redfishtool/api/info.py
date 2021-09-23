from redfishtool.model.info import (
    SystemInfo, Cpu, Memory, Storage, Drive, PciDevice, PciFunction
)
from redfishtool.utils.misc import DictUtil
from redfishtool.utils.convert import mib_to_byte


def get_system_info(rf_conn):
    rf_root = rf_conn.service_root
    rf_sys = rf_root.get_system().data
    rf_bmc = rf_root.get_manager().data

    info = SystemInfo()
    info.manufacturer = rf_sys.get('Manufacturer')
    info.model = rf_sys.get('Model')
    info.sku = rf_sys.get('SKU')
    info.part_number = rf_sys.get('PartNumber')
    info.serial_number = rf_sys.get('SerialNumber')
    info.total_cpu = str(DictUtil.get(rf_sys, 'ProcessorSummary', 'Count'))
    info.total_memory = str(DictUtil.get(
        rf_sys, 'MemorySummary', 'TotalSystemMemoryGiB'))
    info.bios_ver = rf_sys.get('BiosVersion')
    info.bmc_ver = rf_bmc.get('FirmwareVersion')
    info.power_state = rf_sys.get('PowerState')

    return info


def get_cpu_info(rf_conn):
    rf_root = rf_conn.service_root
    rf_col = rf_root.get_system().get_processor_collection()

    info = []
    for _ in rf_col.member_resources():
        data = _.data
        e = Cpu()
        e.manufacturer = data.get('Manufacturer')
        e.socket = str(data.get('Socket'))
        e.cores = str(data.get('TotalCores'))
        e.hyper_threads = str(data.get('TotalThreads'))
        e.max_speed = str(data.get('MaxSpeedMHz'))

        info.append(e)

    return info


def get_memory_info(rf_conn):
    rf_root = rf_conn.service_root
    rf_col = rf_root.get_system().get_memory_collection()

    info, absent = [], []
    for _ in rf_col.member_resources():
        rf_status = _.get_status()
        data = _.data

        if rf_status.state == 'Absent':
            absent.append(data.get('DeviceLocator'))

        else:
            e = Memory()
            e.manufacturer = data.get('Manufacturer')
            e.part_number = DictUtil.get(data, 'PartNumber')
            e.serial_number = data.get('SerialNumber')
            e.device_type = data.get('MemoryDeviceType')
            e.dimm_slot = data.get('DeviceLocator')
            e.size = mib_to_byte(data.get('CapacityMiB'))
            e.speed = data.get('OperatingSpeedMhz')

            info.append(e)

    return info, absent


def _get_drive_info(rf_storage):
    drives = []
    for _ in rf_storage.get_drive():
        data = _.data
        drive = Drive()
        drive.model = data.get('Model')
        drive.serial_number = data.get('SerialNumber')
        drive.protocol = data.get('Protocol')
        drive.media_type = data.get('MediaType')
        drive.size = str(data.get('CapacityBytes'))

        drives.append(drive)

    return drives


def get_storage_info(rf_conn):
    rf_root = rf_conn.service_root
    rf_stor_col = rf_root.get_system().get_storage_collection()

    info = []
    for _ in rf_stor_col.get_storage():
        stor = Storage(_.property('Name'))
        stor.drive = _get_drive_info(_)
        info.append(stor)

    return info


def get_pci_device_info(rf_conn):
    rf_root = rf_conn.service_root
    rf_pci_devices = rf_root.get_chassis().get_pcie_devices()

    info = []
    for _ in rf_pci_devices:
        device = PciDevice(_.data.get('Id'))
        for _ in _.get_pcie_function():
            data = _.data

            e = PciFunction()
            e.description = data.get('Descripition')
            e.device_class = data.get('DeviceClass')
            e.vid = data.get('VendorId')
            e.did = data.get('DeviceId')
            e.subsystem_vendor_id = data.get('SubsystemVendorId')
            e.subsystem_id = data.get('SubsystemId')
            e.func_number = data.get('FunctionId')

            device.function.append(e)

        info.append(device)

    return info
