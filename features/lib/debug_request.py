import requests

class DebugRequest:
    def __init__(self, host):
        self.host = f"{host}/serve/debug"
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'

    def get(self, params):
        self.response_data = self.session.get(f"{self.host}?{params}").json()
        return self.response_data
    
    def get_pixel_url(self):
        return self.response_data['impressionPixel']