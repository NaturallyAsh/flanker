# Current flanker build as of 9/24/19


import psychopy 
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
nIntervals = 500
nTrials = 6
nSplit = 3
randomizeBlocks = True
flankerDur = 0.080
targetDur = 0.030
respDur = 1.4
respKeys = ['z', 'm']
arrowNames = ['Left', 'Right']
rtDeadline = 3.000      # responses after this time will be considered too slow (in seconds)
rtTooSlowDur = 0.600    # duration of 'too slow!' message (in seconds)
arrowChars = ["\u2190","\u2192"]
expName = 'Flanker Test'
instructions = "Press the key that matches the arrow in the CENTER -- try to ignore all other arrows. \n \
                \n Press on z if the arrow points to the left.\n\
                \n Press on m if the arrow points to the right.\n\
                \n Press the SPACEBAR to start the test."

dateStr = time.strftime("%b_%d_%H%M", time.localtime())
expInfo = {'participant': '', 'session': 1}
dlg = gui.DlgFromDict(dictionary=expInfo, title = expName)
if dlg.OK:
    #save params to file for next time
    #toFile('lastParams.pickle', expInfo)
    print('ok')
else:
    core.quit() #the user hit cancel so exit

expInfo['date'] = dateStr
expInfo['expName'] = expName

fileName = expInfo['participant'] + dateStr
globalClock = core.Clock()
logging.setDefaultClock(globalClock)

#logging file
logFileName = 'MyTestFlanker-%s-%s' % (expInfo['participant'], dateStr)
logging.LogFile((logFileName + '.log'), level=logging.INFO)
logging.log(level=logging.INFO, msg='---START PARAMS---')
logging.log(level=logging.INFO, msg='participant: %s' % expInfo['participant'])
logging.log(level=logging.INFO, msg='session: %s' % expInfo['session'])
logging.log(level=logging.INFO, msg='date: %s' % dateStr)
logging.log(level=logging.INFO, msg='respKeys: %s' % respKeys)



endExpNow = False #flag for 'escape' from exp

# Handles exp data as a whole. 
thisExp = data.ExperimentHandler(
        name=expName,
        extraInfo=expInfo,
        savePickle=True,
        saveWideText=True,
        dataFileName=fileName)

# Start Code - runs before window

widthPix = 800
heightPix = 600
mon = monitors.Monitor('test', width=53.1, distance=60.)
mon.setSizePix((widthPix, heightPix))
win = visual.Window(
    monitor=mon,
    size=(widthPix, heightPix),
    colorSpace='rgb',
    allowGUI=False,
    units='deg')

# if i want to keep track of frames for measuring RT
win.recordFrameIntervals = True

