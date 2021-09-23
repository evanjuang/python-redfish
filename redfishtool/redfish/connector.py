import json
import requests
import base64
import logging
from dataclasses import dataclass
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.packages.urllib3.util.retry import Retry
from urllib3.connection import NewConnectionError
from . import constants
from .exceptions import HTTPRequestError, HTTPClientError, HTTPServerError
from redfishtool.redfish.resources.service_root import ServiceRoot

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

LOG = logging.getLogger(__name__)


@dataclass
class BMCConfig:
    host: str
    user: str
    password: str


class HttpClient:
    RETRY = 5
    RETRY_BACKOFF = 1

    def __init__(self, baseurl, header):
        self.baseurl = baseurl
        self.header = header

        # session
        self.session = requests.Session()
        retries = Retry(total=self.RETRY, backoff_factor=self.RETRY_BACKOFF, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def request(self, path, method='GET', req_data=None, timeout=30, use_session=False):
        if method not in ['GET', 'POST', 'PATCH', 'DELETE']:
            raise HTTPRequestError(f'Unsupport method: {method}')

        LOG.debug(f'{method}: {path}, data: {req_data}')

        params = {
            'method': method,
            'url': '{}{}'.format(self.baseurl, path),
            'headers': self.header,
            'timeout': timeout,
            'verify': False
        }

        if req_data:
            params.update({'json': req_data})

        try:
            if use_session:
                resp = self.session.request(**params)
            else:
                resp = requests.request(**params)

            resp.raise_for_status()
            return resp

        except (NewConnectionError, ConnectionError) as ex:
            raise HTTPRequestError(f'Connection failed: {type(ex).__name__}')

        except HTTPError as ex:
            status = ex.response.status_code
            if 400 <= status < 500:
                raise HTTPClientError(ex)
            elif 500 <= status < 600:
                raise HTTPServerError(ex)

        except Exception as ex:
            raise HTTPRequestError(ex)


class RedfishConnector():
    def __init__(self, bmc_config,
                 service_root_path=constants.REDFISH_SERVICE_ROOT_PATH,
                 odata_ver=constants.ODATA_VERSION):

        self.baseurl = f'https://{bmc_config.host}'
        self.header = {
            "OData-Version": odata_ver,
            "Authorization": self.create_basic_auth(bmc_config.user, bmc_config.password)
        }

        self.http_client = HttpClient(self.baseurl, self.header)
        self.service_root_path = service_root_path
        self._service_root = ServiceRoot(self, self.service_root_path)

    def create_basic_auth(self, user, password):
        key = base64.b64encode(f'{user}:{password}'.encode('utf-8')).decode('utf-8')
        return f'Basic {key}'

    @property
    def service_root(self):
        return self._service_root

    def get(self, path):
        resp = self.http_client.request(path, use_session=True)
        resp.encoding = 'UTF-8'
        return json.loads(resp.text)

    def post(self, path, data):
        resp = self.http_client.request(path, method='POST', req_data=data)
        return resp

    def patch(self, path, data):
        resp = self.http_client.request(path, method='PATCH', req_data=data)
        return resp
