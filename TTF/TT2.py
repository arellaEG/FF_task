

class _Recorder(object):   
    def __init__(self, fname, scale, channels, rates, buffers, audio):
        import pyaudio
        import wave
        self.fname = fname
        self.wav = wave.open(fname, "wb")
        self.wav.setnchannels(channels)
        self.wav.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        self.wav.setframerate(rates)
        def cb(in_data, count, time_info, status):
            self.wav.writeframes(in_data)
            return in_data, pyaudio.paContinue
        self.stream = audio.open(format = pyaudio.paInt16,
    								channels = 2*channels,
									rate = rates/2,
									input = True,
									frames_per_buffer = buffers,
									stream_callback = cb)
    def start(self):
        self.stream.start_stream()
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.wav.close()


class Language(object):
    
    def __init__(self):
        import pyaudio
        self.SCALE = 500
        self.CHANNELS = 1
        self.RATE = 44100
        self.BUFFER = 2048
        self.AUDIO = pyaudio.PyAudio()
        
        ###################################
        ########fill in subject ID #######
        
        self.subject ='999'
        
        ###################################
        ###################################
        
        
        # presents four word from TT trial, one under the other, for participants to read
        # little blue dot on the left serves as pacer - marking which word should
        # be said; moving at a predetermined speed "pacerTempo"
        self.develop = False
        self.ifFam = True
        self.pacerTempo = .55 # speed of pacer
        self.timeBreak = 80 # every how many seconds do they get a break screen
        self.intervalStep = 3
        
        self.header=["subject", "trialNum", "trialType", "itemID", "rep", "wordInd", "audioName", "curWord", "expOnset", "expVowel", "expCoda"
                     , "expRhyme", "conCluster", "respWord", "respOnset", "respVowel", "respCoda", "respRhyme", "acc", "RT"]
        self.headers = '\t'.join(self.header) + '\n'
        ### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length
        self.units=['z','R','S','P','xv','uv','yf','wg']
        self.allUnits = {'z':'z', 'R':'zl', 'S':'sh', 'P':'shp', 'x':'a', 'u':'oo', 'y':'a', 'w': 'oo', 'v':'v', 'f':'f', 'g':'f'}
        self.onsets=['z','R','S','P']
        self.rhymes=['xv','uv','yf','wg']
        
        self.transKeys = {'R':'zl', 'S':'sh', 'P':'shp', 'xv':'av','uv':'oov','yf':'af', 'wg':'oof'}
        
        
    def start(self):
        from psychopy import visual, core
        import sys
        self.createTrials()
        if len(sys.argv) == 1:
            self.setSubject()
        else:
            self.subject = sys.argv[1]
        self.win = visual.Window([800, 500], fullscr=True,
                        color="black", units='pix')

        self.instruct = visual.TextStim(win=self.win, height=28, 
                         color='black', wrapWidth = 1000, pos = (0,43), alignHoriz='center', 
                         alignVert='center')
        self.instruct1 = "In the final part of this experiment you will be reading sequences of words.\
 These are not real words, so we'll start by getting you familiar with\
 them. Each word will be presented in the middle of the screen, and \
 your job is to simply say it loud and clear."
        
        self.instruct2a = "Great! Now we can move on to the task itself.\
 \n\n On each trial you will be presented with four words.\
 Your task is to simply say them aloud in order, from top to bottom."
        
        self.instruct2b = "At the beginning of every trial you will see a\
 red circle on the top left for two seconds. You can use this\
 time to quickly preview the words you will be reading. Then, the\
 red circle will disappear and a rectangle will begin scrolling down from the top.\
 \n\nThe rectangle is your cue - once it reaches a word,\
 you say that word aloud. Every trial will be repeated three\
 times before moving on to the next.\
 \n\n\nLet's get started!" 
         
        
        self.background = visual.Rect(win=self.win, size = (2250, 900), fillColor = 'white', pos = ([0,0]))
        
        
        # for participants to press 'c' when they've read instructions on that page
        # and are ready to continue:
        self.cToBegin =  visual.TextStim(win=self.win, height=35, 
                                    text ="\n\n\tPress 'c' to continue.",
                         color='black', wrapWidth = 1000, pos = (0,-120), alignHoriz='center', 
                         alignVert='center')
        self.breakText=visual.TextStim(win=self.win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='black')

        self.endText=visual.TextStim(win=self.win, height=40,
                         text="All Done! Please call the experimenter.",
                         color='black')
        
        self.pacer= visual.Circle(win=self.win, radius = 10, fillColor='blue') # blue dot that marks which word should be pressed
        
        self.fixationView = visual.Circle(win=self.win, radius = 20, fillColor='red', pos=(-150,160)) # red circle for viewing time
        
        
        self.fixationCross= visual.ShapeStim(win = self.win, vertices=((0, -70), (0, 70), (0,0),  
                                                       (70,0), (-70, 0)),
                                                lineWidth=5, closeShape=False, 
                                                lineColor='grey') # used between trials
        
        # single-word presentation in the middle of the screen:
        self.word0 = visual.TextStim(win=self.win,pos=(0,0), height = 40, color='black')
        # four words at a time, from top(word1) to bottom (word4)
        self.word1 = visual.TextStim(win=self.win,pos=(0,155), height = 40, color='black')
        self.word2 = visual.TextStim(win=self.win,pos=(0,50), height = 40, color='black')
        self.word3 = visual.TextStim(win=self.win,pos=(0,-55), height = 40, color='black')
        self.word4 = visual.TextStim(win=self.win,pos=(0,-160), height = 40, color='black')
        self.rect1 = visual.Rect(win=self.win,size=(500,100),lineColor="black", pos = ([0,155]), opacity = 0.4)
        self.rect2 = visual.Rect(win=self.win,size=(500,100),lineColor="black", pos = ([0,50]), opacity = 0.4)
        self.rect3 = visual.Rect(win=self.win,size=(500,100),lineColor="black", pos = ([0,-55]), opacity = 0.4)
        self.rect4 = visual.Rect(win=self.win,size=(500,100),lineColor="black", pos = ([0,-160]), opacity = 0.4)
        self.pacer1 = visual.Rect(win=self.win,size=(500,106),lineColor="black", pos = ([0,250]))
        
        if self.ifFam:
            self.famPhase()
        self.testPhase()
        self.AUDIO.terminate()
        self.win.close()
        core.quit()
        
        
        
    def setSubject(self):
        from psychopy import gui
        dlg = gui.Dlg()
        dlg.addText("If you are not a developer, just click OK")
        dlg.addField("password")
        dlg.show()
        
        if dlg.data[0] == '1234':
            self.develop = True
        else:
            self.develop = False
        
        if self.develop:
            dlg = gui.Dlg()
            dlg.addText("starting stage number")
            dlg.addField("")
            dlg.show()
            
            if dlg.data[0] == '2':
                self.ifFam = False
            

        dlg = gui.Dlg()
        dlg.addText("Enter the ID: ");
        dlg.addField("subject ID");
        dlg.show();
        
        if dlg.OK:
            if len(dlg.data[0]) != 0:
                self.subject = dlg.data[0]
            else:
                self.subject = '999'
        else:
            self.subject = '999'
    
        
    def importTrials(self, numTrials):
        #import io
        #import csv
        sep=','
        bTrial= open ('TTstim_TT.csv', 'rb') 
        colNames = bTrial.next().rstrip().split(sep)
        #reader=csv.DictReader(bTrial)
        self.trialsList = []
        for t in range(numTrials):
            trialStr=bTrial.next().rstrip().split(sep)
            assert len(trialStr) == len(colNames)
            trialDict = dict(zip(colNames, trialStr))
            self.trialsList.append(trialDict)
            
    def createTrials(self):
        import random
        self.importTrials(88)
        # random 5 familiarization trials:
        self.fam = random.sample([x for x in self.trialsList if x['type'] == 'fam'], 5)
        # create experimental list by excluding "familiarization" phase trials
        self.exp = [x for x in self.trialsList if x['type'] <> 'fam']
        random.shuffle(self.exp) # shuffle order of experimental items
        
        # trialsList is 5 familiarization trials, followed by 48 experimental items:
        self.trialsList = self.fam+self.exp
        
        # getting all possible words in our experiment(instead of hard coding, go through
        # the trialsList and extract from there - useful in case we change specific words)
        self.allWords = []
        for i in self.trialsList:
            w1,w2,w3,w4 = i['fullTrial'].split()
            self.allWords.extend([w1,w2,w3,w4])
        self.allWords = list(set(self.allWords)) # reduce to only unique words, then make into list again
        random.shuffle(self.allWords)  # shuffle their order before using for practice

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
        
    def write4(self): 
        self.background.draw()
        self.word1.draw()
        self.word2.draw()
        self.word3.draw()
        self.word4.draw()
        self.rect1.draw()
        self.rect2.draw()
        self.rect3.draw()
        self.rect4.draw()
    
    def famPhase(self):
        import os
        from psychopy import core
        if not os.path.exists(str(self.subject) + "_TT"):
            os.mkdir(str(self.subject) + "_TT")
        with open(self.subject + "_TT/" + self.subject+'_TT_fam.txt','wb') as self.resultsFile:
            self.resultsFile.write(self.headers)
            self.resultsFile.flush()
            self.cClick(self.instruct1)
            self.background.draw()
            self.fixationCross.draw()
            self.win.flip()
            core.wait(3)
            os.mkdir(self.subject + "_TT/" + self.subject + '_audio')
            # first they read words one-by-one, we'll use this later when analyzing the data -
            # since these are non-words, we want to make sure they pronounce them our way
            # the audio file will be a single continous recording, starting just before
            # the first word and ending after the last (will include all silences of
            # fixation time, etc.)
            recorder = _Recorder(self.subject + "_TT/" + self.subject + "_audio/" + self.subject + "_fam.wav", self.SCALE, self.CHANNELS, self.RATE, self.BUFFER, self.AUDIO) # name of fam audio file
            recorder.start() # begin recording familiarization
            trialNum = 0 # initiating order for familiarization phase
            for word in self.allWords:
                trialNum+=1
                
                actual = word
                for i in self.transKeys.keys():
                    actual = actual.replace(self.transKeys[i], i)
                #print actual
                expOnset = self.allUnits[actual[0]]
                expVowel = self.allUnits[actual[1]]
                expCoda = self.allUnits[actual[2]]
                expRhyme = expVowel + expCoda
                conCluster = 0 if len(expOnset) == 1 else 1
                audioName = self.subject + "_audio/" + self.subject + "_fam.wav"
                
                
                self.word0.setText(word)
                self.background.draw()
                self.word0.draw()
                self.win.flip()
                core.wait(3)
                self.background.draw()
                self.fixationCross.draw()
                self.win.flip()
                core.wait(1)
                string = [str(var) for var in self.subject, trialNum, "itemID", "rep", "wordInd", audioName, word, expOnset, expVowel,
                          expCoda, expRhyme, conCluster, '', '', '', '', '', '', '']
                print string
                line= '\t'.join(string) + '\n'
                self.resultsFile.write(line)
                self.resultsFile.flush()
                
            recorder.stop() # after going through all words, stop recorder
            self.resultsFile.close()
            self.cClick(self.instruct2a)
            self.cClick(self.instruct2b)
            self.breakTime=core.Clock()
            trialNum=0   
        
    def testPhase(self):
        from psychopy import core, visual, event
        import os
        self.breakTime = core.Clock()
        if not os.path.exists(str(self.subject) + "_TT"):
            os.mkdir(str(self.subject) + "_TT")
        with open(self.subject + "_TT/" + self.subject+'_TT_test.txt','wb') as self.resultsFile:
            self.resultsFile.write(self.headers)
            self.resultsFile.flush()
            if not os.path.isdir(self.subject + "_TT/" + self.subject + "_audio"):
                os.mkdir(self.subject + "_TT/" + self.subject + "_audio")
            trialNum = 0
            for trial in self.trialsList:
                trialNum+=1
                self.background.draw()
                self.fixationCross.draw()
                self.win.flip()
                core.wait(1)
                t = trial['fullTrial'].split()
                w1,w2,w3,w4=t
                self.word1.setText(w1)
                self.word2.setText(w2)
                self.word3.setText(w3)
                self.word4.setText(w4)
                self.write4()
                self.fixationView.draw() # fixation to allow brief viewing - 2 sec of big red circle
                self.win.flip()
                core.wait(2)
                       
                audioName = (self.subject + "_" + str(trialNum) + "_" + str(trial['ID']) + ".wav")
                recorder = _Recorder(self.subject + "_TT/" + self.subject + "_audio/" + self.subject + "_" + str(trialNum) + "_" + str(trial['ID']) + ".wav", self.SCALE, self.CHANNELS, self.RATE, self.BUFFER, self.AUDIO)
                recorder.start()
                start = core.Clock()
                self.pacer1.pos = (0, 240)
                
                #test = True
                
                for rep in range(1,4):
                    # begin recorder, saving file name by subject, trialNum, rep
                    # each recording is a rep - will include 4 words
                    
                    ############ recorder start: 0.000s #########################
                    ### 1: 0.131s 2: 0.580s  3: 1.031s  4: 1.481s  end: 1.933s###
                    ### 5: 1.997s  6: 2.447s  7: 2.896s  8: 3.347s end: 3.785s###
                    ### 9: 3.847s 10: 4.298s 11: 4.747s 12: 5.198s end: 5.645s###
                    ##########last word stop: 5.645s ############################
                    ########### recorder stop: 6.228s ###########################
                    #print "xxxxx"
                    self.pacer2 = visual.Rect(win=self.win,size=(500,105),lineColor="black", pos = ([0,680]))
                    self.wordInd=0 # index of word within trial (first word, second...)
                    self.pacer.pos = (-150,155)
                    for curWord in trial['fullTrial'].split():
                        self.wordInd += 1
                        
                        actual = curWord
                        for i in self.transKeys.keys():
                            actual = actual.replace(self.transKeys[i], i)
                        #print actual
                        expOnset = self.allUnits[actual[0]]
                        expVowel = self.allUnits[actual[1]]
                        expCoda = self.allUnits[actual[2]]
                        expRhyme = expVowel + expCoda
                        conCluster = 0 if len(expOnset) == 1 else 1
                        
                        #self.pacerTime=core.Clock()              
                        
                        string=[str(var) for var in self.subject, trialNum, trial['type'], trial['ID'], 
                                rep, self.wordInd, audioName, curWord, expOnset, expVowel, expCoda, expRhyme, conCluster,
                                '', '', '', '', '', '', '']              
                        #print string               
                        line='\t'.join(string) + '\n'
                        self.resultsFile.write(line)
                        self.resultsFile.flush()
                    
                    
                    
                    while True:
                        #print self.pacer1.pos[1]
                        #print self.pacer2.pos[1]
                        self.write4()
                        self.pacer1.pos -= (0, 3.330)   #3.476 (500) 3.136(550) 3.330
                        self.pacer2.pos = (0,430 + self.pacer1.pos[1])
                        
