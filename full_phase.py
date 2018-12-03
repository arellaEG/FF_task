##################################
########fill in subject ID #######
##################################

subject ='999'

##################################
##################################

######### timers  ################

interStepInterval = 1.7 # speed for practice trials until criterion met ~1.2s = 1.8 iSI.
# speed for test phase will be ~1s per word, which is an iSI of 2.2


crit = .85 # criterion for passing practice phase

timeBreak = 60 # every how often they get break screen (will wait till trial ends)

##################################
##################################

######## interval time limit ####
## Naturally, there will be slight differences in the timing of each key-press
## within a word (even though they're supposed to press them all together). This
## intervalTime limit determines how much of an interval we're willing to accept.
## if they wait too long between keys in the practice + feedback stage,
## they will get a message saying they have to press all keys at once.
intervalTime = 0.5   

##################################

import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui
import time

### R = tr, L = sl, x = ee. changed to keep all words 3 characters.
units=['t','R','v','L','eb','Xb','ig','Ug']
onsets=['t','R','v','L']
rhymes=['eb','Xb','ig','Ug']
#define keys to be used and corresponding sounds
capKeys = {'t':'1','R':'2','v':'3','L':'4',
          'eb':'7','Xb':'8','ig':'9', 'Ug':'0'}
keys=capKeys.values()

#### map that sort responses based on keyboard layout - so [0,1,9] would turn into [1,9,0] ####
srtMap = {key: i for i, key in enumerate(['1', '2', '3', '4', '7','8', '9', '0'])}
srtWord= {key: i for i, key in enumerate(units)} # the same but for letters, translating keys into corresponding sounds - not important for now!




#### importing trials from our stimuli file, currently set at 48. 
#### participants will have to go through 16 at the first stage, and if accuracy
#### criterion not met, will get additional trials until met. max number of
#### extra trials available to reach criterion = 16.


sep=','
def importTrials(numTrials):
    bTrial= open ('CS.csv', 'rb') 
    colNames = bTrial.next().rstrip().split(sep)
    reader=csv.DictReader(bTrial)
    global trialsList
    trialsList = []
    for t in range(numTrials):
        trialStr=bTrial.next().rstrip().split(sep)
        assert len(trialStr) == len(colNames)
        trialDict = dict(zip(colNames, trialStr))
        trialsList.append(trialDict)
importTrials(48)


# dictionary of translations from 3-letter code to full word
# we have words like "treeb", "slig", "teb" - all different lengths. To keep them equal length
# within our code, we use the following letters as substitutes. To remember it's 
# not the real letter, I used upper case.
transKeys = {'tr':'R','vl':'L','oo':'U','ee':'X'}

# translating the 'fullTrial' string from the stimuli list
for trial in trialsList:
    for i in transKeys.keys():
        trial['fullTrial'] = trial['fullTrial'].replace(i, transKeys[i])



famTrials0 = trialsList [0:4] # 4 trials only self-paced
famTrials = trialsList [4:22] # 18 trials for FULL practice:
# first 3 with no accuracy monitoring, then 15 with monitoring to reach accuracy criterion

# getting all possible words in our experiment(instead of hard coding, go through
# the trialsList and extract from there - useful in case we change specific words)
allWords = []
for i in trialsList:
    w1,w2,w3,w4 = i['fullTrial'].split()
    allWords.extend([w1,w2,w3,w4])
allWords = list(set(allWords)) # reduce to only unique words, then make into list again
random.shuffle(allWords)  # shuffle their order before using for practice



#####################################
#### running from pre-saved pics ####
#####################################



win = visual.Window([800, 500], fullscr=True,
                        color="black", units='pix')

endText=visual.TextStim(win=win, height=40,
                 text="Practice phase completed! \n\nFinally, we can move on to the\
                 task itself. It is exactly the same as what you've been doing,\
                 except this time there will be no feedback. \n\nDo your best!",
                 color='black')

wrongText=visual.TextStim(win=win, height=40, 
                 text="Look at the template again and give it another try.",
                 color='black') # for when they make a mistake and have to press again

wrongTextb=visual.TextStim(win=win, height=40,
                 text="Try pressing all keys at the same time.",
                 color='black') # for when they dont press all keys at the same time


# when they make a mistake in stage 2, a red X appears on the bottom right
wrongX = visual.ShapeStim(win, pos = (450,-150), vertices=((0, -60), (0, 60), (0,0), 
                                               (60,0), (-60, 0)), ori = 45,
                                        lineWidth=5, closeShape=False, 
                                        lineColor='red')