#Changing the font to Arial fixed the right arrow problem.
target_arrow = visual.TextStim(win, 
    pos=[0,0], 
    color='#000000',
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
    color='#000000',
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

pauseText = visual.TextStim(win,
    name='pause',
    text='break for 30 seconds',
    font='Arial',
    color='black', colorSpace='rgb',
    )

feedbackText = visual.TextStim(win,
    name='feedback',
    text='Test feedback',
    font='Arial',
    color='black',
    colorSpace='rgb'
    )

lastRoundFeedbackText = visual.TextStim(win,
    name='last feedback',
    text='Test feedback',
    font='Arial',
    color='black',
    colorSpace='rgb'
    )

# Created some handy clocks and timers to keep track of blocks and trials
trialTimer = core.CountdownTimer()
pauseTimer = core.CountdownTimer()
pauseClock = core.Clock()
feedbackClock = core.Clock()
lastFeedbackClock = core.Clock()
trialClock = core.Clock()
instructClock = core.Clock()
blockClock = core.Clock()


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

# -----Start Instuctions------
while continueTrial:
    # print('continuing')
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

    # print(f'keyboard status: {ready.status}')
    if ready.status == STARTED:
        theseKeys = ready.getKeys(keyList=["space"], waitRelease=False)
        # print(len(theseKeys))
        # print(theseKeys)
        if len(theseKeys):
            theseKeys = theseKeys[0]

            if "escape" == theseKeys:
                endExpNow = True
            # print('not continuing')
            continueTrial = False
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        print('core quit')
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

blockClock.reset()

blocks = data.TrialHandler(
    nReps=1,
    method='random',
    extraInfo=expInfo,
    originPath=1,
    trialList=data.importConditions('block_params.xlsx'),
    seed=None,
    name='blocks')
thisExp.addLoop(blocks)
thisBlock = blocks.trialList[0]

if thisBlock != None:
    for paramName in thisBlock:
        exec('{} = thisBlock[paramName]'.format(paramName))

for thisBlock in blocks:
    currentLoop = blocks
    block_RT_list = []
    corr_list = []

    block_RT_list.clear()
    corr_list.clear()

    if thisBlock != None:
        for paramName in thisBlock:
            exec('{} = thisBlock[paramName]'.format(paramName))


    trials = data.TrialHandler(nReps=1,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=data.importConditions(condsFile),
            seed=None,
            name='trials')
    thisExp.addLoop(trials)
    thisTrial = trials.trialList[0]

    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))

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

        # update w/ new params every repeat
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
            # print('continuing')
            t = trialClock.getTime()
            # print(f'thisComp status: {thisComp.status}')
            # print(f't = {t}')
            # print(t)
            frameN = frameN + 1 
            # print(f'frame = {frameN}')
            # print(frameN)

            if t >= 0.5:
                fixationText.setAutoDraw(True)
            if t >= 3.0:
                fixationText.setAutoDraw(False)
                win.flip()
            if t >= 3.0:
                # doing a for loop to set autodraw true to ALL flanks
                for flanker in flanker_stimuli:
                    # win.timeOnFlip(flanker, 'tStartRefresh')
                    flanker.setAutoDraw(True)

            if t >= 4.0 and target_arrow.status == NOT_STARTED:
                target_arrow.tStart = t
                target_arrow.frameNStart = frameN
                win.timeOnFlip(target_arrow, 'tStartRefresh')
                target_arrow.setAutoDraw(True)

            if t >= 4.0 and resp.status == NOT_STARTED:
                resp.tStart = t 
                resp.frameNStart = frameN
                win.timeOnFlip(resp, 'tStartRefresh')
                resp.status = STARTED
                win.callOnFlip(resp.clock.reset)
                resp.clearEvents(eventType='keyboard')

            if t >= 7.0:
                target_arrow.setAutoDraw(False)
                for flanker in flanker_stimuli:
                    flanker.setAutoDraw(False)
                tooSlowStim.setAutoDraw(True)

            if t >= 8.5:
                tooSlowStim.setAutoDraw(False)
                continueTrial = False

            # print(f'resp status: {resp.status}')

            if resp.status == STARTED:
                theseKeys = resp.getKeys(keyList=respKeys, waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]

                    if "escape" == theseKeys:
                        endExpNow = True
                    resp.keys = theseKeys.name 
                    resp.rt = theseKeys.rt 

                    if (resp.keys == str(corrAns)) or (resp.keys == corrAns):
                        resp.corr = 1
                        print(f"{resp.corr}: correct")
                        print(f"key: {resp.keys}")
                    else:
                        resp.corr = 0
                        print(f"{resp.corr}: incorrect")
                        print(f"key: {resp.keys}")

                    if resp.keys in ['', [], None]:
                        resp.corr = None

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

        
        trials.addData('kb.keys', resp.keys)
        trials.addData('kb.corr', resp.corr)
        corr_list.append(resp.corr)
        if resp.keys != None:
            trials.addData('kb.rt', resp.rt)
            block_RT_list.append(resp.rt)
            # print(f"kb RT: {kb.rt}")
        thisExp.nextEntry()

    if blocks.thisTrialN == 2:
        # if this is the end of the 2nd block...
        break
    elif blocks.thisTrialN == 0:
        # Prepare to start "Feedback" routine
        fb = keyboard.Keyboard()
        fb.clearEvents()
        # event.clearEvents()
        frameN = -1
        t = 0
        waiting = True
        feedbackClock.reset()
        feedbackComps = [feedbackText, fb]
        for thisFbComp in feedbackComps:
            thisFbComp.tStart = None
            thisFbComp.tStop = None 
            thisFbComp.tStartRefresh = None 
            thisFbComp.tStopRefresh = None 
            if hasattr(thisFbComp, 'status'):
                thisFbComp.status = NOT_STARTED

        rt_array = np.array(block_RT_list)
        corr_array = np.array(corr_list)
        fc_mean_rt = rt_array.mean()
        corr_sum = corr_array.sum()

        txt = 'Good Job!\n\n'
        txt += ('You got {} correct out of 12\n\n'.format(corr_sum))
        txt += ('Your average reaction time was {0:.2f} seconds\n\n'.format(fc_mean_rt))
        txt += 'Try to be as quick and accurate as possible\n\n'
        txt += 'Get ready for the next round!\n\n\n'
        txt += 'Press ENTER when ready'


        while waiting:
            # print('waiting top true')
            fb.clearEvents()
            t = feedbackClock.getTime()
            frameN = frameN + 1
            # print(f'feedback status: {feedbackText.status}')
            if t >= 0.5 and feedbackText.status == NOT_STARTED:
                feedbackText.tStart = t
                feedbackText.frameNStart = frameN
                win.timeOnFlip(feedbackText, 'tStartRefresh')
                feedbackText.setText(txt)
                feedbackText.setAutoDraw(True)

            # print(block_RT_list)
            if t >= 1.5 and fb.status == NOT_STARTED:
                fb.tStart = t
                fb.frameNStart = frameN
                win.timeOnFlip(fb, 'tStartRefresh')
                fb.status = STARTED
                fb.clearEvents(eventType='keyboard')

            # print(f'fb status: {fb.status}')
            if fb.status == STARTED:
                theseKeys = fb.getKeys(keyList=["return"], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]
                    print(f'key pressed: {theseKeys}')    

                    if "escape" == theseKeys:
                        endExpNow = True
                    waiting = False 
                    print('waiting keyboard false')

            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit

            if not waiting:
                print('waiting false. break')
                break

            waiting = False
            # print('waiting false. after if not waiting')

            # print(f'fb status before fbComp: {fb.status}')
            for thisFbComp in feedbackComps:
                # print(f'comp status: {thisFbComp.status}')

                if hasattr(thisFbComp, "status") and thisFbComp.status != FINISHED:
                    waiting = True
                    # print('waiting true. this comp')
                    break

            if waiting:
                win.flip()
                # print('waiting, flip')

        for thisFbComp in feedbackComps:
            if hasattr(thisFbComp, "setAutoDraw"):
                thisFbComp.setAutoDraw(False)

    elif blocks.thisTrialN == 1:
        lfb = keyboard.Keyboard()
        lfb.clearEvents()
        # event.clearEvents()
        frameN = -1
        t = 0
        waiting = True
        lastFeedbackClock.reset()
        lastFeedbackComps = [lastRoundFeedbackText, lfb]
        for thisComp in lastFeedbackComps:
            thisComp.tStart = None
            thisComp.tStop = None 
            thisComp.tStartRefresh = None 
            thisComp.tStopRefresh = None 
            if hasattr(thisComp, 'status'):
                thisComp.status = NOT_STARTED

        rt_array = np.array(block_RT_list)
        corr_array = np.array(corr_list)
        fc_mean_rt = rt_array.mean()
        corr_sum = corr_array.sum()

        txt = 'Good Job!\n\n'
        txt += ('You got {} correct out of 12\n\n'.format(corr_sum))
        txt += ('Your average reaction time was {0:.2f} seconds\n\n'.format(fc_mean_rt))
        txt += 'Get ready for the final round!!!\n\n\n'
        txt += 'Press ENTER when ready'



        while waiting:
            # print('waiting top true')
            lfb.clearEvents()
            t = lastFeedbackClock.getTime()
            frameN = frameN + 1
            # print(f'feedback status: {feedbackText.status}')
            if t >= 0.5 and lastRoundFeedbackText.status == NOT_STARTED:
                lastRoundFeedbackText.tStart = t
                lastRoundFeedbackText.frameNStart = frameN
                win.timeOnFlip(lastRoundFeedbackText, 'tStartRefresh')
                lastRoundFeedbackText.setText(txt)
                lastRoundFeedbackText.setAutoDraw(True)

            # print(block_RT_list)
            if t >= 1.5 and lfb.status == NOT_STARTED:
                lfb.tStart = t
                lfb.frameNStart = frameN
                win.timeOnFlip(lfb, 'tStartRefresh')
                lfb.status = STARTED
                lfb.clearEvents(eventType='keyboard')

            # print(f'fb status: {fb.status}')
            if lfb.status == STARTED:
                theseKeys = lfb.getKeys(keyList=["return"], waitRelease=False)
                if len(theseKeys):
                    theseKeys = theseKeys[0]
                    # print(f'key pressed: {theseKeys}')    

                    if "escape" == theseKeys:
                        endExpNow = True
                    waiting = False 
                    # print('waiting keyboard false')

            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit

            if not waiting:
                # print('waiting false. break')
                break

            waiting = False
            # print('waiting false. after if not waiting')

            # print(f'fb status before fbComp: {fb.status}')
            for thisComp in lastFeedbackComps:
                if hasattr(thisComp, "status") and thisComp.status != FINISHED:
                    waiting = True
                    break

            if waiting:
                win.flip()

        for thisComp in lastFeedbackComps:
            if hasattr(thisComp, "setAutoDraw"):
                thisComp.setAutoDraw(False)

        # pauseTimer.reset()

        # # Prepare to start "Pause" routine
        # t = 0
        # pauseClock.reset()
        # frameN = -1
        # continueTrial = True
        # # will update with 30 secs later
        # pauseTimer.add(5.0)

        # pauseComps = [pauseText]
        # for thisComp in pauseComps:
        #     thisComp.tStart = None
        #     thisComp.tStop = None 
        #     thisComp.tStartRefresh = None 
        #     thisComp.tStopRefresh = None 
        #     if hasattr(thisComp, 'status'):
        #         thisComp.status = NOT_STARTED

        # while pauseTimer.getTime() > 0:
        #     t = pauseClock.getTime()
        #     frameN = frameN + 1

        #     if t >= 0.0: 
        #         pauseText.draw()
        #         win.logOnFlip(level=logging.EXP, msg='Display pause time')

        #     if endExpNow or defaultKeyboard.getKeys(keyList=['escape']):
        #         core.quit

        #     win.flip()


    # get stimulus params names
    if trials.trialList in ([], [None], None):
        params = []
    else:
        params = trials.trialList[0].keys()

