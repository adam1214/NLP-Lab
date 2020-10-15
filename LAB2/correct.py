#!/usr/bin/env python
from collections import Counter, defaultdict
import math, re
import kenlm
import operator
import itertools

model = kenlm.Model('bnc.prune.arpa')


def words(text): return re.findall(r'\w+|[,.?]', text.lower())


WORDS = Counter(words(open('big.txt').read()))


def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return float(WORDS[word] / N)


def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    
    return set(deletes + transposes + replaces + inserts)


def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def suggest(word):
    '''return top 5 words as suggestion, original_word as top1 when original_word is correct'''
    suggest_P = {}
    edits_set = edits1(word).union(set(edits2(word)))
    for candidate in known(edits_set):
        suggest_P[candidate] = P(candidate)
    if word in WORDS:
        suggest_P[word] = 1
    suggest_can = sorted(suggest_P, key=suggest_P.get, reverse=True)[:5]
    
    return suggest_can



###### Task1 ######
def tokens_check(sentence):
    sentence_seg = sentence.split(" ")
    err_index = []
    for i in range(0, len(sentence_seg)):
        if WORDS[sentence_seg[i]] == 0:
            #print(sentence_seg[i])
            err_index.append(i)
    return err_index

###### Task2 ######
dets = {"", "the", "a", "an"}
list_dets = list(dets)
preps = {"", "about", "at", "by", "for", "from", "in", "of", "on", "to", "with"}
list_preps = list(preps)
'''
def generate_candidates(tokens):
    print("TODO")
'''
    
def process_sent(text_seg, text):
    copy_text = text
    candi_index_dets = []
    for i in range(0, len(text_seg)):
        token_list = [text_seg[i]]
        if set(token_list) & dets:
            candi_index_dets.append(i)
    for i in range(0, len(candi_index_dets)):
        for j in range(0, len(list_dets)):
            candi_text = copy_text
            candi_text_list = words(candi_text)
            candi_text_list[candi_index_dets[i]] = list_dets[j]
            candi_text = ""
            candi_text = " ".join(candi_text_list)
            #print(candi_text)

            if (model.score(candi_text,bos=True, eos=True) / len(candi_text_list)) > (model.score(text,bos=True, eos=True) / len(text_seg)):
                text = candi_text
                text_seg = words(text)
    copy_text = text
    #print(text)
    ###################################################
    candi_index_preps = []
    for i in range(0, len(text_seg)):
        token_list = [text_seg[i]]
        if set(token_list) & preps:
            candi_index_preps.append(i)
    for i in range(0, len(candi_index_preps)):
        for j in range(0, len(list_preps)):
            candi_text = copy_text
            candi_text_list = words(candi_text)
            candi_text_list[candi_index_preps[i]] = list_preps[j]
            candi_text = ""
            candi_text = " ".join(candi_text_list)
            #print(candi_text)

            if (model.score(candi_text,bos=True, eos=True) / len(candi_text_list)) > (model.score(text,bos=True, eos=True) / len(text_seg)):
                sent = candi_text
                text_seg = words(text)
    print(text)
if __name__ == "__main__":

    text = 'he sold everythin except the housee'
    text_seg = words(text)
    #print(tokens_check(text))
    copy_text = text
    copy_text_edit = text
    for i in range(0, len(tokens_check(copy_text))):
        for j in range(0, len(suggest(text_seg[tokens_check(copy_text)[i]]))):
            candi_text = copy_text_edit
            candi_text_list = words(candi_text)
            candi_text_list[tokens_check(copy_text)[i]] = suggest(text_seg[tokens_check(copy_text)[i]])[j]
            candi_text = ""
            candi_text = " ".join(candi_text_list)
            #print(candi_text)
            if (model.score(candi_text,bos=True, eos=True) / len(candi_text_list)) > (model.score(text,bos=True, eos=True) / len(text_seg)):
                text = candi_text
                text_seg = words(text)
        copy_text_edit = text
    print(text)
    #Output = 'he sold everything except the house'

    
    sent = 'we discuss a possible meaning by it .'
    process_sent(words(sent), sent)

    #Output = 'we discuss the possible meaning of it .'
    