import requests

class GoshawkClient:

    def __init__(self, api_url):
        self.api_url = api_url

    def _get(self, path, defaults, params):
        p = dict(**defaults, **params)
        p = '&'.join( "{}={}".format(k, v) for k, v in p.items() )
        url = self.api_url + path + "?" + p
        response = requests.get(url)
        if response.status_code != 200:
            print(response.text)
            raise

        return response.json()

    def get_list(self, **kwargs):
        return self.get_lists(**kwargs)[0]

    def get_lists(self, **kwargs):
        defaults = {}
        path = "/lists/"
        return self._get(path, defaults, kwargs)['results']

    def get_reporter(self, **kwargs):
        return self.get_reporters(**kwargs)[0]

    def get_reporters(self, **kwargs):
        defaults = {}
        path = "/reporters/"
        return self._get(path, defaults, kwargs)['results']

    def get_records(self, **kwargs):
        defaults = {
            'active': True,
            'policy': 'B',
        }

        self._list_name_to_id(kwargs)

        path = "/records/"
        return self._get(path, defaults, kwargs)
        
    def get_records_values(self, **kwargs):
        results = self.get_records(**kwargs)['results']

        for result in results:
            yield result['value']

    def _post(self, path, defaults, params):
        p = dict(**defaults, **params)
        url = self.api_url + path
        response = requests.post(url, json=p)
        if response.status_code != 201:
            print(response.text)
            raise

        return response.json()

    def _list_name_to_id(self, kwargs):
        _list = self.get_list(name=kwargs['list_name'])
        kwargs['list'] = _list['id']
        del kwargs['list_name']

    def _reporter_name_to_id(self, kwargs):
        _reporter = self.get_reporter(name=kwargs['reporter_name'])
        kwargs['reporter'] = _reporter['id']
        del kwargs['reporter_name']

    def post_record(self, **kwargs):
        defaults = {
            'policy': 'B',
        }

        self._list_name_to_id(kwargs)
        self._reporter_name_to_id(kwargs)

        path = "/records/"
        return self._post(path, defaults, kwargs)