fixationCross= visual.ShapeStim(win, vertices=((0, -70), (0, 70), (0,0), 
                                               (70,0), (-70, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey') # fixation cross at the beginning of each trial

pic1 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,155), size=(1000,50))
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,50), size=(1000,50))
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-55), size=(1000,50))
pic4 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-160), size=(1000,50))

pictures = {1:pic1, 2:pic2, 3:pic3, 4:pic4}

# picture in the center for the initial phase where they practice each word separately
centerPic = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,0), size=(1000,50))
 

#####################################
#### text stimuli - instructions ####
#####################################


# general instructions object, nothing written on it - needs
# to be set with the numbered instructions that follow:
instruct = visual.TextStim(win=win, height=35, 
                 color='black', wrapWidth = 1000, pos = (0,85), alignHoriz='center', 
                 alignVert='center')

# intructions for the first part
instruct1 = "In this task you will see a template of 8 small boxes on the screen, \
corresponding to the 8 keys you have your fingers on:"


# appears on the same screen as the previous, but on the bottom
instruct1b =  visual.TextStim(win=win, height=35, 
                            text ="Your job is to press only the keys of the boxes colored in black.\
                            Press them all at once, as quickly and accurately as you can. \
                            \n\n\tPress 'c' to begin.",
                 color='black', wrapWidth = 1000, pos = (0,-120), alignHoriz='center', 
                 alignVert='center')


instruct1c = "Great, looks like you're starting to get the hang of it. \
\n\nFrom now on, if you don't press the correct keys\
 you will see a red X on the bottom right of the screen. Let's try to avoid that!"


# different instructions that can be set for the general "instruct" object
instruct2 = "Nice work! \nNow we can begin with full practice trials. \n\n Every trial\
 consists of four templates. First you will have them appear one at a time\
 like you just practiced. \nThen, all 4 templates will appear on the\
 screen at once. Your task is to press the correct keys for each\
 template in order, from top to bottom. You will repeat the\
 whole sequence 3 times."
 
instruct2b = "A rectangle will scroll down from the top of\
 the screen, indicating when you should press each template.\
 You can press the keys from the first moment the rectangle touches\
 the template, even if it's only partially overlapping.\
 Make sure to keep up with the rectangle's speed! \n\nOnce you reach a high\
 level of accuracy, the practice phase will end and we can move\
 on to the task itself."
 
instruct5 = 'Test Phase'


# message to appear if they're 65 - 84% accurate:
accNotMet = "Let's practice some more to get you really good. Do your best!" 
 
 
phaseComplete = "First Phase Completed!"

# for participants to press 'c' when they've read instructions on that page
# and are ready to continue:
cToBegin =  visual.TextStim(win=win, height=35, 
                            text ="\n\n\tPress 'c' to continue.",
                 color='black', wrapWidth = 1000, pos = (0,-120), alignHoriz='center', 
                 alignVert='center')


# column names for our results file

headers=["trialNum", "trialType", "itemID", "rep", "wordInd", "curWord", 
                        "expKeys", "pressedKeys", 
                        "acc", "RT", "countCorrect", "correctKeys", 
                        "addedKeys", "missingKeys","accRate"]




#################################################################
############ PACER SETTINGS - SCROLLING RECTANGLE ###############
#################################################################


pacer = visual.Rect(win=win,size=(1700,100),lineColor="black", pos = ([0,250]))
background = visual.Rect(win=win, size = (2250, 900), fillColor = 'white', pos = ([0,0]))
pacerLocs = {'w1':[0,300], 'w2':[0,100], 'w3':[0,-100], 'w4':[0,-300]}
pacerLoc = {1:'w1', 2:'w2', 3:'w3', 4:'w4'}
startPos = [0,250]



fixationCross= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0), 
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey')


###################################################################################
#### a few things that are repeated in the code, just made them into functions ####
###################################################################################

def draw4():  # draws the 4 relevant pics
        background.draw()
        pic1.draw()
        pic2.draw()
        pic3.draw()
        pic4.draw()


def set4(): # sets the 4 relevant pics
    pic1.setImage('stimShots_FF/'+trial['w1']+'_FF.png')            
    pic2.setImage('stimShots_FF/'+trial['w2']+'_FF.png')           
    pic3.setImage('stimShots_FF/'+trial['w3']+'_FF.png')
    pic4.setImage('stimShots_FF/'+trial['w4']+'_FF.png')


