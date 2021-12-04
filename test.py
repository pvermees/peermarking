import os
import numpy as np
import shutil
import scipy.stats as ss

np.random.seed(1) # for the sake of reproducibility

dirs = ['1-submissions','2-assignments','3-reviews','4-feedback','5-marks']

for dir in dirs:
    os.system('rm -rf ' + dir + '/*')

students = ['Abigail','Alexander','Catarina','Giulio','Hantao',\
            'James','Jiawei','Jordan','Joseph','Lin','Matthew',\
            'Miriam','Morgan','Oscar','Sicun','Summer','Tang',\
            'Thomas','Umit','Wei','William','Yinyu','Zara']
n = len(students)
truerank = np.arange(0,n)+1
#np.random.shuffle(truerank)

# 1. populate 1-submissions
for i in range(n):
    file = os.path.join(dirs[0],students[i] + '.txt')
    f = open(file, 'a+')
    f.write('my true rank is ' + str(truerank[i]) + ' out of ' + str(n))
    f.close()

# 2. populate 2-assignments
exec(open("setup.py").read())

# 3. populate 3-reviews
feedback = ['outstanding','great','good','okay','bad']
for i in range(n):
    path = os.path.splitext(os.path.basename(submissions[i]))
    marker = path[0]
    ext = path[1]
    peers = pairs[i,:]
    ranks = ss.rankdata(truerank[peers])
    feedbackfile = os.path.join(dirs[2],marker + ext)
    f = open(feedbackfile, 'a+')
    shutil.copy(instructions,feedbackfile)
    for j in range(k):
        alias = str(aliases[peers[j]]) + ext
        f.write('File name: ' + alias + '\n\n')
        f.write('Rank:  ' + str(int(ranks[j])) + '/' + str(k) + '\n\n')
        f.write('Feedback: ')
        f.write(feedback[int(ranks[j])-1] + '\n\n')
        f.write('---------------------------------------------')
        f.write('---------------------------------------------\n')
    f.close()

# 3. extract the ranks
exec(open("mark.py").read())
