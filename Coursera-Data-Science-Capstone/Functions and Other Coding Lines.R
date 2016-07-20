options( java.parameters = "-Xmx4g" )
library(ggplot2)
library(dplyr)
library("tm")
library(RWeka)
setwd("~/downloads/final/en_US")
tokenize <- function(file_name){
    
    strings <- readLines(con =  file(file_name, "r", blocking = FALSE), n = 1000000)
    splited <- strsplit(strings, " ")
    unlisted <- unlist(splited)
    cleaned <- gsub("[[:punct:]]", "", unlisted)
    result <- tolower(cleaned)
    return (result)
}


profane_filter <- function(list){
    bad.words <- readLines("~/Google Drive/en_US/bad-words.txt")
    filtered <- subset(list, !(list %in% (intersect(bad.words,list))))
    return (filtered)
}

three_gram <- function(list) {
    op = vector()
    2 {
        
        if (i > 2) {
            g1 <- list[i]
            g2 <- list[i-1]
            g3 <- list[i-2]
            result <- paste(g3,g2,g1)
            op<- c(op, result)
        }
        
        
        else if (i == 2) {
            g1 <- list[i]
            g2 <- list[i-1]
            result <- paste(g2, g1)
            op <- c(op,result)
        }
        
        else op <- c(op, list[1])
        
    }
    return (op)
    
}
twitter <- tokenize("en_US.twitter.txt")
twitter_cleaned <- profane_filter(twitter)
strings <- readLines(con =  file("en_US.twitter.txt", "r", blocking = FALSE), n = 1000000)
two_gram_twitter <- NGramTokenizer(strings, Weka_control(min = 1, max = 2))
two_gram_twitter <- tolower(two_gram_twitter)
three_gram_twitter <- NGramTokenizer(strings, Weka_control(min = 3, max = 3))
three_gram_twitter <- tolower(three_gram_twitter)
onecount <- table(twitter_cleaned)
onecount <- sort(onecount, decreasing = TRUE)
onecount_sample <- onecount[1:10]
twocount <- table(two_gram_twitter)
twocount <- sort(twocount, decreasing = TRUE)
twocount_sample <- twocount[1:10]
threecount <- table(three_gram_twitter)
threecount <- sort(threecount, decreasing = TRUE)
threecount_sample <- threecount[1:10]

twitter_general <- readLines(con =  file('en_US.twitter.txt', "r", blocking = FALSE), n = -1)
blogs_general <- readLines(con =  file('en_US.blogs.txt', "r", blocking = FALSE), n = -1)
news_general <- readLines(con =  file('en_US.news.txt', "r", blocking = FALSE), n = -1)
total_dataset <- c(twitter_general, blogs_general, news_general)

# Hey, here is how you get the data working!
total_sample <- sample(total_dataset, 400000)

string_processing <- function(total_sample) { 
    total_sample <- lapply(total_sample, function(x) gsub("[[:punct:]]", "", x))
    total_sample <- lapply(total_sample, function(x) paste(x, '<e>', sep = " "))
    total_sample <- lapply(total_sample, function(x) tolower(x))
    total_sample <- lapply(total_sample, function(x) strsplit(x, " "))
    return(total_sample)
}
total_sample <- string_processing(total_sample)
total_sample <- unlist(total_sample)
sorted_unigram <- sort(table(total_sample), decreasing = TRUE)
#ct <- length(sorted_unigram) * .05
#common_words <- names(sorted_unigram[1:ct])
#total_splited <- total_sample[-(which(total_sample %in% common_words))]
#total <- paste(total, collapse = " ")
#sorted_unigram <- sort(table(total_splited), decreasing = TRUE)

total_sample_gram <- paste(total_sample, collapse = " ")
#bigram
library(RWeka)

bigram_set <- NGramTokenizer(total_sample_gram, Weka_control(min = 2, max = 2))
sorted_bigram <- sort(table(bigram_set), decreasing = TRUE)

#trigram
library(RWeka)

trigram_set <- NGramTokenizer(total_sample_gram, Weka_control(min = 3, max = 3))
sorted_trigram <- sort(table(trigram_set), decreasing = TRUE)


sentence = "The guy in front of me just bought a pound of bacon, a bouquet, and a case of"

test <- function(){
    count = 0
    for (i in (1:length(three_gram_test))) {
        threeg <- three_gram_test[i]
        splited <- strsplit(threeg, " ")
        splited <- unlist(splited)
        twog <- paste(splited[1:2], collapse = " ")
        result <- trigram_prediction(twog, sorted_unigram, sorted_bigram, sorted_trigram)
        if (result[1] == splited[3]) {count = count + 1 
        print(count)}}
    return (count/length(three_gram_test))
}
bigram_prediction <- function(sentence) {
    library(gdata)
    new_s <- string_processing(sentence)
    new_s <- unlist(new_s)
    #new_s <- new_s[-(which(new_s %in% common_words))]
    #new_s <- paste(new_s, collapse = " ")
    previous <- tail(new_s,2)[1]
    bottom <- sorted_unigram[previous]
    possibilities <- names(sorted_bigram)
    pos_freq_table <- sorted_bigram[startsWith(possibilities, previous)][1:5]
    result <- strsplit(names(pos_freq_table), " ")
    
    for (i in 1:5) { 
    if (is.na(result[i])) {
        result[i:5] = names(sorted_unigram[1:(5-i+1)])
        break
    }}
    result <- unlist(lapply(result, function(x) x[2]))
    return (result)
    
}

