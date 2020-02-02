import logging
import pyttsx3
import threading

from multiprocessing import Lock

class Speaker():

    _lock = Lock()

    def __init__(self):
        super().__init__()

    def _speak(self, text):
        try:
            self._lock.acquire()
            engine = pyttsx3.init()
            engine.say(text)
        except:
            logging.error('TextToSpeechCommand : Error in speaker calling')
        finally:
            self._lock.release()
    
    def execute(self, text):
        t1 = threading.Thread(target=self._speak, args=(text,))
        t1.start()
    
if __name__ == "__main__":
    obj = Speaker()
    obj.execute("Who am I?")