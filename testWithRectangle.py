
###################################
########fill in subject ID #######

subject ='AAA'

###################################
###################################

pacerTempo = 1.2 # speed of blue cue
timeBreak = 60 # seconds till break (will wait till end of trial to break)

###################################
###################################

import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui
import time

### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length.
# only changed in trial ['fullTrial'], not in w1,2,3,4
units=['t','R','v','L','eb','Xb','ig','Ug']
onsets=['t','R','v','L']
rhymes=['eb','Xb','ig','Ug']
#define keys to be used and corresponding sounds
capKeys = {'t':'1','R':'2','v':'3','L':'4',
          'eb':'7','Xb':'8','ig':'9', 'Ug':'0'}
keys=capKeys.values()




 # order by keyboard layout:
srtMap = {key: i for i, key in enumerate(['1', '2', '3', '4', '7','8', '9', '0'])}
srtWord= {key: i for i, key in enumerate(units)}


# importing trials
sep=','
import io
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
random.shuffle(trialsList)
trialsList[0]

headers=["trialNum", "trialType", "itemID", "rep", "wordInd", "curWord", 
                        "pressedWord","expKeys", "pressedKeys", 
                        "acc", "RT", "countCorrect", "correctKeys", 
                        "addedKeys", "missingKeys"]


# translate spelling into letters more comfortable for coding - only 3 letters per word.
# only the 'fullTrial' string is translated, since it is the one that is later used
# to split() and determine required keys.
transKeys = {'tr':'R','vl':'L','oo':'U','ee':'X'}
for trial in trialsList:
    for i in transKeys.keys():
        trial['fullTrial'] = trial['fullTrial'].replace(i, transKeys[i])





##running from pre-saved pics
win = visual.Window([800, 500], fullscr=True,
                        color="white", units='pix')
breakText=visual.TextStim(win=win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='black')
endText=visual.TextStim(win=win, height=40,
                 text="All Done! Please call the experimenter.",
                 color='black')


############ PACER SETTINGS - SCROLLING RECTANGLE ###############
pacer = visual.Rect(win=win,size=(1800,120),lineColor="black", pos = ([0,300]))
pacerLocs = {'w1':[0,300], 'w2':[0,100], 'w3':[0,-100], 'w4':[0,-300]}
startPos = [0,600]
interStepInterval = 6.0

fixationCross= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0), 
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey')

pic1 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,300), size=(1200,280))
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,100), size=(1200,280))
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-100), size=(1200,280))
pic4 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-300), size=(1200,280))




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


with open(subject+'_FF.txt','wb') as resultsFile:
    Rwriter=csv.DictWriter(resultsFile, fieldnames=headers)
    Rwriter.writeheader()
    core.wait(0.5)
    breakTime=core.Clock()
    trialNum=0     
    for trial in trialsList: # goes through the random  trials they'll be practicing
        fixationCross.draw()
        win.flip()
        core.wait(1)
        set4()
        trialNum += 1
        wordInd = 0 # index of word within trial (first word, second...)
        rep = 0 # rep 0 means it's the word-by-word presentation at the beginnign
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
            wordByWord() # function we defined before, making sure only one word is presented at a time, in it's corresponding place from top to bottom
            temp = event.getKeys(keyList=keys)
            win.flip()  
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
              
            line='\t'.join(string) + '\n'
            resultsFile.write(line)
            resultsFile.flush()

        
        win.flip()
        core.wait(1)
        for rep in range(1,4):
            hitBoundary = False
            wordInd=0 # index of word within trial (first word, second...)
            while True:
                draw4()
                pacer.draw()
                pacer.pos -= (0,interStepInterval)
                win.flip()                    
                for p in pacerLocs.values():# check if the pacer contains the locations of our words
                    if pacer.contains(p): # if it does, 'curPacer' is which template that is [w1,w2...]
                        curPacer = pacerLocs.keys()[pacerLocs.values().index(p)]                  
                        if hitBoundary == False: # it's the first instance of "contains", just got to the border
                            start = time.clock() #  if so, RT calculation should begin
                            hitBoundary = True
                            #### hit next template - what is it and which keys do we expect? ####                            
                            curWord = trial[curPacer] # define the word we're looking for (e.g., 'w1' --> 'teeb')
                            for i in transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                                curWord = curWord.replace(i, transKeys[i])                                                    
                            
