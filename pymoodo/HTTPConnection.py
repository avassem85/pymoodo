import calendar
import datetime
import json
import requests
import logging

_LOGGER = logging.getLogger(__name__)

class HTTPConnection(object):
    """Connection to Moodo API"""
    def __init__(self, email, password):
        """Initialize connection object"""
        self.__authenticated = False
        self.user_agent = 'Mozilla/5.0'
        self.baseurl = 'https://rest.moodo.co'
        self.api = '/api'
        self.oauth = {
            "email": email,
            "password": password}
        self.token = None
        self.expiration = 0
        self.__login()

    @property
    def authenticated(self):
        """Return the display name of this light."""
        return self.__authenticated

    def get(self, command):
        """Utility command to get data from API"""
        self.__updatesession()
        url = self.__buildurl(command)

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8')) if response.status_code == 200 else None 
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error("Http Error: %s",errh)
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("Error Connecting: %s",errc)
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("Timeout Error: %s",errt)
        except requests.exceptions.RequestException as err:
            _LOGGER.error("OOps: Something Else %s",err)
            
    def put(self, command, data={}):
        """Utility command to put data to API"""
        self.__updatesession()
        url = self.__buildurl(command)

        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8')) if response.status_code == 200 else None 
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error("Http Error: %s",errh)
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("Error Connecting: %s",errc)
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("Timeout Error: %s",errt)
        except requests.exceptions.RequestException as err:
            _LOGGER.error("OOps: Something Else %s",err)

    def patch(self, command, data={}):
        """Utility command to patch data to the API"""
        self.__updatesession()
        url = self.__buildurl(command)

        try:
            response = requests.patch(url, headers=self.headers, json=data)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8')) if response.status_code == 200 else None 
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error("Http Error: %s",errh)
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("Error Connecting: %s",errc)
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("Timeout Error: %s",errt)
        except requests.exceptions.RequestException as err:
            _LOGGER.error("OOps: Something Else %s",err)

    def delete(self, command):
        """Utility command to patch data to the API"""
        self.__updatesession()
        url = self.__buildurl(command)

        try:
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8')) if response.status_code == 200 else None 
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error("Http Error: %s",errh)
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("Error Connecting: %s",errc)
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("Timeout Error: %s",errt)
        except requests.exceptions.RequestException as err:
            _LOGGER.error("OOps: Something Else %s",err)

    def post(self, command, data={}):
        """Utility command to post data to the API"""
        self.__updatesession()
        url = self.__buildurl(command)

        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8')) if response.status_code == 200 else None 
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error("Http Error: %s",errh)
            response_dict = json.loads(response.text)
            if response_dict['error']:
                _LOGGER.error(response_dict['error'])
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("Error Connecting: %s",errc)
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("Timeout Error: %s",errt)
        except requests.exceptions.RequestException as err:
            _LOGGER.error("OOps: Something Else %s",err)

    def __login(self):
        self.__setheaders()
        auth = self.post('/login', data=self.oauth)
        if auth:
            self.token = auth['token']
            self.__setheaders(self.token)
            self.__authenticated = True

    def __setheaders(self, access_token=None):
        """Set HTTP header"""
        
        now = calendar.timegm(datetime.datetime.now().timetuple())
        self.expiration = now + 1800
        self.headers = {"Accept": "application/json",
                     "Content-Type": "application/json",
                     "User-Agent": self.user_agent}
        if access_token:
            self.access_token = access_token
            self.headers['Token'] = self.access_token

    def __updatesession(self):
        now = calendar.timegm(datetime.datetime.now().timetuple())
        if now > self.expiration:
            self.__login()

    def __buildurl(self, command):
        return "%s%s%s" % (self.baseurl, self.api, command)