def wordByWord(): # defines which pic should appear in the one-by-one stage
    if wordInd == 1:
        pic1.draw()
    elif wordInd == 2:
        pic2.draw()
    elif wordInd == 3:
        pic3.draw()
    else:
        pic4.draw()


def cClick (instructName): # displays instructions and waits for 'c' press - feed in instruction name (e.g., instruct1)
    cClick = False
    while not cClick:
        instruct.setText (instructName)
        background.draw()
        instruct.draw()
        cToBegin.draw() 
        win.flip()
        if event.waitKeys (['c']) == ['c']:
            cClick = True

def learn (curWord): # presents template to be pressed, if wrong - says so and returns to word
    while True:
        stage = 1
        RT = 'NA'
        accRate='NA'
        pressedKeys = []
        accKeys=[]
        add = []
        miss = []
        expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
        
        if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
            expKeys.append('3') # this is hard coded, see if there's a better way...
        if curWord[0] == 'R':
            expKeys.append('1')
        expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
        for i in transKeys.keys(): # return to full word
            curWord = curWord.replace(transKeys[i], i)      
        background.draw()
        fixationCross.draw()
        win.flip()
        core.wait(1)
        pic2.setImage('stimShots_FF/'+curWord+'_FF.png')
        background.draw()
        pic2.draw()
        temp = event.getKeys(keyList=keys)
        win.flip()
        start = time.clock()
        react = False
        interval = False
        end = 0
        #### getting responses ####
    
        while len(pressedKeys) < len(expKeys):
            if react:
                intervalTimer = time.clock()
                if (intervalTimer - end) > intervalTime:
                    interval = True
                    break
            getKeys = event.getKeys(keyList=keys)
            if react == False and len(getKeys) != 0: # if we haven't collected RTs yet
                end = time.clock() 
                RT = (end - start) * 1000  # check how much time passed since we started the RT clock
                react = True
            pressedKeys.extend(getKeys)    
            
        #### changing response keys into easy-to-read + writing to results file ####   
        
        pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
        pressedKeys ="".join(pressedKeys)              
        add = set(pressedKeys) - set(pressedKeys) # key additions
        add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
        if len(add) == 0:
            add = 'NA'
        miss = set(expKeys) - set(pressedKeys) # key omissions
        miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
        if len(miss) == 0:
            miss = 'NA'
        accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
        expKeys = "".join(expKeys)
        Acc = 1 if expKeys==pressedKeys else 0 # accuracy is 1 if all and only correct keys were pressed
        string=[str(var) for var in subject, stage, 'trialNum', "trialType", "trialID",
                        "rep", "wordInd", curWord,
                        expKeys, pressedKeys, Acc, RT,  
                        len(accKeys), accKeys, add, miss, accRate]      
        print string
        line='\t'.join(string) + '\n'
        resultsFile.write(line)
        resultsFile.flush()
        background.draw()
        if Acc == 0: # if accuracy is wrong, 
            if interval: # if it's because they didn't press at the same time
                wrongTextb.draw() # tell them to press all at once
            else: # if they got it wrong for any other reason
                wrongText.draw() # tell them to try again
                
            win.flip()
            core.wait(2)
            for i in transKeys.keys(): # return to coded word
                curWord = curWord.replace(i, transKeys[i])
            continue # go back to the beginning of this word and have them do it again.
        elif Acc == 1: # if accuracy is good,
            break # break loop and go on to next word
    



###################################################################################
###################### actual practice and writing to file ############################
###################################################################################
       