#                            wordInd += 1
#                            pressedKeys = [] # keys that subject pressed
#                            accKeys = [] # accurate presses
#                            pressedWord = [] # translates key presses into corresponding word
#                            pressedUnits = [] # not important
#                            add = [] # keys pressed that were not in word
#                            miss = [] # keys not pressed
#                            RT = 'NA' # reaction time, to be defined later            
#                            expKeys = [capKeys[curWord[0]], capKeys[curWord[1:]]] # define correct answer keys per word
#                            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
#                                expKeys.append('3') # this is hard coded, see if there's a better way...
#                            if curWord[0] == 'R':
#                                expKeys.append('1')
#                            expKeys = sorted(expKeys, key = lambda x:  srtMap[x])
#                            pacerTime=core.Clock()
#                            reactionTime=core.Clock()
#                            start = time.clock()
#                            react = False
#                            
#                            while pacer.contains(p): # change this - should be while p contained in....
#                                if len(pressedKeys) < len(expKeys):
#                                    getKeys = event.getKeys(keyList=keys)
#                                    if len(getKeys) != 0:
#                                        if react == False:
#                                            end = time.clock()
#                                            RT = (end - start) * 1000
#                                            react = True
#                                    pressedKeys.extend(getKeys)    
#                                else:
#                                    break
#                            event.clearEvents()
#                            if react == False:
#                                RT = 'NA'
#                            
#                            # exits the while pacer.contains(p) loop and sorts out the info:
#                            
#                            pressedKeys = (sorted(set(pressedKeys), key = lambda x:  srtMap[x]))
#                            pressedKeys ="".join(pressedKeys)              
#                            for i in pressedKeys: # translating keys into word
#                                pressedUnit = [unit for unit, value in capKeys.iteritems() if value == i]
#                                pressedUnits.append(pressedUnit)
#                                pressedWord = pressedWord + pressedUnit
#                            pressedWord = sorted(pressedWord, key = lambda x:  srtWord[x])
#                            pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
#                            if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
#                                pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
#                                
#                            # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
#                            # will appear as strings):               
#                            add = set(pressedKeys) - set(expKeys) # key additions
#                            add = "".join(sorted(add, key = lambda x:  srtMap[x])) # sort them by keyboard space
#                            miss = set(expKeys) - set(pressedKeys) # key omissions
#                            miss = "".join(sorted(miss, key = lambda x:  srtMap[x])) # sort them by keyboard space
#                            accKeys = "".join([x for x in pressedKeys if x in expKeys])                    
#                            expKeys = "".join(expKeys)
#                            Acc = 1 if expKeys==pressedKeys else 0
#                            string=[str(var) for var in trialNum, trial['type'], trial['ID'], 
#                                    rep, wordInd, curWord, pressedWord, 
#                                    expKeys, pressedKeys, Acc, RT,  
#                                    len(accKeys), accKeys, add, miss]              
#                            print string               
#                            line='\t'.join(string) + '\n'
#                            resultsFile.write(line)
#                            resultsFile.flush()
#                            getKeys = []
#                            
                            
                if  pacer.pos[1] <= -400:
                    pacer.setPos(startPos)
              
                if event.getKeys(['space']):
                    break


                                   
        
        fixationCross.draw()
        win.flip()
        core.wait(.5)
        if int(breakTime.getTime())>timeBreak:
            breakClick=False
            while not breakClick:
                breakText.draw()
                win.flip()
                stop= event.waitKeys(['c','q'])
                if stop==['c']:
                    breakTime.reset()
                    breakClick=True
                elif stop==['q']:
                    win.close()
                    core.quit()

    endText.draw()
    resultsFile.close()
    win.flip()
    core.wait(5)
    win.close()
win.close()
core.quit()
