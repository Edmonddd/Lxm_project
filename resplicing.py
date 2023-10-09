import os
import json

# 存放被比较的序列
compare_berfor_tokens = []
ltokens = []
rtokens = []
orig_id = []

def compare_string_arrays(array1, array2):
    if len(array1) != len(array2):
        return False
    for i in range(len(array1)):
        if array1[i] != array2[i]:
            return False
    return True


def refix(tokens,entities):
    # 匹配
    for i,compare in enumerate(compare_berfor_tokens):
        is_same_order = compare_string_arrays(tokens,compare)

        if(is_same_order):
            print("tokens is ",tokens ,"\n",\
              "cpmpare with ", i)
            break
        if(i==len(compare_berfor_tokens)-1):
            print("匹配不上")
    # 拼接
    word = {
        'tokens'    : compare,
        'entities'  :entities,
        'relations' : [],
        'orig_id'   : orig_id[i],
        'ltokens'   : ltokens[i],
        'rtokens'   : rtokens[i]
    }
    return word
    



def convert(aug_json_file_path,before_json_file_path,output_file_path):
    global compare_berfor_tokens
    global ltokens
    global rtokens
    global orig_id
    result = []
    with open(aug_json_file_path) as f:
        data1 = json.load(f)
    with open(before_json_file_path) as f:
        data2 = json.load(f)
    for i in data2:
        compare_berfor_tokens.append(i['tokens'])
        orig_id.append(i['orig_id'])
        ltokens.append(i['ltokens'])
        rtokens.append(i['rtokens'])

    for i in data1:
        tokens = i['tokens']
        entities = i['entities']
        result.append(refix(tokens,entities))
    
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)


def main():
    aug_json_file_path = './acc1_reverse.json'
    before_json_file_path = './ace2004_dev_context.json'
    output_file_path = './result.json'
    convert(aug_json_file_path,before_json_file_path,output_file_path)
    

if __name__ == "__main__":
    main()
  