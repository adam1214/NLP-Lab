import nltk
import random
from nltk import NaiveBayesClassifier
from random import sample


def sent_features(sent, word_cnt_dict):
    sent_list = sent.split(" ")
    #print(sent_list)
    count = 0
    dirty_cnt = 0
    digit_num_cnt = 0
    upper_letter_cnt = 0
    dot_cnt = 0
    title_cnt = 0
    comma_cnt = 0
    num_cnt = 0
    exclamation_mark_cnt = 0
    question_mark_cnt = 0
    for index in range(0,len(sent_list),1):
        #print(sent_list[index])
        if sent_list[index].isdigit() == True:
            num_cnt += 1
        if sent_list[index].isupper() == True:
            upper_letter_cnt += 1
        if sent_list[index].istitle() == True:
            title_cnt += 1
        if sent_list[index].find(',') >= 0:
            comma_cnt += 1
        if word_cnt_dict.get(sent_list[index].lower()) != None and word_cnt_dict[sent_list[index].lower()] > 1800000:
            count += 1
        if sent_list[index].find('.') >= 0:
            dot_cnt += 1
        if sent_list[index].find('!') >= 0:
            exclamation_mark_cnt += 1
        if sent_list[index].find('?') >= 0:
            question_mark_cnt += 1
        if sent_list[index].find('-') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('/') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('(') >= 0:
            dirty_cnt += 1
        if sent_list[index].find(')') >= 0: 
            dirty_cnt += 1
        if sent_list[index].find('`') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('"') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('[') >= 0:
            dirty_cnt += 1
        if sent_list[index].find(']') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('{') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('}') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('`') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('&') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('*') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('$') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('@') >= 0:
            dirty_cnt += 1 
        if sent_list[index].find('%') >= 0:
            dirty_cnt += 1 
        if sent_list[index].find('<') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('>') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('#') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('=') >= 0:
            dirty_cnt += 1
        if sent_list[index].find(';') >= 0:
            dirty_cnt += 1
        if sent_list[index].find('0') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('1') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('2') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('3') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('4') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('5') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('6') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('7') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('8') >= 0:
            digit_num_cnt += 1
        if sent_list[index].find('9') >= 0:
            digit_num_cnt += 1
    #print({'count': count, 'len': len(sent_list), 'dirty_cnt': dirty_cnt, 'digit_num_cnt': digit_num_cnt, 'upper_letter_cnt': upper_letter_cnt, 'dot_cnt': dot_cnt, 'title_cnt': title_cnt, 'comma_cnt': comma_cnt, 'num_cnt': num_cnt, 'exclamation_mark_cnt': exclamation_mark_cnt, 'question_mark_cnt': question_mark_cnt})
    return {'count': count, 'len': len(sent_list), 'dirty_cnt': dirty_cnt, 'digit_num_cnt': digit_num_cnt, 'upper_letter_cnt': upper_letter_cnt, 'dot_cnt': dot_cnt, 'title_cnt': title_cnt, 'comma_cnt': comma_cnt, 'num_cnt': num_cnt, 'exclamation_mark_cnt': exclamation_mark_cnt, 'question_mark_cnt': question_mark_cnt}

if __name__ == '__main__':
    
    word_cnt_dict = {}
    f = open("word.txt", "r")
    for line in f.readlines():
        line_list = line.split('\t')
        word_cnt_dict[line_list[0].lower()] = int(line_list[1])
    
    data_set = []
    good_file = open("sents.cam.txt", "r", encoding="utf-8")
    bad_file = open("sents.bnc.txt", "r", encoding="utf-8")
    for line in good_file.readlines():
        data_set.append((line[:-1], 'G')) #remove '\n'
    for line in bad_file.readlines():
        data_set.append((line[:-1], 'B')) #remove '\n'
    random.seed(1)
    Train = sample(data_set, 5000) # 隨機抽取5000個元素當training data
    Test = data_set.copy()
    for e in Train: # 剩下5000個當test data
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