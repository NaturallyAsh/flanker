# Current flanker build as of 2/19/20

# CREATE A COMMENTED SUMMARY OVERVIEW (significations of groups
# variable meanings, block meanings, etc.)

# create 2 dlg boxes: 1st one for the group letter and a subject
# id number, both of which i input
# myself; the 2nd with just age and gender

# group A = no feedback
# group B = 'good job' feedback only on corr resp
# group C = 'good job' feedback regardless of performance

# using block_params file containing block1, block2, and block3_params xlsx

# remove PARTICIPANT field from dlg

# INSTRUCTIONS: something about paying atten to fixation cross
# create an exit screen that only i can exit (Thanks for participant)
# ask about putting oops after incorrect group B

# todo: figure how to handle missing values; jamovi is confused
# measure accuracy? is there a trade-off that effects reaction time
# create equal arrow display times for all groups
# 30 sec warm-up instead of dropping block?
# predict an inverse relationship: RT increases, Accur decreases
# A and C: predict 
# B could be motivated to be more accurate

import psychopy 
import pdb
from psychopy.hardware import keyboard
from psychopy import core, visual, gui, data, event, monitors, logging 
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED, STOPPED)
import random
import time, numpy as np 
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import csv
from pandas.io.common import EmptyDataError 


# def kb to keep track of 'escape' presses
defaultKeyboard = keyboard.Keyboard()
respKeys = ['z', 'm']
arrowNames = ['Left', 'Right']
arrowChars = ["\u2190","\u2192"]
expName = 'Flanker Task'
msg = ''
instructions = "Focus on the fixation cross (+) sign in the middle of the screen at the start of each trial.\n\
                \nWhen the fixation cross (+) disappears and the arrow appears, press the key that matches the arrow direction. \n\
                \n Press on z if the arrow points to the left.\n\
                \n Press on m if the arrow points to the right.\n\
                \n Press the SPACEBAR to start the test."

dateStr = time.strftime("%b_%d_%H%M", time.localtime())
fixedExpInfo = {'Subject ID': '','group': ''}
fixedDlg = gui.DlgFromDict(
    dictionary=fixedExpInfo,
    title = expName,
    order = ['Subject ID', 'group']
    )
if fixedDlg.OK:
    print('ok')
else:
    core.quit()
expInfo = {'age': '', 'gender': ''}
dlg = gui.DlgFromDict(
    dictionary=expInfo, 
    title = expName,
    order = ['age', 'gender'])
if dlg.OK:
    #save params to file for next time
    #toFile('lastParams.pickle', expInfo)
    print('ok')
else:
    core.quit() #the user hit cancel so exit

expInfo['date'] = dateStr
expInfo['expName'] = expName

fixedExpInfo.update(expInfo)

print(fixedExpInfo['group'])

fileName = fixedExpInfo['group'] +' SubID-' + fixedExpInfo['Subject ID'] + '-' + dateStr
globalClock = core.Clock()
logging.setDefaultClock(globalClock)

# --------------- LOGGING FILE --------------- #
logFileName = 'MyFlanker-%s-%s' % (expInfo['date'], dateStr)
logging.LogFile((logFileName + '.log'), level=logging.INFO)
logging.log(level=logging.INFO, msg='---START PARAMS---')
logging.log(level=logging.INFO, msg='date: %s' % expInfo['date'])
logging.log(level=logging.INFO, msg='group: %s' % fixedExpInfo['group'])
logging.log(level=logging.INFO, msg='date: %s' % dateStr)
logging.log(level=logging.INFO, msg='respKeys: %s' % respKeys)



endExpNow = False #flag for 'escape' from exp

# Handles exp data as a whole. 
thisExp = data.ExperimentHandler(
        name=expName,
        extraInfo=fixedExpInfo,
        savePickle=True,
        saveWideText=True,
        dataFileName=fileName)

# --------------- MONITOR & STIMULI CREATION --------------- #

widthPix = 720
heightPix = 540
# widthPix = 2560
# heightPix = 1600
# mon = monitors.Monitor('test', width=53.1, distance=60.)
mon = monitors.Monitor('testMonitor')
# mon.setSizePix((widthPix, heightPix))
win = visual.Window(
    monitor=mon,
    # size=(widthPix, heightPix),
    colorSpace='rgb',
    color = '#000000',
    fullscr=False,
    allowGUI=False, #switch to true to add to exp window
    units='deg')

