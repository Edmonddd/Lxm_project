import os
import json
from augconversion import texConversion


# 存放被比较的序列
compare_berfor_tokens = []
ltokens = []
rtokens = []
orig_id = []
#用于对比旧，左右tokens
compare_map1 = []
#用于对比新，type
compare_map2 = []

def compare_string_arrays(array1, array2):
    if len(array1) != len(array2):
        return False
    for i in range(len(array1)):
        if array1[i] != array2[i]:
            return False
    return True


def refix(tokens,entities):
    # 匹配
    flag = 0
    not_compare = 0
    for i,compare in enumerate(compare_map2):
        
        is_same_order = compare_string_arrays(tokens,compare)

        if(is_same_order):
            print("tokens is ",tokens ,"\n",\
              "cpmpare with ", i+1)
            print("原来的是",compare_map1[i])
            flag = i
            break
        # if(i==len(compare_berfor_tokens)):
            # not_compare = 1
            # print("匹配不上\n")

    if(is_same_order == False):
        not_compare = 1
        print("匹配不上\n")

    for i,compare in enumerate(compare_berfor_tokens):
        if(not_compare == 1):
            break
        
        is_same_order = compare_string_arrays(compare_map1[flag],compare)

        if(is_same_order):
            print("原来的token能匹配上左右tokens")
            # print("tokens is ",tokens ,"\n",\
            #   "cpmpare with ", i)
            # print("原来的是",compare_map1[i])
            flag = i
            break

    if(is_same_order == False):
        not_compare = 1
        print("匹配不上\n")

    print("\n")

    if(not_compare != 1):
        word = {
            'tokens'    : tokens,
            'entities'  : entities,
            'relations' : [],
            'orig_id'   : orig_id[flag],
            'ltokens'   : ltokens[flag],
            'rtokens'   : rtokens[flag]
        }
    else:
        return ''

    return word
    



def convert(aug_json_havetype_file_path, aug_text_file, before_json_file_path, output_file_path):
    global compare_berfor_tokens
    global ltokens
    global rtokens
    global orig_id
    global compare_map1
    global compare_map2
    result = []

    # 增强文件 用于匹配
    compare_map1 , compare_map2 = texConversion(aug_text_file)

    # 原文件 用于加左右tokens
    with open(before_json_file_path) as f:
        data2 = json.load(f)
    for i in data2:
        compare_berfor_tokens.append(i['tokens'])
        orig_id.append(i['orig_id'])
        ltokens.append(i['ltokens'])
        rtokens.append(i['rtokens'])

    # 增强文件 用于加type
    with open(aug_json_havetype_file_path) as f:
        data1 = json.load(f)
    for number,i in enumerate(data1):
        tokens = i['tokens']
        entities = i['entities']
        print("number is ",number)
        if(number == 2500):
            print("1")
        resTemp = refix(tokens,entities)
        if(resTemp != ''):
            result.append(resTemp)


    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


def main():
    
    # aug_json_havetype_file_path = './json_file/aug_havetype_indeal.json'
    # aug_text_file = 'aug_file/ace04_train_attn_0.3_xlm-roberta-large-0.3-false-gauss-attention-dynamic-0.3-5-false-100-xlm-large-ace04-mixup-42-retrain-test.txt'
    # before_json_file_path = './json_file/ace2004_train_context.json'

    # 假数据
    aug_json_havetype_file_path = './fake_data/train_undeal.json'
    aug_text_file = 'M:\\llc\\数据记录\\ACLM\\untext\\ace04\\ace04_train_attn_0.3_xlm-roberta-large-ace04-mixup-42-retrain-only-aug-1.txt'
    before_json_file_path = './fake_data/train.json'

    output_file_path = 'M:\\llc\\数据记录\\ACLM\\untext\\ace04\\output\\result.json'

    convert(aug_json_havetype_file_path, aug_text_file, before_json_file_path, output_file_path)

if __name__ == "__main__":
    main()
  