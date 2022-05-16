from multiprocessing import AuthenticationError
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

    def return_request_dump(self):
        request_dump = self.authentication().text
        return request_dump

    def return_status_code(self):
        request_status_code = self.authentication().status_code
        return request_status_code

    def return_authentication_session_id(self, request):
        response = json.loads(request)
        sessionId = response['sessionID']
        return sessionId
