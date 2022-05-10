from multiprocessing import AuthenticationError

from requests import session
from imports import json, requests


class Authenticator():
    def authentication(self, url, usr, psswd, verify, platform):
        authenticationRequest = requests.post(url,
                                              verify=verify,
                                              data=json.dumps({
                                                  'userName': usr,
                                                  'password': psswd,
                                                  'platform': platform
                                              }),
                                              headers={
                                                  'Accept': 'application/json',
                                                  'Content-Type': 'application/json'
                                              })
        return authenticationRequest

    def return_request_output(self):
        request_text = self.authentication().text
        # print(request_text)
        return request_text

    def return_status_code(self):
        request_status_code = self.authentication().status_code
        # print(request_status_code)
        return request_status_code
        

    def return_authentication_session_id(self):
        request_text = self.return_request_output()
        response = json.loads(request_text)
        sessionId = response['sessionID']
        return sessionId