win.flip()
# save data for this loop
# trials.saveAsExcel(fileName + '.xlsx',
#     sheetName='trials',
#     stimOut=params,
#     dataOut=['n', 'all_mean', 'all_std', 'all_raw'])
thisExp.saveAsExcel(fileName + '.xlsx')

thisExp.abort()
win.close()
core.quit()


# def runTrial(targetDir, flankerDir):
#     continueTrial = True

#     # while continueTrial:

#     event.clearEvents()
#     fixation.draw()
#     win.logOnFlip(level=logging.EXP, msg='Display Fixation')
#     win.flip()
#     core.wait(1.0)
    
# #   get trial time
#     tTrial = globalClock.getTime()
#     # print(f'tTrial {tTrial}')
#     timer = core.Clock()
    
# #    display flankers
#     for flanker in flanker_stimuli:
#         flanker.text = arrowChars[flankerDir]
#         flanker.draw()
#     win.logOnFlip(level=logging.EXP, msg=
#         'Display %s Flankers'%arrowNames[flankerDir])
#     win.flip()
#     core.wait(2.0)
    
# #   display flankers AND target arrow
#     for flanker in flanker_stimuli:
#         flanker.draw()
#     target_arrow.text = arrowChars[targetDir]
#     target_arrow.draw()
#     trialClock.reset()
#     win.logOnFlip(level=logging.EXP, msg=
#         'Display %s Target'%arrowNames[targetDir])
#     win.flip()
#     event.clearEvents()
#     timer.reset()
#     kb.clock.reset()
#     waitAllKeys = event.waitKeys()[0]
#     print("wait all keys")
#     # kb.status = STARTED
#     core.wait(2.0)
    