with open(subject+'_fam'+'_FF.txt','wb') as resultsFile: # opens new results file in current directory
    Rwriter=csv.DictWriter(resultsFile, fieldnames = headers)
    ccClick = False 
    breakTime=core.Clock()
    #### 1. start with word-by-word single presentation: ####
    while not ccClick: # present the following instruction screen (includes a pic as an example), until 'c' is pressed
        centerPic.setImage('stimShots_FF/'+'treeb'+'_FF.png')
        background.draw()
        centerPic.draw()
        instruct.setText(instruct1) # using the general instruct object but setting it with instruct 1
        instruct.draw()
        instruct1b.draw() # (instruct 1b is separate from the general instruct object)
        win.flip()
        if event.waitKeys (['c']) == ['c']:
            ccClick = True
    for curWord in allWords: # goes through each word and has them press it
        learn (curWord)
        
        ###########################################################################
        ################## commented out for playing around #######################
        ###########################################################################
        
    # learn (curWord) # each word must be correctly pressed twice. 
    # for curWord in allWords: # after each word was pressed twice (one after the other), go back to the beginning of the list and go through all words - one correct press per word
    # learn (curWord) # after this, they've pressed each word correctly 3 times total 
    background.draw()
    fixationCross.draw()
    win.flip()
    core.wait(1)
    cClick(instruct1c)
    for trial in famTrials0: # goes through the control trials of self-paced only practice
        stage = 2 # what we defined as the self-paced stage
        wordInd = 0 # keeps track of what word number we're at within the trial (1-4)
        set4() # sets the 4 images in place
        for curWord in trial['fullTrial'].split(): # goes through each of the 4 words in the trial     
            core.wait(0.1) 
            wordInd += 1
            pressedKeys = [] # keys that subject pressed
            accKeys = [] # accurate presses
            pressedWord = [] # translates key presses into corresponding word
            pressedUnits = [] # not important (translates keys into corresponding sounds)
            add = [] # keys pressed that were not in word
            miss = [] # keys not pressed (but should have been)
            RT = 'NA' # reaction time, to be defined later            
            expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word, separated by onset vs rhyme
            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                expKeys.append('3') # this is hard coded, see if there's a better way...
            if curWord[0] == 'R':
                expKeys.append('1')
            expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
            background.draw()
            wordByWord() # draw the correct word based on index (1,2,3,4) 
            temp = event.getKeys(keyList=keys)
            win.flip()     
            
            # getting responses and reaction time - first zero all variables
            RT = 'NA'
            start = time.clock()
            react = False
            #### getting responses ####
        
            while len(pressedKeys) < len(expKeys):
                getKeys = event.getKeys(keyList=keys)
                if react == False and len(getKeys) != 0: # if we haven't collected RTs yet
                    end = time.clock() 
                    RT = (end - start) * 1000  # check how much time passed since we started the RT clock
                    react = True 
                pressedKeys.extend(getKeys)  
            pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
            pressedKeys ="".join(pressedKeys)              
            # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
            # will appear as strings):               
            add = set(pressedKeys) - set(expKeys) # key additions
            add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
            if len(add) == 0:
                add = 'NA'
            miss = set(expKeys) - set(pressedKeys) # key omissions
            miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
            if len(miss) == 0:
                miss = 'NA'
            accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
            expKeys = "".join(expKeys)
            
            Acc = 1 if expKeys==pressedKeys else 0
            string=[str(var) for var in subject, stage, 'trialNum', trial['type'], trial['ID'], 
                        "rep", wordInd, curWord,
                        expKeys, pressedKeys, Acc, RT,  
                        len(accKeys), accKeys, add, miss]              
            line='\t'.join(string) + '\n'
            resultsFile.write(line)
            resultsFile.flush()
            if Acc == 0:
                background.draw()
                wrongX.draw()
                win.flip()
                core.wait(0.5)
        
   
    cClick (instruct2) # shows first instructions for next part and waits for 'c'
    cClick (instruct2b)
    
    ####### beginning full trial practice ########
    
    accCount= []
    trialNum = 0 # initiate trial number count
    go = True # initiate experiment flow. when go == false, familiarization phase will end. 
              #  we will make go == false, only when 85% accuracy reached, and it is only 
             # first checked after a minimum of 16 trials. 

    for trial in famTrials: # goes through the control trials they'll be practicing
        stage = 3 # beginning the fullTrials
        accRate = 'NA' # initialize accRate
        notMet = 0 # monitors how many additional trials they get after initial accuracy not met
        if go:
            background.draw()
            fixationCross.draw()
            win.flip()
            core.wait(1)
            set4()
            trialNum += 1
            wordInd = 0 # index of word within trial (first word, second...)
            rep = 0 # rep 0 means it's the word-by-word presentation at the beginnign
            background.draw()
            win.flip()
            for curWord in trial['fullTrial'].split(): # goes through each word in current trial
                core.wait(0.1)
                wordInd += 1
                # zeroing all variables:
                RT = 'NA'
                pressedKeys = [] # keys that subject pressed
                accKeys = [] # accurate presses
                pressedWord = [] # translates key presses into corresponding word
                pressedUnits = [] # not important
                add = [] # keys pressed that were not in word
                miss = [] # keys not pressed         
                expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
                if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                    expKeys.append('3') # this is hard coded, see if there's a better way...
                if curWord[0] == 'R':
                    expKeys.append('1')
                expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
                background.draw()
                wordByWord() # function we defined before, making sure only one word is presented at a time, in it's corresponding place from top to bottom
                temp = event.getKeys(keyList=keys)
                win.flip()  
                ##### getting responses and reaction time ####      
                start = time.clock()
                react = False
                
                while len(pressedKeys) < len(expKeys):
                    getKeys = event.getKeys(keyList=keys)
                    if react == False and len(getKeys) != 0: # if we haven't collected RTs yet
                        end = time.clock() 
                        RT = (end - start) * 1000  # check how much time passed since we started the RT clock
                        react = True 
                    pressedKeys.extend(getKeys)  
                event.clearEvents()
                pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
                pressedKeys ="".join(pressedKeys)              
                for i in pressedKeys: # translating keys into word, not important
                    pressedUnit = [unit for unit, value in capKeys.iteritems() if value == i]
                    pressedUnits.append(pressedUnit)
                    pressedWord = pressedWord + pressedUnit
                pressedWord = sorted(pressedWord, key = lambda x:  srtWord[x])
                pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
                if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                    pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
                # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                # will appear as strings):               
                add = set(pressedKeys) - set(expKeys) # key additions
                add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
                if len(add) == 0:
                    add = 'NA'
                miss = set(expKeys) - set(pressedKeys) # key omissions
                miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
                if len(miss) == 0:
                    miss = 'NA'
                accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
                expKeys = "".join(expKeys)
                Acc = 1 if expKeys==pressedKeys else 0
                string=[str(var) for var in subject, '3', trialNum, trial['type'], trial['ID'],  # collect all the info we're interested in
                        rep, wordInd, curWord, 
                        expKeys, pressedKeys, Acc, RT,  
                        len(accKeys), accKeys, add, miss]              
                print string 
                  
                line='\t'.join(string) + '\n'
                resultsFile.write(line)
                resultsFile.flush()
                if Acc == 0:
                    background.draw()
                    wrongX.draw()
                    win.flip()
                    core.wait(0.3)
    
            background.draw()
            win.flip()
            core.wait(1)
            pacer.setPos (startPos)
            for rep in range(1,4):
                hitBoundary = False
                wordInd=1 # index of word within trial (first word, second...)
                pressedKeys = [] # keys that subject pressed
                accKeys = [] # accurate presses
                pressedWord = [] # translates key presses into corresponding word
                pressedUnits = [] # not important
                add = [] # keys pressed that were not in word
                miss = [] # keys not pressed
                RT = 'NA' # reaction time, to be defined later     
                curWord = trial[pacerLoc[wordInd]]
                for i in transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                    curWord = curWord.replace(i, transKeys[i])
                expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
                if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                    expKeys.append('3') # this is hard coded, see if there's a better way...
                if curWord[0] == 'R':
                    expKeys.append('1')
                expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
                react = False
                temp = event.getKeys(keyList=keys)
                pacer2 = visual.Rect(win=win,size=(1700,100),lineColor="black", pos = ([0,685]))
                while True:
                    draw4()
                    if Acc == 0: # keep the red x up as long as accuracy equals 0
                        wrongX.draw()
                    if wordInd < 5:
                        pacer.draw()
                    if wordInd < 4:
                        pacer2.draw()
                    pacer2.pos = (0,435 + pacer.pos[1])
                    pacer.pos -= (0,interStepInterval)
                    win.flip()
                    if  pacer.pos[1] <= -220:
                        pacer = pacer2
                        print start.getTime()
                        #pacer.setPos(startPos)
                        break
                    if wordInd >=5:
                        continue
                    if pictures[wordInd].overlaps(pacer):
                        if hitBoundary == False:
                            temp = event.getKeys(keyList=keys)
                            Acc = 'NA'
                            hitBoundary = True
                            start = core.Clock()
                        if len(pressedKeys) < len(expKeys):
                            getKeys = event.getKeys(keyList=keys)
                            if len(getKeys) != 0:
                                if react == False:
                                    RT = start.getTime() * 1000
                                    react = True
                            pressedKeys.extend(getKeys)            
                    else:
                        if hitBoundary:
                            event.clearEvents()
                            temp = event.getKeys(keyList=keys)
                            pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
                            pressedKeys ="".join(pressedKeys)              
                            for i in pressedKeys: # translating keys into word, not important
                                pressedUnit = [unit for unit, value in capKeys.iteritems() if value == i]
                                pressedUnits.append(pressedUnit)
                                pressedWord = pressedWord + pressedUnit
                            pressedWord = sorted(pressedWord, key = lambda x:  srtWord[x])
                            pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
                            if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                                pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
    
                            # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                            # will appear as strings):               
                            add = set(pressedKeys) - set(expKeys) # key additions
                            add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
                            if len(add) == 0:
                                add = 'NA'
                            miss = set(expKeys) - set(pressedKeys) # key omissions
                            miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
                            if len(miss) == 0:
                                miss = 'NA'
                            accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
                            expKeys = "".join(expKeys)
                            Acc = 1 if expKeys==pressedKeys else 0
                            if trialNum > 3: # only start counting accuracy after first 3 trials
                                accCount.append(Acc)
                                accRate = float(sum(accCount))/len(accCount)
                            string=[str(var) for var in subject, "3", trialNum, trial['type'], trial['ID'],  # collect all the info we're interested in
                                                                      rep, wordInd, curWord, 
                                                                      expKeys, pressedKeys, Acc, RT,  
                                                                      len(accKeys), accKeys, add, miss, accRate]              
                            print string 
                            line='\t'.join(string) + '\n'
                            resultsFile.write(line)
                            resultsFile.flush()
                            hitBoundary = False
                            
                            wordInd+=1 # index of word within trial (first word, second...)
                            pressedKeys = [] # keys that subject pressed
                            accKeys = [] # accurate presses
                            pressedWord = [] # translates key presses into corresponding word
                            pressedUnits = [] # not important
                            add = [] # keys pressed that were not in word
                            miss = [] # keys not pressed
                            RT = 'NA' # reaction time, to be defined later     
                            if wordInd < 5:
                                curWord = trial[pacerLoc[wordInd]]
                            for i in transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                                curWord = curWord.replace(i, transKeys[i])
                            expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
                            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                                expKeys.append('3') # this is hard coded, see if there's a better way...
                            if curWord[0] == 'R':
                                expKeys.append('1')
                            expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
                            react = False
                            temp = event.getKeys(keyList=keys)
        background.draw()
        fixationCross.draw()
        win.flip()
        core.wait(.5)
        if trialNum >= 18:
            if accRate >= .85:                
                go = False
            else:
                if notMet%5 ==0: # only present the following message every five trials
                    cClick (accNotMet) # message saying they're doing well but need more practice.
                    notMet+=1         # only appears if they're under 85%, and then they will 
                                    # get more trials one-by-one until they reach 85%.

         ##### finished - close results file and present screen 
         #### saying phase 1 complete. 
         #("else" is of the "if" statement from line 459, "if go:", when beginning trial flow)           
    else:  
        resultsFile.close()
        instruct.setText(phaseComplete)
        background.draw()
        instruct.draw()
        win.flip()
        core.wait(1) 
        
        
