
import json

# 定义全局变量
sentences = []

def extract_duplicates(lst):
    duplicates = []
    unique_elements = []
    
    for item in lst:
        if item not in unique_elements:
            unique_elements.append(item)
        else:
            duplicates.append(item)
    
    for item in duplicates:
        lst.remove(item)
    
    return duplicates


def has_duplicates(lst):
    seen = set()
    for item in lst:
        if item in seen:
            return True
        else:
            seen.add(item)
    return False


def have1type(entities):
    stack_list_res = {}
    def add_value(key, value):
        if key not in stack_list_res:
            stack_list_res[key] = []
        stack_list_res[key].append(value)

    entities_ret = []
    stack_list = [[] for _ in range(50)]

    for i,type in enumerate(entities):
    # 存到栈里面
        typet = type[1].split('-')[1]
        stack_list[i].append((type[0],typet))

    #处理栈
    for i,type in enumerate(stack_list):
        if(type == []):
            break
        add_value(type[0][1],type[0][0])
          
    for i in stack_list_res:
        duplicates_lst = []
        if(has_duplicates(stack_list_res[i])):
            duplicates_lst = extract_duplicates(stack_list_res[i])
            print(duplicates_lst)
            print(stack_list_res[i])

        for k,j in enumerate(stack_list_res[i]):
            if(k == 0):
                start = j
            elif(j != stack_list_res[i][k-1]+1 ):
                start = j
            if(k == len(stack_list_res[i])-1):
                end = j+1
                word = {
                    "type"  : i,
                    "start" : start,
                    "end"   : end,
                }
                entities_ret.append(word)
            elif(j != stack_list_res[i][k+1]-1):
                end = j+1
                word = {
                    "type"  : i,
                    "start" : start,
                    "end"   : end,
                }
                entities_ret.append(word)

    # type = entities[0][1].split('-')[1]
    # start = entities[0][0]
    # end = entities[0][0]+ len(entities)
    # word = {
    #     "type"  : type,
    #     "start" : start,
    #     "end"   : end,
    # }
    # entities_ret.append(word)

    return entities_ret



def have2type(entities):

    entities_ret = []
    stack_list_res = {}
    duplicates_lst = []

    def add_value(key, value):
        if key not in stack_list_res:
            stack_list_res[key] = []
        stack_list_res[key].append(value)

    stack_list = [[] for _ in range(50)]
    stack_list_res = {}
    stack_number = 0
    entities
    count_pre = 0
    for i,type in enumerate(entities):
        if(i!=0):
            count_pre = entities[i-1][1].count('-')
        count_now = type[1].count('-')
        number = type[0]
        type1 = type[1].split('-')[1]
        if(count_now == 2):
            type2 = type[1].split('-')[2]
        else:
            type2 = None
        
        # 存到栈里面
        stack_list[i].append((number,type1))
        if(count_now == 2):
            stack_list[i].append((number,type2))

    # 处理栈
    for i,type in enumerate(stack_list):
        if(type == []):
            break
        if(len(type)==1):
            add_value(type[0][1],type[0][0])
        else:
            add_value(type[0][1],type[0][0])
            add_value(type[1][1],type[1][0])
            
    for i in stack_list_res:
        duplicates_lst = []
        if(has_duplicates(stack_list_res[i])):
            duplicates_lst = extract_duplicates(stack_list_res[i])
            print(duplicates_lst)
            print(stack_list_res[i])

        for k,j in enumerate(stack_list_res[i]):
            if(k == 0):
                start = j
            elif(j != stack_list_res[i][k-1]+1 ):
                start = j
            if(k == len(stack_list_res[i])-1):
                end = j+1
                word = {
                    "type"  : i,
                    "start" : start,
                    "end"   : end,
                }
                entities_ret.append(word)
            elif(j != stack_list_res[i][k+1]-1):
                end = j+1
                word = {
                    "type"  : i,
                    "start" : start,
                    "end"   : end,
                }
                entities_ret.append(word)
        
        if(len(duplicates_lst)>0):
            for k,j in enumerate(duplicates_lst):
                if(k == 0):
                    start = j
                elif(j != duplicates_lst[k-1]+1 ):
                    start = j
                if(k == len(duplicates_lst)-1):
                    end = j+1
                    word = {
                        "type"  : i,
                        "start" : start,
                        "end"   : end,
                    }
                    entities_ret.append(word)
                elif(j != duplicates_lst[k+1]-1):
                    end = j+1
                    word = {
                        "type"  : i,
                        "start" : start,
                        "end"   : end,
                    }
                    entities_ret.append(word)

    return entities_ret


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
    



# 处理每一个entities
def solveEntities(entities):
    entities_ret = []
    # flag为1则单type
    flag = 1
    #判断是哪种类型 单type 还是 双type
    for i in entities:
        if(i[1].count('-') >= 2):
            flag =2
    
    if(flag == 1):
        entities_ret += have1type(entities)
    elif(flag == 2):
        entities_ret += have2type(entities)

    return entities_ret








def solveOneToken(lines):
    sentence = []
    tokens = []
    # 先将整个记录下来
    entities = []
    entities_ret = []
    
    for i ,line in enumerate(lines):
        line = line.strip()
        if line.startswith('#'):
            continue
        if line == '':
            if sentence:
                sentences.append(sentence)
                sentence = []
        else:
            parts = line.split('\t')
            tokens.append(parts[0])
            if(len(parts) ==2):
                types = parts[1]
                if(types[0] == 'B') :
                    # 重新初始化entities
                    entities = []
                    entities.append([i,types])
                elif (types[0] == 'I'):
                    entities.append([i,types])

                # 判断 1.下个为O 2.最后一个I 
                if(i < len(lines)-1):
                    if((types[0] == 'I' or types[0] == 'B')  \
                       and lines[i+1].split('\t')[1][0] == 'O'):
                        entities_ret += solveEntities(entities)
                elif(i == len(lines)-1):
                    if(types[0] == 'I'):
                        entities_ret += solveEntities(entities)
                    
    word = {
        "tokens" : tokens,
        "entities" :  entities_ret,
    }
    sentences.append(word)

    return 0








def read_conll_file(file_path):
    global sentences
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        tokens = []
        entities_type1 = []
        entities_type2 = []
        entities = []
        sentence = []

        # 分割多个token
        lines = splitTokens(lines)
        
        # 处理每个token的
        for  line in lines:
            solveOneToken(line)
    return sentences







def convert_to_json(conll_file_path, json_file_path):
    sentences = read_conll_file(conll_file_path)
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(sentences, file, ensure_ascii=False, indent=2)







if __name__ == "__main__":
    # 使用示例
    conll_file_path = 'M:\\llc\\数据记录\\ACLM\\untext\\ace04\\ace04-undeal.txt'
    json_file_path = 'M:\\llc\\数据记录\\ACLM\\untext\\ace04\\ace04-undeal.json'
    convert_to_json(conll_file_path, json_file_path)