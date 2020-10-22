import fileinput
from tqdm import tqdm
from collections import Counter
from multiprocessing import Pool
import re
import operator

# tokenize text and get words list
def words(text): return re.findall(r'\w+', text.lower())

def mapper(row):
    row_split = row.split('\t')
    if len(row_split) == 1:
        return None
    if len(words(row_split[0])) == 1:
        return None
    row_space_split = row_split[0].split(' ')
    ret_str = ""
    i = 0
    for s in row_space_split:
        if i == 0:
            ret_str += s
        elif i == len(row_space_split)-1:
            ret_str += " " + s
        i = i + 1
    return ((ret_str, len(words(row_split[0]))-1), int(row_split[1]))

def reducer(data):
    ret_dict = {}
    for d in data:
        if ret_dict.get(d[0]) != None:
            ret_dict[d[0]] += d[1]
        else:
            ret_dict[d[0]] = d[1]
    ret_dict_sorted = sorted(ret_dict.items(), key=lambda x: x[1], reverse=True)
    f = open('result.txt','w')
    for i in range(0,30,1):
        f.write("{}\t{}\n".format(ret_dict_sorted[i][0], ret_dict_sorted[i][1]))
        print(ret_dict_sorted[i][0], ret_dict_sorted[i][1])
    f.close()

if __name__ == "__main__":

    # Create multiprocessing pool
    pool = Pool()

    # Map
    print("Map Stage...")
    with open("web1t.baby") as f:
        baby1t = f.read().splitlines()
    skipgram_count = [row for row in pool.map(mapper, baby1t) if row]
    skipgram_count.sort(key=lambda x: x[0])
    # skipgram_count:
    # [
    #   ... ,
    #   (('of the', 1), 12345678),
    #   (('of the', 1), 123),
    #   (('at the', 2), 456),
    #   ...
    # ]

    # Reduce
    print("Reduce Stage...")
    reducer(skipgram_count)
