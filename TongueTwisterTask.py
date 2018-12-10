###################################
########fill in subject ID #######

subject ='999'

###################################
###################################


# presents four word from TT trial, one under the other, for participants to read
# little blue dot on the left serves as pacer - marking which word should
# be said; moving at a predetermined speed "pacerTempo"

pacerTempo = .45 # speed of pacer
timeBreak = 80 # every how many seconds do they get a break screen


#### imports ####
import random
import csv
import sys
import numpy as np
from psychopy import visual, core, event, gui, microphone
import pyaudio
import wave


###################################
####### AUDIO CONFIGURATION #######
###################################

SCALE = 500
CHANNELS = 1
RATE = 44100
BUFFER = 2048
AUDIO = pyaudio.PyAudio()

class _Recorder(object):
	def __init__(self, fname):
		self.fname = fname
		self.wav = wave.open(fname, "wb")
		self.wav.setnchannels(CHANNELS)
		self.wav.setsampwidth(AUDIO.get_sample_size(pyaudio.paInt16))
		self.wav.setframerate(RATE)
		def cb(in_data, count, time_info, status):
			self.wav.writeframes(in_data)
			return in_data, pyaudio.paContinue
		self.stream = AUDIO.open(format = pyaudio.paInt16,
									channels = 2*CHANNELS,
									rate = RATE/2,
									input = True,
									frames_per_buffer = BUFFER,
									stream_callback = cb)
	def start(self):
		self.stream.start_stream()
	def stop(self):
		self.stream.stop_stream()
		self.stream.close()
		self.wav.close()

###################################
######## trialList creation #######
###################################
        
sep=','
import io
def importTrials(numTrials):
    bTrial= open ('TTstim_KS.csv', 'rb') 
    colNames = bTrial.next().rstrip().split(sep)
    reader=csv.DictReader(bTrial)
    global trialsList
    trialsList = []
    for t in range(numTrials):
        trialStr=bTrial.next().rstrip().split(sep)
        assert len(trialStr) == len(colNames)
        trialDict = dict(zip(colNames, trialStr))
        trialsList.append(trialDict)
importTrials(88)

# random 5 familiarization trials:
fam = random.sample([x for x in trialsList if x['type'] == 'fam'], 5)
# create experimental list by excluding "familiarization" phase trials
exp = [x for x in trialsList if x['type'] <> 'fam'] 
random.shuffle(exp) # shuffle order of experimental items

# trialsList is 5 familiarization trials, followed by 48 experimental items:
trialsList = fam+exp



# headers for results file
headers=["trialNum", "trialType", "itemID", "rep", "wordInd", "curWord"]



### R = tr, L = vl, x = ee. changed for programming purposes of keeping all words same length
units=['t','R','v','L','eb','xb','ig','ug']
onsets=['t','R','v','L']
rhymes=['eb','xb','ig','ug']

transLetter = {'R':'tr', 'L':'fl', 'x':'ee','u': 'oo'}


win = visual.Window([800, 500], fullscr=True,
                        color="white", units='pix')

instruct = visual.TextStim(win=win, height=30, 
                 color='black', wrapWidth = 1000, pos = (0,85), alignHoriz='center', 
                 alignVert='center')
instruct1 = "In the final part of this experiment you will be reading sequences of words.\
 These are not real words, so we'll start by getting you familiar with\
 them. Each word will be presented in the middle of the screen, and \
 your job is to simply say it loud and clear."

instruct2a = "Great! Now we can move on to the task itself.\
 \n\n On each trial you will be presented with four words.\
 Your task is to simply read them aloud in order, from top to bottom."

instruct2b = "At the beginning of every trial you will see a\
 red circle on the top left for two seconds. You can use this\
 time to quickly preview the words you will be reading. Then, the\
 red circle will disappear and a small blue circle will appear. \
 \n\nThe blue circle is your cue - when it appears next to a word, \
 you read that word aloud. The blue circle will always move in order, \
 from top to bottom, but you must keep up with its speed. Every trial\
 will be repeated three times before moving on to the next. \
 \n\n\nLet's get started!" 




# for participants to press 'c' when they've read instructions on that page
# and are ready to continue:
cToBegin =  visual.TextStim(win=win, height=35, 
                            text ="\n\n\tPress 'c' to continue.",
                 color='black', wrapWidth = 1000, pos = (0,-120), alignHoriz='center', 
                 alignVert='center')


def cClick (instructName): # displays instructions and waits for 'c' press - feed in instruction name (e.g., instruct1)
    cClick = False
    while not cClick:
        instruct.setText (instructName)
        #background.draw()
        instruct.draw()
        cToBegin.draw() 
        win.flip()
        if event.waitKeys (['c']) == ['c']:
            cClick = True



