from enum import Enum


REDFISH_SERVICE_ROOT_PATH = '/redfish/v1/'
ODATA_VERSION = '4.0'


# Redfish attribute
class STATE(Enum):
    ENABLED = 'Enabled'
    DISABLED = 'Disabled'
    ABSENT = 'Absent'


PCIE_DEVICE_CLASS_STORCTRL = 'MassStorageController'
PCIE_DEVICE_CLASS_NIC = 'NetworkController'
