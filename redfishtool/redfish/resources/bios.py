from .base import Resource


class Bios(Resource):

    @property
    def attribute(self):
        return self.property('Attributes')

    def get_attribute_registry(self):
        reg_name = self.property('AttributeRegistry')
        if not reg_name:
            return None

        reg_resource = Resource(self.conn, f'/redfish/v1/Registries/{reg_name}')
        reg_location = reg_resource.property('Location')
        for _ in reg_location:
            if _.get('Language') == 'en':
                return Resource(self.conn, _.get('Uri'))

        return None

    def get_settings_object(self):
        return BiosSettingsObject(self.conn, self.get_odata_link('@Redfish.Settings', 'SettingsObject'))


class BiosSettingsObject(Resource):
    @property
    def attribute(self):
        return self.property('Attributes')

    def update(self, data):
        if not isinstance(data, dict):
            raise TypeError()

        self.conn.patch(self.path, {'Attributes': data})