breakText=visual.TextStim(win=win, height=40,
                 text="Please take a short break. Press 'c' to continue.",
                 color='black')

endText=visual.TextStim(win=win, height=40,
                 text="All Done! Please call the experimenter.",
                 color='black')

pacer= visual.Circle(win=win, radius = 20, fillColor='blue') # blue dot that marks which word should be pressed

fixationView = visual.Circle(win=win, radius = 40, fillColor='red', pos=(-200,310)) # red circle for viewing time


fixationCross= visual.ShapeStim(win, vertices=((0, -80), (0, 80), (0,0),  
                                               (80,0), (-80, 0)),
                                        lineWidth=5, closeShape=False, 
                                        lineColor='grey') # used between trials

# single-word presentation in the middle of the screen:
word0 = visual.TextStim(win=win,pos=(0,0), height = 60, color='black')
# four words at a time, from top(word1) to bottom (word4)
word1 = visual.TextStim(win=win,pos=(0,300), height = 60, color='black')
word2 = visual.TextStim(win=win,pos=(0,100), height = 60, color='black')
word3 = visual.TextStim(win=win,pos=(0,-100), height = 60, color='black')
word4 = visual.TextStim(win=win,pos=(0,-300), height = 60, color='black')


def write4():   
        word1.draw()
        word2.draw()
        word3.draw()
        word4.draw()


# getting all possible words in our experiment(instead of hard coding, go through
# the trialsList and extract from there - useful in case we change specific words)
allWords = []
for i in trialsList:
    w1,w2,w3,w4 = i['fullTrial'].split()
    allWords.extend([w1,w2,w3,w4])
allWords = list(set(allWords)) # reduce to only unique words, then make into list again
random.shuffle(allWords)  # shuffle their order before using for practice

with open(subject+'_fam.txt','wb') as resultsFile:

    cClick(instruct1)
    fixationCross.draw()
    win.flip()
    core.wait(3)
    # first they read words one-by-one, we'll use this later when analyzing the data -
    # since these are non-words, we want to make sure they pronounce them our way
    # the audio file will be a single continous recording, starting just before
    # the first word and ending after the last (will include all silences of
    # fixation time, etc.)
    recorder = _Recorder(subject + "_fam.wav") # name of fam audio file
    recorder.start() # begin recording familiarization
    trialNum = 0 # initiating order for familiarization phase
    for word in allWords: 
        trialNum+=1
        word0.setText(word)
        word0.draw()
        win.flip()
        core.wait(3)
        fixationCross.draw()
        win.flip()
        core.wait(1)
        string = [str(var) for var in subject, word, trialNum]
        line= '\t'.join(string) + '\n'
        resultsFile.write(line)
        resultsFile.flush()
        
    recorder.stop() # after going through all words, stop recorder
    resultsFile.close()
    cClick(instruct2a)
    cClick(instruct2b)
    breakTime=core.Clock()
    trialNum=0   


with open(subject+'_TTwb.txt','wb') as resultsFile:
    Rwriter=csv.DictWriter(resultsFile, fieldnames=headers)
    Rwriter.writeheader()
    for trial in trialsList:
        trialNum+=1
        fixationCross.draw()
        win.flip()
        core.wait(1)
        t = trial['fullTrial'].split()
        w1,w2,w3,w4=t
        word1.setText(w1)
        word2.setText(w2)
        word3.setText(w3)
        word4.setText(w4)
        write4()
        fixationView.draw() # fixation to allow brief viewing - 2 sec of big red circle
        win.flip()
        core.wait(2)
        write4()
        win.flip() 
        core.wait(.4) # big red circle disappears, nothing on screen for 1 sec ;
                     # then small blue circle appears and participants must begin              

        for rep in range(1,4):
            # begin recorder, saving file name by subject, trialNum, rep
            # each recording is a rep - will include 4 words
            audioName = (subject + "_" + str(trialNum) + "_" + str(rep) + ".wav")
            recorder = _Recorder(audioName) 
            recorder.start()
            wordInd=0 # index of word within trial (first word, second...)
            write4()
            pacer.pos = (-200,300)
            pacer.draw()
            win.flip()
            for curWord in trial['fullTrial'].split():
                wordInd += 1           
                write4()
                pacer.draw()
                win.flip()                
                reactionTime=core.Clock()
                pacerTime=core.Clock()              
                core.wait(pacerTempo-(pacerTime.getTime())) # wait full time even if participant answered before time's up

                string=[str(var) for var in trialNum, trial['type'], trial['ID'], 
                        rep, wordInd, curWord, audioName]              
                print string               
                line='\t'.join(string) + '\n'
                resultsFile.write(line)
                resultsFile.flush()
                pacer.pos -=(0,200)
            recorder.stop()                                  
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
AUDIO.terminate()
win.close()
core.quit()
