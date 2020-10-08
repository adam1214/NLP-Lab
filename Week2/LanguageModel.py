#!/usr/bin/env python
# coding: utf-8

import math, re
from collections import Counter
from itertools import islice


# tokenize text and get words list
def words(text): return re.findall(r'\w+', text.lower())

'''
# get all bigrams
def bigrams(text):
    pass
'''

# these are word-level 1-grams(unigram) and 2-grams(bigram)
# count of the number of times they appeared
uni_count = Counter(words(open('big.txt').read()))
bi_count = Counter(zip(words(open('big.txt').read()), islice(words(open('big.txt').read()), 1, None))) 
#print(uni_count['min'])
#print(bi_count[('a', 'new')])

# ==Format==
# call add1_smooth("He is") or add1_smooth(("He", "is")) something like that...
# retrun 1.306 (probability with add one smooth)
V = len(list(uni_count.keys()))
'''
def add1_smooth(bigram):
    pass
'''
# ==Format==
# call sentence_prob("He is looking a new job.")
# retrun -33.306 (sentence probability)
def sentence_prob(sentence):
    str_list = sentence.split(" ")
    sum = 0
    for i in range(1, len(str_list)):
        #print(str_list[i])
        print(str_list[i-1])
        print(str_list[i])
        print(bi_count[(str_list[i-1], str_list[i])])
        print(uni_count[i-1] + 1)
        sum = sum + math.log((bi_count[(str_list[i-1], str_list[i])] + 1) / (uni_count[i-1] + V))
        print("=====================")
    return sum


if __name__ == "__main__":
    lm1 = sentence_prob("He is looking to a new job")
    lm2 = sentence_prob("He is looking for a new job")
    print(lm1)
    print(lm2)