import re
from textblob import TextBlob
from nltk.tokenize import word_tokenize

f_old = open('../data/TweetData_Original.txt','r')
f_new = open('../data/TweetData_Transfered.txt', 'w+')

english_punctuations = [',', ':', '.', '..', '...', '....', '.....', 'trump', 'trump.', 'trumpies', '``', '’', '”', '—', '?', '=', '!'
                       'is', 'it', 'he', 'she', 'the', 'for', 'this', 'that', 'and', 'you', 'with', 'or','of','to','on']

for line in f_old.readlines():
    new_words=[]
    line_words=word_tokenize(line.lower())
    
    for word in line_words:
        
        # if word in english_punctuations:
        #     continue
        if len(word) <= 2:
            continue
            
        #只保留字母
        # word =  list(filter(str.isalpha, word))
        # word = ''.join(word)
        
        word = str(TextBlob(word).correct())
        new_words.append(word)

    context = ' '.join(new_words)
    #b = TextBlob(context)
    #context = b.correct()
    # print(context)
    print(context, file = f_new)