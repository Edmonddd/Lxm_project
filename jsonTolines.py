import os 
import json

compare_berfor_tokens = []
ltokens = []
rtokens = []
orig_id = []

recompare_berfor_tokens = []
reltokens = []
rertokens = []

augTokens = []
reaugTokens = []
entities= []

before_json_file_path = './json_file/ace2004_train_context.json'
aug_json_file_path = './output/deleteO.json'
output_file_path = './output/temp/before.json'

def writeToJson1(output_text):
    global recompare_berfor_tokens
    global reltokens
    global rertokens
    returnJson = []
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i in range(len(recompare_berfor_tokens)):
            word = {
            "tokens"    : recompare_berfor_tokens[i],
            "ltokens"   : reltokens[i],
            "rtokens"   : rertokens[i]
            }
            returnJson.append(word)

        json.dump(returnJson, file, ensure_ascii=False, indent=2)


def writeToJson2(output_text):
    returnJson = []
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for i in range(len(reaugTokens)):
            word = {
            "tokens"    : reaugTokens[i],
            "entities"   : entities[i],
            }
            returnJson.append(word)

        json.dump(returnJson, file, ensure_ascii=False, indent=2)

def jsonToLines1(before_json_file_path, output_file_path):
    global compare_berfor_tokens
    global ltokens
    global rtokens
    global orig_id

    global recompare_berfor_tokens
    global reltokens
    global rertokens
    result = []
    temp = ""

    # 增强文件 用于匹配
    # compare_map1 , compare_map2 = texConversion(aug_text_file)

    # 原文件 用于加左右tokens
    with open(before_json_file_path) as f:
        data2 = json.load(f)
    for i in data2:
        compare_berfor_tokens.append(i['tokens'])
        orig_id.append(i['orig_id'])
        ltokens.append(i['ltokens'])
        rtokens.append(i['rtokens'])
           
    for word in compare_berfor_tokens:
        temp = ""
        for i in word:
            temp += i + ' '
        recompare_berfor_tokens.append(temp)
    
    for word in ltokens:
        temp = ""
        for i in word:
            temp += i + ' '
        reltokens.append(temp)

    for word in rtokens:
        temp = ""
        for i in word:
            temp += i + ' '
        rertokens.append(temp)


    writeToJson1(result)


def jsonToLines2(json_file_path, output_file_path):
    global augTokens
    global reaugTokens 
    global entities
    result = []
    temp = ""

    # 增强文件 用于匹配
    # compare_map1 , compare_map2 = texConversion(aug_text_file)

    # 原文件 用于加左右tokens
    with open(json_file_path) as f:
        data2 = json.load(f)
    for i in data2:
        augTokens.append(i['tokens'])
        entities.append(i['entities'])
           
    for word in augTokens:
        temp = ""
        for i in word:
            temp += i + ' '
        reaugTokens.append(temp)

    writeToJson2(result)



def main():
    # 原本的train文件转化
    jsonToLines1(before_json_file_path, output_file_path)

    # 增强后的文件转化
    #jsonToLines2(aug_json_file_path, output_file_path)

if __name__ == "__main__":
    main()
  