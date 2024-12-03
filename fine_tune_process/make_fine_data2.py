import json
import random
name = []
cnt = 0
list = []
zero_shot_word = []
data = []                    # テストデータ中の対象単語と同じ名前の単語を含まない文章のみを訓練データとして格納する ex. test→アクセス　data→アクセスを含む文章を訓練データとはしない
test = []
data_2 = []                  # テストデータ中の対象単語と同じ名前の単語を含む文章のみを訓練データとして格納する ex. test→アクセス　data_2→アクセスを含む文章を訓練データとする
data_end = []
test_end = []
data_2_end = []
t = {}
role_user = {"role" : "user"}
role_assistant = {"role" : "assistant"}
role_system = {"role" : "system"}

with open("./circle.txt","r",encoding="utf-8") as q: # nameに対象単語をセット
    for line in q:
        if line.rstrip('\n')[0] != "△" and line.rstrip('\n')[0] != "×":
            name.append(line.rstrip('\n'))

for i in range(len(name)): 
    dictio = {}
    path = "./source/circle/" + name[i] + ".txt"
    with open(path, 'r',encoding="utf-8") as f:
        for line in f: 
            temp = line.split(" : ") 
            temp[1] = temp[1].rstrip("\n")
            if temp[1] =="0" or temp[1] =="1" or temp[1] =="2" or temp[1] =="3":
                cnt = cnt
            else:
                cnt += 1
                if temp[1] not in dictio:
                    dictio[temp[1]] = 1
                else:
                    dictio[temp[1]] += 1
    list.append(dictio)


count = 0
word_data = []
for i,word in enumerate(name):
    for k, v in list[i].items():
        if v == 1:
            s = word + " : " + str(k) + "\n"
            word_data.append(word)
            key = str(k)
            zero_shot_word.append(key)
            count += 1
word_data = set(word_data) # zero_shot_word内のwordのみ格納 出現頻度が1の意味を持つ文章の単語を格納

for i in range(len(name)):
    path = "./source/circle/" + name[i] + ".txt"
    system = "あなたは言語分析家です。次の文章中に含まれる{0}の意味を教えてください。回答に解説は必要ありません。".format(name[i])
    split_word = []
    with open(path, 'r',encoding="utf-8") as f:
        for line in f: 
            temp = line.split(" : ") 
            temp[1] = temp[1].rstrip("\n")
            if temp[1] =="0" or temp[1] =="1" or temp[1] =="2" or temp[1] =="3":
                cnt = cnt
            else:
                cnt += 1
                role_user["content"] = temp[0]
                role_assistant["content"] = temp[1]
                role_system["content"] = system
                t["messages"]= [role_system,role_user,role_assistant]
                if temp[1] in zero_shot_word:
                    test.append(json.dumps(t,ensure_ascii=False)) 
                else:
                    if name[i] in word_data:
                        data.append(json.dumps(t,ensure_ascii=False)) 
                    else:
                        data_2.append(json.dumps(t,ensure_ascii=False)) 
            # 辞書型は参照性があるため、一度json型からstr型に変換する


print(len(test)) # testに含まれるzero-shot用データの量 確認用

for i in range(len(data)):
    data_end.append(json.loads(data[i])) # json型に元の戻す

for i in range(len(test)):
    test_end.append(json.loads(test[i])) 

for i in range(len(data_2)):
    data_2_end.append(json.loads(data_2[i]))

# 訓練データ量を半分にする
# data_end = random.sample(data_end, len(data_end)//2)

d = "./data.jsonl"
with open(d,'w', encoding='utf-8') as f:
    for t in data_end:
        json.dump(t, f, ensure_ascii=False)
        f.write('\n')

te = "./test.jsonl"
with open(te,'w', encoding='utf-8') as f:
    for t in test_end:
        json.dump(t, f, ensure_ascii=False)
        f.write('\n')

d = "./data_2.jsonl"
with open(d,'w', encoding='utf-8') as f:
    for t in data_2_end:
        json.dump(t, f, ensure_ascii=False)
        f.write('\n')

'''
# 訓練データ量を半分にする
data2 = random.sample(data_2_end, 245//2)

d = "./data2.jsonl" # zero_shot用データ以外
with open(d,'w', encoding='utf-8') as f:
    for t in data2:
        json.dump(t, f, ensure_ascii=False)
        f.write('\n')
'''