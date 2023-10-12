import os
from conlltojson import splitTokens

sentence = []
outputFile = './output/step_1/deleteO.conll'
conll_file_path = './step_1/ace04-equal.conll'

def writeToConll(output_text):
    with open(outputFile, 'w') as file:
    # 将字符串写入文件
        for i in output_text:
            output_string = ''.join(i)
        file.write(output_string)

def slove(lines):
    tokens = []
    entities = []
    flag = 1

    for i ,line in enumerate(lines):
        line = line.strip()
        if line.startswith('#'):
            continue
        # if line == '':
        #     if sentence:
        #         sentences.append(sentence)
        #         sentence = []
        else:
            parts = line.split('\t')
            tokens.append(parts[0])
            entities.append(parts[1])
    
    for i in entities:
        if(i != 'O'):
            flag = 0

    return flag

def main():
    global sentence
    deleteNumber = 0

    with open(conll_file_path, 'r') as file:
        lines = file.readlines()
        lines = splitTokens(lines)
        for line in lines:
            res = slove(line)
            deleteNumber += res
            if(res == 0):
                sentence.append(line)
    
    writeToConll(sentence)
    print("转化 写入文件完成\n")
    print("全为O的句子一共有:",deleteNumber)

if __name__ == "__main__":
    main()
  