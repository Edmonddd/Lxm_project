import json

def dealOneLine(lines):
    # 将字符串转换为 JSON 格式
    json_data = json.loads(lines)

    #处理start:
    json_data[0] = json_data[0].split(':  ')[1] 
    json_data[1] = json_data[1].split(':  ')[1] 

    #将空格分开：
    json_data[0] = json_data[0].split(' ')
    json_data[1] = json_data[1].split(' ')

    return json_data

def texConversion(aug_text_file_path):
    res = []
    res1 = []
    res1 = []
    #aug_text_file_path = 'aug_file/ace04_train_attn_0.3_xlm-roberta-large-0.3-false-gauss-attention-dynamic-0.3-5-false-100-xlm-large-ace04-mixup-42-retrain-test.txt'
    # before_json_file_path = './ace2004_dev_context.json'
    # output_file_path = './result.json'
    with open(aug_text_file_path, 'r') as file:
        for lines in file: 
            res.append(dealOneLine(lines))

    res1 = [x[0] for x in res]
    res2 = [x[1] for x in res]

    return res1,res2 

def main():
    aug_text_file_path = 'aug_file/ace04_train_attn_0.3_xlm-roberta-large-0.3-false-gauss-attention-dynamic-0.3-5-false-100-xlm-large-ace04-mixup-42-retrain-test.txt'
    print(texConversion(aug_text_file_path))

if __name__ == "__main__":
    main()
  