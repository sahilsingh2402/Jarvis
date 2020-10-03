# Importing important libraries

import aiml # AIML stands for Artificial Intelligence Markup Language. 
import sys # To access command line arguments in python.
import traceback # An exception handler to down the call chain at the point where the exception was raised.
import src # To structure your program files in a better accessible way.

from src import google_tts # It uses Google's Text to Speech engine to convert passed text to a wav(audio) file.
from src import google_stt # It uses Google's Speech to Text engine to convert passed flac(audio) to text.
from src import microphone # It uses PyAudio to record on terminal.
from src import commonsense # It will play pre-recorded uhoh, sorry and sleepy wav files.
from src import brain # It will load core things in Jarvis' brain.
from excp.exception import NotUnderstoodException # To pass exception handling.

# Declaring Variables
exit_flag = 0

# Calling Required Functions
tts_engine = google_tts.Google_TTS()
jarvis_brain = brain.Brain()
mic = microphone.Microphone()
k = aiml.Kernel()

# Defining Functions
def check_sleep(words):
    if 'sleep' in words or 'hibernate' in words:
        commonsense.sleepy()
        sleep()
    if ('shut' in words and 'down' in words) or 'bye' in words or 'goodbye' in words:
        tts_engine.say("I am shutting down")
        exit_flag = 1
        return True


def sleep():
    while not exit_flag:
        try:
            #mic = microphone.Microphone()
            a, s_data = mic.listen()
            stt_engine = google_stt.Google_STT(mic)
            stt_response = stt_engine.get_text()
            words_stt_response = stt_response.split(' ')
            if 'wake' in words_stt_response or 'jarvis' in words_stt_response or 'wakeup' in words_stt_response:
                tts_engine.say("Hello Sir, I am back once again.")
                wakeup()
        except Exception:
            pass


def wakeup():
    while not exit_flag:
        #mic = microphone.Microphone()
        a, s_data = mic.listen()
        a = 0
        if mic.is_silent(s_data):
            commonsense.sleepy()
            sleep()
        try:
            stt_engine = google_stt.Google_STT(mic)
            stt_response = stt_engine.get_text()
            print("Heard: %r" % stt_response)
            if(jarvis_brain.process(stt_response)):
                pass
            else:
                if check_sleep(stt_response.split(' ')):
                    break
                response = k.respond(stt_response)
                print(response)
                tts_engine.say(response)
        except NotUnderstoodException:
            commonsense.sorry()
        except Exception:
            print("Error in processing loop:")
            traceback.print_exc()
            commonsense.uhoh()

k.loadBrain('data/jarvis.brn')

# Handling Exception
try:
    f = open('data/jarvis.cred')
except IOError:
    sys.exit(1)

bot_predicates = f.readlines()
f.close()
for bot_predicate in bot_predicates:
    key_value = bot_predicate.split('::')
    if len(key_value) == 2:
        k.setBotPredicate(key_value[0], key_value[1].rstrip('\n'))
wakeup()
