import speech_recognition as sr
from typing import Optional

class SpeechRecognizer:
    """Reconnaissance vocale pour les symptômes"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe(self, audio_path: str, language: str = "fr-FR") -> str:
        try:
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio, language=language)
                return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        except Exception as e:
            return ""
    
    def transcribe_from_microphone(self, duration: int = 5, language: str = "fr-FR") -> str:
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=duration)
                text = self.recognizer.recognize_google(audio, language=language)
                return text
        except:
            return ""