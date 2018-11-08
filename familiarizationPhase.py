###################################
########fill in subject ID #######

subject =''

###################################
###################################

######### timers  ################

pacerTempo = 1.2 # speed for first x practice trials


##################################

import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui
import time

### R = tr, L = vl, x = ee. changed to keep all words 3 characters.
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






#### importing trials from our stimuli file. currently set at 32 cause that's the num
#### of trials in there.
sep=','
def importTrials(numTrials):
    bTrial= open ('TTstim.csv', 'rb') 
    colNames = bTrial.next().rstrip().split(sep)
    reader=csv.DictReader(bTrial)
    global trialsList
    trialsList = []
    for t in range(numTrials):
        trialStr=bTrial.next().rstrip().split(sep)
        assert len(trialStr) == len(colNames)
        trialDict = dict(zip(colNames, trialStr))
        trialsList.append(trialDict)
importTrials(32)


# dictionary of translations from 3-letter code to full word
# we have words like "treeb", "vlig", "teb" - all different lengths. To keep them equal length
# within our code, we use the following letters as substitutes. To remember it's 
# not the real letter, I used upper case.
transKeys = {'tr':'R','vl':'L','oo':'U','ee':'X'}

# translating the 'fullTrial' string from the stimuli list
for trial in trialsList:
    for i in transKeys.keys():
        trial['fullTrial'] = trial['fullTrial'].replace(i, transKeys[i])

# first set of 8 practice trials - where they only go through the 4 words one-by-one from top to bottom at their own speed
# takes every 4th trials from trialsList (unique set of four words - take a look at the trials csv file to understand)
exTrials1 = [i for i in trialsList if int(i['ID']) in range(1,32,4)]

# 16 trials for FULL practice - both word-by-word and paced by the blue circle:
# 8 of these will be TT, 8 NON (in our trials file, 1-16 are TT, 17-32 are NON)
exTTtrials = [i for i in trialsList if int(i['ID']) in range(2,16,2)] # 8 TT examples
exNONtrials = [i for i in trialsList if int(i['ID']) in range(18,32,2)] # NON examples
exTrials2 =  exTTtrials + exNONtrials # combine TT and NON for full set of example trials



# getting all possible words in our experiment(instead of hard coding, go through
# the trialsList and extract from there - useful in case we change specific words)
allWords = []
for i in trialsList:
    w1,w2,w3,w4 = i['fullTrial'].split()
    allWords.extend([w1,w2,w3,w4])
allWords = list(set(allWords)) # reduce to only unique words, then make into list again
random.shuffle(allWords)  # shuffle their order before using for practice


#### running from pre-saved pics ####
win = visual.Window([800, 500], fullscr=True,
                        color="white", units='pix')

endText=visual.TextStim(win=win, height=40,
                 text="First phase completed!",
                 color='black')

pacer = visual.Circle(win=win, radius = 20, fillColor='blue') # little blue dot 
fixationView= visual.Circle(win=win, radius = 40, fillColor='red', pos=(-620,350)) # big red circle


wrongText=visual.TextStim(win=win, height=40, 
                 text="Look at the template again and give it another try.",
                 color='black') # for when they make a mistake and have to press again


fixationCross= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0), 
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey') # fixation cross at the beginning of each trial


# 4 pictures (the exact images set later in the code), at 4 different positions from top to bottom of screen 
pic1 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,350), size=(1200,300))
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,100), size=(1200,300))
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-150), size=(1200,300))
pic4 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-400), size=(1200,300))


# picture in the center for the initial phase where they practice each word separately
centerPic = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,0), size=(1200,300))
 

#### text stimuli - instructions ####

# general instructions object, nothing written on it - needs
# to be set with the numbered instructions that follow:
instruct = visual.TextStim(win=win, height=35, 
                 color='black', wrapWidth = 1000, pos = (0,250), alignHoriz='center', 
                 alignVert='center')

# intructions for the first part
instruct1 = "In this task you will see a template of 8 small boxes on the screen, \
corresponding to the 8 keys you have your fingers on:"


# appears on the same screen as the previous, but on the bottom
instruct1b =  visual.TextStim(win=win, height=35, 
                            text ="Your job is to press only the keys of the boxes colored in black.\
                            Press them all at once, as quickly and accurately as you can. \
                            \n\n\tPress 'c' to begin.",
                 color='black', wrapWidth = 1000, pos = (0,-200), alignHoriz='center', 
                 alignVert='center')


# different instructions that can be set for the general "instruct" object
instruct2 = "Great! Let's keep practicing. \nThis time there will be no feedback, but make sure to \
pay attention and press the correct keys."
instruct3 = "Nice work! \nNow we can begin with full trials. Every trial\
 consists of four templates. First\
 you will have them appear one at a time\
like you just practiced."
instruct4 = "Then, all 4 templates will \
 appear on the screen at once. \nOn the left side of the screen you will see a \
 red circle. After 2 seconds the red circle will disappear, and a small blue\
 circle will appear near the first template. \n\nThe blue circle is \
 your cue - when it appears next to a template, you press the correct keys \
 for that template. The order will always be the same, from top to bottom, \
 but you must keep up with the speed of the blue circle. \n Let's start \
 with a few trials as an example."

