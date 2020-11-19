import nltk
import random
from nltk import NaiveBayesClassifier
from random import sample


def sent_features(sent, word_cnt_dict):
    sent_list = sent.split(" ")
    #print(sent_list)
    count = 0
    dirty_or_not = 0
    digit_num_or_not = 0
    for index in range(0,len(sent_list)-1,1):
        #print(sent_list[index].lower(), word_cnt_dict[sent_list[index].lower()])
        if word_cnt_dict.get(sent_list[index].lower()) != None and word_cnt_dict[sent_list[index].lower()] > 1825541:
            count += 1
        if sent_list[index].lower().find('-') >= 0 or sent_list[index].lower().find('/') >= 0 or sent_list[index].lower().find('(') >= 0 or sent_list[index].lower().find(')') >= 0 or sent_list[index].lower().find('`') >= 0 or sent_list[index].lower().find('&') >= 0 or sent_list[index].lower().find('*') >= 0 or sent_list[index].lower().find('$') >= 0 or sent_list[index].lower().find('@') >= 0 or sent_list[index].lower().find('%') >= 0 or sent_list[index].lower().find('<') >= 0 or sent_list[index].lower().find('>') >= 0 or sent_list[index].lower().find('#') >= 0 or sent_list[index].lower().find(';') >= 0:
            dirty_or_not = 1
        if sent_list[index].lower().find('0') >= 0 or sent_list[index].lower().find('1') >= 0 or sent_list[index].lower().find('2') >= 0 or sent_list[index].lower().find('3') >= 0  or sent_list[index].lower().find('4') >= 0 or sent_list[index].lower().find('5') >= 0 or sent_list[index].lower().find('6') >= 0 or sent_list[index].lower().find('7') >= 0 or sent_list[index].lower().find('8') >= 0 or sent_list[index].lower().find('9') >= 0:
            digit_num_or_not = 1
    return {'count': count, 'len': len(sent_list), 'dirty_or_not': dirty_or_not, 'digit_num_or_not': digit_num_or_not}

if __name__ == '__main__':
    word_cnt_dict = {}
    f = open("word.txt", "r")
    for line in f.readlines():
        line_list = line.split('\t')
        word_cnt_dict[line_list[0].lower()] = int(line_list[1])

    #print(sent_features('giving blood/mosquito bites/toilet seats/kissing/from normal day-to-day contact', word_cnt_dict))
    
    data_set = []
    good_file = open("sents.cam.txt", "r", encoding="utf-8")
    bad_file = open("sents.bnc.txt", "r", encoding="utf-8")
    for line in good_file.readlines():
        data_set.append((line[:-1].lower(), 'G')) #remove '\n'
    for line in bad_file.readlines():
        data_set.append((line[:-1].lower(), 'B')) #remove '\n'
    random.seed(1)
    Train = sample(data_set, 9000) # 隨機抽取9000個元素當training data
    Test = data_set.copy()
    for e in Train: # 剩下1000個當test data
        Test.remove(e)
    Train_feature_set = []
    Test_feature_set = []
    #feature_set = [ ({'count': 4, ...}, 'B'), ({'count': 10, ...}, 'B')] 
    for index in range(0,len(Train),1):
        Train_feature_set.append((sent_features(Train[index][0], word_cnt_dict), Train[index][1]))
    for index in range(0,len(Test),1):
        Test_feature_set.append((sent_features(Test[index][0], word_cnt_dict), Test[index][1]))
    
    classifier = nltk.NaiveBayesClassifier.train(Train_feature_set)
    print(nltk.classify.accuracy(classifier, Test_feature_set))