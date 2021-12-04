set.seed(1) # for the sake of reproducibility

dirs <- c('1-submissions','2-assignments','3-reviews','4-feedback','5-marks')

for (dir in dirs) system(paste0('rm -rf ',dir,'/*'))

students <- c('Abigail','Alexander','Catarina','Giulio','Hantao',
              'James','Jiawei','Jordan','Joseph','Lin','Matthew',
              'Miriam','Morgan','Oscar','Sicun','Summer','Tang',
              'Thomas','Umit','Wei','William','Yinyu','Zara')

n <- length(students)
truerank <- 1:n

# 1. populate 1-submissions
for (i in 1:n){
    fname <- paste0(dirs[1],'/',students[i],'.txt')
    contents <- paste0('my true rank is ', truerank[i], ' out of ', n)
    f <- file(fname)
    write(contents,f)
    close(f)
}

# 2. populate 2-assignments
source('setup.R')

# 3. populate 3-reviews
feedback = c('outstanding','great','good','okay','bad')
for (i in 1:n){
    path <- strsplit(submissions[i],'\\.')[[1]]
    marker <- path[1]
    ext <- path[2]
    peers <- pairs[i,]
    r <- rank(truerank[peers])
    f <- paste0(dirs[3],'/',marker,'.',ext)
    file.copy(instructions,f)
    for (j in 1:k){
        alias <- paste0(aliases[peers[j]],'.',ext)
        write(paste0('File name: ',alias,'\n\n'),file=f,append=TRUE)
        write(paste0('Rank:  ',r[j],'/',k,'\n\n'),file=f,append=TRUE)
        write(paste0('Feedback: '),file=f,append=TRUE)
        write(paste0(feedback[r[j]],'\n\n'),file=f,append=TRUE)
        write(paste0('---------------------------------------------',
                     '---------------------------------------------\n'),
              file=f,append=TRUE)
    }
}

# 4. mark and rank
source('mark.R')
