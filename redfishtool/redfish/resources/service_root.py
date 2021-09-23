import logging
from .base import Resource, ResourceCollection
from redfishtool.redfish.exceptions import RedfishUnsupportAPI

LOG = logging.getLogger(__name__)


class ServiceRoot(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)

        # keep service
        self.system = None
        self.chassis = None
        self.manager = None
        self._version = self.data.get('RedfishVersion')

    @property
    def version(self):
        return self._version

    def _create_resource(self, name, _type):
        path = self.get_odata_link(name)
        if path:
            collection = ResourceCollection(self.conn, path)

            klass = globals()[_type]

            return klass(self.conn, collection.first_member_link())
        else:
            raise RedfishUnsupportAPI(name)

    def get_system(self):
        if self.system is None:
            self.system = self._create_resource('Systems', 'System')

        return self.system

    def get_chassis(self):
        if self.chassis is None:
            self.chassis = self._create_resource('Chassis', 'Chassis')

        return self.chassis

    def get_manager(self):
        if self.manager is None:
            self.manager = self._create_resource('Managers', 'Manager')

        return self.manager
