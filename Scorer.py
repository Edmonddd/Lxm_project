import random
import json

returnJson = []
# 定义全局变量
outputFile = './output/scorereuslt.json'
FilePath = './output/deleteO.conll'

# 随机得分，模拟 bert_ppl_original 函数
def random_score():
    return random.randint(0,10)

def writeToConll(output_text):
    with open(outputFile, 'w', encoding='utf-8') as file:
        json.dump(returnJson, file, ensure_ascii=False, indent=2)


# 分割多个token
def splitTokens(lines):
    sub_lists = []
    split_key = '\n'
    last_i = 0 
    for i ,line in enumerate(lines) :
        if(line == split_key):
            if(lines[i-1] == split_key):
                last_i = i + 1 
                continue
            sub_lists.append(lines[last_i:i])
            last_i = i + 1 
        if(line != split_key and i == len(lines)-1):
            sub_lists.append(lines[last_i:i])
    return sub_lists
    
# 评分排序
def sortScore(my_map):
    global returnJson
    sorted_list = sorted(my_map.items(), key=lambda x: x[1])
    for item in sorted_list:
        word = {
            "sentence"  : item[0],
            "score"     : item[1]
        }
        returnJson.append(word)
        print(item[0])


def create_score():
    setence_socre_ls = []
    sentence = ''
    sentence_all = []
    map = {}
    
    with open(FilePath, 'r') as file:
        lines = file.readlines()
        lines = splitTokens(lines)
        for i in lines:
            sentence = ''
            score = 0
            for j in i:
                sentence += (j.split('\t')[0]) + (' ')
            # print(sentence)
            sentence_all.append(sentence)
            score = random_score()
            setence_socre_ls.append(score)
            map[sentence] = score

        sortScore(map)


    writeToConll(returnJson)
    print("finish")
    


def main():
    create_score()


if __name__ == "__main__":
    main()

# sentence = 'Xinhua News Agency , Canberra , January 13 , by Xinhua News Agency , in Manila , by reporter Changyi Xiong'
# score = bert_ppl_original(sentence)
# print(score)