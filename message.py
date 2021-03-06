import requests
import json


class Message:
    supported_types = ['text', 'audio', 'document', 'photo', 'voice']

    def __init__(self, message, TELEGRAM_TOKEN):
        self.chat_id = message['from']['id']
        self.TELEGRAM_TOKEN = TELEGRAM_TOKEN
        for message_type in self.supported_types:
            if message.get(message_type):
                self.type = message_type
                self.value = message[message_type]
                break
            else:
                self.type = False
                self.value = False

    def _text_get_response(self):
        response = {
            'text': self.value,
        }
        method_name = 'sendMessage'
        return method_name, response

    def _get_file(self):
        get_file_api_url = f'https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/getFile'
        get_file_content_api_url = f'https://api.telegram.org/file/bot{self.TELEGRAM_TOKEN}/' + '{file_path}'
        response = requests.post(url=get_file_api_url, params={'file_id': self.value['file_id']})
        json_response = json.loads(response.content)
        if response.status_code != 200 or not json_response.get('ok'):
            raise FileNotFoundError()
        response = requests.get(url=get_file_content_api_url.format(file_path=json_response['result']['file_path']))
        if response.status_code != 200:
            raise FileNotFoundError()
        return response.content

    def _document_get_response(self):
        try:
            file_content = self._get_file()
            with open(self.value['file_name'], 'wb') as file:
                file.write(file_content)
            response = {
                'text': 'Received your file!'
            }
        except FileNotFoundError:
            response = {
                'text': 'Could not download your file!'
            }
        method_name = 'sendMessage'
        return method_name, response

    def _get_voice_transcript(self, file_content):
        IBM_API_URL = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/41ca9fb2-3937-4268-ad74-607eda41bf40'
        response = requests.post(url=IBM_API_URL,
                                 data=file_content,
                                 headers={'Content-Type': self.value['mime_type']},
                                 auth=('apikey', '5Qvym-DOzR8-sB4eCWp63ZNVhjbdiqFthd3v4kodueqt'))
        json_response = json.loads(response.content)
        if response.status_code != 200 or not json_response.get('results'):
            return 'Could not hear you well!'
        return json_response['results'][0]['alternatives'][0]['transcript']

    def _voice_get_response(self):
        try:
            file_content = self._get_file()
            voice_transcript = self._get_voice_transcript(file_content)
            response = {
                'text': voice_transcript,
            }
        except FileNotFoundError:
            response = {
                'text': 'Could not get your voice message!'
            }
        method_name = 'sendMessage'
        return method_name, response

    def _not_implemented_response(self):
        response = {
            'text': 'I am sorry. This type is not implemented!',
        }
        method_name = 'sendMessage'
        return method_name, response

    def get_response(self):
        if self.type and hasattr(self, '_%s_get_response' % self.type):
            result = getattr(self, '_%s_get_response' % self.type)()
        else:
            result = self._not_implemented_response()

        assert isinstance(result, tuple) and len(result) == 2 and isinstance(result[1], dict)

        result[1].update({
            'chat_id': self.chat_id,
        })
        return result