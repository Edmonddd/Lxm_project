import json
import os

# 定义全局变量
JsonPath = "./files/ace.json"
outputFile = "./files/acc1.conll"
order = ["ltokens","tokens","rtokens"]
sum_Three = 0
#若flag为1，则删除带三个-的句子
deleteFlag = 0
countMaxLen = 0
# countMaxLen_result = 0

def conplextSum():
    global sum_Three
    sum_Three += 1

def writeToConll(output_text):
    with open(outputFile, 'w') as file:
    # 将字符串写入文件
        output_string = ''.join(output_text)
        file.write(output_string)


def writeType(words, entities, output_text):
    global countMaxLen
    words_list = []
    lable_list = []
    label_count_list = []
    size = 0
    # 初始化
    for i,word in enumerate(words):
        words_list.append(word)
        label_count_list.append(0)
        lable_list.append("")
        countMaxLen += 1
        size+=1
    
    # lable_list处理
    countNumberMoreThanThreeType_sum = 0
    sum = 0
    for _ ,obj in enumerate(entities):
        for i,word in enumerate(words):
            if(int(obj["start"]) <= i and int(obj["end"]) > i):
                label_count_list[i] += 1
                lable_list[i] = lable_list[i]+("-"+obj["type"])
                # print(words_list[i])

    # 统计 --- 数量
    for i,word in enumerate(words):
        sum=0
        for j in lable_list[i]:
            if(j =="-"):
                sum += 1
        if(sum >= 3):
            countNumberMoreThanThreeType_sum += 1

    #记录 并中途退出
    if(countNumberMoreThanThreeType_sum > 0):
        conplextSum()
        if(deleteFlag):
            return output_text
    
    # 整合words_list和lable_list
    count = 0
    for i,word in enumerate(words):
        if(label_count_list[i]>0 and count==0):
            lable_list[i] = "\t"+"B"+lable_list[i]
            count = count+1
        else:
            if(label_count_list[i]>0):
                lable_list[i] = "\t"+"I"+lable_list[i]
            else:
                lable_list[i] = "\t"+"O"
                count = 0
        words_list[i] = words_list[i]+lable_list[i]+"\n"
    output_text += words_list
    return output_text

def main():
# 打开JSON文件
    global countMaxLen
    countMaxLen_result = 0 
    output_text = []
    with open(JsonPath) as file:
        data = json.load(file)
    for obj in data:
        countMaxLen = 0
        # keys belong to : ["tokens","entities","relations","ltokens","rtokens"]
        for keys in order:
            TokensValue = obj[keys]
            if(keys == "tokens"):
                output_text = writeType(obj["tokens"],obj["entities"],output_text)
            else:
                for i in TokensValue:   
                    output_text.append(i+"\t"+"O"+"\n")
                    countMaxLen += 1
        output_text.append("\n")
        countMaxLen_result = max(countMaxLen,countMaxLen_result)


    # 写入conll文件
    writeToConll(output_text)
    print("所有句子的最长长度为",countMaxLen_result)
    print(sum_Three)
    print("转换完成")

if __name__ == "__main__":
    main()
