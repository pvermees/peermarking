import os
import numpy as np
import shutil

dirs = ['1-submissions','2-assignments','3-reviews','4-feedback','5-marks']

readfeedback = False

# 1. parse the review files
ranks = dict()
feedback = dict()
for marker in submissions:
    ranks[marker] = dict(alias=[],student=[],rank=[])
    feedbackfile = os.path.join(dirs[2],marker)
    f = open(feedbackfile,'r')
    lines = f.readlines()
    for line in lines:
        i = line.find('File name:')
        if (i>=0):
            bits = line.split()
            for bit in bits:
                j = bit.find('.txt')
                if (j>=0):
                    alias = bit.split('.txt')[0]
                    ranks[marker]['alias'].append(alias)
                    i = int(np.where(aliases == int(alias))[0])
                    student = submissions[i]
                    ranks[marker]['student'].append(student)
                    if (not student in feedback):
                        feedback[student] = []
        i = line.find('Rank:')
        if (i>=0):
            bits = line.split()
            for bit in bits:
                j = bit.find('/')
                if (j>=0):
                    ranks[marker]['rank'].append(int(bit.split('/')[0]))
        if readfeedback:
            i = line.find('----------------')
            if (i>=0):
                feedback[student].append(comments)
                readfeedback = False
            else:
                comments += line
        i = line.find('Feedback:')
        if (i>=0):
            readfeedback = True
            comments = line.replace("Feedback:","")
    f.close()

# 2. feedback files
keys = list(feedback.keys())
for key in keys:
    feedbackfile = os.path.join(dirs[3],str(key))
    f = open(feedbackfile, 'w')
    for comment in feedback[key]:
        f.write(comment)
    f.close()
    
# 3. PGF file
PGF = ''
keys = list(ranks.keys())
for key in keys:
    PGF += 'task1 ' + str(key) + ' '
    nr = len(ranks[key]['rank'])
    for i in range(nr-1):
        r = ranks[key]['rank'][i]
        PGF += ranks[key]['student'][r-1] + ' > '
    PGF += ranks[key]['student'][nr-1] + '\n'
PGFfile = os.path.join(dirs[4],'ranks.pgf')
f = open(PGFfile, 'w')
f.write(PGF)
f.close()
