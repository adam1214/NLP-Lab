import json
import math
import requests
from bs4 import BeautifulSoup as soup

prefix_freq = {}
affix_freq = {}
suffix_freq = {}
count = 0
def Dataprocessing():
    global count
    #File from Lab9
    with open('data/etym.entries.v1.format.json') as f:
        content = json.load(f)
    count = content["count"]
    content = content["results"]
    #print(content[:1])
    for c in content:
        for f in c["foreigns"]+c["cross-references"]:
            if ' ' not in f and len(f)>=1:
                if f[0] !='*' and f[0] == '-' and f[-1] !='-':
                    #print(f , " S")
                    f = f[1:]
                    if f not in suffix_freq:
                        suffix_freq[f]=1
                    else:
                        suffix_freq[f] +=1
                elif f[0] !='*' and f[0] !='-' and f[-1] =='-':
                    #print(f , " P")
                    f = f[:-1]
                    if f not in prefix_freq:
                        prefix_freq[f]=1
                    else:
                        prefix_freq[f] +=1
                elif f[0] =='*' or ( f[0] =='-' and f[-1] =='-' ):
                    pass
                else:
                    #print(f , " A")
                    if f not in affix_freq:
                        affix_freq[f]=1
                    else:
                        affix_freq[f] +=1
    #Additional Data
    #if set(line)==2 it means line[1] == suffix ? or affix?     
    with open('data/eng.train') as f:
        lines = f.readlines()
    lines= [i.strip().split('\t')[1].split('/') for i in lines]
    #print(lines[:10])
    for line in lines:
        if(set(line)==3):
            if line[0] not in prefix_freq:
                prefix_freq[ line[0] ] = 1
            else:
                prefix_freq[ line[0] ] += 1
            if line[1] not in  affix_freq:
                affix_freq[ line[1] ] = 1
            else:
                affix_freq[ line[1] ] += 1
            if line[2] not in suffix_freq:
                suffix_freq[ line[2] ] = 1
            else:
                suffix_freq[ line[2] ] += 1
        elif(set(line)==2):
            if line[0] not in prefix_freq:
                prefix_freq[ line[0] ] = 1
            else:
                prefix_freq[ line[0] ] += 1
            if line[1] not in suffix_freq:
                suffix_freq[ line[1] ] = 1
            else:
                suffix_freq[ line[1] ] += 1
                
def IsWord(test):
    url = 'https://www.etymonline.com/search?q='
    response = requests.get(url+test)
    if response.status_code == 200:
        #print("A")
        content = response.content
        html = soup(content, "html.parser")
        #print(html)
        div = html.find('div')
        paragraph = div.find_all('a', class_="word__name--TTbAA word_thumbnail__name--1khEg")
        try:
            p_title = paragraph[0].get_text()
            #print("title:",p_title)
            return True
        except:
            #print(len(paragraph))
            return False
        return False
        
def Calculation(P,A,S):
    if P not in prefix_freq:
        pro_P = 1 /( len(prefix_freq) * pow( 10,len(P) ) )
    else:
        pro_P = prefix_freq[P] /sum(prefix_freq.values())
    if A not in affix_freq:
        if(IsWord(A)):
            pro_A = 1 /( len(affix_freq) * pow( 10,1.5 ) )
        else:
            pro_A = 1 /( len(affix_freq) * pow( 10,len(A) ) )
    else:
        pro_A = affix_freq[A] /sum(affix_freq.values())
    if S not in suffix_freq:
        if(IsWord(S)):
            pro_S = 1 /( len(affix_freq) * pow( 10,1.5 ) )
        else:
            pro_S = 1 /(len(suffix_freq) * pow( 10,len(S) ) )
    else:
        pro_S = suffix_freq[S] /sum(suffix_freq.values())
    #print(pro_P,pro_A,pro_S)
    if A =='':
        return [ math.log(pro_P) + math.log(pro_S), math.log(pro_P),math.log(pro_A),math.log(pro_S)]
    else:
        return [math.log(pro_P) + math.log(pro_S) + math.log(pro_A), math.log(pro_P),math.log(pro_A),math.log(pro_S)]
        
    
                        
def Segment(word):
    seg = []
    for i in range(1,len(word)):
        #print(word[:i],word[i:])
        P = word[:i]
        AS = word[i:]
        for j in range(len(AS)):
            #print(word[:i],part[:j],part[j:])
            A = AS[:j]
            S = AS[j:]
            #print(P,A,S,Calculation(P,A,S))
            #print("*"*20)
            #print(Calculation(P,A,S))
            #seg.append([P,A,S,round(Calculation(P,A,S)[0],3),Calculation(P,A,S)[1:]])
            seg.append([P,A,S,round(Calculation(P,A,S)[0],3)])
    return seg

