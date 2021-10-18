import json
import os
import numpy as np
import shutil

# 1. setup
np.random.seed(1) # for the sake of reproducibility
dirs = ['1-submissions','2-assignments','3-reviews','4-feedback']
k = 5 # number of peers assigned to each student
submissions = os.listdir(dirs[0])
n = len(submissions)
blocks = json.loads(open('blocks.json').read())

# 2. find the appropriate block design
for key in list(blocks.keys()):
    b = blocks.get(key)
    if len(b[1]) >= k and len(b) >= n:
        block = np.array(b)
        break

# 3. assign the pairs
pairs = np.zeros(shape=(n,k)).astype(int)
nb = len(block)
j = np.arange(nb-1)
np.random.shuffle(j)
alias = []
for i in range(n):
    peers = block[j[i],:]
    goodpeers = peers[peers<n]
    ngp = len(goodpeers)
    nchoices = min(ngp,k)
    chosenpeers = np.random.choice(goodpeers,size=nchoices,replace=False)
    if ngp < k:
        otherpeers = np.setdiff1d(np.arange(n),chosenpeers)
        randompeers = np.random.choice(otherpeers,size=k-ngp,replace=False)
        chosenpeers = np.concatenate([chosenpeers,randompeers])
    pairs[i,:] = chosenpeers

# 4. copy and anonymise the assignments
aliases = np.arange(n)+1
np.random.shuffle(aliases)
for i in range(n):
    path = os.path.splitext(os.path.basename(submissions[i]))
    marker = path[0]
    ext = path[1]
    peers = pairs[i,:]
    feedbackfile = os.path.join(dirs[1],marker,'feedback.txt')
    shutil.copy('instructions.txt',feedbackfile)
    f = open(feedbackfile, 'a+')
    for j in range(k):
        src = os.path.join(dirs[0],submissions[peers[j]])
        dstdir = os.path.join(dirs[1],marker)
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        alias = str(aliases[peers[j]]) + ext
        dst = os.path.join(dirs[1],marker,alias)
        shutil.copy(src,dst)
        f.write('File name: ' + alias + '\n\n')
        f.write('Rank:  ' + '/' + str(k) + '\n\n')
        f.write('Feedback:\n\n\n\n')
        f.write('---------------------------------------------')
        f.write('---------------------------------------------\n')
    f.close()
