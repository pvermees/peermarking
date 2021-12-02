import json
import os
import numpy as np
import shutil

# 1. setup
np.random.seed(2) # for the sake of reproducibility
dirs = ['1-submissions','2-assignments','3-reviews','4-feedback']
instructions = 'instructions.txt'
k = 5 # number of peers assigned to each student
submissions = sorted(os.listdir(dirs[0]))
n = len(submissions)
blocks = json.loads(open('blocks.json').read())

# 2. find the appropriate block design
for key in list(blocks.keys()):
    b = blocks.get(key)
    if len(b[1]) >= k and len(b) >= n:
        block = np.array(b)
        break

# 3. assign the pairs
aliases = np.arange(n)+1
np.random.shuffle(aliases) # anonymise the submissions
pairs = np.zeros(shape=(n,k)).astype(int)
nb = len(block)
j = np.arange(nb-1)
np.random.shuffle(j)
done = []
for ia in range(n): # loop through students/aliases
    alias = aliases[ia]
    for ib in range(nb-1): # loop through the block
        if not ib in done:
            peers = block[j[ib],:]
            goodpeers = peers[peers<n]
            ngp = len(goodpeers)
            nchoices = min(ngp,k)
            chosenpeers = np.random.choice(goodpeers,size=nchoices,replace=False)
            if ngp < k:
                otherpeers = np.setdiff1d(np.arange(n),np.append(chosenpeers,ia))
                randompeers = np.random.choice(otherpeers,size=k-ngp,replace=False)
                chosenpeers = np.concatenate([chosenpeers,randompeers])
            if not alias in chosenpeers:
                pairs[ia,:] = chosenpeers
                done.append(ib)
                break

# 4. copy the assignments
for i in range(n):
    path = os.path.splitext(os.path.basename(submissions[i]))
    marker = path[0]
    ext = path[1]
    peers = pairs[i,:]
    dstdir = os.path.join(dirs[1],marker)
    if not os.path.exists(dstdir):
        os.mkdir(dstdir)
    feedbackfile = os.path.join(dirs[1],marker,'feedback.txt')
    f = open(feedbackfile, 'a+')
    shutil.copy(instructions,feedbackfile)
    for j in range(k):
        src = os.path.join(dirs[0],submissions[peers[j]])
        alias = str(aliases[peers[j]]) + ext
        dst = os.path.join(dirs[1],marker,alias)
        shutil.copy(src,dst)
        f.write('File name: ' + alias + '\n\n')
        f.write('Rank:  ' + '/' + str(k) + '\n\n')
        f.write('Feedback:\n\n\n\n')
        f.write('---------------------------------------------')
        f.write('---------------------------------------------\n')
    f.close()