def Word2Morphemes(word):
    list1 = words(open('data/big.txt').read())
    
    #word_count = Counter(list3) #word_count類似dict，鍵存某單字，值存該單字的出現次數，共有32198個鍵
    word_count = Counter(list1) #word_count類似dict，鍵存某單字，值存該單字的出現次數，共有32198個鍵
    Dataprocessing()
    print(word,":")
    seg = Segment(word)
    seg = sorted(seg,key=lambda x: x[3],reverse = True)
    ListReturn = {}
    Pro = []
    for p in seg[:5]:
        Pro.append(p)
        print(p)
    ListReturn[word] = Pro
    given_word_root_tuple = (ListReturn[word][0][0], ListReturn[word][0][1], ListReturn[word][0][2])
    given_word_root_1 = given_word_root_tuple[0] + '-'
    given_word_root_2 = given_word_root_tuple[1]
    given_word_root_3 = '-' + given_word_root_tuple[2]
    given_word_root_1_mean = get_root_mean(given_word_root_1)
    given_word_root_2_mean = get_root_mean(given_word_root_2)
    given_word_root_3_mean = get_root_mean(given_word_root_3)
    
    root_1_dict = {}
    root_1_dict['mean_of_root'] = given_word_root_1_mean
    root_2_dict = {}
    root_2_dict['mean_of_root'] = given_word_root_2_mean
    root_3_dict = {}
    root_3_dict['mean_of_root'] = given_word_root_3_mean
    
    '''
    find family of roots
    '''    
    family_of_root_1 = correction_2(given_word_root_tuple[0], word_count)
    family_of_root_2 = correction_2(given_word_root_tuple[1], word_count)
    family_of_root_3 = correction_2(given_word_root_tuple[2], word_count)
    
    root_1_dict['family_of_root'] = family_of_root_1
    root_2_dict['family_of_root'] = family_of_root_2
    root_3_dict['family_of_root'] = family_of_root_3

    '''
    find original word for each root
    '''
    origin_of_root_1 = correction(given_word_root_tuple[0], word_count)
    origin_of_root_2 = correction(given_word_root_tuple[1], word_count)
    origin_of_root_3 = correction(given_word_root_tuple[2], word_count)
    
    root_1_dict['origin_of_root'] = origin_of_root_1
    root_2_dict['origin_of_root'] = origin_of_root_2
    root_3_dict['origin_of_root'] = origin_of_root_3    
    
    given_word_root_dict = {}
    given_word_root_dict[given_word_root_tuple[0]] = root_1_dict
    given_word_root_dict[given_word_root_tuple[1]] = root_2_dict
    given_word_root_dict[given_word_root_tuple[2]] = root_3_dict
       
    return given_word_root_dict

#import json
from collections import Counter
#import math
#import requests
from bs4 import BeautifulSoup
import re

def segment(word):
    segment_list = []
    for i in range(len(word) - 1):
        prefix = word[:i + 1]
        affix = ''
        for j in range(len(word) - i - 1):
            suffix = word[i + j + 1:]
            affix = word[i + 1: i + j + 1]
            segment_list.append((prefix, affix, suffix))
    return segment_list
    
def prob(word_list, prefix_dict, prefix_total_count, n_prefix, affix_dict, affix_total_count, n_affix, suffix_dict, suffix_total_count, n_suffix):
    prob_list = []
    for i in range(len(word_list)):
        if(len(word_list[i][1]) != 0):
            try:
                prefix_prob = prefix_dict[word_list[i][0] + '-'] / prefix_total_count
                prefix_prob = math.log(prefix_prob, 10)                
            except:
                prefix_prob = 1 / (n_prefix * math.pow(10, len(word_list[i][0])))
                prefix_prob = math.log(prefix_prob, 10) 
                #p(prefix) = 1 / ( N * 10^len(prefix) )
            try:
                affix_prob = affix_dict[word_list[i][1]] / affix_total_count
                affix_prob = math.log(affix_prob, 10)                
            except:
                affix_prob = 1 / (n_affix * math.pow(10, len(word_list[i][1])))
                affix_prob = math.log(affix_prob, 10) 
                #p(prefix) = 1 / ( N * 10^len(prefix) )
            try:
                suffix_prob = suffix_dict['-' + word_list[i][2]] / suffix_total_count
                suffix_prob = math.log(suffix_prob, 10)                
            except:
                suffix_prob = 1 / (n_suffix * math.pow(10, len(word_list[i][2])))
                suffix_prob = math.log(suffix_prob, 10) 
                #p(prefix) = 1 / ( N * 10^len(prefix) )
            prob = prefix_prob + affix_prob + suffix_prob
        else:
            try:
                prefix_prob = prefix_dict[word_list[i][0] + '-'] / prefix_total_count
                prefix_prob = math.log(prefix_prob, 10)                
            except:
                prefix_prob = 1 / (n_prefix * math.pow(10, len(word_list[i][0])))
                prefix_prob = math.log(prefix_prob, 10)
            try:
                suffix_prob = suffix_dict['-' + word_list[i][2]] / suffix_total_count
                suffix_prob = math.log(suffix_prob, 10)                
            except:
                suffix_prob = 1 / (n_suffix * math.pow(10, len(word_list[i][2])))
                suffix_prob = math.log(suffix_prob, 10)
            prob = prefix_prob + suffix_prob            
        prob_list.append((word_list[i], prob))
    return prob_list