trigram_prediction <- function(sentence) {
    library(gdata)
    new_s <- string_processing(sentence)
    new_s <- unlist(new_s)
    previous <- tail(new_s,3)[1:2]
    previous <- paste(previous, collapse = " ")
    bottom <- sorted_bigram[previous]
    possibilities <- names(sorted_trigram)
    pos_freq_table <- sorted_trigram[startsWith(possibilities, previous)][1:5]
    result <- names(pos_freq_table)
    bg <- bigram_prediction(sentence)
    result <- strsplit(names(pos_freq_table), " ")
    for (i in 1:5) { 
        if (is.na(result[i])){
            result[i:5] = bg[1:(5-i+1)]
            break
        }
    }
    result <- unlist(lapply(result, function(x) { 
        if (length(x) == 3) x[3]
        else x
            }))
    return (result)
}

n_gram_prediction <- function(previous, n, set) {
    n_gram_set <- NGramTokenizer(set, Weka_control(min = n, max = n))
    training <- unlist(n_gram_set)
    training <- tolower(training)
    previous <- strsplit(previous, " ")
    previous <- unlist(previous)
    previous <- tolower(previous)
    poss <- list()
    counter <- 0
    for (j in 1:length(training)){
        splited_training <- strsplit(training[j], " ")
        splited_training <- unlist(splited_training)
        
        if (all.equal((splited_training)[1:n-1], previous[1:n-1])== TRUE) {
            counter = counter + 1
            word = splited_training[n]
            poss <- append(poss, word)
        }
    }
    table <- table(unlist(poss))
    table <- sort(table, decreasing = TRUE)
    return (table[1:10])
}

two_gram <- function(sample) {
    two_gram_storage = list()
    for (i in 1:length(sample)) {
        splited <- strsplit(sample[i], " ")
        unlisted <- unlist(splited)
        cleaned <- gsub("[[:punct:]]", "", unlisted)
        result <- tolower(cleaned)
        result <- profane_filter(result)
        op = list()
        for (j in 1:length(result)) {
            
            if (j == 1) { 
                g <- paste ("<s>", result[j])
                }
            
            else if (j == length(result)) {
                g <- paste (result[j], "<e>")}
            
            else {
                g1 <- result[j]
                g2 <- result[j-1]
                g <- paste(g2,g1)
                
            }
            op <- c(op,g)
            
        }
        two_gram_storage <- append(two_gram_storage, op)
        
            
            
            
    }
    return (two_gram_storage)}
    

two_gram_model <- function(sentence, two_gram_set) {
    training <- unlist(two_gram_set)
    pred <- NGramTokenizer(sentence, Weka_control(min = 2, max = 2))
    pred <- unlist(pred)
    prob <- 1
    for (i in 1:length(pred)) {
        bottom <- 0
        top <- 0
        
        for (j in 1:length(training)){
        splited_pred <- strsplit(pred[i], " ")
        splited_pred <- unlist(splited_pred)
        splited_training <- strsplit(training[j], " ")
        splited_training <- unlist(splited_training)
       
        if ((splited_training)[1] == splited_pred[1]) {
            if (splited_training[2] == splited_pred[2]) {
                top <- top + 1
            }
            bottom <- bottom + 1
        }
        
        }
        if (top != 0) {
            prob = prob * (top/bottom)}
        }
    return (prob)
}


two_gram_prediction <- function(previous, two_gram_set) {
    training <- unlist(two_gram_set)
    poss <- list()
    counter <- 0
        for (j in 1:length(training)){
            splited_training <- strsplit(training[j], " ")
            splited_training <- unlist(splited_training)
            
            if ((splited_training)[1] == previous) {
                    counter = counter + 1
                    word = splited_training[2]
                    poss <- append(poss, word)
            }
        }
        table <- table(unlist(poss))
        table <- sort(table, decreasing = TRUE)
        return (table[1:3])
}
two_gram_frequency <- function(entry) {
    n_gram_set
}
n_gram_prediction <- function(previous, n, set) {
    n_gram_set <- NGramTokenizer(set, Weka_control(min = n, max = n))
    training <- unlist(n_gram_set)
    training <- tolower(training)
    previous <- strsplit(previous, " ")
    previous <- unlist(previous)
    previous <- tolower(previous)
    poss <- list()
    counter <- 0
    for (j in 1:length(training)){
        splited_training <- strsplit(training[j], " ")
        splited_training <- unlist(splited_training)
        
        if (all.equal((splited_training)[1:n-1], previous[1:n-1])== TRUE) {
            counter = counter + 1
            word = splited_training[n]
            poss <- append(poss, word)
        }
    }
    table <- table(unlist(poss))
    table <- sort(table, decreasing = TRUE)
    return (table[1:10])
}