background.draw()
win.flip()
cClick(instruct5)




################################################
interStepInterval = 1.8

pacer = visual.Rect(win=win,size=(1700,100),lineColor="black", pos = ([0,250]))

breakText=visual.TextStim(win=win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='black')
endText=visual.TextStim(win=win, height=40,
                 text="All Done! Please call the experimenter.",
                 color='black')




fixationCross= visual.ShapeStim(win, vertices=((0, -70), (0, 70), (0,0), 
                                               (70,0), (-70, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey')

pic1 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,155), size=(1000,50))
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,50), size=(1000,50))
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-55), size=(1000,50))
pic4 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-160), size=(1000,50))


trialList = []
sep=','
import io
def importTestTrials(numTrials):
    bTrial= open ('TTstim.csv', 'rb') 
    colNames = bTrial.next().rstrip().split(sep)
    reader=csv.DictReader(bTrial)
    for t in range(numTrials):
        trialStr=bTrial.next().rstrip().split(sep)
        assert len(trialStr) == len(colNames)
        trialDict = dict(zip(colNames, trialStr))
        trialList.append(trialDict)
importTestTrials(32)
random.shuffle(trialList)
trialList[0]
for trial in trialList:
    for i in transKeys.keys():
        trial['fullTrial'] = trial['fullTrial'].replace(i, transKeys[i])
