import json
from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.matching import NodeMatcher
from gensim.models import KeyedVectors, word2vec
from jieba import cut, load_userdict, cut_for_search
import re
from zhon.hanzi import punctuation as cn_punctuation
from string import punctuation as en_punctuation


def connectNeo4j():
    return Graph("http://localhost:7474", auth=("neo4j", "130340"))


def model2json():
    with open('model/sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5', 'r', encoding='utf-8') as f:
        word2vec = {}
        inf = f.readline()
        inf = inf.split(' ')
        length = int(inf[0])
        dim = inf[1]
        for line in range(0, length):
            data = f.readline().split(' ')
            word2vec[data[0]] = data[1:]
            if(line % 10000) == 0:
                if line == 0:
                    with open('word2vec.json', 'w') as json_file:
                        json.dump(word2vec, json_file)
                else:
                    with open('word2vec.json', 'a') as json_file:
                        json.dump(word2vec, json_file)
                print(str(line / length * 100) + '%')
                word2vec = {}
        with open('word2vec.json', 'a') as json_file:
            json.dump(word2vec, json_file)
        print(str(line / length * 100) + '%')


def generateModel():
    graph = connectNeo4j()

    model = KeyedVectors.load_word2vec_format('sgns.target.word-word.dynwin5.thr10.neg5.dim300.iter5',
                                                       binary=False, encoding="utf8", unicode_errors='ignore')
    # word2vecModel = KeyedVectors.load_word2vec_format('word2vecModel.bin', binary=True, encoding="utf8", unicode_errors='ignore')
    print('Word2vec model load finished!')

    modelKey = []
    for key in model.index_to_key:
        modelKey.append(str(key) + '\n')
    with open('model_key.txt', 'w', encoding='utf-8') as f:
        f.writelines(modelKey)

    word2vec = {}
    load_userdict('model_key.txt')
    nodeMatcher = NodeMatcher(graph)
    nodes = nodeMatcher.match().order_by('_.index')
    for node in list(nodes):
        search_list = cut_for_search(node['label'])
        for key in search_list:
            try:
                word2vec[key] = model[key].tolist()
                print(key, word2vec[key])
            except:
                pass

    with open('model.json', 'w') as f:
        json.dump(word2vec, f)


    with open('model.json', 'r') as f:
        model_data = json.load(f)
    lines = []
    lines.append(str(len(model_data)) + ' 300\n')
    for key, value in model_data.items():
        line = str(key)
        for i in range(0, len(value)):
            line += ' ' + str(value[i])
        lines.append(line + '\n')

    with open('model', 'w', encoding="utf8") as f:
        f.writelines(lines)


def generateData(fileName):
    with open('data.txt', 'w', encoding='utf-8') as ff:
        pass
    with open(fileName, errors='ignore', encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            seg_list = cut(line)
            # print(list(seg_list))
            seg_list = preprocess_Chinese(seg_list)
            # seg_list = preprocess_English(seg_list)
            # print(seg_list)
            with open('data.txt', 'a', encoding='utf-8') as ff:
                ff.write(' '.join(seg_list))  # 词汇用空格分开


def preprocess_Chinese(content):
    # print(list(content))
    train = []
    for line in content:
        line = re.sub(r'[{}]+'.format(cn_punctuation), '', line)
        if len(line) > 0:
            train.append(line)
    return train


def preprocess_English(content):
    train_data = []
    for word in content:
        word = re.sub(r'[{}]+'.format(en_punctuation), '', word)
        if len(word) > 0:
            train_data.append(word)
    return train_data


def trainMyModel():
    # 加载语料
    sentences = word2vec.Text8Corpus('data.txt')

    # 训练模型
    model = word2vec.Word2Vec(sentences)

    # 选出最相似的10个词
    for e in model.wv.most_similar(positive=['项'], topn=10):
        print(e[0], e[1])

# generateData('chap18 关联规则挖掘.txt')
trainMyModel()

# word2vecModel = KeyedVectors.load_word2vec_format('word2vecModel', binary=False, encoding="utf8", unicode_errors='ignore')
# print(word2vecModel['关联'])
# print(word2vecModel.similarity('关联', '规则'))
# print(word2vecModel.most_similar('关联', topn=10))
# word2vecModel.save_word2vec_format('word2vecModel.bin', binary=True)