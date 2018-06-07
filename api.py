import requests
import xmltodict
import json

# api documentation http://service.velocify.com/ClientService.asmx

class Api():

    host = 'http://service.leads360.com'

    @staticmethod
    def get_config(filename):
        with open(filename, 'r') as f:
            config = json.load(f)
        return config['VELOCIPY']
        

    @staticmethod
    def get_from_init(initfile='credentials.json'):
        cfg = Api.get_config(initfile)
        print(cfg)
        return Api(
            cfg['username'],
            cfg['password']
        )


    def __init__(self, username, password):
        self.username = username
        self.password = password

    def _build_params(self, **kwargs):
        return {'username': self.username, 'password': self.password, **kwargs}

    def _build_url(self, command):
        return f'{self.host}/{command}'

    def _raw_get(self, command, **kwargs):
        result = requests.get(
            self._build_url(command),
            self._build_params(**kwargs)
        )
        return xmltodict.parse(result.content)

    def get_fields(self):
        return self._raw_get('ClientService.asmx/GetFields')

    def get_report_results(self, report_id):
        return self._raw_get(
            'ClientService.asmx/GetReportResultsWithoutFilters',
            reportId=report_id
        )

    def get_lead(self, lead_id):
        return self._raw_get(
            'ClientService.asmx/GetLead',
            leadId=lead_id
        )


def main():
    api = Api.get_from_init()
    #r = api.get_fields()
    #r = api.get_report_results('67')
    r = api.get_lead('14019')
    print(json.dumps(r))


if __name__ == '__main__':
    main()
