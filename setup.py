import json
import os
import numpy as np
import shutil

# 1. setup
np.random.seed(2) # for the sake of reproducibility
dirs = ['1-submissions','2-assignments','3-reviews','4-feedback','5-marks']
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
nomarker = np.zeros(shape=(nb,n)).astype(bool)
for b in range(nb):
    for s in range(n):
        nomarker[b][s] = s not in block[b]

# m = marker
# nmarked = number of times each student has been marked
# block = block design
# done = logical vector showing which block entries have already been used
def nextblock(m,nmarked,block,done):
    n = len(nmarked)
    nb = len(block)
    # 1. count the number of marks per block
    marksperblock = np.zeros(nb,dtype=int)
    for i in range(nb):
        b = block[i]
        for s in b:
            if s < n:
                marksperblock[i] += nmarked[s]
    # 2. loop through the rows of the block and find the 
    #    most undersampled one that does not contain the marker
    out = k+1
    nmarks = max(marksperblock)
    for i in range(nb):
        if (m not in block[i]) and (marksperblock[i]<nmarks) and (not done[i]):
            nmarks = marksperblock[i]
            out = i
    return(out)

pairs = np.zeros(shape=(n,k)).astype(int) # peers for each marker
done = np.zeros(nb,dtype=bool) # blocks that are done
nmarked = np.zeros(n,dtype=int) # number of times each student has been marked
for m in range(n): # loop through the markers
    bi = nextblock(m,nmarked,block,done)
    done[bi] = True
    b = block[bi]
    goodpeers = b[b<n]
    ngp = len(goodpeers)
    nchoices = min(ngp,k)
    chosenpeers = np.random.choice(goodpeers,size=nchoices,replace=False)
    if ngp < k:
        otherpeers = np.setdiff1d(np.arange(n),np.append(chosenpeers,m))
        randompeers = np.random.choice(otherpeers,size=k-ngp,replace=False)
        chosenpeers = np.append(chosenpeers,randompeers)
    pairs[m,:] = chosenpeers
    for j in chosenpeers:
        nmarked[j] += 1

# anonymise the assignments
aliases = np.arange(n)# + 1
#np.random.shuffle(aliases) # anonymise the submissions

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