# for participants to press 'c' when they've read instructions on that page
# and are ready to continue:
cToBegin =  visual.TextStim(win=win, height=35, 
                            text ="\n\n\tPress 'c' to continue.",
                 color='black', wrapWidth = 1000, pos = (0,-200), alignHoriz='center', 
                 alignVert='center')



###################################################################################
#### a few things that are repeated in the code, just made them into functions ####
###################################################################################

def draw4():  # draws the 4 relevant pics
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
        instruct.draw()
        cToBegin.draw() 
        win.flip()
        if event.waitKeys (['c']) == ['c']:
            cClick = True

def learn (curWord): # presents template to be pressed, if wrong - says so and returns to word
    while True:
        RT = 'NA'
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
        fixationCross.draw()
        win.flip()
        core.wait(1)
        pic2.setImage('stimShots_FF/'+curWord+'_FF.png')
        pic2.draw()
        temp = event.getKeys(keyList=keys)
        win.flip()
        start = time.clock()
        react = False
        #### getting responses ####
    
        while len(pressedKeys) < len(expKeys):
            getKeys = event.getKeys(keyList=keys)
            if react == False and len(getKeys) != 0: # if we haven't collected RTs yet
                end = time.clock() 
                RT = (end - start) * 1000 # check how much time passed since we started the RT clock
                react = True 
            pressedKeys.extend(getKeys)    
            
        #### changing response keys into easy-to-read + writing to results file ####   
        
        pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
        pressedKeys ="".join(pressedKeys)              
        add = set(pressedKeys) - set(pressedKeys) # key additions
        add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
        miss = set(expKeys) - set(pressedKeys) # key omissions
        miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
        accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
        expKeys = "".join(expKeys)
        Acc = 1 if expKeys==pressedKeys else 0 # accuracy is 1 if all and only correct keys were pressed
        string=[str(var) for var in subject, curWord, # collect the info we want to keep
                            expKeys, pressedKeys, Acc, RT, accKeys, add, miss]       
        print string
        line='\t'.join(string) + '\n'
        resultsFile.write(line)
        resultsFile.flush()
        if Acc == 0: # if accuracy is wrong, 
            wrongText.draw() # present screen saying they should try again +
            win.flip()
            core.wait(2)
            for i in transKeys.keys(): # return to coded word
                curWord = curWord.replace(i, transKeys[i])
            continue # go back to the beginning of this word and have them do it again.
        elif Acc == 1: # if accuracy is good,
            break # break loop and go on to next word
    



###################################################################################
###################### actual task and writing to file ############################
###################################################################################
       