def get_root_mean(given_word_root):
    if(given_word_root == ''):
        root_mean = 'No results were found for empty string.'
    else:
        url = 'https://www.etymonline.com/search?q=' + given_word_root # 目標 url
        response = requests.get(url) # 使用 GET 送出 request
        if response.status_code == 200: # 「200 OK」代表請求成功被處理
            text = response.text # 把 response 內容取出
            soup = BeautifulSoup(text, "html.parser")
            section = soup.find('section', class_='word__defination--2q7ZH undefined')
            if section:
                root_mean = section.text
            else:
                root_mean = 'No results were found for ' + given_word_root + '.'
    return root_mean

def words(text): return re.findall(r'\w+', text.lower())
#print(type(words(open('big.txt').read())))

def edits1(word):
    '''
    (for finding family of roots)
    輸入: word(單字字串) / 輸出: set(所有可能的單字)
    功能:回傳和word相似的所有單字
    '''   
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    adds = []   #自己本身不加入候選字
    for i1 in range(len(letters)):
        adds.append(word + letters[i1])
        for i2 in range(len(letters)):
            adds.append(word + letters[i1] + letters[i2])
            for i3 in range(len(letters)):
                adds.append(word + letters[i1] + letters[i2] + letters[i3])
                for i4 in range(len(letters)):
                    adds.append(word + letters[i1] + letters[i2] + letters[i3] + letters[i4])
#                    for i5 in range(len(letters)):
#                        adds.append(word + letters[i1] + letters[i2] + letters[i3] + letters[i4] + letters[i5])        
    return set(adds)

def edits2(word):
    '''
    (for finding original word for each root)
    輸入: word(單字字串) / 輸出: set(所有可能的單字)
    功能:回傳和word相似的所有單字
    '''
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    adds = []
    adds.append(word)   #自己本身也要加入候選字
    for i1 in range(len(letters)):
        adds.append(word + letters[i1])
        for i2 in range(len(letters)):
            adds.append(word + letters[i1] + letters[i2])
            for i3 in range(len(letters)):
                adds.append(word + letters[i1] + letters[i2] + letters[i3])
                for i4 in range(len(letters)):
                    adds.append(word + letters[i1] + letters[i2] + letters[i3] + letters[i4])  
    return set(adds)

def correction(word, word_count):
    '''
    取出現機率最高的單字(for finding original word for each root)
    '''
    if word:
        min_length = 1000
        min_word = ''
        min_prob = 0
        for w in candidates_2(word, word_count):
            if(p_2(w, word) < min_length):
                min_length = p_2(w, word)
                min_word = w
                min_prob = P(w, word_count)
            elif(p_2(w, word) == min_length):
                if(P(w, word_count) > P(min_word, word_count)):
                    min_word = w
                    min_prob = P(w, word_count)
        original_word = min_word
    else:
        original_word = 'the root is empty root.'
    return original_word

def correction_2(word, word_count):
    '''
    取出現機率最高的單字(for finding family of roots)
    '''
    if word:
        true_word = []
        candidates_set = candidates(word, word_count)
        if(candidates_set == [word]):
            true_word = 'the root does not have extended word.'
        else:
            for w in candidates_set:
                if(word_count[w] >= 1):
                    true_word.append(w)
    else:
        true_word = 'the root is empty root.'
    return true_word

def candidates(word, word_count):
    '''
    回傳所有可能的有意義單字(for finding family of roots)
    '''
    return (known(edits1(word), word_count) or [word])  #回傳第一個非空的set 

def candidates_2(word, word_count):
    '''
    回傳所有可能的有意義單字(for finding original word for each root)
    '''
    return (known(edits2(word), word_count) or [word])  #回傳第一個非空的set