#                        if self.pacer1.pos[1] <= 205: # 205 100 -4  -110 -213
#                            print start.getTime()
#                            #print xxx
                          
                            
                            
                        if self.pacer1.pos[1] >= -210:
                            self.pacer1.draw()
                        if rep < 3:
                            self.pacer2.draw()
                        
                        
                        #self.pacer1.draw()
                        self.win.flip()
                        if self.pacer1.pos[1] <= -215:
                            self.pacer1 = self.pacer2
                            #print start.getTime()
                            break

                    self.write4()
                    if rep != 3:
                        self.pacer1.draw()
                    self.win.flip()
                core.wait(0.55)
                print start.getTime()
                recorder.stop()
                self.background.draw()                                
                self.fixationCross.draw()
                self.win.flip()
                core.wait(.5)
                if int(self.breakTime.getTime())>self.timeBreak:
                    breakClick=False
                    while not breakClick:
                        self.background.draw()
                        self.breakText.draw()
                        self.win.flip()
                        stop= event.waitKeys(['c','q'])
                        if stop==['c']:
                            self.breakTime.reset()
                            breakClick=True
                        elif stop==['q']:
                            self.win.close()
                            core.quit()
            self.background.draw()
            self.endText.draw()
            self.resultsFile.close()
            self.win.flip()
            core.wait(5)
            
      
        
if __name__ == '__main__':
#    import sys
#    if len(sys.argv) != 1:
#        language = Language()
#        language.start()
    language = Language()
    language.start()