# if i want to keep track of frames for measuring RT
win.recordFrameIntervals = True

#Changing the font to Arial fixed the right arrow problem.
target_arrow = visual.TextStim(win, 
    pos=[0,0], 
    color='#FFFFFF',
    alignHoriz='center',
    height=2,
    font='Arial',
    name='target',
    text='')
    
flanker_stimuli = []
flanker_pos = [-4, -2, 2, 4]
for i in range(0, len(flanker_pos)):
    flanker_stimuli.append(visual.TextStim(win,
    pos=[0,flanker_pos[i]],
    color='#FFFFFF',
    alignHoriz='center',
    height=2,
    font='Arial',
    name='flanker%d'%(i+1),
    text=''))
    
# too-slow
tooSlowStim = visual.TextStim(win, 
    pos=[0,0], 
    color='red', 
    alignHoriz='center', 
    name='tooSlow', 
    text="Too Slow!")

#fixation
fixationText=visual.ShapeStim(win,
    vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5,0)),
    lineWidth=5,
    closeShape=False,
    name='fixation',
    lineColor="white")

instructText = visual.TextStim(win,
    text=instructions,
    name='instruct message')

getreadyText = visual.TextStim(win,
    text='Get Ready!',
    name='get ready message',
    font='Arial',
    color='white'
    )

pauseText = visual.TextStim(win,
    name='pause',
    text='break for 10 seconds',
    font='Arial',
    color='black', colorSpace='rgb',
    )

feedbackText = visual.TextStim(win,
    name='feedback',
    pos=[0,0],
    text='default text',
    font='Arial',
    color='green',
    colorSpace='rgb'
    )

thanksText = visual.TextStim(win,
    name='thanks text',
    pos=[0,0],
    text='Thank you for your participation!\n\
    \n To minimize distraction, Please remain seated until all participants have finished.',
    font='Arial',
    color='white',
    colorSpace='rgb'
    )

# Created some handy clocks and timers to keep track of blocks and trials
trialClock = core.Clock()
instructClock = core.Clock()
blockClock = core.Clock()
pauseClock = core.Clock()
feedbackClock = core.Clock()
thanksClock = core.Clock()
trialTimer = core.CountdownTimer()
pauseTimer = core.CountdownTimer()
getReadyTimer = core.CountdownTimer()
feedbackTimer = core.CountdownTimer()

# pdb.set_trace()
# breakpoint()

t = 0
instructClock.reset()
frameN = -1
continueTrial = True

ready = keyboard.Keyboard()

instructComps = [instructText, ready]
for thisComp in instructComps:
    thisComp.tStart = None
    thisComp.tStop = None
    thisComp.tStartRefresh = None
    thisComp.tStopRefresh = None
    if hasattr(thisComp, 'status'):
        thisComp.status = NOT_STARTED

# --------------- STARTING INSTRUCTIONS --------------- #
while continueTrial:
    t = instructClock.getTime()
    frameN = frameN + 1

    if t >= 0 and instructText.status == NOT_STARTED:
        instructText.tStart = t 
        instructText.frameNStart = frameN
        win.timeOnFlip(instructText, 'tStartRefresh')
        instructText.setAutoDraw(True)

    if t >=0 and ready.status == NOT_STARTED:
        ready.tStart = t 
        ready.frameNStart = frameN 
        win.timeOnFlip(ready, 'tStartRefresh')
        ready.status = STARTED
        ready.clearEvents(eventType='keyboard')

    if ready.status == STARTED:
        theseKeys = ready.getKeys(keyList=["space"], waitRelease=False)
        if len(theseKeys):
            theseKeys = theseKeys[0]

            if "escape" == theseKeys:
                endExpNow = True
            continueTrial = False
    # clear events or it will register keys have already been pressed
    defaultKeyboard.clearEvents()
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        print('core start trial quit')
        core.quit()

    if not continueTrial:
        break
    continueTrial = False

    for thisComp in instructComps:
        if hasattr(thisComp, "status") and thisComp.status != FINISHED:
            continueTrial = True
            break

    if continueTrial:
        win.flip()

