import requests
from bs4 import BeautifulSoup as soup
import json 
import math

prefix_freq = {}
affix_freq = {}
suffix_freq = {}

def segment(word):
    word_list = []
    for prefix in range(1, len(word), 1):
        for affix in range(prefix, len(word), 1):
            word_list.append((word[:prefix], word[prefix: affix], word[affix:]))
    return word_list
def construct_dict():
    if len(w) > 0 and (w[0] != '*' or (w[0] != '-' and w[len(w)-1] != '-')):
        if w[len(w)-1] == '-':
            if prefix_freq.get(w[0:len(w)-1]) != None:
                prefix_freq[w[0:len(w)-1]] += 1
            else:
                prefix_freq[w[0:len(w)-1]] = 1

        elif w[len(w)-1] != '-' and w[0] != '-':
            if affix_freq.get(w) != None:
                affix_freq[w] += 1
            else:
                affix_freq[w] = 1
        elif w[0] == '-':
            if suffix_freq.get(w[1:]) != None:
                suffix_freq[w[1:]] += 1
            else:
                suffix_freq[w[1:]] = 1

if __name__ == '__main__':
    f = open('etym.entries.v1.format.json') 
    word_dict = json.load(f) 
    for word in word_dict['results']:
        for w in word["foreigns"]:
            #print(w)
            construct_dict()
        for w in word["cross-references"]:
            #print(w)
            construct_dict()
    prefix_total_cnt = 0
    affix_total_cnt = 0
    suffix_total_cnt = 0

    for cnt in prefix_freq.values():
        prefix_total_cnt += cnt
    for cnt in affix_freq.values():
        affix_total_cnt += cnt
    for cnt in suffix_freq.values():
        suffix_total_cnt += cnt
    query_list = ['international', 'scholarship', 'university', 'education', 'programme']
    for query in query_list:
        score_list = []
        for seg in segment(query):
            P_prefix = 0
            P_affix = 0
            P_suffix = 0

            if prefix_freq.get(seg[0]) != None:
                P_prefix = prefix_freq[seg[0]] / prefix_total_cnt
            else:
                P_prefix = 1 / (len(prefix_freq) * 10**len(seg[0]))
            if seg[1] != "":
                if affix_freq.get(seg[1]) != None:
                    P_affix = affix_freq[seg[1]] / affix_total_cnt
                else:
                    P_affix = 1 / (len(affix_freq) * 10**len(seg[1]))
            
            if suffix_freq.get(seg[2]) != None:
                P_suffix = suffix_freq[seg[2]] / suffix_total_cnt
            else:
                P_suffix = 1 / (len(suffix_freq) * 10**len(seg[2]))
            if P_affix != 0:
                score = math.log(P_prefix, 10)+math.log(P_affix, 10)+math.log(P_suffix, 10)
            else:
                score = math.log(P_prefix, 10)+math.log(P_suffix, 10)
            score_list.append((seg, score))
            #print(seg, score)
        result = sorted(score_list, key = lambda s: s[1], reverse = True)
        for index in range(0,10,1):
            print(result[index])
        print("==================================================================")