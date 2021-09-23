import logging
from redfishtool.redfish.resources.base import Resource, ResourceCollection
from redfishtool.redfish.resources.bios import Bios

LOG = logging.getLogger(__name__)


class System(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)

    def get_processor_collection(self):
        return ResourceCollection(self.conn, self.get_odata_link('Processors'))

    def get_memory_collection(self):
        return ResourceCollection(self.conn, self.get_odata_link('Memory'))

    def get_storage_collection(self):
        return StorageCollection(self.conn, self.get_odata_link('Storage'))

    def get_bios(self):
        return Bios(self.conn, self.get_odata_link('Bios'))


class StorageCollection(ResourceCollection):
    def __init__(self, conn, path):
        super().__init__(conn, path)

    def get_storage(self):
        for path in self.member_links():
            try:
                yield Storage(self.conn, path)
            except Exception as ex:
                LOG.error(str(ex))


class Storage(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)

    def get_drive(self):
        for path in self.get_odata_links('Drives'):
            try:
                yield Resource(self.conn, path)
            except Exception as ex:
                LOG.error(str(ex))


class Chassis(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)

    def get_pcie_devices(self):
        for path in self.get_links('PCIeDevices'):
            try:
                yield PCIeDevice(self.conn, path)
            except Exception as ex:
                LOG.error(str(ex))

    def get_pcie_devices_count(self):
        devices = self.property('Links', 'PCIeDevices')
        return len(devices) if isinstance(devices, list) else 0


class PCIeDevice(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)

    def get_pcie_function(self):
        for path in self.get_links('PCIeFunctions'):
            try:
                yield Resource(self.conn, path)
            except Exception as ex:
                LOG.error(str(ex))


class Manager(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)
