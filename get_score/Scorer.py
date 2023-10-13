import numpy as np
import torch
from transformers import BertTokenizer, BertForMaskedLM, XLMRobertaTokenizer, XLMRobertaForMaskedLM
import json
import copy
import gc
from tqdm import tqdm
import json

# 定义全局变量
outputScoreFile_first = './output/first/scorereuslt.json'
outputFile_first = './output/first/deleteOscorereuslt.conll'

outputScoreFile_middle = './output/middle/scorereuslt.json'
outputFile_middle = './output/middle/deleteOscorereuslt.conll'

outputScoreFile_last = './output/last/scorereuslt.json'
outputFile_last = './output/last/deleteOscorereuslt.conll'

FilePath = './output/deleteO.conll'

#比例
firstPartRatio = 0.2
lastPartRatio = 0.8

model_path = "/home/lxm/ACLM-main/xlm-roberta-large"
max_len = 120
device = 'cuda'

with torch.no_grad():
    model = XLMRobertaForMaskedLM.from_pretrained(model_path)
    model.to(device)
    model.eval()
    # Load pre-trained model tokenizer (vocabulary)
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)


def loadModel():
    with torch.no_grad():
        model = XLMRobertaForMaskedLM.from_pretrained(model_path)
        model.to(device)
        model.eval()
        # Load pre-trained model tokenizer (vocabulary)
        tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)

def bert_ppl_original(sent):
    with torch.no_grad():
        tokenize_input = tokenizer.tokenize(sent)
        sen_len = len(tokenize_input)

        if sen_len < max_len:
            tensor_input = tokenizer.convert_tokens_to_ids(tokenize_input)
            all_input = []
            for i, word in enumerate(tensor_input):
                text = copy.copy(tensor_input)
                text[i] = tokenizer.unk_token_id
                all_input.append(text)
            all_input = torch.tensor(all_input).to(device)
            output = model(all_input)
            pred_scores = output[0]
            # print(pred_scores.shape)
            index1 = torch.tensor([[_] for _ in range(pred_scores.shape[0])])
            index2 = torch.tensor([[_] for _ in tensor_input])
            probs = pred_scores[index1, index1].squeeze(1)
            probs = torch.log_softmax(probs, dim=1)
            word_loss = probs[index1, index2]
            sent_loss = torch.sum(word_loss).item()
            ppl = np.exp(-sent_loss / sen_len)
            del tokenize_input, tensor_input, all_input, output, pred_scores, index1, index2, probs, word_loss, sent_loss
            gc.collect()
            return ppl

        else:
            tensor_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)])
            sent_loss = 0.
            for i, word in enumerate(tokenize_input):
                tokenize_input[i] = tokenizer.mask_token
                mask_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)]).to(device)
                output = model(mask_input)
                pred_scores = output[0]
                ps = torch.log_softmax(pred_scores[0, i], dim=0)
                word_loss = ps[tensor_input[0, i]]
                sent_loss += word_loss.item()
                tokenize_input[i] = word  # restore
            ppl = np.exp(-sent_loss / sen_len)
            return ppl


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

    return returnlines,returnJson

# 评分排序
def sortScore(my_map):
    global returnJson
    returnlines = []
    sorted_list = sorted(my_map.items(), key=lambda x: x[1], reverse=False)

    #比例筛选 
    # 前面
    firstPart_num_elements = int(len(sorted_list) * firstPartRatio)
    firstPart_filtered_list = sorted_list[:firstPart_num_elements]

    #后面
    lastPart_num_elements = int(len(sorted_list) * lastPartRatio)
    lsatPart_filtered_list = sorted_list[lastPart_num_elements:]

    #中间
    middlePart_filtered_list = sorted_list[firstPart_num_elements:lastPart_num_elements]
    
    return firstPart_filtered_list,middlePart_filtered_list,lsatPart_filtered_list


def create_score():
    number = 0
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
            with torch.no_grad():
                score = bert_ppl_original(sentence)
            number += 1 
            if(number%1==0):
                torch.cuda.empty_cache()
                # print(torch.cuda.memory_summary())
                # loadModel()
            setence_socre_ls.append(score)

            map_2[sentence] = i
            map_1[sentence] = score

    firstPart_filtered_list,middlePart_filtered_list,lsatPart_filtered_list = sortScore(map_1)

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


    print("last part 一共有:",len(lines))


def main():
    create_score()


if __name__ == "__main__":
    main()

