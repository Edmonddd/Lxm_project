import random
import json
from tqdm import tqdm

'''
    create_score_to1()
        得到一个总的得分文件。

    create_score_to3()
        得到三个总的得分文件，按比例划分。

    create_score_fromExist_to3()
        得到三个总的得分文件，按比例划分，但是不需要导入评分函数，直接从create_score_to1()得到的得分文件按比例划分。

'''



# 定义全局变量
# 比例输出的路径
outputScoreFile_first = './output/first/scorereuslt.json'
outputFile_first = './output/first/deleteOscorereuslt.conll'

outputScoreFile_middle = './output/middle/scorereuslt.json'
outputFile_middle = './output/middle/deleteOscorereuslt.conll'

outputScoreFile_last = './output/last/scorereuslt.json'
outputFile_last = './output/last/deleteOscorereuslt.conll'

FilePath = './output/step_1/deleteO.conll'

# 总分导入路径
FileResultPath = './output/first/scorereuslt.json'
FileResultConllPath = './output/first/deleteOscorereuslt.conll'

# 总分输出路径
OutputScoreFile = './output/first/scorereuslt.json'
OutputFile = './output/first/deleteOscorereuslt.conll'

#比例
FirstPartRatio = 0.2
LastPartRatio = 0.8

# 随机得分，模拟 bert_ppl_original 函数
def random_score():
    return random.randint(0,10)

def writeToConll(outputFile,output_text):
    with open(outputFile, 'w') as file:
    # 将字符串写入文件
        # output_string = ''.join(output_text)
        # file.write(output_string)
        for row in output_text:
            for i in row:
                line = i
                file.write(line)
            file.write('\n')

def writeToScoreJson(outputScoreFile,returnJson):
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
    

def convertToJson(sorted_list,map_2):
    returnJson = []
    returnlines = []

    for number,item in enumerate(sorted_list):
        # 加入得分筛选
        word = {
            "sentence"  : item[0],
            "score"     : item[1]
        }
        returnJson.append(word)
        returnlines.append(map_2[item[0]])
        # print(item[0])

    return returnlines,returnJson

# 评分排序
def sortScoreTo3(my_map):
    global returnJson
    returnlines = []
    sorted_list = sorted(my_map.items(), key=lambda x: x[1], reverse=True)

    #比例筛选 
    # 前面
    firstPart_num_elements = int(len(sorted_list) * FirstPartRatio)
    firstPart_filtered_list = sorted_list[:firstPart_num_elements]

    #后面
    lastPart_num_elements = int(len(sorted_list) * LastPartRatio)
    lsatPart_filtered_list = sorted_list[lastPart_num_elements:]

    #中间
    middlePart_filtered_list = sorted_list[firstPart_num_elements:lastPart_num_elements]
    
    return firstPart_filtered_list,middlePart_filtered_list,lsatPart_filtered_list


def sortScoreTo1(my_map):
    global returnJson
    returnlines = []
    sorted_list = sorted(my_map.items(), key=lambda x: x[1], reverse=True)
    return sorted_list


def create_score_to3():
    setence_socre_ls = []
    sentence = ''
    sentence_all = []
    #sent to score
    map_1 = {}
    #sent to sent_before
    map_2 = {}

    with open(FilePath, 'r') as file:
        lines = file.readlines()
        lines = splitTokens(lines)
        for i in tqdm(lines):
            sentence = ''
            score = 0
            for j in i:
                sentence += (j.split('\t')[0]) + (' ')
            # print(sentence)
            sentence_all.append(sentence)
            score = random_score()
            setence_socre_ls.append(score)

            map_2[sentence] = i
            map_1[sentence] = score

    firstPart_filtered_list,middlePart_filtered_list,lsatPart_filtered_list = sortScoreTo3(map_1)

    #first part
    lines,json = convertToJson(firstPart_filtered_list,map_2)
    writeToConll(outputFile_first,lines)
    writeToScoreJson(outputScoreFile_first,json)
    print("frist part 一共有:",len(lines))

    #middle part
    lines,json = convertToJson(middlePart_filtered_list,map_2)
    writeToConll(outputFile_middle,lines)
    writeToScoreJson(outputScoreFile_middle,json)
    print("middle part 一共有:",len(lines))

    #middle part
    lines,json = convertToJson(lsatPart_filtered_list,map_2)
    writeToConll(outputFile_last,lines)
    writeToScoreJson(outputScoreFile_last,json)
    print("last part 一共有:",len(lines))

    print("比分筛选finish")
    


def create_score_to1():
    setence_socre_ls = []
    sentence = ''
    sentence_all = []
    #sent to score
    map_1 = {}
    #sent to sent_before
    map_2 = {}

    with open(FilePath, 'r') as file:
        lines = file.readlines()
        lines = splitTokens(lines)
        for i in tqdm(lines):
            sentence = ''
            score = 0
            for j in i:
                sentence += (j.split('\t')[0]) + (' ')
            # print(sentence)
            sentence_all.append(sentence)
            score = random_score()
            setence_socre_ls.append(score)

            map_2[sentence] = i
            map_1[sentence] = score

    resultlist = sortScoreTo1(map_1)

    #first part
    lines,json = convertToJson(resultlist,map_2)
    writeToConll(outputFile_first,lines)
    writeToScoreJson(outputScoreFile_first,json)
    print("frist part 一共有:",len(lines))

    print("比分筛选finish")



def create_score_fromExist_to3():
    setence_socre_ls = []
    sentence = ''
    sentence_all = []
    #sent to score
    map_1 = {}
    #sent to sent_before
    map_2 = {}

    with open(FileResultPath, 'r') as file:
        data = json.load(file)
        for line in data:
            map_1[line['sentence']]=line['score']

    with open(FileResultConllPath, 'r') as file:
        lines = file.readlines()
        lines = splitTokens(lines)
        for i in lines:
            sentence = ''
            for j in i:
                sentence += (j.split('\t')[0]) + (' ')
            map_2[sentence] = i

    firstPart_filtered_list,middlePart_filtered_list,lsatPart_filtered_list = sortScoreTo3(map_1)

    #first part
    lines,jsonr = convertToJson(firstPart_filtered_list,map_2)
    writeToConll(outputFile_first,lines)
    writeToScoreJson(outputScoreFile_first,jsonr)
    print("frist part 一共有:",len(lines))

    #middle part
    lines,jsonr = convertToJson(middlePart_filtered_list,map_2)
    writeToConll(outputFile_middle,lines)
    writeToScoreJson(outputScoreFile_middle,jsonr)
    print("middle part 一共有:",len(lines))

    #middle part
    lines,jsonr = convertToJson(lsatPart_filtered_list,map_2)
    writeToConll(outputFile_last,lines)
    writeToScoreJson(outputScoreFile_last,jsonr)
    print("last part 一共有:",len(lines))

    print("比分筛选finish")

    
def main():
    # create_score_to1()
    # create_score_to3()
    create_score_fromExist_to3()


if __name__ == "__main__":
    main()
