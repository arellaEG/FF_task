# -*- coding: utf-8 -*-
"""
Created on Mon Aug 06 12:23:19 2018

@author: Arella Gussow
"""

import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui
import time

### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length
units=['t','R','v','L','eb','xb','ig','ug']
onsets=['t','R','v','L']
rhymes=['eb','xb','ig','ug']
#define keys to be used and corresponding phonemes from stim creation
capKeys = {'t':'1','R':'2','v':'3','L':'4',
          'eb':'7','xb':'8','ig':'9', 'ug':'0'}


keys=capKeys.values()
pacerTempo = 1
 # order by keyboard layout:
srtMap = {key: i for i, key in enumerate(['1', '2', '3', '4', '7','8', '9', '0'])}
srtWord= {key: i for i, key in enumerate(units)}
##still under old version
#hand = {'t':'Right','d':'Right','b':'Right',
#                   'p':'Right','k':'Left','g':'Left',
#                   'c':'Left','j':'Left',
#                   'e':'Left','i':'Right',
#                   'u':'Left','y':'Right'}


#finger = {'T':'ring','D':'ring','S':'mid',
#                   'Z':'mid','K':'mid', 'G': 'mid',
#                   'F':'ring','V':'ring',
#                   'A':'ind','E':'ind',
#                   'I':'ind','i':'ind'}


##running from pre-saved pics
win = visual.Window([800, 500], fullscr=True,
                        color="white", units='pix')
breakText=visual.TextStim(win=win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='black')
endText=visual.TextStim(win=win, height=40,
                 text="All Done! Please call the experimenter.",
                 color='black')

pacer= visual.Circle(win=win, radius = 20, fillColor='blue') # blue dot that marks which word should be pressed
fixationView = visual.Circle(win=win, radius = 40, fillColor='red', pos=(-565,310)) # red circle for viewing time



fixationCross= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0), 
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey')

pic1 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,300), size=(1200,280))
pic2 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,100), size=(1200,280))
pic3 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-100), size=(1200,280))
pic4 = visual.ImageStim(win=win, mask=None,interpolate=True,pos=(0,-300), size=(1200,280))



sep=','
import io
def importTrials(numTrials):
    bTrial= open ('trials_TTwb.csv', 'rb') 
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


def draw4():   
        pic1.draw()
        pic2.draw()
        pic3.draw()
        pic4.draw()
    
# define expected keys per word

     
with open('subject'+'_TTwb.csv','wb') as resultsFile:
    Rwriter=csv.DictWriter(resultsFile, fieldnames=headers)
    Rwriter.writeheader()
    core.wait(2)
    breakTime=core.Clock()
    trialNum=0   
    for trial in trialsList:
        trialNum+=1
        fixationCross.draw()
        win.flip()
        core.wait(1)
        pic1.setImage('stimShots_bw/'+trial['w1']+'_wb.png')            
        pic2.setImage('stimShots_bw/'+trial['w2']+'_wb.png')           
        pic3.setImage('stimShots_bw/'+trial['w3']+'_wb.png')
        pic4.setImage('stimShots_bw/'+trial['w4']+'_wb.png')
        # big red circle disappears, nothing on screen for 1 sec ;
        # then small blue circle appears and participants must begin              

        
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
            if wordInd == 1:
                pic1.draw()
            elif wordInd == 2:
                pic2.draw()
            elif wordInd == 3:
                pic3.draw()
            else:
                pic4.draw()
            win.flip()     
            RT = 'NA'
            # getting responses and reaction time:
            getKeys = event.waitKeys(keyList=keys)
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
            string=[str(var) for var in trialNum, trial['type'], trial['ID'], 
                    rep, wordInd, curWord, pressedWord, 
                    expKeys, pressedKeys, Acc, RT,  
                    len(accKeys), accKeys, add, miss]              
            print string               
            line='\t'.join(string) + '\n'
            resultsFile.write(line)
            resultsFile.flush()
            pacer.pos -=(0,200)
            getKeys = []                  

        win.flip()
        core.wait(3)
        draw4()
        fixationView.draw() # fixation to allow brief viewing - 2 sec of big red circle
        win.flip()
        core.wait(2)
        draw4()
        win.flip() 
        for rep in range(1,4):
            wordInd=0 # index of word within triak (first word, second...)
            draw4()
            pacer.pos = (-550,300)
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
                pacerTime=core.Clock()      
                start = time.clock()
                react = False
                event.clearEvents()
                # getting responses and reaction time:
                while pacerTime.getTime()< pacerTempo:
                    if len(pressedKeys) < len(expKeys):
                        getKeys = event.getKeys(keyList=keys)
                        if len(getKeys) != 0:
                            #react = True
                            if react == False:
                                end = time.clock()
                                RT = (end - start) * 1000
                                print RT
                                react = True
                        pressedKeys.extend(getKeys)    
                    else:
                        print pressedKeys
                        break
                event.clearEvents()
                if react == False:
                    RT = 'NA'

                core.wait(pacerTempo-(pacerTime.getTime())) # wait full time even if participant answered before time's up
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
                string=[str(var) for var in trialNum, trial['type'], trial['ID'], 
                        rep, wordInd, curWord, pressedWord, 
                        expKeys, pressedKeys, Acc, RT,  
                        len(accKeys), accKeys, add, miss]              
                print string               
                line='\t'.join(string) + '\n'
                resultsFile.write(line)
                resultsFile.flush()
                pacer.pos -=(0,200)
                getKeys = []                                   
        fixationCross.draw()
        win.flip()
        core.wait(.5)
        if int(breakTime.getTime())>10:
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