with open(subject+'_fam'+'_FF.csv','wb') as resultsFile: # opens new results file in current directory
    Rwriter=csv.DictWriter(resultsFile, fieldnames= None)
    ccClick = False 
    while not ccClick: # present the following intrsuction screen (includes a pic as an example), until 'c' is pressed
        centerPic.setImage('stimShots_FF/'+'treeb'+'_FF.png')
        centerPic.draw()
        instruct.setText(instruct1) # using the general instruct object but setting it with instruct 1
        instruct.draw()
        instruct1b.draw() # (instruct 1b is separate from the general instruct object)
        win.flip()
        if event.waitKeys (['c']) == ['c']:
            ccClick = True
    for curWord in allWords: # goes through each word and has them press it
        learn (curWord)
        learn (curWord) # each word must be correctly pressed twice. 
    for curWord in allWords: # after each word was pressed twice (one after the other), go back to the beginning of the list and go through all words - one correct press per word
        learn (curWord) # after this, they've pressed each word correctly 3 times total 
    
    
    cClick (instruct2) # presents 2nd instructions - just saying good work and continue, 
    # though there's a slight difference they're not tols about - words are now presented one-by-one
    # from top to bottom (the way they will be later in the full trials)
 
    for trial in exTrials1: # goes through the 5 random trials we chose earlier
        
        wordInd = 0 # keeps track of what word number we're at within the trial (1-4)
        set4() # sets the 4 images in place
        for curWord in trial['fullTrial'].split(): # goes through each of the 4 words in the trial
            temp = event.getKeys(keyList=keys)
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
            
            wordByWord() # draw the correct word based on index (1,2,3,4) 
            
            win.flip()     
            
            # getting responses and reaction time - first zero all variables
            RT = 'NA'
            getKeys = event.waitKeys(keyList=keys)
            pressedKeys.extend(getKeys)    
            event.clearEvents()
            pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
            pressedKeys ="".join(pressedKeys)              
            # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
            # will appear as strings):               
            add = set(pressedKeys) - set(expKeys) # key additions
            add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
            miss = set(expKeys) - set(pressedKeys) # key omissions
            miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
            accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
            expKeys = "".join(expKeys)
            Acc = 1 if expKeys==pressedKeys else 0
            string=[str(var) for var in trial['type'], trial['ID'], 
                    wordInd, curWord, 
                    expKeys, pressedKeys, Acc, RT,  
                    len(accKeys), accKeys, add, miss]              
            print string
            
    cClick (instruct3) # shows first instructions for next part and wait's for 'c'
    cClick (instruct4) # shows second instructions for next part and wait's for 'c'

    ####### beginning full trial practice ########
    for trial in exTrials2: # goes through the random 5 trials they'll be practicing
        fixationCross.draw()
        win.flip()
        core.wait(1)
        set4()
        wordInd=0 # index of word within trial (first word, second...)
        rep = 0 # rep 0 means it's the word-by-word presentation at the beginnign
        win.flip()
        for curWord in trial['fullTrial'].split(): # goes through each word in current trial
            temp = event.getKeys(keyList=keys)
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
            RT = 'NA' # reaction time, to be defined later            
            expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                expKeys.append('3') # this is hard coded, see if there's a better way...
            if curWord[0] == 'R':
                expKeys.append('1')
            expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
            wordByWord() # function we defined before, making sure only one word is presented at a time, in it's corresponding place from top to bottom
            win.flip()  
            # getting responses and reaction time:       
            while len(pressedKeys) < len(expKeys):
                getKeys = event.waitKeys(keyList=keys) 
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
            miss = set(expKeys) - set(pressedKeys) # key omissions
            miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
            accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
            expKeys = "".join(expKeys)
            Acc = 1 if expKeys==pressedKeys else 0
            string=[str(var) for var in subject, trial['type'], trial['ID'],  # collect all the info we're interested in
                    rep, wordInd, curWord, pressedWord, 
                    expKeys, pressedKeys, Acc, RT,  
                    len(accKeys), accKeys, add, miss]              
            print string 
              
            line='\t'.join(string) + '\n'
            resultsFile.write(line)
            resultsFile.flush()
            
        
        win.flip()
        core.wait(1)
        draw4()
        fixationView.draw() # fixation to allow brief viewing - 2 sec of big red circle
        win.flip()
        core.wait(2)
        draw4()
        win.flip() 
        core.wait(0.5)
        for rep in range(1,4):
            temp = event.getKeys(keyList=keys)
            wordInd=0 # index of word within trial (first word, second...)
            draw4()
            pacer.pos = (-550,350) # sets little blue dot at first word
            pacer.draw()
            win.flip()
            for curWord in trial['fullTrial'].split():
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
                draw4()
                pacer.draw()
                win.flip()
                pacerTime=core.Clock() # starts counting for when the blue dot should move   
                start = time.clock() # starts counting for reaction times
                react = False
                # getting responses and reaction time:
                #  although they're supposed to press all keys at once, there are tiny differences.
                # what we do her is collect RT for the first key pressed, but still wait for more key presses - 
                # until the blue dot moves on (which is only around 1 sec, so really any difference between key presses is tiny...)
                while pacerTime.getTime()< pacerTempo: # if the time since the blue dot appeared is still under the speed we've determined at the top of the script (will probably be ~1 second)
                    if len(pressedKeys) < len(expKeys): # if the number of keys pressed is less than the number of keys required
                        getKeys = event.getKeys(keyList=keys) # record key responses
                        if len(getKeys) != 0: # if they pressed more than one key
                            if react == False: # if we haven't collected RTs yet
                                end = time.clock() 
                                RT = (end - start) * 1000 # check how much time passed since we started the RT clock
                                react = True 
                        pressedKeys.extend(getKeys)   # add whatever keys are pressed to the "pressedKeys"  
                    else:
                        break
                event.clearEvents()
                if react == False:
                    RT = 'NA'

                core.wait(pacerTempo-(pacerTime.getTime())) # wait full time even if participant answered before time's up
                
                
                pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
                pressedKeys ="".join(pressedKeys)              

                # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                # will appear as strings):               
                add = set(pressedKeys) - set(expKeys) # key additions
                add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
                miss = set(expKeys) - set(pressedKeys) # key omissions
                miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
                accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
                expKeys = "".join(expKeys)
                Acc = 1 if expKeys==pressedKeys else 0
                string=[str(var) for var in subject, trial['type'], trial['ID'], 
                        rep, wordInd, curWord,
                        expKeys, pressedKeys, Acc, RT,  
                        len(accKeys), accKeys, add, miss]              
                print string               
                line='\t'.join(string) + '\n'
                resultsFile.write(line)
                resultsFile.flush()
                pacer.pos -=(0,250)
 
                                      
        fixationCross.draw()
        win.flip()
        core.wait(.5)
  
win.close()
core.quit()