def known(words, word_count): 
    '''
    將有意義的單字存成set
    '''
    return set(w for w in words if w in word_count)

def P(word, word_count):
    N = sum(word_count.values())    #N存所有單字的總出現次數
    return word_count[word] / N # float  #回傳word的出現機率

def p_2(w, word):
    return abs(len(w) - len(word))

def main_function(given_word):
    list1 = words(open('data/big.txt').read())
    
    #word_count = Counter(list3) #word_count類似dict，鍵存某單字，值存該單字的出現次數，共有32198個鍵
    word_count = Counter(list1) #word_count類似dict，鍵存某單字，值存該單字的出現次數，共有32198個鍵
    
    file = 'etym.entries.v1.format.json'
    with open(file, 'r') as obj:
        data = json.load(obj)
    
    prefix_list = []
    affix_list = []
    suffix_list = []
    
    words_list = data['results']
    for i in range(len(words_list)):
        word_list = []
        word_list.extend(words_list[i]['foreigns'])
        word_list.extend(words_list[i]['cross-references'])
        for j in range(len(word_list)):
            if(len(word_list[j]) != 0):        
                if(word_list[j][0] != '*'):
                    if((word_list[j][0] != '-') and (word_list[j][-1] == '-')):
                        prefix_list.append(word_list[j])
                    elif((word_list[j][0] != '-') and (word_list[j][-1] != '-')):
                        affix_list.append(word_list[j])
                    elif((word_list[j][0] == '-') and (word_list[j][-1] != '-')):
                        suffix_list.append(word_list[j])
    prefix_dict = Counter(prefix_list)
    affix_dict = Counter(affix_list)
    suffix_dict = Counter(suffix_list)
    n_prefix = len(prefix_dict)
    n_affix = len(affix_dict)
    n_suffix = len(suffix_dict)
    prefix_count_list = prefix_dict.values()
    prefix_total_count = sum(prefix_count_list)
    affix_count_list = affix_dict.values()
    affix_total_count = sum(affix_count_list)
    suffix_count_list = suffix_dict.values()
    suffix_total_count = sum(suffix_count_list)
    
    international_list = segment(given_word)
    international_prob_list = prob(international_list, prefix_dict, prefix_total_count, n_prefix, affix_dict, affix_total_count, n_affix, suffix_dict, suffix_total_count, n_suffix)
    international_prob_list.sort(key=lambda x: x[1], reverse = True)
    given_word_root_tuple = international_prob_list[0][0]
    given_word_root_1 = given_word_root_tuple[0] + '-'
    given_word_root_2 = given_word_root_tuple[1]
    given_word_root_3 = '-' + given_word_root_tuple[2]
    given_word_root_1_mean = get_root_mean(given_word_root_1)
    given_word_root_2_mean = get_root_mean(given_word_root_2)
    given_word_root_3_mean = get_root_mean(given_word_root_3)
    
    root_1_dict = {}
    root_1_dict['mean_of_root'] = given_word_root_1_mean
    root_2_dict = {}
    root_2_dict['mean_of_root'] = given_word_root_2_mean
    root_3_dict = {}
    root_3_dict['mean_of_root'] = given_word_root_3_mean
    
    '''
    find family of roots
    '''    
    family_of_root_1 = correction_2(given_word_root_tuple[0], word_count)
    family_of_root_2 = correction_2(given_word_root_tuple[1], word_count)
    family_of_root_3 = correction_2(given_word_root_tuple[2], word_count)
    
    root_1_dict['family_of_root'] = family_of_root_1
    root_2_dict['family_of_root'] = family_of_root_2
    root_3_dict['family_of_root'] = family_of_root_3

    '''
    find original word for each root
    '''
    origin_of_root_1 = correction(given_word_root_tuple[0], word_count)
    origin_of_root_2 = correction(given_word_root_tuple[1], word_count)
    origin_of_root_3 = correction(given_word_root_tuple[2], word_count)
    
    root_1_dict['origin_of_root'] = origin_of_root_1
    root_2_dict['origin_of_root'] = origin_of_root_2
    root_3_dict['origin_of_root'] = origin_of_root_3    
    
    given_word_root_dict = {}
    given_word_root_dict[given_word_root_tuple[0]] = root_1_dict
    given_word_root_dict[given_word_root_tuple[1]] = root_2_dict
    given_word_root_dict[given_word_root_tuple[2]] = root_3_dict
       
    return given_word_root_dict

#word = "unhappy"
#given_word_root_dict = Word2Morphemes(word)
    