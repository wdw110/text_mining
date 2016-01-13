library(wordcloud)

data = read.table('/Users/wdw/Desktop/work/data/data_tousu.txt',header=F)

words = as.vector(data$V1)
freq = data$V2

par(family='STXihei')
wordcloud(words, freq, scale = c(5,0.5), min.freq=100,colors=c(1:20),random.order=F,random.color=F,ordered.colors=F,rot.per=F)
