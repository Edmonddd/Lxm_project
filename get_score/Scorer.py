import numpy as np
import torch
from transformers import BertTokenizer, BertForMaskedLM, XLMRobertaTokenizer, XLMRobertaForMaskedLM
import json
import copy
import gc
from tqdm import tqdm

returnJson = []
# 定义全局变量
outputFile = '/home/lxm/ACLM-main/step_3/scorereuslt.json'
FilePath = '/home/lxm/ACLM-main/step_3/unequal_deleteO.conll'

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
    number = 0
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
            with torch.no_grad():
                score = bert_ppl_original(sentence)
            number += 1 
            if(number%1==0):
                torch.cuda.empty_cache()
                # print(torch.cuda.memory_summary())
                # loadModel()
            if(number%200==0):
                print(1)
            print(number)
            setence_socre_ls.append(score)
            map[sentence] = score

        sortScore(map)


    writeToConll(returnJson)
    print("finish")


def main():
    # loadModel()
    create_score()


if __name__ == "__main__":
    main()

# def create_score(filepath):
#     setence_socre_ls = []
#     with open(filepath, 'w') as f:
#         for sentence in tqdm(f):
#             score = bert_ppl_original(sentence)
#             tmp = {sentence: score}
#             setence_socre_ls.append(tmp)
#             f.write(score)


# create_score()


# sentence = 'Xinhua News Agency , Canberra , January 13 , by Xinhua News Agency , in Manila , by reporter Changyi Xiong'
# score = bert_ppl_original(sentence)
# print(score)



