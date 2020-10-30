import spacy
from nltk.corpus import wordnet as wn
import nltk
from transformers import *
from itertools import product

# 步驟 1
def check_sentence_vn(doc):
    miscollocation = []
    for token in doc:
        annotations.append([token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head])
    i = 0
    for annotation in annotations:
        #print(annotation[4])
        if annotation[4] == "dobj":
            head = annotation[5]
            j = 0
            for annotation_ in annotations:
                if str(annotation_[0]) == str(head) and (str(annotation_[2]) == "VERB" or str(annotation_[2]) == "AUX"):
                    miscollocation.append([(annotation_[0], j), (annotation[0], i)])
                j += 1
        i += 1
    #print(miscollocation)
    return miscollocation

# 步驟 2
def mask_cand(sentence, miscollocation):
    #print(sentence)
    #print(miscollocation)
    for m in miscollocation:
        sentence_list = sentence.split(" ")
        sentence_list[m[0][1]] = '[MASK]'
        #print(sentence_list)
        mask_sentence = ' '.join(sentence_list)
        candidates = p(mask_sentence)
        ret = []
        for cand in candidates:
            ret.append((cand['token_str'], cand['score']))
            #print(f"{cand['token_str']} \t {cand['score']}")
        similarity(sentence, [m], mask_sentence, ret)
''' mask_cand() Output
[('produce', 0.319),
 ('achieve', 0.101),
 ('make', 0.0869),
 ('have', 0.0644),
 ('obtain', 0.0523),
 ('get', 0.0424),
 ('generate', 0.0295),
 ('provide', 0.0219),
 ('create', 0.0134),
'''

# 步驟 3
def similarity(sentence, miscollocation, mask_sentence, mask_cand_):
    nltk.download('wordnet')
    '''
    print(sentence)
    print(miscollocation)
    print(mask_sentence)
    print(mask_cand_)
    '''
    ret = []

    sentence_list = sentence.split(" ")
    ori_v = sentence_list[miscollocation[0][0][1]]
    syn_ori = wn.synsets(ori_v, 'v') #list
    for c in mask_cand_:
        syn_candi = wn.synsets(c[0], 'v')
        for i in product(syn_ori, syn_candi):
            #print(i)
            #print(i[0].path_similarity(i[1]))
            if i[0].path_similarity(i[1]) > 0.4:
                index = 0
                append_or_not = 1
                for r in ret:
                    if c[0] == r[0] and sentence_list[miscollocation[0][1][1]] == r[1] and c[0] != ori_v:
                        append_or_not = 0
                        if i[0].path_similarity(i[1]) > r[2]:
                            ret.pop(index)
                            ret.append((c[0], sentence_list[miscollocation[0][1][1]], i[0].path_similarity(i[1]), c[1]))
                            break
                    index += 1
                if (append_or_not == 1 or len(ret) == 0) and c[0] != ori_v:
                    ret.append((c[0], sentence_list[miscollocation[0][1][1]], i[0].path_similarity(i[1]), c[1]))
    sort_ret = sorted(ret, key = lambda s: (s[2], s[3]), reverse = True)
    print(mask_sentence)
    index = 0
    for s in sort_ret:
        if index == 5:
            break    
        print(s)
        index += 1
    '''
    cat = wn.synset('cat.n.01')
    dog = wn.synset('dog.n.01')
    print(dog.path_similarity(cat))
    '''

''' similarity() Output
Just as we must [MASK] all the outputs necessary to reach the purpose .
('consider', 'output', 0.5, 0.00335)
('see', 'output', 0.5, 0.0016)
('determine', 'output', 0.5, 0.000828)

Just as we must identify all the outputs necessary to [MASK] the purpose .
('achieve', 'purpose', 1.0, 0.548)
('accomplish', 'purpose', 1.0, 0.262)
('attain', 'purpose', 1.0, 0.0117)
'''

if __name__ == "__main__":
    nlp = spacy.load('en_core_web_sm')
    annotations = []
    sentence = "Just as we must identify all the outputs necessary to reach the purpose ."
    doc = nlp(sentence)

    miscollocation = check_sentence_vn(doc)
    ''' check_sentence_vn() Output
    [[('identify', 4), ('output', 7)], [('reach', 10), ('purpose', 12)]]  
    '''

    model = "bert-large-uncased"
    p = pipeline("fill-mask", model=model, topk=100)

    mask_cand(sentence, miscollocation)
