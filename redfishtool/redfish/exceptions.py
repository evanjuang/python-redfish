
class HTTPRequestError(Exception):
    pass


class HTTPClientError(Exception):
    pass


class HTTPServerError(Exception):
    pass


class RedfishRequestError(Exception):
    pass


class RedfishUnsupportAPI(Exception):
    pass


class RedfishUnavaliableResource(Exception):
    pass
