
class Campaign():

    def __init__(self, get_campaign_results):
        self.campaign_list = get_campaign_results['Campaigns']['Campaign']

    @staticmethod
    def fetch_from_velocify(api):
        return Campaign(api.get_campaigns())

    def get_campaign_id(self, campaign):
        return next((item for item in self.campaign_list if item['@CampaignTitle'] == campaign))['@CampaignId']
    