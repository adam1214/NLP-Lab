import requests 
from linggle import Linggle
def get_sbg_stat(sbg):
    response = requests.get('http://thor.nlplab.cc:5566/search?q=' + sbg.lower())
    return response.json()

def sum_of_distance_cnt_value(distance_cnt):
    sum = 0
    for val in distance_cnt.values():
        sum += val
    return sum

def process_sentence(query_sentence, linggle):
    #print(query_sentence)
    list_query_sentence = query_sentence.split()
    #print(list_query_sentence)
    print('Incorrect index:', incorrect_index)
    distance_cnt = get_sbg_stat(list_query_sentence[incorrect_index-1] + " " + list_query_sentence[incorrect_index+1])
    Delete_rate = round(distance_cnt['1']/sum_of_distance_cnt_value(distance_cnt), 4)
    print('Delete:', str(round(float(Delete_rate)*100, 2)) + '%')

    distance_cnt = get_sbg_stat(list_query_sentence[incorrect_index] + " " + list_query_sentence[incorrect_index+1])
    Insert_rate_1 = round(distance_cnt['2']/sum_of_distance_cnt_value(distance_cnt), 4)
    distance_cnt = get_sbg_stat(list_query_sentence[incorrect_index] + " " + list_query_sentence[incorrect_index+2])
    Insert_rate_2 = round(distance_cnt['3']/sum_of_distance_cnt_value(distance_cnt), 4)
    Insert_rate = (Insert_rate_1 + Insert_rate_2)/2
    print('Insert:', str(round(float(Insert_rate)*100, 2)) + '%')
    if Delete_rate > Insert_rate:
        list_query_sentence[incorrect_index] = '?'+ list_query_sentence[incorrect_index]
        query_sentence = ' '.join(list_query_sentence)
        print(query_sentence)
        seg_query_sentence = list_query_sentence[incorrect_index-1] + " " + list_query_sentence[incorrect_index] + " " + list_query_sentence[incorrect_index+1]
        print('Query to linggle:', seg_query_sentence)
        res = linggle.query(seg_query_sentence)
        if len(res) == 0:
            print("linggle response is none")
        else:
            print("linggle response:")
            for i in range(0,3,1):
                if i < len(res):
                    print(res[i])
                else:
                    break
    else:
        list_query_sentence_copy = list_query_sentence.copy()

        list_query_sentence.insert(incorrect_index+1, '_')
        query_sentence = ' '.join(list_query_sentence)
        print(query_sentence)
        seg_query_sentence = list_query_sentence[incorrect_index] + " " + list_query_sentence[incorrect_index+1] + " " + list_query_sentence[incorrect_index+2]
        print('Query to linggle:', seg_query_sentence)
        res = linggle.query(seg_query_sentence)
        if len(res) == 0:
            print("linggle response is none")
        else:
            print("linggle response:")
            for i in range(0,3,1):
                if i < len(res):
                    print(res[i])
                else:
                    break
        print('')
        list_query_sentence_copy.insert(incorrect_index+2, '_')
        query_sentence = ' '.join(list_query_sentence_copy)
        print(query_sentence)
        seg_query_sentence = list_query_sentence_copy[incorrect_index] + " " + list_query_sentence_copy[incorrect_index+1] + " " + list_query_sentence_copy[incorrect_index+2] + " " + list_query_sentence_copy[incorrect_index+3]
        print('Query to linggle:', seg_query_sentence)
        res = linggle.query(seg_query_sentence)
        if len(res) == 0:
            print("linggle response is none")
        else:
            print("linggle response:")
            for i in range(0,3,1):
                if i < len(res):
                    print(res[i])
                else:
                    break
    
if __name__ == '__main__':
    linggle = Linggle()
    query_sentence = ''
    incorrect_index = -1
    index = 0
    with open('sentences-test.tsv', 'rt', encoding = 'utf-8') as f:
        for line in f:
            line = line.split('\t')
            if line[0] == '\n':
                process_sentence(query_sentence, linggle)
                print("=============================================================")
                incorrect_index = -1
                index = 0
                query_sentence = ''
                continue
            query_sentence += line[0] + ' '
            if line[1] == 'i\n' or line[1] == 'i':
                incorrect_index = index
            index += 1
        process_sentence(query_sentence, linggle) #the last test
