import os
import ssl
import json
import urllib.request
from decouple import config as cf


class Settings:
    def __init__(self):
        self.api_key = cf('API_KEY')
        self.rest_endpoint = cf('REST_ENDPOINT')
        if not self.api_key:
            raise ValueError("API key must be provided.")
        self.allow_self_signed_https()

    @staticmethod
    def allow_self_signed_https():
        if not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context


class ChatSession:
    def __init__(self):
        self.history = []

    def add_interaction(self, question, answer):
        self.history.append({
            "inputs": {"question": question},
            "outputs": {"answer": answer}
        })

    def get_chat_history(self):
        return self.history


class RequestManager:
    HEADERS = {
        'Content-Type': 'application/json',
        'azureml-model-deployment': 'afad-app'
    }

    def __init__(self, settings, session):
        self.api_key = settings.api_key
        self.rest_endpoint = settings.rest_endpoint
        self.headers = self.HEADERS.copy()
        self.headers['Authorization'] = f'Bearer {self.api_key}'
        self.session = session

    def send_request(self, question):
        data = self._prepare_data(question)
        body = str.encode(json.dumps(data))
        req = urllib.request.Request(self.rest_endpoint, body, self.headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read().decode('utf-8')
            json_result = json.loads(result)
            answer = json_result["answer"]
            self.session.add_interaction(question, answer)
            return answer
        except urllib.error.HTTPError as error:
            raise ConnectionError(f"Request failed with status code: {error.code}") from error

    def _prepare_data(self, question):
        data = {
            "chat_history": self.session.get_chat_history(),
            "question": question
        }
        return data