for thisComp in instructComps:
    if hasattr(thisComp, "setAutoDraw"):
        thisComp.setAutoDraw(False)

# --------------- BLOCKS CREATION --------------- #

blocks = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=fixedExpInfo,
    originPath=1,
    trialList=data.importConditions('block_params.xlsx'),
    seed=None,
    name='blocks')
thisExp.addLoop(blocks)
thisBlock = blocks.trialList[0]

if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

# --------------- LOOPING BLOCKS --------------- #

for thisBlock in blocks:
    currentLoop = blocks
    block_RT_list = []
    corr_list = []

    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))


    # --------------- ADDING TRIALS TO BLOCK LOOP --------------- #
    trials = data.TrialHandler(nReps=1,
            method='random',
            extraInfo=fixedExpInfo,
            originPath=-1,
            trialList=data.importConditions(condsFile),
            seed=None,
            name='trials')
    thisExp.addLoop(trials)
    thisTrial = trials.trialList[0]

    blockClock.reset()
    getReadyTimer.add(4.0)

    while getReadyTimer.getTime() > 0:
        t = blockClock.getTime()
        if t >= 0.0:
            getreadyText.draw()

        win.flip()
    # while pauseTimer.getTime() > 0:
            #     t = pauseClock.getTime()
            #     frameN = frameN + 1

            #     if t >= 0.0: 
            #         pauseText.draw()
            #         win.logOnFlip(level=logging.EXP, msg='Display pause time')

    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))

    # --------------- LAUNCHING GROUP A: NO FB ---------------- #

    if fixedExpInfo['group'] == 'A':
        print('launching group A')

        for thisTrial in trials:
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            continueTrial = True
            resp = keyboard.Keyboard()
            resp.clearEvents(eventType='keyboard')
            no_response_flag = False

            # update w/ new params every repeat
            # using conds from xls files (so magical!)
            # conds xls contains blocks 1, 2, and 3 xls params
            for flanker in flanker_stimuli:
                flanker.text = arrowChars[flankerDirc]

            target_arrow.text = arrowChars[targetDirc]

            trialComps = [flanker, target_arrow, resp]
            for thisComp in trialComps:
                thisComp.tStart = None
                thisComp.tStop = None
                thisComp.tStartRefresh = None
                thisComp.tStopRefresh = None
                if hasattr(thisComp, 'status'):
                    thisComp.status = NOT_STARTED

            

            while continueTrial:
                t = trialClock.getTime()
                
                frameN = frameN + 1 
                
                # group A starts 1 sec faster since it has no 
                # fb routine
                if t >= 1.5:
                    fixationText.setAutoDraw(True)

                if t >= 2.0:
                    fixationText.setAutoDraw(False)
                    win.flip()

                if t >= 2.5:
                    # doing a for loop to set autodraw true to ALL flanks
                    for flanker in flanker_stimuli:
                        flanker.setAutoDraw(True)

                if t >= 3.0 and target_arrow.status == NOT_STARTED:
                    target_arrow.tStart = t
                    target_arrow.frameNStart = frameN
                    win.timeOnFlip(target_arrow, 'tStartRefresh')
                    target_arrow.setAutoDraw(True)

                if t >= 3.0 and resp.status == NOT_STARTED:
                    resp.tStart = t 
                    resp.frameNStart = frameN
                    win.timeOnFlip(resp, 'tStartRefresh')
                    resp.status = STARTED
                    win.callOnFlip(resp.clock.reset)
                    resp.clearEvents(eventType='keyboard')

                if t >= 5.0:
                    no_response_flag = True
                    target_arrow.setAutoDraw(False)
                    for flanker in flanker_stimuli:
                        flanker.setAutoDraw(False)
                    tooSlowStim.setAutoDraw(True)

                if t >= 6.0:
                    tooSlowStim.setAutoDraw(False)
                    continueTrial = False

                f = 0
                feedbackClock.reset()
                trialTimer.reset()

                # adding no_response_flag makes sure keypresses and rts
                # won't be recorded after too-slow appears
                if resp.status == STARTED and no_response_flag != True:
                    theseKeys = resp.getKeys(keyList=respKeys, waitRelease=False)
                    if len(theseKeys):
                        theseKeys = theseKeys[0]
                        if "escape" == theseKeys:
                            endExpNow = True
                        resp.keys = theseKeys.name 
                        print(f'resp.key: {resp.keys}')
                        resp.rt = theseKeys.rt
                        print(f'resp.rt: {resp.rt}')

                        if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                            resp.corr = 1
                            
                            print(f"{resp.corr}: correct")
                            print(f"key: {resp.keys}")
                        else:
                            resp.corr = 0
                            print(f"{resp.corr}: incorrect")
                            print(f"key: {resp.keys}")

                        # condition to check if element is in List of ['',[],None]
                        # if resp.keys in ['', [], None]:
                        #     resp.corr = None

                        continueTrial = False


                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()

                if not continueTrial:
                    break

                continueTrial = False
                for thisComp in trialComps:
                    if hasattr(thisComp, "status") and thisComp.status != FINISHED:
                        continueTrial = True
                        break

                if continueTrial:
                    win.flip()

            for thisComp in trialComps:
                if hasattr(thisComp, "setAutoDraw"):
                    thisComp.setAutoDraw(False)
                    # feedbackText.setAutoDraw(False)
                # doing a for loop in order to set ALL flanks to autodraw false
                for flanker in flanker_stimuli:
                    flanker.setAutoDraw(False)
            
            if resp.keys in ['', [], None]:
                resp.keys = 'NaN'
                trials.addData('kb.keys', resp.keys)
                trials.addData('kb.corr', resp.corr)
            else:
                trials.addData('kb.keys', resp.keys)
                trials.addData('kb.corr', resp.corr)
                corr_list.append(resp.corr)
            if resp.keys != None and resp.keys != 'NaN':
                trials.addData('kb.rt', resp.rt)
                block_RT_list.append(resp.rt)
            else:
                resp.rt = 'NaN'
                trials.addData('kb.rt', resp.rt)
            thisExp.nextEntry()


    # --------------- LAUNCHING GROUP B: FB ON CORR RESP ---------------- #

    if fixedExpInfo['group'] == 'B':
        print('launching group B')

        for thisTrial in trials:
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            continueTrial = True
            resp = keyboard.Keyboard()
            resp.clearEvents(eventType='keyboard')
            no_response_flag = False

            # update w/ new params every repeat
            # using conds from xls files (so magical!)
            for flanker in flanker_stimuli:
                flanker.text = arrowChars[flankerDirc]

            target_arrow.text = arrowChars[targetDirc]

            trialComps = [flanker, target_arrow, resp]
            for thisComp in trialComps:
                thisComp.tStart = None
                thisComp.tStop = None
                thisComp.tStartRefresh = None
                thisComp.tStopRefresh = None
                if hasattr(thisComp, 'status'):
                    thisComp.status = NOT_STARTED

            

            while continueTrial:
                t = trialClock.getTime()
                
                frameN = frameN + 1 
                
                if t >= 0.5:
                    fixationText.setAutoDraw(True)

                if t >= 1.0:
                    fixationText.setAutoDraw(False)
                    win.flip()

                if t >= 1.5:
                    # doing a for loop to set autodraw true to ALL flanks
                    for flanker in flanker_stimuli:
                        flanker.setAutoDraw(True)

                if t >= 2.0 and target_arrow.status == NOT_STARTED:
                    target_arrow.tStart = t
                    target_arrow.frameNStart = frameN
                    win.timeOnFlip(target_arrow, 'tStartRefresh')
                    target_arrow.setAutoDraw(True)

                if t >= 2.0 and resp.status == NOT_STARTED:
                    resp.tStart = t 
                    resp.frameNStart = frameN
                    win.timeOnFlip(resp, 'tStartRefresh')
                    resp.status = STARTED
                    win.callOnFlip(resp.clock.reset)
                    resp.clearEvents(eventType='keyboard')

                if t >= 4.0:
                    no_response_flag = True
                    target_arrow.setAutoDraw(False)
                    for flanker in flanker_stimuli:
                        flanker.setAutoDraw(False)
                    tooSlowStim.setAutoDraw(True)

                if t >= 5.0:
                    tooSlowStim.setAutoDraw(False)
                    continueTrial = False

                f = 0
                feedbackClock.reset()
                trialTimer.reset()

                # adding no_response_flag makes sure keypresses and rts
                # won't be recorded after too-slow appears
                if resp.status == STARTED and no_response_flag != True:
                    theseKeys = resp.getKeys(keyList=respKeys, waitRelease=False)
                    if len(theseKeys):
                        theseKeys = theseKeys[0]
                        if "escape" == theseKeys:
                            endExpNow = True
                        resp.keys = theseKeys.name 
                        resp.rt = theseKeys.rt 
                        print(f'resp.rt: {resp.rt}')
                        if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                            resp.corr = 1
                            
                            print(f"{resp.corr}: correct")
                            print(f"key: {resp.keys}")
                        else:
                            resp.corr = 0
                            print(f"{resp.corr}: incorrect")
                            print(f"key: {resp.keys}")

                        # if resp.keys in ['', [], None]:
                        #     resp.corr = None

                        continueTrial = False

                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()

                if not continueTrial:
                    break

                continueTrial = False
                for thisComp in trialComps:
                    if hasattr(thisComp, "status") and thisComp.status != FINISHED:
                        continueTrial = True
                        break

                if continueTrial:
                    win.flip()

            for thisComp in trialComps:
                if hasattr(thisComp, "setAutoDraw"):
                    thisComp.setAutoDraw(False)
                # doing a for loop in order to set ALL flanks to autodraw false
                for flanker in flanker_stimuli:
                    flanker.setAutoDraw(False)
            
            # trials.addData('kb.keys', resp.keys)
            # trials.addData('kb.corr', resp.corr)
            # corr_list.append(resp.corr)
            # if resp.keys != None:
            #     trials.addData('kb.rt', resp.rt)
            #     block_RT_list.append(resp.rt)

            if resp.keys in ['', [], None]:
                resp.keys = 'NaN'
                trials.addData('kb.keys', resp.keys)
                trials.addData('kb.corr', resp.corr)
            else:
                trials.addData('kb.keys', resp.keys)
                trials.addData('kb.corr', resp.corr)
                corr_list.append(resp.corr)
            if resp.keys != None and resp.keys != 'NaN':
                trials.addData('kb.rt', resp.rt)
                block_RT_list.append(resp.rt)
            else:
                resp.rt = 'NaN'
                trials.addData('kb.rt', resp.rt)
        
            feedbackTimer.reset()
            # ---------- PREPARING FEEDBACK ----------- #
            t = 0
            feedbackClock.reset()
            frameN = -1
            continueTrial = True
            feedbackTimer.add(1)
            print(f'resp corr: {resp.corr}')
            if resp.corr == 1:
                msg = "Correct! Good job!"
            else:
                msg = ""

            feedbackText.setText(msg)

            feedbackComps = [feedbackText]
            for thisComp in feedbackComps:
                    thisComp.tStart = None
                    thisComp.tStop = None
                    thisComp.tStartRefresh = None
                    thisComp.tStopRefresh = None
                    if hasattr(thisComp, 'status'):
                        thisComp.status = NOT_STARTED

            # ---------- STARTING FEEDBACK ---------- #
            while continueTrial and feedbackTimer.getTime() > 0:
                t = feedbackClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and feedbackText.status == NOT_STARTED:
                    feedbackText.tStart = t 
                    feedbackText.frameNStart = frameN
                    win.timeOnFlip(feedbackText, 'tStartRefresh')
                    feedbackText.setAutoDraw(True)

                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit

                if not continueTrial:
                    break

                continueTrial = False
                for thisComp in feedbackComps:
                    if hasattr(thisComp, "status") and thisComp.status != FINISHED:
                        continueTrial = True
                        break

                if continueTrial:
                    win.flip()

            for thisComp in feedbackComps:
                if hasattr(thisComp, "setAutoDraw"):
                    thisComp.setAutoDraw(False)

            thisExp.nextEntry()


    # --------------- LAUNCHING GROUP C: FB EVERY TIME ---------------- #

    if fixedExpInfo['group'] == 'C':
        print('launching group C')

        for thisTrial in trials:
            currentLoop = trials
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            # ------Prepare to start Routine "trial"-------
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            continueTrial = True
            tooSlowFlag = False
            no_response_flag = False
            resp = keyboard.Keyboard()
            resp.clearEvents(eventType='keyboard')

            # update w/ new params every repeat
            # using conds from xls files (so magical!)
            for flanker in flanker_stimuli:
                flanker.text = arrowChars[flankerDirc]

            target_arrow.text = arrowChars[targetDirc]

            trialComps = [flanker, target_arrow, resp]
            for thisComp in trialComps:
                thisComp.tStart = None
                thisComp.tStop = None
                thisComp.tStartRefresh = None
                thisComp.tStopRefresh = None
                if hasattr(thisComp, 'status'):
                    thisComp.status = NOT_STARTED

            

            while continueTrial:
                t = trialClock.getTime()
                
                frameN = frameN + 1 
                
                if t >= 0.5:
                    fixationText.setAutoDraw(True)

                if t >= 1.0:
                    fixationText.setAutoDraw(False)
                    win.flip()

                if t >= 1.5:
                    # doing a for loop to set autodraw true to ALL flanks
                    for flanker in flanker_stimuli:
                        flanker.setAutoDraw(True)

                if t >= 2.0 and target_arrow.status == NOT_STARTED:
                    target_arrow.tStart = t
                    target_arrow.frameNStart = frameN
                    win.timeOnFlip(target_arrow, 'tStartRefresh')
                    target_arrow.setAutoDraw(True)

                if t >= 2.0 and resp.status == NOT_STARTED:
                    resp.tStart = t 
                    resp.frameNStart = frameN
                    win.timeOnFlip(resp, 'tStartRefresh')
                    resp.status = STARTED
                    win.callOnFlip(resp.clock.reset)
                    resp.clearEvents(eventType='keyboard')

                if t >= 4.0:
                    no_response_flag = True
                    target_arrow.setAutoDraw(False)
                    for flanker in flanker_stimuli:
                        flanker.setAutoDraw(False)
                    tooSlowStim.setAutoDraw(True)
                    tooSlowFlag = True

                if t >= 5.0:
                    tooSlowStim.setAutoDraw(False)
                    continueTrial = False


                f = 0
                feedbackClock.reset()
                trialTimer.reset()

                # adding no_response_flag makes sure keypresses and rts
                # won't be recorded after too-slow appears
                if resp.status == STARTED and no_response_flag != True:
                    theseKeys = resp.getKeys(keyList=respKeys, waitRelease=False)
                    if len(theseKeys):
                        theseKeys = theseKeys[0]
                        if "escape" == theseKeys:
                            endExpNow = True
                        resp.keys = theseKeys.name 
                        resp.rt = theseKeys.rt 
                        print(f'resp.rt: {resp.rt}')
                        if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                            resp.corr = 1
                            
                            print(f"{resp.corr}: correct")
                            print(f"key: {resp.keys}")
                        else:
                            resp.corr = 0
                            print(f"{resp.corr}: incorrect")
                            print(f"key: {resp.keys}")

                        # if resp.keys in ['', [], None]:
                        #     resp.corr = None

                        continueTrial = False

                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit()

                if not continueTrial:
                    break

                continueTrial = False
                for thisComp in trialComps:
                    if hasattr(thisComp, "status") and thisComp.status != FINISHED:
                        continueTrial = True
                        break

                if continueTrial:
                    win.flip()

            for thisComp in trialComps:
                if hasattr(thisComp, "setAutoDraw"):
                    thisComp.setAutoDraw(False)
                # doing a for loop in order to set ALL flanks to autodraw false
                for flanker in flanker_stimuli:
                    flanker.setAutoDraw(False)
            
            # trials.addData('kb.keys', resp.keys)
            # trials.addData('kb.corr', resp.corr)
            # corr_list.append(resp.corr)
            # if resp.keys != None:
            #     trials.addData('kb.rt', resp.rt)
            #     block_RT_list.append(resp.rt)

            if resp.keys in ['', [], None]:
                resp.keys = 'NaN'
                trials.addData('kb.keys', resp.keys)
                trials.addData('kb.corr', resp.corr)
            else:
                trials.addData('kb.keys', resp.keys)
                trials.addData('kb.corr', resp.corr)
                corr_list.append(resp.corr)
            if resp.keys != None and resp.keys != 'NaN':
                trials.addData('kb.rt', resp.rt)
                block_RT_list.append(resp.rt)
            else:
                resp.rt = 'NaN'
                trials.addData('kb.rt', resp.rt)
                
            feedbackTimer.reset()

            # ---------- PREPARING FEEDBACK ----------- #
            t = 0
            feedbackClock.reset()
            frameN = -1
            continueTrial = True
            feedbackTimer.add(1)
            print(f'resp corr: {resp.corr}')
            print(f'too slow flag: {tooSlowFlag}')
            # flag prevents "good job" from showing after "too slow"
            if resp.corr or tooSlowFlag == False:
                msg = "Good job!"
            else:
                msg = ''

            feedbackText.setText(msg)

            feedbackComps = [feedbackText]
            for thisComp in feedbackComps:
                    thisComp.tStart = None
                    thisComp.tStop = None
                    thisComp.tStartRefresh = None
                    thisComp.tStopRefresh = None
                    if hasattr(thisComp, 'status'):
                        thisComp.status = NOT_STARTED

            # ---------- STARTING FEEDBACK ---------- #
            while continueTrial and feedbackTimer.getTime() > 0:
                t = feedbackClock.getTime()
                frameN = frameN + 1
                if t >= 0.0 and feedbackText.status == NOT_STARTED:
                    feedbackText.tStart = t 
                    feedbackText.frameNStart = frameN
                    win.timeOnFlip(feedbackText, 'tStartRefresh')
                    feedbackText.setAutoDraw(True)

                if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                    core.quit

                if not continueTrial:
                    break

                continueTrial = False
                for thisComp in feedbackComps:
                    if hasattr(thisComp, "status") and thisComp.status != FINISHED:
                        continueTrial = True
                        break

                if continueTrial:
                    win.flip()

            for thisComp in feedbackComps:
                if hasattr(thisComp, "setAutoDraw"):
                    thisComp.setAutoDraw(False)

            thisExp.nextEntry()

    
    if blocks.thisTrialN == 2:
        break

    # get stimulus params names
    if trials.trialList in ([], [None], None):
        params = []
    else:
        params = trials.trialList[0].keys()

