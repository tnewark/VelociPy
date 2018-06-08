import requests
import xmltodict
import json
from zeep import Client
from lxml import etree

# api documentation http://service.velocify.com/ClientService.asmx

class Api():

    host = 'http://service.leads360.com'
    velocify_wsdl = 'https://service.leads360.com/ClientService.asmx?WSDL'

    @staticmethod
    def get_config(filename):
        with open(filename, 'r') as f:
            config = json.load(f)
        return config['VELOCIPY']
        

    @staticmethod
    def get_from_init(initfile='credentials.json'):
        cfg = Api.get_config(initfile)
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
        return xmltodict.parse(result.content,dict_constructor=dict)


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

    def get_reports(self):
        return self._raw_get(
            'ClientService.asmx/GetReports'
        )

    def modify_lead_campaign(self, lead_id, campaign_id):
        return self._raw_get(
            'ClientService.asmx/ModifyLeadCampaign',
            leadId = lead_id,
            campaignId = campaign_id
        )

    def get_campaigns(self):
        return self._raw_get(
            'ClientService.asmx/GetCampaigns'
        )

    # these are zeep based methods... necessary for now
    def get_lead_xml(self, lead_id):
        client = Client(Api.velocify_wsdl)
        return client.service.GetLead(username=self.username, password=self.password, leadId=lead_id)

    def modify_leads_xml(self, modified_leads):
        client = Client(Api.velocify_wsdl)
        client.service.ModifyLeads(username=self.username, password=self.password, leads=modified_leads)


def main():
    api = Api.get_from_init()
    r = api.get_reports()    
    reportInfo = [(k['@ReportTitle'], k['@ReportId']) for k in r['Reports']['Report']]
    print(reportInfo)


if __name__ == '__main__':
    main()
