import json
import logging
from collections import namedtuple
from redfishtool.utils.misc import DictUtil
from redfishtool.redfish.exceptions import RedfishUnavaliableResource

LOG = logging.getLogger(__name__)


Status = namedtuple('Status', ['health', 'health_rollup', 'state'])


class Resource():
    def __init__(self, conn, path):
        self.conn = conn
        self.path = path

        try:
            self._data = self.conn.get(self.path)

        except Exception as ex:
            raise RedfishUnavaliableResource(f'Cannot access resource: {self.path}, ({ex})')

    @property
    def data(self):
        return self._data

    @property
    def json(self):
        return json.dumps(self._data, indent=4)

    def property(self, *keys):
        return DictUtil.get(self._data, *keys)

    # @data_id
    def get_odata_link(self, *keys):
        return self.property(*keys, '@odata.id')

    def get_odata_links(self, *keys):
        for _ in (self.property(*keys) or []):
            yield _.get('@odata.id')

    # Links
    def get_links(self, *keys):
        yield from self.get_odata_links('Links', *keys)

    def get_status(self):
        s = self.property('Status')
        if s:
            return Status(s.get('Health'), s.get('HealthRollup'), s.get('State'))
        return None


class ResourceCollection(Resource):
    def __init__(self, conn, path):
        super().__init__(conn, path)
        self._members = self.get_odata_links('Members')

    def member_count(self):
        return self.data.get('Members@odata.count')

    def member_links(self):
        for _ in self._members:
            yield _

    def first_member_link(self):
        for _ in self._members:
            return _

    def member_resources(self):
        for path in self.member_links():
            try:
                yield Resource(self.conn, path)

            except Exception as ex:
                LOG.error(f'get resource: {path}, ex: {str(ex)}')