#     getAllKeys = kb.getKeys(keyList= respKeys, waitRelease=False)  
#     print(len(getAllKeys))  
#     # if len(getAllKeys):
#     #     getAllKeys = getAllKeys[0]
#     #     continueTrial = False

#     win.logOnFlip(level=logging.EXP, msg='Display Blank')
#     win.flip()
#     core.wait(2.0)
    

#     return (tTrial, getAllKeys)

# trials = data.TrialHandler(nReps=1.0,
#         method='random',
#         extraInfo=expInfo,
#         originPath=-1,
#         trialList=data.importConditions('flanker_trial_params.xlsx'),
#         seed=None,
#         name='trials')
# thisExp.addLoop(trials)
# thisTrial = trials.trialList[0]
# tkb = keyboard.Keyboard()

# if thisTrial != None:
#         for paramName in thisTrial:
#             exec('{} = thisTrial[paramName]'.format(paramName))

# for thisTrial in trials:
#     tkb.clearEvents()
#     currentLoop = trials
#     if thisTrial != None:
#         for paramName in thisTrial:
#             exec('{} = thisTrial[paramName]'.format(paramName))

#     flankerDir = flankerDirc
#     targetDir = targetDirc

#     [tTrial, allKeys] = runTrial(targetDir, flankerDir)

#     if len(allKeys):
#         allKeys = allKeys[0]

#         tkb.keys = allKeys.name
#         tkb.rt = allKeys.rt * 1000

#         if (tkb.keys == str(corrAns)) or (tkb.keys == corrAns):
#             tkb.corr = 1
#             print(f"{tkb.corr}: correct")
#             print(f"key: {tkb.keys}")
#         else:
#             tkb.corr = 0
#             print(f"{tkb.corr}: incorrect")
#             print(f"key: {tkb.keys}")

#     if tkb.keys in ['', [], None]:
#         tkb.corr = None

#     trials.addData('kb.keys', tkb.keys)
#     trials.addData('kb.corr', tkb.corr)
#     if tkb.keys != None:
#         trials.addData('kb.rt', tkb.rt)
#         # print(f"kb RT: {kb.rt}")

#     thisExp.nextEntry()

# # get stimulus params names
# if trials.trialList in ([], [None], None):
#     params = []
# else:
#     params = trials.trialList[0].keys()

# # save data for this loop
# trials.saveAsExcel(fileName + '.xlsx',
#     sheetName='trials',
#     stimOut=params,
#     dataOut=['n', 'all_mean', 'all_std', 'all_raw'])

# thisExp.abort()
# win.close()
# core.quit()

