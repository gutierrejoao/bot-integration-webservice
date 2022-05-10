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

    def showFullTextOutput(self):
        print(self.authentication.text)

    def showStatusCode(self):
        print(self.authentication.status_code)

    def showAuthenticationSessionId(self):
        response = json.loads(self.authentication.text)
        sessionId = response['sessionID']
        print("O SessionID é: " + sessionId)