headers=["subject", "trialNum", "trialType", "itemID", "rep", "wordInd", "curWord", 
                        "pressedWord","expKeys", "pressedKeys", 
                        "acc", "RT", "countCorrect", "correctKeys", 
                        "addedKeys", "missingKeys"]



    
# define expected keys per word

     
with open(subject + '_TTwb.csv','wb') as resultsFile:
    Rwriter=csv.DictWriter(resultsFile, fieldnames=headers)
    Rwriter.writeheader()
    core.wait(2)
    breakTime=core.Clock()
    trialNum=0   
    for trial in trialList:
        trialNum+=1
        background.draw()
        fixationCross.draw()
        win.flip()
        core.wait(1)
        pic1.setImage('stimShots_FF/'+trial['w1']+'_FF.png')            
        pic2.setImage('stimShots_FF/'+trial['w2']+'_FF.png')           
        pic3.setImage('stimShots_FF/'+trial['w3']+'_FF.png')
        pic4.setImage('stimShots_FF/'+trial['w4']+'_FF.png')
        # big red circle disappears, nothing on screen for 1 sec ;
        # then small blue circle appears and participants must begin              

        background.draw()
        wordInd=0 # index of word within triak (first word, second...)
        rep = 0
        win.flip()
        for curWord in trial['fullTrial'].split():
            core.wait(0.1)
            wordInd += 1
            pressedKeys = [] # keys that subject pressed
            accKeys = [] # accurate presses
            pressedWord = [] # translates key presses into corresponding word
            pressedUnits = [] # not important
            add = [] # keys pressed that were not in word
            miss = [] # keys not pressed
            RT = 'NA' # reaction time, to be defined later            
            expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                expKeys.append('3') # this is hard coded, see if there's a better way...
            if curWord[0] == 'R':
                expKeys.append('1')
            expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
            background.draw()
            if wordInd == 1:
                pic1.draw()
            elif wordInd == 2:
                pic2.draw()
            elif wordInd == 3:
                pic3.draw()
            else:
                pic4.draw()
            temp = event.getKeys(keyList=keys)
            win.flip()     
            RT = 'NA'
            # getting responses and reaction time:
            
            start = time.clock()
            react = False
            #### getting responses ####
        
            while len(pressedKeys) < len(expKeys):
                getKeys = event.getKeys(keyList=keys)
                if react == False and len(getKeys) != 0: # if we haven't collected RTs yet
                    end = time.clock() 
                    RT = (end - start) * 1000  # check how much time passed since we started the RT clock
                    react = True 
                pressedKeys.extend(getKeys)    
            event.clearEvents()
            pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
            pressedKeys ="".join(pressedKeys)              
            for i in pressedKeys: # translating keys into word
                pressedUnit = [unit for unit, value in capKeys.iteritems() if value == i]
                pressedUnits.append(pressedUnit)
                pressedWord = pressedWord + pressedUnit
            pressedWord = sorted(pressedWord, key = lambda x:  srtWord[x])
            pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
            if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit

            # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
            # will appear as strings):               
            add = set(pressedKeys) - set(expKeys) # key additions
            add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
            miss = set(expKeys) - set(pressedKeys) # key omissions
            miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
            accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
            expKeys = "".join(expKeys)
            Acc = 1 if expKeys==pressedKeys else 0
            string=[str(var) for var in subject, trialNum, trial['type'], trial['ID'], 
                    rep, wordInd, curWord, pressedWord, 
                    expKeys, pressedKeys, Acc, RT,  
                    len(accKeys), accKeys, add, miss]              
            print string               
            line='\t'.join(string) + '\n'
            resultsFile.write(line)
            resultsFile.flush()
            getKeys = []

        background.draw()
        win.flip()
        core.wait(1)
        pacer.setPos (startPos)
        for rep in range(1,4):
            hitBoundary = False
            wordInd=1 # index of word within trial (first word, second...)
            pressedKeys = [] # keys that subject pressed
            accKeys = [] # accurate presses
            pressedWord = [] # translates key presses into corresponding word
            pressedUnits = [] # not important
            add = [] # keys pressed that were not in word
            miss = [] # keys not pressed
            RT = 'NA' # reaction time, to be defined later     
            curWord = trial[pacerLoc[wordInd]]
            for i in transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                curWord = curWord.replace(i, transKeys[i])
            expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                expKeys.append('3') # this is hard coded, see if there's a better way...
            if curWord[0] == 'R':
                expKeys.append('1')
            expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
            react = False
            temp = event.getKeys(keyList=keys)
            pacer2 = visual.Rect(win=win,size=(1700,100),lineColor="black", pos = ([0,685]))
            while True:
                draw4()
                if wordInd < 5:
                    pacer.draw()
                if wordInd < 4:
                    pacer2.draw()
                pacer2.pos = (0,435 + pacer.pos[1])
                pacer.pos -= (0,interStepInterval)
                win.flip()
                if  pacer.pos[1] <= -220:
                    print pacer2.pos[1]
                    print pacer.pos[1]
                    pacer = pacer2
                    print start.getTime()
                    #pacer.setPos(startPos)
                    break
                if wordInd >= 5:
                    continue
                if pictures[wordInd].overlaps(pacer):
                    if hitBoundary == False:
                        temp = event.getKeys(keyList=keys)
                        hitBoundary = True
                        #start = time.clock()
                        startt = core.Clock()
                        if wordInd == 1:
                            start = core.Clock()
                    if len(pressedKeys) < len(expKeys):
                        getKeys = event.getKeys(keyList=keys)
                        if len(getKeys) != 0:
                            if react == False:
                                #end = time.clock()
                                #RT = (end - start) * 1000
                                RT = startt.getTime() * 1000
                                react = True
                        pressedKeys.extend(getKeys)            
                else:
                    if hitBoundary:
                        event.clearEvents()
                        temp = event.getKeys(keyList=keys)
                        pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
                        pressedKeys ="".join(pressedKeys)              
                        for i in pressedKeys: # translating keys into word, not important
                            pressedUnit = [unit for unit, value in capKeys.iteritems() if value == i]
                            pressedUnits.append(pressedUnit)
                            pressedWord = pressedWord + pressedUnit
                        pressedWord = sorted(pressedWord, key = lambda x:  srtWord[x])
                        pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
                        if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                            pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit

                        # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                        # will appear as strings):               
                        add = set(pressedKeys) - set(expKeys) # key additions
                        add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
                        if len(add) == 0:
                            add = 'NA'
                        miss = set(expKeys) - set(pressedKeys) # key omissions
                        miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
                        if len(miss) == 0:
                            miss = 'NA'
                        accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
                        expKeys = "".join(expKeys)
                        Acc = 1 if expKeys==pressedKeys else 0
                        string=[str(var) for var in subject, trialNum, trial['type'], trial['ID'],  # collect all the info we're interested in
                                                                  rep, wordInd, curWord, 
                                                                  expKeys, pressedKeys, Acc, RT,  
                                                                  len(accKeys), accKeys, add, miss]              
                        print string 
                        
                        hitBoundary = False
                        wordInd+=1 # index of word within trial (first word, second...)
                        pressedKeys = [] # keys that subject pressed
                        accKeys = [] # accurate presses
                        pressedWord = [] # translates key presses into corresponding word
                        pressedUnits = [] # not important
                        add = [] # keys pressed that were not in word
                        miss = [] # keys not pressed
                        RT = 'NA' # reaction time, to be defined later   
                        if wordInd < 5:
                            curWord = trial[pacerLoc[wordInd]]
                        for i in transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                            curWord = curWord.replace(i, transKeys[i])
                        expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
                        if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                            expKeys.append('3') # this is hard coded, see if there's a better way...
                        if curWord[0] == 'R':
                            expKeys.append('1')
                        expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
                        react = False
                        temp = event.getKeys(keyList=keys)
                        line='\t'.join(string) + '\n'
                        resultsFile.write(line)
                        resultsFile.flush()
                        getKeys = []     
        background.draw()                              
        fixationCross.draw()
        win.flip()
        core.wait(.5)
        if int(breakTime.getTime())>80:
            breakClick=False
            while not breakClick:
                background.draw()
                breakText.draw()
                win.flip()
                stop= event.waitKeys(['c','q'])
                if stop==['c']:
                    breakTime.reset()
                    breakClick=True
                elif stop==['q']:
                    win.close()
                    core.quit()
    background.draw()
    endText.draw()
    resultsFile.close()
    win.flip()
    core.wait(5)
win.close()
core.quit()