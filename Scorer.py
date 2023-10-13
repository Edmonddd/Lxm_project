import random
import json

returnJson = []
# 定义全局变量
outputScoreFile = './output/scorereuslt.json'
outputFile = './output/deleteOscorereuslt.conll'
FilePath = './output/deleteO.conll'

# 随机得分，模拟 bert_ppl_original 函数
def random_score():
    return random.randint(0,10)

def writeToConll(output_text):
    with open(outputFile, 'w') as file:
    # 将字符串写入文件
        # output_string = ''.join(output_text)
        # file.write(output_string)
        for row in output_text:
            for i in row:
                line = i
                file.write(line)
            file.write('\n')

def writeToScoreJson(output_text):
    with open(outputScoreFile, 'w', encoding='utf-8') as file:
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
def sortScore(my_map,lines):
    global returnJson
    returnlines = []
    sorted_list = sorted(my_map.items(), key=lambda x: x[1], reverse=True)
    
    for number,item in enumerate(sorted_list):
        # 加入得分筛选
        if(item[1]>4 and item[1]<8):
            word = {
                "sentence"  : item[0],
                "score"     : item[1]
            }
            returnJson.append(word)
            returnlines.append(lines[number])
        print(item[0])

    return returnlines


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

        lines = sortScore(map,lines)

    writeToConll(lines)
    writeToScoreJson(returnJson)

    print("finish")
    


def main():
    create_score()


if __name__ == "__main__":
    main()