# -------------- "Thanks" Routine ------------------ #
t = 0
thanksClock.reset()
frameN = -1
continueTrial = True
thanksresp = keyboard.Keyboard()

thanksComp = [thanksText, thanksresp]
for thisComp in thanksComp:
    thisComp.tStart = None
    thisComp.tStop = None
    thisComp.tStartRefresh = None
    thisComp.tStopRefresh = None
    if hasattr(thisComp, 'status'):
        thisComp.status = NOT_STARTED

while continueTrial:
    t = thanksClock.getTime()
    frameN = frameN + 1

    if t >= 0 and thanksText.status == NOT_STARTED:
        thanksText.tStart = t 
        thanksText.frameNStart = frameN
        win.timeOnFlip(thanksText, 'tStartRefresh')
        thanksText.setAutoDraw(True)

    if t >= 0 and thanksresp.status == NOT_STARTED:
        thanksresp.tStart = t 
        thanksresp.frameNStart = frameN
        win.timeOnFlip(thanksresp, 'tStartRefresh')
        thanksresp.status = STARTED
        thanksresp.clearEvents(eventType='keyboard')

    if thanksresp.status == STARTED:
        theseKeys = thanksresp.getKeys(keyList=['escape'], waitRelease=False)
        if len(theseKeys):
            theseKeys = theseKeys[0]
            continueTrial = False

    if not continueTrial:
        break
    continueTrial = False

    for thisComp in thanksComp:
        if hasattr(thisComp, 'status') and thisComp.status != FINISHED:
            continueTrial = True
            break

    if continueTrial:
        win.flip()

for thisComp in thanksComp:
    if hasattr(thisComp, "setAutoDraw"):
            thisComp.setAutoDraw(False)


# win.flip()

thisExp.saveAsWideText(fileName + '.csv')
thisExp.abort()
win.close()
core.quit()

