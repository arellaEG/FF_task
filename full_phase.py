# -*- coding: utf-8 -*-
"""
Created on Thu Dec  27 01:34:46 2018

@author: Yuzhe
"""
class Action(object):
    
    #initialize all variables
    def __init__ (self):
        
        ###########develop################
        self.develop = False
        self.ifFam = True
        self.ifOne = True
        self.ifTwo = True
        self.ifThree = True
        self.ifFour = True
        ##################################
        ########fill in subject ID #######
        ##################################
        
        self.subject ='999'
        
        ##################################
        
        ######### timers  ################
        
        self.interStepInterval = 1.4 # speed for practice trials until criterion met ~1.2s = 1.4 iSI.
        # speed for test phase will be ~1s per word, which is an iSI of 1.65
        
        self.crit = .85 # criterion for passing practice phase
        
        self.timeBreak = 80 # every how often they get break screen (will wait till trial ends)
        
        ##################################
        ######## interval time limit ####
        ## Naturally, there will be slight differences in the timing of each key-press
        ## within a word (even though they're supposed to press them all together). This
        ## intervalTime limit determines how much of an interval we're willing to accept.
        ## if they wait too long between keys in the practice + feedback stage,
        ## they will get a message saying they have to press all keys at once.
        self.intervalTime = 1  
        
        ##################################
        ### R = tr, L = sl, x = ee. changed to keep all words 3 characters.
        self.units=['k','R','s','L','eb','Xb','ig','Ug']
        self.onsets=['k','R','s','L']
        self.rhymes=['eb','Xb','ig','Ug']
        #define keys to be used and corresponding sounds
        self.capKeys = {'k':'1','R':'2','s':'3','L':'4',
                  'eb':'7','Xb':'8','ig':'9', 'Ug':'0'}
        self.keys=self.capKeys.values()
        self.leftKeys=["1", "2", "3", "4"]
        self.rightKeys=["7", "8", "9", "0"]
        #### map that sort responses based on keyboard layout - so [0,1,9] would turn into [1,9,0] ####
        self.srtMap = {key: i for i, key in enumerate(['1', '2', '3', '4', '7','8', '9', '0'])}
        self.srtWord= {key: i for i, key in enumerate(self.units)} # the same but for letters, translating keys into corresponding sounds - not important 
        
        # dictionary of translations from 3-letter code to full word
        # we have words like "treeb", "slig", "teb" - all different lengths. To keep them equal length
        # within our code, we use the following letters as substitutes. To remember it's 
        # not the real letter, I used upper case.
        self.transKeys = {'kr':'R','sl':'L','oo':'U','ee':'X'}
        
    #start the action part
    def start(self):
        from psychopy import visual, core
        self.createTrials()
        self.setSubject()
        self.win = visual.Window([800, 500], fullscr=True,
                        color="black", units='pix')
        self.endText=visual.TextStim(win=self.win, height=40,
                         text="Practice phase completed!\n\nFinally, we can move on to the\
                         task itself. It is exactly the same as what you've been doing,\
                         except this time there will be no feedback.\n\nDo your best!",
                         color='black')
        
        self.wrongText=visual.TextStim(win=self.win, height=40, 
                         text="Look at the template again and give it another try.",
                         color='black') # for when they make a mistake and have to press again
        
        self.wrongTextb=visual.TextStim(win=self.win, height=40,
                         text="Try to be a little faster.",
                         color='black') # for when they dont press all keys at the same time
        
        # when they make a mistake in stage 2, a red X appears on the bottom right
        self.wrongX = visual.ShapeStim(win = self.win, pos = (450,-150), vertices=((0, -60), (0, 60), (0,0), 
                                                       (60,0), (-60, 0)), ori = 45,
                                                lineWidth=5, closeShape=False, 
                                                lineColor='red')
        
        self.fixationCross= visual.ShapeStim(win = self.win, vertices=((0, -70), (0, 70), (0,0), 
                                                       (70,0), (-70, 0)),
                                                lineWidth=5, closeShape=False, 
                                                lineColor='grey') # fixation cross at the beginning of each trial
        
        self.pic1 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,155), size=(1000,50))
        self.pic2 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,50), size=(1000,50))
        self.pic3 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,-55), size=(1000,50))
        self.pic4 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,-160), size=(1000,50))
        
        self.pictures = {1:self.pic1, 2:self.pic2, 3:self.pic3, 4:self.pic4}
        
        # picture in the center for the initial phase where they practice each word separately
        self.centerPic = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,0), size=(1000,50))
         
        #####################################
        #### text stimuli - instructions ####
        #####################################
        
        # general instructions object, nothing written on it - needs
        # to be set with the numbered instructions that follow:
        self.instruct = visual.TextStim(win=self.win, height=27, 
                         color='black', wrapWidth = 1000, pos = (0,85), alignHoriz='center', 
                         alignVert='center')
        
        # intructions for the first part
        self.instruct1 = "In this task you will see a template of 8 small boxes on the screen,\
        corresponding to the 8 keys you have your fingers on:"
        
        
        # appears on the same screen as the previous, but on the bottom
        self.instruct1b =  visual.TextStim(win=self.win, height=27, 
                                    text ="Your job is to press only the keys of the boxes colored in black.\
                                    First press the keys on the left side (left hand only), and then the right.\
                                    be as quick and accurate as you can!\
                                    \n\n\tPress 'c' to begin.",
                         color='black', wrapWidth = 1000, pos = (0,-125), alignHoriz='center', 
                         alignVert='center')
        
        
        self.instruct1c = "Great, looks like you're starting to get the hang of it.\
        \n\nFrom now on, if you don't press the correct keys\
         you will see a red X on the bottom right of the screen. Let's try to avoid that!"
        
        
        # different instructions that can be set for the general "instruct" object
        self.instruct2 = "Nice work!\nNow we can begin with full practice trials.\n\nEvery trial\
         consists of four templates. First you will have them appear one at a time\
         like you just practiced.\nThen, all 4 templates will appear on the\
         screen at once. Your task is to press the correct keys for each\
         template in order, from top to bottom. You will repeat the\
         whole sequence 3 times."
         
        self.instruct2b = "A rectangle will scroll down from the top of\
         the screen, indicating when you should press each template.\
         You can press the keys from the first moment the rectangle touches\
         the template, even if it's only partially overlapping.\
         Remember - for each template you first press the keys on the left side,\
         and then those on the right.\
         Make sure to keep up with the rectangle's speed!\n\nOnce you reach a high\
         level of accuracy, the practice phase will end and we can move\
         on to the task itself."
         

        # message to appear if they're 65 - 84% accurate:
        self.accNotMet = "Let's practice some more to get you really good. Do your best!" 
         
         
        self.phaseComplete = "First Phase Completed!\n\n Now we can finally get\
            to the task itself. No special instructions this time - it's\
            exactly what you've been doing until now, just keep it up and\
            do your best. \n\nGood luck!"
        
        # for participants to press 'c' when they've read instructions on that page
        # and are ready to continue:
        self.cToBegin =  visual.TextStim(win=self.win, height=35, 
                                    text ="\n\n\tPress 'c' to continue.",
                         color='black', wrapWidth = 1000, pos = (0,-120), alignHoriz='center', 
                         alignVert='center')
        
        # column names for our results file
        
        self.header=["subject", "trialNum", "trialType", "itemID", "rep", "wordInd", "curWord", 
                                "expKeys", "pressedKeys", 
                                "err", "RT", "countCorrect", "correctKeys", 
                                "addedKeys", "missingKeys","accRate", "errRate", "expOnset", "pressedOnset", "onsetAcc", "expRhyme", "pressedRhyme", "rhymeAcc", "conCluster", "stage", "key1", "stamp1", "key2", "stamp2", "key3", "stamp3"]
        self.headers = '\t'.join(self.header) + '\n'
        #headers="subject\ttrialNum\ttrialType\titemID\trep\twordInd\tcurWord\texpKeys\tpressedKeys\tacc\tRT\tcountCorrect\tcorrectKeys\taddedKeys\tmissingKeys\taccRate\tstage\n"
        
        #################################################################
        ############ PACER SETTINGS - SCROLLING RECTANGLE ###############
        #################################################################
        
        self.pacer = visual.Rect(win=self.win,size=(1700,100),lineColor="black", pos = ([0,250]))
        self.background = visual.Rect(win=self.win, size = (2250, 900), fillColor = 'white', pos = ([0,0]))
        self.pacerLocs = {'w1':[0,300], 'w2':[0,100], 'w3':[0,-100], 'w4':[0,-300]}
        self.pacerLoc = {1:'w1', 2:'w2', 3:'w3', 4:'w4'}
        self.startPos = [0,250]
        
        self.fixationCross= visual.ShapeStim(win = self.win, vertices=((0, -80), (0, 80), (0,0), 
                                                       (80,0), (-80, 0)),
                                                lineWidth=5, closeShape=False, 
                                                lineColor='grey')
        if self.ifFam:
            self.famPhase()
        self.testPhase()
        self.win.close()
        core.quit()
        
  
    #import trials method
    def importTrials(self, numTrials):
        import csv
        sep=','
        bTrial= open ('TTstim.csv', 'rb') 
        colNames = bTrial.next().rstrip().split(sep)
        reader=csv.DictReader(bTrial)
        self.trialsList = []
        for t in range(numTrials):
            trialStr=bTrial.next().rstrip().split(sep)
            assert len(trialStr) == len(colNames)
            trialDict = dict(zip(colNames, trialStr))
            self.trialsList.append(trialDict)

    def createTrials(self):
        import random
        self.importTrials(88)
        
        # dictionary of translations from 3-letter code to full word
        # we have words like "treeb", "slig", "teb" - all different lengths. To keep them equal length
        # within our code, we use the following letters as substitutes. To remember it's 
        # not the real letter, I used upper case.
        self.transKeys = {'kr':'R','sl':'L','oo':'U','ee':'X'}
        
        # translating the 'fullTrial' string from the stimuli list
        for trial in self.trialsList:
            for i in self.transKeys.keys():
                trial['fullTrial'] = trial['fullTrial'].replace(i, self.transKeys[i])
        
        # extract only "familiarization" stage trials from trialsList:
        self.famTrials = [x for x in self.trialsList if x['type'] == 'fam'] 
        random.shuffle(self.famTrials) 
        
        self.famTrials0 = random.sample(self.famTrials,4) # 4 random trials only self-paced
        self.famTrials1 = random.sample(self.famTrials,18) # 18  random trials for FULL practice:
        # first 3 with no accuracy monitoring, then 15 with monitoring to reach accuracy criterion
        
        
        self.firstTest = []
        indexNum = random.choice(range(len(self.famTrials)))
        self.firstTest.append(self.famTrials[indexNum])
        # define all other trials - to be used in the test phase
        self.trialsList = [x for x in self.trialsList if x['type'] <> 'fam'] 
        random.shuffle(self.trialsList) # random order of trials
        self.trialsList = self.firstTest + self.trialsList
        
        
        
        # getting all possible words in our experiment(instead of hard coding, go through
        # the trialsList and extract from there - useful in case we change specific words)
        self.allWords = []
        for i in self.trialsList:
            w1,w2,w3,w4 = i['fullTrial'].split()
            self.allWords.extend([w1,w2,w3,w4])
        self.allWords = list(set(self.allWords)) # reduce to only unique words, then make into list again
        random.shuffle(self.allWords)  # shuffle their order before using for practice


    def draw4(self):  # draws the 4 relevant pics
        self.background.draw()
        self.pic1.draw()
        self.pic2.draw()
        self.pic3.draw()
        self.pic4.draw()


    def set4(self, trial): # sets the 4 relevant pics
        self.pic1.setImage('stimShots_FF/'+trial['w1']+'_FF.png')            
        self.pic2.setImage('stimShots_FF/'+trial['w2']+'_FF.png')           
        self.pic3.setImage('stimShots_FF/'+trial['w3']+'_FF.png')
        self.pic4.setImage('stimShots_FF/'+trial['w4']+'_FF.png')


    def wordByWord(self): # defines which pic should appear in the one-by-one stage
        if self.wordInd == 1:
            self.pic1.draw()
        elif self.wordInd == 2:
            self.pic2.draw()
        elif self.wordInd == 3:
            self.pic3.draw()
        else:
            self.pic4.draw()


    def cClick (self, instructName): # displays instructions and waits for 'c' press - feed in instruction name (e.g., instruct1)
        from psychopy import event
        cClick = False
        while not cClick:
            self.instruct.setText (instructName)
            self.background.draw()
            self.instruct.draw()
            self.cToBegin.draw() 
            self.win.flip()
            if event.waitKeys (['c']) == ['c']:
                cClick = True

    def setSubject(self):
        from psychopy import gui
        dlg = gui.Dlg()
        dlg.addText("If you are not a developer, just click OK")
        dlg.addField("password")
        dlg.show()
        
        if dlg.data[0] == '19990506':
            self.develop = True
        else:
            self.develop = False
        
        if self.develop:
            dlg = gui.Dlg()
            dlg.addText("starting stage number")
            dlg.addField("")
            dlg.show()
            
            if dlg.data[0] == '2':
                self.ifOne = False
            elif dlg.data[0] == '3':
                self.ifOne = False
                self.ifTwo = False
            elif dlg.data[0] == '4':
                self.ifFam = False
                self.ifOne = False
                self.ifTwo = False
                self.ifThree = False

        dlg = gui.Dlg()
        dlg.addText("Enter the ID: ");
        dlg.addField("subject ID");
        dlg.show();
        
        if dlg.OK:
            self.subject = dlg.data[0]
        else:
            self.subject = '999'


    def compare(self, first, second):
        onset = ('1', '2', '3', '4')
        #rhyme = ('7', '8', '9', '0')
        bool1 = onset.__contains__(first)
        bool2 = onset.__contains__(second)
        return (bool1 == bool2)




    def split(self, actual):
        onset = ('1', '2', '3', '4')
        #rhyme = ('7', '8', '9', '0')
        pressOnset = 'NA'
        pressRhyme = 'NA'
        actualOnset = []
        actualRhyme = []
        if len(actual) == 0:
            return pressOnset, pressRhyme
        if len(actual) == 1:
            if onset.__contains__(actual[0]):
                actualOnset.append(actual[0])
            else:
                actualRhyme.append(actual[0])
        else:
            for i in range(len(actual)):
                if i == len(actual) - 1:
                    if onset.__contains__(actual[0]):
                        actualOnset.extend(actual)
                        #actualOnset = (sorted(set(actualOnset), key = lambda x:  self.srtMap[x]))
                    else:
                        actualRhyme.extend(actual)
                        #actualRhyme = (sorted(set(actualRhyme), key = lambda x:  self.srtMap[x]))
                    break
                first = actual[i]
                second = actual[i + 1]
                compared = self.compare(first, second)
                if not compared:
                    actualOnset = actual[0: i + 1]
                    actualRhyme = actual[i + 1:]
                    #actualOnset = (sorted(set(actualOnset), key = lambda x:  self.srtMap[x]))
                    #actualRhyme = (sorted(set(actualRhyme), key = lambda x:  self.srtMap[x]))
                    break
            if len(actualOnset) != 0:
                pressOnset = "".join(actualOnset)
            if len(actualRhyme) != 0:
                pressRhyme = "".join(actualRhyme)
            return pressOnset, pressRhyme
                    
                    
            
    
    
    #learn all the words
    def learn (self, curWord): # presents template to be pressed, if wrong - says so and returns to word
        from psychopy import visual, core, event
        import time
        while True:
            block = visual.Rect(win=self.win, size = (700, 200), fillColor = 'white', pos = ([200,50]))
            stage = 1
            RT = 'NA'
            pressedKeys = []
            accKeys=[]
            add = []
            miss = []
            actualKeys = []
            timeStamp = []
            expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                expKeys.append('3') # this is hard coded, see if there's a better way...
            if curWord[0] == 'R':
                expKeys.append('1')
            expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
            for i in self.transKeys.keys(): # return to full word
                curWord = curWord.replace(self.transKeys[i], i)      
            self.background.draw()
            self.fixationCross.draw()
            self.win.flip()
            core.wait(1)
            self.pic2.setImage('stimShots_FF/'+curWord+'_FF.png')
            self.background.draw()
            self.pic2.draw()
            block.draw()
            temp = event.getKeys(keyList=self.keys)
            self.win.flip()
            start = core.Clock()
            react = False
            interval = False
            end = 0
            
            intervalTime2 = 0.3
            
            #### getting responses ###
            
            while len(pressedKeys) < len(expKeys) - 1:
                if react:
                    intervalTimer = time.clock()
                    if (intervalTimer - end) > intervalTime2:
                        interval = True
                        break
                getKeys = event.getKeys(keyList=self.leftKeys)
                if len(getKeys) != 0: # if we haven't collected RTs yet 
                    if react == False:
                        end = time.clock()
                        RT = int(start.getTime() * 1000)  # check how much time passed since we started the RT clock
                        react = True
                    for i in range(len(getKeys)):
                        if i == 0:
                            timeStamp.append(int(start.getTime() * 1000))
                        else:
                            timeStamp.append(0)
                    start = core.Clock()
                actualKeys.extend(getKeys)
                pressedKeys.extend(getKeys)
            #print react
            if react and not interval:
                block.pos = [-200, 50]
                self.background.draw()
                self.pic2.draw()
                block.draw()
                temp = event.getKeys(keyList=self.keys)
                self.win.flip()
                while len(pressedKeys) < len(expKeys):
                    intervalTimer = time.clock()
                    if (intervalTimer - end) > self.intervalTime:
                        interval = True
                        break
                    getKeys = event.getKeys(keyList=self.rightKeys)
                    if len(getKeys) != 0:
                        for i in range(len(getKeys)):
                            if i == 0:
                                timeStamp.append(int(start.getTime() * 1000))
                            else:
                                timeStamp.append(0)
                        start = core.Clock()
                    actualKeys.extend(getKeys)
                    pressedKeys.extend(getKeys)
            #### changing response keys into easy-to-read + writing to results file ####   
            
            pressedKeys1 = pressedKeys[0: len(pressedKeys) - 1]
            pressedKeys2 = pressedKeys[len(pressedKeys) - 1: len(pressedKeys)]
            pressedKeys1 = (sorted(set(pressedKeys1), key = lambda x:  self.srtMap[x]))
            pressedKeys1.extend(pressedKeys2)
            pressedKeys = pressedKeys1
            pressedKeys ="".join(pressedKeys)              
            add = set(pressedKeys) - set(expKeys) # key additions
            add = "".join(sorted(add, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
            if len(add) == 0:
                add = 'NA'
            miss = set(expKeys) - set(pressedKeys) # key omissions
            miss = "".join(sorted(miss, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
            if len(miss) == 0:
                miss = 'NA'
            accKeys = "".join([x for x in pressedKeys if x in expKeys])
            if len(accKeys) == 0:
                accKeys = 'NA'                    
            expKeys = "".join(expKeys)
            Acc = 0 if expKeys==pressedKeys else 1 # accuracy is 1 if all and only correct keys were pressed
            
            pressedOnset, pressedRhyme = self.split(actualKeys)
            #print pressedOnset
            #print pressedRhyme
            
#            pressedOnset = "".join(x for x in pressedKeys if x in self.leftKeys)
#            if len(pressedOnset) == 0:
#                pressedOnset = 'NA'
            expOnset = expKeys[0: len(expKeys) - 1]
#            pressedRhyme = "".join(x for x in pressedKeys if x in self.rightKeys)
#            if len(pressedRhyme) == 0:
#                pressedRhyme = 'NA'
            expRhyme = expKeys[len(expKeys) - 1: len(expKeys)]
            onsetAcc = 1 if set(expOnset) == set(pressedOnset) else 0
            rhymeAcc = 1 if set(expRhyme) == set(pressedRhyme) else 0
            
            conCluster = 0
            if len(expOnset) == 2:
                conCluster = 1
            string=[str(var) for var in self.subject, 'trialNum', "trialType", "trialID",
                            "rep", "wordInd", curWord,
                            expKeys, pressedKeys, Acc, RT,  
                            len(accKeys), accKeys, add, miss, 'NA','NA', expOnset, pressedOnset, onsetAcc, expRhyme, pressedRhyme, rhymeAcc, conCluster,stage]      
            #print string
            stamps = ''
            index = 0
            for index in range(3 - len(actualKeys)):
                actualKeys.append('NA')
                timeStamp.append('NA')
            index = 0
            for index in range(len(actualKeys)):
                stamps += '\t' + str(actualKeys[index]) + '\t' + str(timeStamp[index])
            line='\t'.join(string) + stamps + '\n'
            print line
            self.resultsFile.write(line)
            self.resultsFile.flush()
            self.background.draw()
            if Acc == 1: # if accuracy is wrong, 
                if interval: # if it's because they didn't press at the same time
                    self.wrongTextb.draw() # tell them to press all at once
                else: # if they got it wrong for any other reason
                    self.wrongText.draw() # tell them to try again
                    
                self.win.flip()
                core.wait(2)
                for i in self.transKeys.keys(): # return to coded word
                    curWord = curWord.replace(i, self.transKeys[i])
                continue # go back to the beginning of this word and have them do it again.
            elif Acc == 0: # if accuracy is good,
                break # break loop and go on to next word
    
    
    def famPhase(self):
        from psychopy import visual, core, event
        import time
        with open(self.subject+'_fam'+'_FF.txt','wb') as self.resultsFile: # opens new results file in current directory
            #Rwriter=csv.DictWriter(resultsFile, fieldnames = headers)
            #Rwriter.writeheader()
            self.resultsFile.write(self.headers)
            self.resultsFile.flush()
            ccClick = False 
            self.breakTime=core.Clock()
            #### 1. start with word-by-word single presentation: ####
            while not ccClick: # present the following instruction screen (includes a pic as an example), until 'c' is pressed
                self.centerPic.setImage('stimShots_FF/'+'kreeb'+'_FF.png')
                self.background.draw()
                self.centerPic.draw()
                self.instruct.setText(self.instruct1) # using the general instruct object but setting it with instruct 1
                self.instruct.draw()
                self.instruct1b.draw() # (instruct 1b is separate from the general instruct object)
                self.win.flip()
                if event.waitKeys (['c']) == ['c']:
                    ccClick = True
            
            if self.ifOne:
                for curWord in self.allWords: # goes through each word and has them press it
                    self.learn (curWord)
                
                ###########################################################################
                ################## commented out for playing around #######################
                ###########################################################################
                
                # learn (curWord) # each word must be correctly pressed twice. 
                # for curWord in allWords: # after each word was pressed twice (one after the other), go back to the beginning of the list and go through all words - one correct press per word
                # learn (curWord) # after this, they've pressed each word correctly 3 times total 
                self.background.draw()
                self.fixationCross.draw()
                self.win.flip()
                core.wait(1)
            
            if self.ifTwo:
                self.cClick(self.instruct1c)
                for trial in self.famTrials0: # goes through the control trials of self-paced only practice
                    stage = 2 # what we defined as the self-paced stage
                    self.wordInd = 0 # keeps track of what word number we're at within the trial (1-4)
                    self.set4(trial) # sets the 4 images in place
                    for curWord in trial['fullTrial'].split(): # goes through each of the 4 words in the trial  
                        core.wait(0.1) 
                        self.wordInd += 1
                        pressedKeys = [] # keys that subject pressed
                        accKeys = [] # accurate presses
                        pressedWord = [] # translates key presses into corresponding word
                        pressedUnits = [] # not important (translates keys into corresponding sounds)
                        add = [] # keys pressed that were not in word
                        miss = [] # keys not pressed (but should have been)
                        actualKeys = []
                        timeStamp = []
                        RT = 'NA' # reaction time, to be defined later            
                        expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word, separated by onset vs rhyme
                        if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                            expKeys.append('3') # this is hard coded, see if there's a better way...
                        if curWord[0] == 'R':
                            expKeys.append('1')
                        expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                        self.background.draw()
                        self.wordByWord() # draw the correct word based on index (1,2,3,4) 
                        temp = event.getKeys(keyList=self.keys)
                        self.win.flip()     
                        
                        # getting responses and reaction time - first zero all variables
                        RT = 'NA'
                        start = core.Clock()
                        react = False
                        #### getting responses ####
                    
                        while len(pressedKeys) < len(expKeys):
                            getKeys = event.getKeys(keyList=self.keys)
                            if len(getKeys) != 0: # if we haven't collected RTs yet
                                if react == False:
                                    RT = int(start.getTime() * 1000)  # check how much time passed since we started the RT clock
                                    react = True
                                for i in range(len(getKeys)):
                                    if i == 0:
                                        timeStamp.append(int(start.getTime() * 1000))
                                    else:
                                        timeStamp.append(0)
                                start = core.Clock()
                            actualKeys.extend(getKeys)
                            pressedKeys.extend(getKeys)  
                        pressedKeys1 = pressedKeys[0: len(pressedKeys) - 1]
                        pressedKeys2 = pressedKeys[len(pressedKeys) - 1: len(pressedKeys)]
                        pressedKeys1 = (sorted(set(pressedKeys1), key = lambda x:  self.srtMap[x]))
                        pressedKeys1.extend(pressedKeys2)
                        pressedKeys = pressedKeys1
                        pressedKeys ="".join(pressedKeys)              
                        # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                        # will appear as strings):               
                        add = set(pressedKeys) - set(expKeys) # key additions
                        add = "".join(sorted(add, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                        if len(add) == 0:
                            add = 'NA'
                        miss = set(expKeys) - set(pressedKeys) # key omissions
                        miss = "".join(sorted(miss, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                        if len(miss) == 0:
                            miss = 'NA'
                        accKeys = "".join([x for x in pressedKeys if x in expKeys])   
                        if len(accKeys) == 0:
                            accKeys = 'NA'
                        expKeys = "".join(expKeys)
                        Acc = 0 if expKeys==pressedKeys else 1
                        
                        pressedOnset, pressedRhyme = self.split(actualKeys)
                        #print pressedOnset
                        #print pressedRhyme
                        
#                        pressedOnset = "".join(x for x in pressedKeys if x in self.leftKeys)
#                        if len(pressedOnset) == 0:
#                            pressedOnset = 'NA'
                        expOnset = expKeys[0: len(expKeys) - 1]
#                        pressedRhyme = "".join(x for x in pressedKeys if x in self.rightKeys)
#                        if len(pressedRhyme) == 0:
#                            pressedRhyme = 'NA'
                        expRhyme = expKeys[len(expKeys) - 1: len(expKeys)]
                        onsetAcc = 1 if set(expOnset) == set(pressedOnset) else 0
                        rhymeAcc = 1 if set(expRhyme) == set(pressedRhyme) else 0
                        conCluster = 0
                        if len(expOnset) == 2:
                            conCluster = 1
                        string=[str(var) for var in self.subject, 'trialNum', trial['type'], trial['ID'], 
                                    "rep", self.wordInd, curWord,
                                    expKeys, pressedKeys, Acc, RT,  
                                    len(accKeys), accKeys, add, miss, 'NA', 'NA', expOnset, pressedOnset, onsetAcc, expRhyme, pressedRhyme, rhymeAcc, conCluster, stage]              
                        
                        stamps = ''
                        index = 0
                        for index in range(3 - len(actualKeys)):
                            actualKeys.append('NA')
                            timeStamp.append('NA')
                        index = 0
                        for index in range(len(actualKeys)):
                            stamps += '\t' + str(actualKeys[index]) + '\t' + str(timeStamp[index])
                        line='\t'.join(string) + stamps + '\n'
                        self.resultsFile.write(line)
                        self.resultsFile.flush()
                        if Acc == 1:
                            self.background.draw()
                            self.wrongX.draw()
                            self.win.flip()
                            core.wait(0.5)
                
           
            if self.ifThree:
                self.cClick (self.instruct2) # shows first instructions for next part and waits for 'c'
                self.cClick (self.instruct2b)
                
                ####### beginning full trial practice ########
                
                accCount= []
                trialNum = 0 # initiate trial number count
                go = True # initiate experiment flow. when go == false, familiarization phase will end. 
                          #  we will make go == false, only when 85% accuracy reached, and it is only 
                         # first checked after a minimum of 16 trials. 
                notMet = 0  # monitors how many additional trials they get after initial accuracy not met
                for trial in self.famTrials: # goes through the control trials they'll be practicing
                    stage = 3 # beginning the fullTrials
                    accRate = 'NA' # initialize accRate
                    if go:
                        self.background.draw()
                        self.fixationCross.draw()
                        self.win.flip()
                        core.wait(1)
                        self.set4(trial)
                        trialNum += 1
                        self.wordInd = 0 # index of word within trial (first word, second...)
                        rep = 0 # rep 0 means it's the word-by-word presentation at the beginnign
                        self.background.draw()
                        self.win.flip()
                        for curWord in trial['fullTrial'].split(): # goes through each word in current trial
                            core.wait(0.1)
                            self.wordInd += 1
                            # zeroing all variables:
                            RT = 'NA'
                            pressedKeys = [] # keys that subject pressed
                            accKeys = [] # accurate presses
                            pressedWord = [] # translates key presses into corresponding word
                            pressedUnits = [] # not important
                            add = [] # keys pressed that were not in word
                            miss = [] # keys not pressed      
                            actualKeys = []
                            timeStamp = []
                            expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
                            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                                expKeys.append('3') # this is hard coded, see if there's a better way...
                            if curWord[0] == 'R':
                                expKeys.append('1')
                            expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                            self.background.draw()
                            self.wordByWord() # function we defined before, making sure only one word is presented at a time, in it's corresponding place from top to bottom
                            temp = event.getKeys(keyList=self.keys)
                            self.win.flip()  
                            ##### getting responses and reaction time ####      
                            start = core.Clock()
                            react = False
                            
                            while len(pressedKeys) < len(expKeys):
                                getKeys = event.getKeys(keyList=self.keys)
                                if len(getKeys) != 0: # if we haven't collected RTs yet
                                    if react == False:
                                        RT = int(start.getTime() * 1000)  # check how much time passed since we started the RT clock
                                        react = True
                                    for i in range(len(getKeys)):
                                        if i == 0:
                                            timeStamp.append(int(start.getTime() * 1000))
                                        else:
                                            timeStamp.append(0)
                                    start = core.Clock()
                                actualKeys.extend(getKeys)
                                pressedKeys.extend(getKeys)  
                            event.clearEvents()
                            pressedKeys1 = pressedKeys[0: len(pressedKeys) - 1]
                            pressedKeys2 = pressedKeys[len(pressedKeys) - 1: len(pressedKeys)]
                            pressedKeys1 = (sorted(set(pressedKeys1), key = lambda x:  self.srtMap[x]))
                            pressedKeys1.extend(pressedKeys2)
                            pressedKeys = pressedKeys1
                            pressedKeys ="".join(pressedKeys)              
                            for i in pressedKeys: # translating keys into word, not important
                                pressedUnit = [self.unit for self.unit, value in self.capKeys.iteritems() if value == i]
                                pressedUnits.append(pressedUnit)
                                pressedWord = pressedWord + pressedUnit
                            pressedWord = sorted(pressedWord, key = lambda x:  self.srtWord[x])
                            pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
                            if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                                pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
                            # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                            # will appear as strings):               
                            add = set(pressedKeys) - set(expKeys) # key additions
                            add = "".join(sorted(add, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                            if len(add) == 0:
                                add = 'NA'
                            miss = set(expKeys) - set(pressedKeys) # key omissions
                            miss = "".join(sorted(miss, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                            if len(miss) == 0:
                                miss = 'NA'
                            accKeys = "".join([x for x in pressedKeys if x in expKeys]) 
                            if len(accKeys) == 0:
                                accKeys = 'NA'
                            expKeys = "".join(expKeys)
                            Acc = 0 if expKeys==pressedKeys else 1
                            
                            pressedOnset, pressedRhyme = self.split(actualKeys)
                            
#                            pressedOnset = "".join(x for x in pressedKeys if x in self.leftKeys)
#                            if len(pressedOnset) == 0:
#                                pressedOnset = 'NA'
                            expOnset = expKeys[0: len(expKeys) - 1]
#                            pressedRhyme = "".join(x for x in pressedKeys if x in self.rightKeys)
#                            if len(pressedRhyme) == 0:
#                                pressedRhyme = 'NA'
                            expRhyme = expKeys[len(expKeys) - 1: len(expKeys)]
                            onsetAcc = 1 if set(expOnset) == set(pressedOnset) else 0
                            rhymeAcc = 1 if set(expRhyme) == set(pressedRhyme) else 0
                            conCluster = 0
                            if len(expOnset) == 2:
                                conCluster = 1
                            string=[str(var) for var in self.subject, trialNum, trial['type'], trial['ID'],  # collect all the info we're interested in
                                    rep, self.wordInd, curWord, 
                                    expKeys, pressedKeys, Acc, RT,  
                                    len(accKeys), accKeys, add, miss, 'NA', 'NA', expOnset, pressedOnset, onsetAcc, expRhyme, pressedRhyme, rhymeAcc, conCluster, stage]              
                            print string 
                              
                            stamps = ''
                            index = 0
                            for index in range(3 - len(actualKeys)):
                                actualKeys.append('NA')
                                timeStamp.append('NA')
                            index = 0
                            for index in range(len(actualKeys)):
                                stamps += '\t' + str(actualKeys[index]) + '\t' + str(timeStamp[index])
                            line='\t'.join(string) + stamps + '\n'
                            self.resultsFile.write(line)
                            self.resultsFile.flush()
                            if Acc == 1:
                                self.background.draw()
                                self.wrongX.draw()
                                self.win.flip()
                                core.wait(0.3)
                
                        self.background.draw()
                        self.win.flip()
                        core.wait(1)
                        self.pacer.setPos (self.startPos)
                        for rep in range(1,4):
                            hitBoundary = False
                            self.wordInd=1 # index of word within trial (first word, second...)
                            pressedKeys = [] # keys that subject pressed
                            accKeys = [] # accurate presses
                            pressedWord = [] # translates key presses into corresponding word
                            pressedUnits = [] # not important
                            add = [] # keys pressed that were not in word
                            miss = [] # keys not pressed
                            actualKeys = []
                            timeStamp = []
                            RT = 'NA' # reaction time, to be defined later     
                            curWord = trial[self.pacerLoc[self.wordInd]]
                            for i in self.transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                                curWord = curWord.replace(i, self.transKeys[i])
                            expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
                            if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                                expKeys.append('3') # this is hard coded, see if there's a better way...
                            if curWord[0] == 'R':
                                expKeys.append('1')
                            expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                            react = False
                            temp = event.getKeys(keyList=self.keys)
                            self.pacer2 = visual.Rect(win=self.win,size=(1700,100),lineColor="black", pos = ([0,685]))
                            while True:
                                self.draw4()
                                if Acc == 1: # keep the red x up as long as accuracy equals 0
                                    self.wrongX.draw()
                                if self.wordInd < 5:
                                    self.pacer.draw()
                                if self.wordInd < 4:
                                    self.pacer2.draw()
                                self.pacer2.pos = (0,435 + self.pacer.pos[1])
                                self.pacer.pos -= (0,self.interStepInterval)
                                self.win.flip()
                                if  self.pacer.pos[1] <= -220:
                                    self.pacer = self.pacer2
                                    break
                                if self.wordInd >=5:
                                    continue
                                if self.pictures[self.wordInd].overlaps(self.pacer):
                                    if hitBoundary == False:
                                        temp = event.getKeys(keyList=self.keys)
                                        Acc = 'NA'
                                        hitBoundary = True
                                        start = core.Clock()
                                    if len(pressedKeys) < len(expKeys):
                                        getKeys = event.getKeys(keyList=self.keys)
                                        if len(getKeys) != 0:
                                            if react == False:
                                                RT = int(start.getTime() * 1000)
                                                react = True
                                            for i in range(len(getKeys)):
                                                if i == 0:
                                                    timeStamp.append(int(start.getTime() * 1000))
                                                else:
                                                    timeStamp.append(0)
                                            start = core.Clock()
                                        actualKeys.extend(getKeys)
                                        pressedKeys.extend(getKeys)            
                                else:
                                    if hitBoundary:
                                        event.clearEvents()
                                        temp = event.getKeys(keyList=self.keys)
                                        #print start.getTime()
                                        pressedKeys1 = pressedKeys[0: len(pressedKeys) - 1]
                                        pressedKeys2 = pressedKeys[len(pressedKeys) - 1: len(pressedKeys)]
                                        pressedKeys1 = (sorted(set(pressedKeys1), key = lambda x:  self.srtMap[x]))
                                        pressedKeys1.extend(pressedKeys2)
                                        pressedKeys = pressedKeys1
                                        pressedKeys ="".join(pressedKeys)              
                                        for i in pressedKeys: # translating keys into word, not important
                                            pressedUnit = [self.unit for self.unit, value in self.capKeys.iteritems() if value == i]
                                            pressedUnits.append(pressedUnit)
                                            pressedWord = pressedWord + pressedUnit
                                        pressedWord = sorted(pressedWord, key = lambda x:  self.srtWord[x])
                                        pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
                                        if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                                            pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
                
                                        # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                                        # will appear as strings):               
                                        add = set(pressedKeys) - set(expKeys) # key additions
                                        add = "".join(sorted(add, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                                        if len(add) == 0:
                                            add = 'NA'
                                        miss = set(expKeys) - set(pressedKeys) # key omissions
                                        miss = "".join(sorted(miss, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                                        if len(miss) == 0:
                                            miss = 'NA'
                                        accKeys = "".join([x for x in pressedKeys if x in expKeys])  
                                        if len(accKeys) == 0:
                                            accKeys = 'NA'
                                        expKeys = "".join(expKeys)
                                        Acc = 0 if expKeys==pressedKeys else 1
                                        
                                        pressedOnset, pressedRhyme = self.split(actualKeys)
                                        
#                                        pressedOnset = "".join(x for x in pressedKeys if x in self.leftKeys)
#                                        if len(pressedOnset) == 0:
#                                            pressedOnset = 'NA'
                                        expOnset = expKeys[0: len(expKeys) - 1]
#                                        pressedRhyme = "".join(x for x in pressedKeys if x in self.rightKeys)
#                                        if len(pressedRhyme) == 0:
#                                            pressedRhyme = 'NA'
                                        expRhyme = expKeys[len(expKeys) - 1: len(expKeys)]
                                        onsetAcc = 1 if set(expOnset) == set(pressedOnset) else 0
                                        rhymeAcc = 1 if set(expRhyme) == set(pressedRhyme) else 0
                                        conCluster = 0
                                        if len(expOnset) == 2:
                                            conCluster = 1
                                        if trialNum > 3: # only start counting accuracy after first 3 trials
                                            accCount.append(Acc)
                                            if len(accCount) > 120:
                                                accCount = accCount[1: len(accCount)]
                                            accRate = 1- round((float(sum(accCount))/len(accCount)), 2)
                                        if accRate == 'NA':
                                            errRate = 'NA'
                                        else:
                                            errRate = 1.0 - float(accRate)
                                        string=[str(var) for var in self.subject, trialNum, trial['type'], trial['ID'],  # collect all the info we're interested in
                                                                                  rep, self.wordInd, curWord, 
                                                                                  expKeys, pressedKeys, Acc, RT,  
                                                                                  len(accKeys), accKeys, add, miss, accRate, errRate, expOnset, pressedOnset, onsetAcc, expRhyme, pressedRhyme, rhymeAcc, conCluster, stage]              
                                        print string
                                        #print actualKeys
                                        #print timeStamp
                                        stamps = ''
                                        index = 0
                                        for index in range(3 - len(actualKeys)):
                                            actualKeys.append('NA')
                                            timeStamp.append('NA')
                                        index = 0
                                        for index in range(len(actualKeys)):
                                            stamps += '\t' + str(actualKeys[index]) + '\t' + str(timeStamp[index])
                                        line='\t'.join(string) + stamps + '\n'
                                        
                                        self.resultsFile.write(line)
                                        self.resultsFile.flush()
                                        hitBoundary = False
                                        
                                        self.wordInd+=1 # index of word within trial (first word, second...)
                                        pressedKeys = [] # keys that subject pressed
                                        accKeys = [] # accurate presses
                                        pressedWord = [] # translates key presses into corresponding word
                                        pressedUnits = [] # not important
                                        add = [] # keys pressed that were not in word
                                        miss = [] # keys not pressed
                                        actualKeys = []
                                        timeStamp = []
                                        RT = 'NA' # reaction time, to be defined later     
                                        if self.wordInd < 5:
                                            curWord = trial[self.pacerLoc[self.wordInd]]
                                        for i in self.transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                                            curWord = curWord.replace(i, self.transKeys[i])
                                        expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
                                        if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                                            expKeys.append('3') # this is hard coded, see if there's a better way...
                                        if curWord[0] == 'R':
                                            expKeys.append('1')
                                        expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                                        react = False
                                        temp = event.getKeys(keyList=self.keys)
                    self.background.draw()
                    self.fixationCross.draw()
                    self.win.flip()
                    core.wait(.5)
                    if trialNum >= 18:
                        if accRate <= .15:                
                            go = False
                        else:
                            if notMet%5 ==0: # only present the following message every five trials
                                self.cClick (self.accNotMet) # message saying they're doing well but need more practice.
                                notMet+=1         # only appears if they're under 85%, and then they will 
                                                # get more trials one-by-one until they reach 85%.
            
                     ##### finished - close results file and present screen 
                     #### saying phase 1 complete. 
                     #("else" is of the "if" statement from line 459, "if go:", when beginning trial flow)           
                else:  
                    self.resultsFile.close()       
                    self.background.draw()
                    self.cClick(self.phaseComplete)
                    self.win.flip()
                
                
        self.background.draw()
        self.win.flip()
    
    
    def testPhase(self):
        from psychopy import visual, core, event
        
        ################################################
        self.interStepInterval = 1.8 ###########
        
        self.pacer = visual.Rect(win=self.win,size=(1700,100),lineColor="black", pos = ([0,250]))
        
        self.breakText=visual.TextStim(win=self.win, height=40,
                         text="Please take a short break. Press 'c' to continue.",
                         color='black')
        self.finalText=visual.TextStim(win=self.win, height=40,
                         text="All Done! Please call the experimenter.",
                         color='black')
        
        
        
        
        self.fixationCross= visual.ShapeStim(win = self.win, vertices=((0, -70), (0, 70), (0,0), 
                                                       (70,0), (-70, 0)),
                                                lineWidth=5, closeShape=False, 
                                                lineColor='grey')
        
        self.pic1 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,155), size=(1000,50))
        self.pic2 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,50), size=(1000,50))
        self.pic3 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,-55), size=(1000,50))
        self.pic4 = visual.ImageStim(win=self.win, mask=None,interpolate=True,pos=(0,-160), size=(1000,50))
        
        
        self.header=["subject", "trialNum", "trialType", "itemID", "rep", "wordInd", "curWord", 
                                "expKeys", "pressedKeys", 
                                "err", "RT", "countCorrect", "correctKeys", 
                                "addedKeys", "missingKeys", 'accRate', 'errRate', 'expOnset', 'pressedOnset', 'onsetAcc', 'expRhyme', 'pressedRhyme', 'rhymeAcc', 'conCluster', 'key1', 'stamp1', 'key2', 'stamp2', 'key3', 'stamp3']
        self.headers = '\t'.join(self.header) + '\n'
        #headers="subject\ttrialNum\ttrialType\titemID\trep\twordInd\tcurWord\texpKeys\tpressedKeys\tacc\tRT\tcountCorrect\tcorrectKeys\taddedKeys\tmissingKeys\taccRate\n"
        
            
        # define expected keys per word
        
             
        with open(self.subject + '_TTwb.txt','wb') as self.resultsFile:
            self.resultsFile.write(self.headers)
            self.resultsFile.flush()
            core.wait(2)
            breakTime=core.Clock()
            trialNum=0
            for trial in self.trialsList:
                trialNum+=1
                self.background.draw()
                self.fixationCross.draw()
                self.win.flip()
                core.wait(1)
                self.set4(trial)
                # big red circle disappears, nothing on screen for 1 sec ;
                # then small blue circle appears and participants must begin              
        
                self.background.draw()
                self.wordInd=0 # index of word within triak (first word, second...)
                rep = 0
                accCount = []
                self.win.flip()
                for curWord in trial['fullTrial'].split():
                    core.wait(0.1)
                    self.wordInd += 1
                    accRate = 'NA'
                    pressedKeys = [] # keys that subject pressed
                    accKeys = [] # accurate presses
                    pressedWord = [] # translates key presses into corresponding word
                    pressedUnits = [] # not important
                    add = [] # keys pressed that were not in word
                    miss = [] # keys not pressed
                    actualKeys = []
                    timeStamp = []
                    RT = 'NA' # reaction time, to be defined later            
                    expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
                    if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                        expKeys.append('3') # this is hard coded, see if there's a better way...
                    if curWord[0] == 'R':
                        expKeys.append('1')
                    expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                    self.background.draw()
                    if self.wordInd == 1:
                        self.pic1.draw()
                    elif self.wordInd == 2:
                        self.pic2.draw()
                    elif self.wordInd == 3:
                        self.pic3.draw()
                    else:
                        self.pic4.draw()
                    temp = event.getKeys(keyList=self.keys)
                    self.win.flip()     
                    RT = 'NA'
                    # getting responses and reaction time:
                    
                    start = core.Clock()
                    react = False
                    #### getting responses ####
                
                    while len(pressedKeys) < len(expKeys):
                        getKeys = event.getKeys(keyList=self.keys)
                        if len(getKeys) != 0: # if we haven't collected RTs yet
                            if react == False:  
                                RT = int(start.getTime() * 1000)  # check how much time passed since we started the RT clock
                                react = True
                            for i in range(len(getKeys)):
                                if i == 0:
                                    timeStamp.append(int(start.getTime() * 1000))
                                else:
                                    timeStamp.append(0)
                            start = core.Clock()
                        actualKeys.extend(getKeys)
                        pressedKeys.extend(getKeys)    
                    event.clearEvents()
                    pressedKeys1 = pressedKeys[0: len(pressedKeys) - 1]
                    pressedKeys2 = pressedKeys[len(pressedKeys) - 1: len(pressedKeys)]
                    pressedKeys1 = (sorted(set(pressedKeys1), key = lambda x:  self.srtMap[x]))
                    pressedKeys1.extend(pressedKeys2)
                    pressedKeys = pressedKeys1
                    pressedKeys ="".join(pressedKeys)              
                    for i in pressedKeys: # translating keys into word
                        pressedUnit = [self.unit for self.unit, value in self.capKeys.iteritems() if value == i]
                        pressedUnits.append(pressedUnit)
                        pressedWord = pressedWord + pressedUnit
                    pressedWord = sorted(pressedWord, key = lambda x:  self.srtWord[x])
                    pressedWord = "".join(pressedWord) # gives back the equivalent word of key presses
                    if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                        pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
        
                    # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                    # will appear as strings):               
                    add = set(pressedKeys) - set(expKeys) # key additions
                    add = "".join(sorted(add, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                    if len(add) == 0:
                        add = 'NA'
                    miss = set(expKeys) - set(pressedKeys) # key omissions
                    miss = "".join(sorted(miss, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                    if len(miss) == 0:
                        miss = 'NA'
                    accKeys = "".join([x for x in pressedKeys if x in expKeys])      
                    if len(accKeys) == 0:
                        accKeys = 'NA'
                    expKeys = "".join(expKeys)
                    Acc = 0 if expKeys==pressedKeys else 1
                    
                    pressedOnset, pressedRhyme = self.split(actualKeys)
                    
#                    pressedOnset = "".join(x for x in pressedKeys if x in self.leftKeys)
#                    if len(pressedOnset) == 0:
#                        pressedOnset = 'NA'
                    expOnset = expKeys[0: len(expKeys) - 1]
#                    pressedRhyme = "".join(x for x in pressedKeys if x in self.rightKeys)
#                    if len(pressedRhyme) == 0:
#                        pressedRhyme = 'NA'
                    expRhyme = expKeys[len(expKeys) - 1: len(expKeys)]
                    onsetAcc = 1 if set(expOnset) == set(pressedOnset) else 0
                    rhymeAcc = 1 if set(expRhyme) == set(pressedRhyme) else 0
                    conCluster = 0
                    if len(expOnset) == 2:
                        conCluster = 1
                    string=[str(var) for var in self.subject, trialNum, trial['type'], trial['ID'], 
                            rep, self.wordInd, curWord, 
                            expKeys, pressedKeys, Acc, RT,  
                            len(accKeys), accKeys, add, miss, 'NA', 'NA', expOnset, pressedOnset, onsetAcc, expRhyme, pressedRhyme, rhymeAcc, conCluster]              
                    print string               
                    stamps = ''
                    index = 0
                    for index in range(3 - len(actualKeys)):
                        actualKeys.append('NA')
                        timeStamp.append('NA')
                    index = 0
                    for index in range(len(actualKeys)):
                        stamps += '\t' + str(actualKeys[index]) + '\t' + str(timeStamp[index])
                    line='\t'.join(string) + stamps + '\n'
                    self.resultsFile.write(line)
                    self.resultsFile.flush()
                    getKeys = []
        
                self.background.draw()
                self.win.flip()
                core.wait(1)
                self.pacer.setPos (self.startPos)
                for rep in range(1,4):
                    hitBoundary = False
                    self.wordInd=1 # index of word within trial (first word, second...)
                    pressedKeys = [] # keys that subject pressed
                    accKeys = [] # accurate presses
                    pressedWord = [] # translates key presses into corresponding word
                    pressedUnits = [] # not important
                    add = [] # keys pressed that were not in word
                    miss = [] # keys not pressed
                    actualKeys = []
                    timeStamp = []
                    RT = 'NA' # reaction time, to be defined later     
                    curWord = trial[self.pacerLoc[self.wordInd]]
                    for i in self.transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                        curWord = curWord.replace(i, self.transKeys[i])
                    expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
                    if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                        expKeys.append('3') # this is hard coded, see if there's a better way...
                    if curWord[0] == 'R':
                        expKeys.append('1')
                    expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                    react = False
                    temp = event.getKeys(keyList=self.keys)
                    self.pacer2 = visual.Rect(win=self.win,size=(1700,100),lineColor="black", pos = ([0,685]))
                    while True:
                        self.draw4()
                        if self.wordInd < 5:
                            self.pacer.draw()
                        if self.wordInd < 4:
                            self.pacer2.draw()
                        self.pacer2.pos = (0,435 + self.pacer.pos[1])
                        self.pacer.pos -= (0,self.interStepInterval)
                        self.win.flip()
                        if  self.pacer.pos[1] <= -220:
                            self.pacer = self.pacer2
                            break
                        if self.wordInd >= 5:
                            continue
                        if self.pictures[self.wordInd].overlaps(self.pacer):
                            if hitBoundary == False:
                                temp = event.getKeys(keyList=self.keys)
                                hitBoundary = True
                                startt = core.Clock()
                            if len(pressedKeys) < len(expKeys):
                                getKeys = event.getKeys(keyList=self.keys)
                                if len(getKeys) != 0:
                                    if react == False:
                                        RT = int(startt.getTime() * 1000)
                                        react = True
                                    for i in range(len(getKeys)):
                                        if i == 0:
                                            timeStamp.append(int(start.getTime() * 1000))
                                        else:
                                            timeStamp.append(0)
                                    start = core.Clock()
                                actualKeys.extend(getKeys)
                                pressedKeys.extend(getKeys)            
                        else:
                            if hitBoundary:
                                event.clearEvents()
                                temp = event.getKeys(keyList=self.keys)
                                pressedKeys = (sorted(set(pressedKeys), key = lambda x:  self.srtMap[x]))
                                pressedKeys ="".join(pressedKeys)              
                                
                                pressedKeys1 = pressedKeys[0: len(pressedKeys) - 1]
                                pressedKeys2 = pressedKeys[len(pressedKeys) - 1: len(pressedKeys)]
                                pressedKeys1 = (sorted(set(pressedKeys1), key = lambda x:  self.srtMap[x]))
                                pressedKeys1.extend(pressedKeys2)
                                pressedKeys = pressedKeys1
                                pressedKeys ="".join(pressedKeys)    
                                for i in pressedKeys: # translating keys into word, not important
                                    pressedUnit = [self.unit for self.unit, value in self.capKeys.iteritems() if value == i]
                                    pressedUnits.append(pressedUnit)
                                    pressedWord = pressedWord + pressedUnit
                                if (len(pressedUnits)>1) and (pressedWord[0]=='R' or pressedWord[0]== 'L'):
                                    pressedWord = pressedWord [0] + pressedWord[2:]  # takes care of the fact that keys 1+2 represent only one unit
        
                                # data written to file + format changes to make it easily readable in excel (lists of pressed keys 
                                # will appear as strings):               
                                add = set(pressedKeys) - set(expKeys) # key additions
                                add = "".join(sorted(add, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                                if len(add) == 0:
                                    add = 'NA'
                                miss = set(expKeys) - set(pressedKeys) # key omissions
                                miss = "".join(sorted(miss, key = lambda x:  self.srtMap[x])) # sort them by keyboard space
                                if len(miss) == 0:
                                    miss = 'NA'
                                accKeys = "".join([x for x in pressedKeys if x in expKeys])
                                if len(accKeys) == 0:
                                    accKeys = 'NA'
                                expKeys = "".join(expKeys)
                                Acc = 0 if expKeys==pressedKeys else 1
                                
                                pressedOnset, pressedRhyme = self.split(actualKeys)
                                
#                                pressedOnset = "".join(x for x in pressedKeys if x in self.leftKeys)
#                                if len(pressedOnset) == 0:
#                                    pressedOnset = 'NA'
                                expOnset = expKeys[0: len(expKeys) - 1]
#                                pressedRhyme = "".join(x for x in pressedKeys if x in self.rightKeys)
#                                if len(pressedRhyme) == 0:
#                                    pressedRhyme = 'NA'
                                expRhyme = expKeys[len(expKeys) - 1: len(expKeys)]
                                onsetAcc = 1 if set(expOnset) == set(pressedOnset) else 0
                                rhymeAcc = 1 if set(expRhyme) == set(pressedRhyme) else 0
                                conCluster = 0
                                if len(expOnset) == 2:
                                    conCluster = 1
                                accCount.append(Acc)
                                accRate = 1 - round(float(sum(accCount))/len(accCount), 2)
                                if accRate == 'NA':
                                    errRate = 'NA'
                                else:
                                    errRate = 1.0 - float(accRate)
                                string=[str(var) for var in self.subject, trialNum, trial['type'], trial['ID'],  # collect all the info we're interested in
                                                                          rep, self.wordInd, curWord, 
                                                                          expKeys, pressedKeys, Acc, RT,  
                                                                          len(accKeys), accKeys, add, miss, accRate, errRate, expOnset, pressedOnset, onsetAcc, expRhyme, pressedRhyme, rhymeAcc, conCluster]              
                                print string 
                                
                                hitBoundary = False
                                self.wordInd+=1 # index of word within trial (first word, second...)
                                pressedKeys = [] # keys that subject pressed
                                accKeys = [] # accurate presses
                                pressedWord = [] # translates key presses into corresponding word
                                pressedUnits = [] # not important
                                add = [] # keys pressed that were not in word
                                miss = [] # keys not pressed
                                RT = 'NA' # reaction time, to be defined later   
                                if self.wordInd < 5:
                                    curWord = trial[self.pacerLoc[self.wordInd]]
                                for i in self.transKeys.keys(): # translate it (since we used the full 'w1' spelling)
                                    curWord = curWord.replace(i, self.transKeys[i])
                                expKeys = [self.capKeys[curWord[0]], self.capKeys[curWord[1:]]] # define correct answer keys per word
                                if curWord[0] == 'L': # for words with consonant cluster, add first consonant key to be expected too
                                    expKeys.append('3') # this is hard coded, see if there's a better way...
                                if curWord[0] == 'R':
                                    expKeys.append('1')
                                expKeys = sorted(expKeys, key = lambda x:  self.srtMap[x])
                                react = False
                                temp = event.getKeys(keyList=self.keys)
                                stamps = ''
                                index = 0
                                for index in range(3 - len(actualKeys)):
                                    actualKeys.append('NA')
                                    timeStamp.append('NA')
                                index = 0
                                for index in range(len(actualKeys)):
                                    stamps += '\t' + str(actualKeys[index]) + '\t' + str(timeStamp[index])
                                line='\t'.join(string) + stamps + '\n'
                                self.resultsFile.write(line)
                                self.resultsFile.flush()
                                getKeys = []
                                actualKeys = []
                                timeStamp = []
                self.background.draw()                              
                self.fixationCross.draw()
                self.win.flip()
                core.wait(.5)
                if  int(breakTime.getTime())>self.timeBreak:
                    breakClick=False
                    while not breakClick:
                        self.background.draw()
                        self.breakText.draw()
                        self.win.flip()
                        stop= event.waitKeys(['c'])
                        if stop==['c']:
                            breakTime.reset()
                            breakClick=True
        
            self.background.draw()
            self.finalText.draw()
            self.resultsFile.close()
            self.win.flip()
            core.wait(5)
    
    
        
action = Action()
action.start()
