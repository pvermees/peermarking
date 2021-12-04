# 1. setup
set.seed(2)
dirs <- c('1-submissions','2-assignments','3-reviews','4-feedback','5-marks')
instructions <- 'instructions.txt'
k <- 5 # number of peers assigned to each student
submissions <- sort(list.files(dirs[1]))
n <- length(submissions)
blocks <- IsoplotR:::fromJSON(file='blocks.json')

# 2. find the appropriate block design
for (block in blocks){
    if ((length(block) >= k) & length(block) >= n){
        B <- block
        break
    }
}
block <- unname(t(as.data.frame(B))) + 1
overspill <- which(apply(block>n,1,'all'))
block <- block[-overspill,]
nb <- nrow(block)

# 3. assign the pairs
nextblock <- function(m,nmarked,block,done){
    n <- length(nmarked)
    nb <- nrow(block)
    # 1. count the number of marks per block
    marksperblock <- rep(0,nb)
    for (i in 1:nb){
        b <- block[i,]
        marksperblock[i] <- marksperblock[i] + sum(nmarked[b[b<n]])
    }
    # 2. loop through the rows of the block and find the 
    #    most undersampled one that does not contain the marker
    out <- ncol(block)+1
    nmarks <- max(marksperblock)
    hasm <- apply(apply(block,1,'%in%',m),2,'any')
    eligible <- cbind(1:nb,marksperblock)[!hasm,]
    i <- which.min(eligible[,2])
    eligible[i,1]
}
pairs <- matrix(0,n,k) # peers assigned to each marker
done <- rep(0,nb) # logical vector indicating which block entries have been used
nmarked <- rep(0,n) # number of times each student has been marked
for (m in 1:n){ # loop through the markers
    bi <- nextblock(m,nmarked,block,done)
    done[bi] <- TRUE
    b <- block[bi,]
    goodpeers <- b[b<n]
    ngp <- length(goodpeers)
    nchoices <- min(ngp,k)
    chosenpeers <- sample(goodpeers,size=nchoices,replace=FALSE)
    if (ngp < k){
        eligible <- cbind(1:n,nmarked)[-c(m,chosenpeers),]
        i <- order(eligible[,2])
        additionalpeers <- eligible[i[1:(k-ngp)],1]
        chosenpeers <- c(chosenpeers,additionalpeers)
    }
    pairs[m,] <- chosenpeers
    nmarked[chosenpeers] = nmarked[chosenpeers] + 1
}

# 5. anonymise the assignments
aliases <- sample(1:n,replace=FALSE)
#np.random.shuffle(aliases) # anonymise the submissions

# 6. copy the assignments
for (i in 1:n){
    path <- strsplit(submissions[i],split='\\.')[[1]]
    marker <- path[1]
    ext <- path[2]
    peers <- pairs[i,]
    dstdir <- paste0(dirs[2],'/',marker)
    if (!file.exists(dstdir)){
        dir.create(dstdir)
    }
    f <- paste0(dirs[2],'/',marker,'/feedback.txt')
    file.copy(instructions,f)
    for (j in 1:k){
        src <- paste0(dirs[1],'/',submissions[peers[j]])
        alias <- paste0(aliases[peers[j]],'.',ext)
        dst <- paste0(dirs[2],'/',marker,'/',alias)
        file.copy(src,dst)
        write(paste0('File name: ',alias,'\n'),file=f,append=TRUE)
        write(paste0('Rank:  ','/',k,'\n'),file=f,append=TRUE)
        write('Feedback:\n\n\n\n',file=f,append=TRUE)
        write(paste0('---------------------------------------------',
                     '---------------------------------------------\n'),
              file=f,append=TRUE)
    }
}
