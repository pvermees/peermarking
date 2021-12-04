dirs <- c('1-submissions','2-assignments','3-reviews','4-feedback','5-marks')

readfeedback <- FALSE

# 1. parse the review files
ranks <- list()
feedback <- list()
for (marker in submissions){
    ranks[[marker]] <- list(alias=NULL,student=NULL,rank=NULL)
    feedbackfile <- paste0(dirs[3],'/',marker)
    con <- file(feedbackfile, "r")
    for (line in readLines(con)){
        if (grepl('File name:',line)){
            string <- strsplit(line,'\\.')[[1]][1]
            a <- tail(strsplit(string,' ')[[1]],1)
            s <- submissions[which(aliases %in% a)]
            ranks[[marker]]$alias <- c(ranks[[marker]]$alias,a)
            ranks[[marker]]$student <- c(ranks[[marker]]$student,s)
        }
        if (grepl('Rank:',line)){
            string <- strsplit(line,'/')[[1]][1]
            r <- as.numeric(tail(strsplit(string,' ')[[1]],1))
            ranks[[marker]]$rank <- c(ranks[[marker]]$rank,r)
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
for (s in names(ranks)){
    i <- order(ranks[[s]]$rank)
    part1 <- paste0(PGF,'task1 ',s,' ')
    part2 <- paste(ranks[[s]]$student[i],collapse=' > ')
    part3 <- '\n'
    PGF <- paste0(part1,part2,part3)
    write(PGF,file=paste0(dirs[5],'/ranks.pgf'))
}
