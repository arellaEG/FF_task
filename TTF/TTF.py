from FFp import Action
from TT2 import _Recorder, Language
import os



action = Action()
action.start()


#language = Language()
#language.start(subjectNum = action.subject)
arg = "python TT2.py " + action.subject
os.system(arg)