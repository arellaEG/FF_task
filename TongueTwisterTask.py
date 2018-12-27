

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
    								channels = 1*channels,
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
        self.RATE = 48000
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
        
        self.header=["trialNum", "trialType", "itemID", "rep", "wordInd", "curWord"]
        self.headers = '\t'.join(self.header) + '\n'
        ### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length
        self.units=['t','R','v','L','eb','xb','ig','ug']
        self.onsets=['t','R','v','L']
        self.rhymes=['eb','xb','ig','ug']
        
        self.transLetter = {'R':'tr', 'L':'fl', 'x':'ee','u': 'oo'}
        
        
    def start(self):
        from psychopy import visual, core
        self.createTrials()
        self.setSubject()
        self.win = visual.Window([800, 500], fullscr=True,
                        color="black", units='pix')

        self.instruct = visual.TextStim(win=self.win, height=28, 
                         color='black', wrapWidth = 1000, pos = (0,67), alignHoriz='center', 
                         alignVert='center')
        self.instruct1 = "In the final part of this experiment you will be reading sequences of words.\
         These are not real words, so we'll start by getting you familiar with\
         them. Each word will be presented in the middle of the screen, and \
         your job is to simply say it loud and clear."
        
        self.instruct2a = "Great! Now we can move on to the task itself.\
         \n\n On each trial you will be presented with four words.\
         Your task is to simply read them aloud in order, from top to bottom."
        
        self.instruct2b = "At the beginning of every trial you will see a\
         red circle on the top left for two seconds. You can use this\
         time to quickly preview the words you will be reading. Then, the\
         red circle will disappear and a small blue circle will appear. \
         \n\nThe blue circle is your cue - when it appears next to a word, \
         you read that word aloud. The blue circle will always move in order, \
         from top to bottom, but you must keep up with its speed. Every trial\
         will be repeated three times before moving on to the next. \
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
        self.word0 = visual.TextStim(win=self.win,pos=(0,0), height = 50, color='black')
        # four words at a time, from top(word1) to bottom (word4)
        self.word1 = visual.TextStim(win=self.win,pos=(0,155), height = 50, color='black')
        self.word2 = visual.TextStim(win=self.win,pos=(0,50), height = 50, color='black')
        self.word3 = visual.TextStim(win=self.win,pos=(0,-55), height = 50, color='black')
        self.word4 = visual.TextStim(win=self.win,pos=(0,-160), height = 50, color='black')
        
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
                self.ifFam = False
            

        dlg = gui.Dlg()
        dlg.addText("Enter the ID: ");
        dlg.addField("subject ID");
        dlg.show();
        
        if dlg.OK:
            self.subject = dlg.data[0]
        else:
            self.subject = '999'
    
        
    def importTrials(self, numTrials):
        #import io
        import csv
        sep=','
        bTrial= open ('TTstim_KS.csv', 'rb') 
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
    
    def famPhase(self):
        from psychopy import core
        with open(self.subject+'_fam.txt','wb') as self.resultsFile:
            self.resultsFile.write(self.headers)
            self.resultsFile.flush()
            self.cClick(self.instruct1)
            self.background.draw()
            self.fixationCross.draw()
            self.win.flip()
            core.wait(3)
            # first they read words one-by-one, we'll use this later when analyzing the data -
            # since these are non-words, we want to make sure they pronounce them our way
            # the audio file will be a single continous recording, starting just before
            # the first word and ending after the last (will include all silences of
            # fixation time, etc.)
            recorder = _Recorder(self.subject + "_fam.wav", self.SCALE, self.CHANNELS, self.RATE, self.BUFFER, self.AUDIO) # name of fam audio file
            recorder.start() # begin recording familiarization
            trialNum = 0 # initiating order for familiarization phase
            for word in self.allWords:
                trialNum+=1
                self.word0.setText(word)
                self.background.draw()
                self.word0.draw()
                self.win.flip()
                core.wait(3)
                self.background.draw()
                self.fixationCross.draw()
                self.win.flip()
                core.wait(1)
                string = [str(var) for var in self.subject, word, trialNum]
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
        from psychopy import core, event
        with open(self.subject+'_TTwb.txt','wb') as self.resultsFile:
            self.resultsFile.write(self.headers)
            self.resultsFile.flush()
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
                self.write4()
                self.win.flip() 
                core.wait(.4) # big red circle disappears, nothing on screen for 1 sec ;
                             # then small blue circle appears and participants must begin              
                audioName = (self.subject + "_" + str(trialNum) + ".wav")
                recorder = _Recorder(self.subject + "_fam.wav", self.SCALE, self.CHANNELS, self.RATE, self.BUFFER, self.AUDIO)
                recorder.start()
                for rep in range(1,4):
                    
                    # begin recorder, saving file name by subject, trialNum, rep
                    # each recording is a rep - will include 4 words
                    
                    self.wordInd=0 # index of word within trial (first word, second...)
                    #write4()
                    self.pacer.pos = (-150,155)
                    #pacer.draw()
                    #win.flip()
                    for curWord in trial['fullTrial'].split():
                        self.wordInd += 1           
                        self.write4()
                        self.pacer.draw()
                        self.win.flip()                
                        self.pacerTime=core.Clock()              
                        core.wait(self.pacerTempo) # wait full time even if participant answered before time's up
        
                        string=[str(var) for var in trialNum, trial['type'], trial['ID'], 
                                rep, self.wordInd, curWord, audioName]              
                        print string               
                        line='\t'.join(string) + '\n'
                        self.resultsFile.write(line)
                        self.resultsFile.flush()
                        self.pacer.pos -=(0,105)
                    self.write4()
                    self.win.flip()
                core.wait(0.55)
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
            
            
language = Language()
language.start()
        
        
        
        