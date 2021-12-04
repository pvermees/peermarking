require(PlayerRatings)

dirs <- c('1-submissions','2-assignments','3-reviews','4-feedback','5-marks')

readfeedback <- FALSE

# 1. parse the review files
ranks <- list()
feedback <- list()
for (m in submissions){
    ranks[[m]] <- list(alias=NULL,student=NULL,rank=NULL)
    feedbackfile <- paste0(dirs[3],'/',m)
    con <- file(feedbackfile, "r")
    for (line in readLines(con)){
        if (grepl('File name:',line)){
            string <- strsplit(line,'\\.')[[1]][1]
            a <- tail(strsplit(string,' ')[[1]],1)
            s <- submissions[which(aliases %in% a)]
            ranks[[m]]$alias <- c(ranks[[m]]$alias,a)
            ranks[[m]]$student <- c(ranks[[m]]$student,s)
        }
        if (grepl('Rank:',line)){
            string <- strsplit(line,'/')[[1]][1]
            r <- as.numeric(tail(strsplit(string,' ')[[1]],1))
            ranks[[m]]$rank <- c(ranks[[m]]$rank,r)
        }
        if (readfeedback){
            if (grepl('----------------',line)){
                feedback[[s]] <- paste0(feedback[[s]],comments)
                readfeedback <- FALSE
            } else {
                comments <- paste0(comments,line,'\n')
            }
        }
        if (grepl('Feedback:',line)){
            readfeedback <- TRUE
            comments <- strsplit(line,'Feedback:')[[1]][2]
        }
    }
    close(con)
}

# 2. feedback files
for (s in names(feedback)){
    feedbackfile <- paste0(dirs[4],'/',s)
    write(feedback[[s]],file=feedbackfile)
}

# 3. PGF file
PGF <- ''
for (m in names(ranks)){
    i <- order(ranks[[m]]$rank)
    part1 <- paste0(PGF,'task1 ',s,' ')
    part2 <- paste(ranks[[m]]$student[i],collapse=' > ')
    part3 <- '\n'
    PGF <- paste0(part1,part2,part3)
    write(PGF,file=paste0(dirs[5],'/ranks.pgf'))
}

# 4. Elo table
nr <- n*k*(k-1)/2
tt <- rep(0,nr)
p1 <- NULL
p2 <- NULL
score <- NULL
for (m in submissions){
    r <- ranks[[m]]
    for (i in 1:(k-1)){
        for (j in (i+1):k){
            p1 <- c(p1,r$student[i])
            p2 <- c(p2,r$student[j])
            if (r$rank[i]>r$rank[j]){
                score <- c(score,0)
            } else if (r$rank[i]<r$rank[j]){
                score <- c(score,1)
            } else {
                score <- c(score,1/2)
            }
        }
    }
}
ELO <- data.frame(time=tt,p1=p1,p2=p2,score=score,stringsAsFactors=FALSE)
rating <- elo(ELO)
write.table(rating$ratings,file=paste0(dirs[5],'/elo.txt'))
