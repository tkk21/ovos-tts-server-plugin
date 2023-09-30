import requests
from ovos_plugin_manager.templates.tts import TTS, TTSValidator, RemoteTTSException


class RvcTTS(TTS):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, audio_ext="wav",
                         validator=RvcTTSValidator(self))
        self.type = "wav"

        self.url = self.config.get("url") + "/tts"
        self.rvc_request_body = self.config.get("body")


    def get_tts(self, sentence, wav_file, lang=None, voice=None):
        data = self._post_rvc_request_for_tts(sentence)
        with open(wav_file, "wb") as f:
            f.write(data)
        return wav_file, None

    def _post_rvc_request_for_tts(self, sentence):
        body = self.rvc_request_body
        body["tts_text"] = sentence
        response = requests.post(self.url, json=body, stream=True)
        # might not work and might need to
        # use response.iter_content and chunk
        # https://requests.readthedocs.io/en/latest/user/quickstart/#raw-response-content
        if not response.ok:
            raise RemoteTTSException(f"tts request failed: {response.text}")

        return response.content

class RvcTTSValidator(TTSValidator):
    def __init__(self, tts):
        super(RvcTTSValidator, self).__init__(tts)

    def validate_lang(self):
        pass

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return RvcTTS


RvcTTSConfig = {}
