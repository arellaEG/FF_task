from full_phase import Action
from TongueTwisterTask import _Recorder, Language
from psychopy import gui



action = Action()
action.start()

while True:
    dlg = gui.Dlg()
    dlg.addText("Please call the experimenter.")
    dlg.addField("code")
    dlg.show()
    
    if dlg.data[0] == '0':
        break
    else:
        continue

language = Language()
language.start(subjectNum = action.subject)
