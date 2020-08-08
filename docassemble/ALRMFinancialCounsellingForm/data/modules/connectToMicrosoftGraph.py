from docassemble.base.util import DAOAuth
import requests
import base64

class MicrosoftGraph(DAOAuth):
    _authority_url      = "https://login.microsoftonline.com/common"
    _graph_url          = 'https://graph.microsoft.com/v1.0'
    _authorize_endpoint = "/oauth2/v2.0/authorize"
    _token_endpoint     = "/oauth2/v2.0/token"

    def init(self, *pargs, **kwargs):
        super().init(*pargs, **kwargs)
        self.appname = 'msgraph'
        self.token_uri = '{}{}'.format(self._authority_url, self._token_endpoint)
        self.auth_uri = '{}{}'.format(self._authority_url, self._authorize_endpoint)
        self.scope = 'Files.Read'

    def make_request(self, endpoint, request_type='GET'):
        try:
            request_URL = '{}{}'.format(self._graph_url, endpoint)
            h = self.get_http()
            return h.request(request_URL, request_type)
        except Exception as e:
            return 'Error making request: {}\nURL: {}  type: {}'.format(e, request_URL, request_type)

    def test(self):
        self.ensure_authorized()
        endpoint = '/me/drive'
        return self.make_request(endpoint)
        
    def get_spreadsheet(self):
        share_URL = 'https://flinders.sharepoint.com/:x:/s/FlindersLaw/EVNTVTpEtwhIjwN6rg_Cfc4BpN8jbodNbOOq49RnqmZi0w'
        b64URL = base64.urlsafe_b64encode(share_URL.encode('ascii'))
        # Back to a string so we can strip it and add it to the URL
        b64URL = b64URL.decode('ascii')
        b64URL = b64URL.strip('=')

        endpoint = '/shares/u!{}/driveItem'.format(b64URL)
        return self.make_request(endpoint)

    def logout(self):
        self.delete_credentials()
        return 'logged out'


