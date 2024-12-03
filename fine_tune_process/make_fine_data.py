import json
import random
# ラベリング用のデータを用意 → 12行目のパスを書き換えるだけでjsonlファイルを作成できる
# ラベリング → 意味区分の数字
# ラベリングした後、goo辞書の意味区分を参照して、意味区分の0番目の要素と比較してデータのフラグを確認 → 
# 変数
data = []                                           # 訓練データを格納する
test = []                                           # テストデータを格納する
data_end = []                                       # 文字列をjson型に変換したものを格納(訓練データ)
test_end = []                                       # 文字列をjson型に変換したものを格納(テストデータ)
t = {}                                              # 仮置きのプロンプト文を格納
role_user = {"role" : "user"}                       # 質問対象の文を格納
role_assistant = {"role" : "assistant"}             # 正解の意味を格納
role_system = {"role" : "system"}                   # システム文を格納
name = []                                           # 対象単語を格納

with open("./circle.txt","r",encoding="utf-8") as q: # nameに対象単語をセット
    for line in q:
        if line.rstrip('\n')[0] != "△" and line.rstrip('\n')[0] != "×":
            name.append(line.rstrip('\n'))

# 各対象単語ごとにランダムに3文をテストデータ、それ以外をfien-turning用の訓練データとする
for i in range(len(name)):
    path = "./source/circle/" + name[i] + ".txt"
    system = "あなたは言語分析家です。次の文章中に含まれる{0}の意味を教えてください。回答に解説は必要ありません。".format(name[i])
    k = [] # 仮置き用の変数
    with open(path, 'r',encoding="utf-8") as f:
        for line in f: 
            temp = line.split(" : ") 
            # ??? : 意味 →　messages[[system : あなたは言語分析家です。次の文章中に含まれる{0}の意味を教えてください。回答に解説は必要ありません。 user : ??? assistant : 意味]]
            temp[1] = temp[1].rstrip("\n")
            if temp[1] =="0" or temp[1] =="1" or temp[1] =="2" or temp[1] =="3":
                pass
            else:
                role_system["content"] = system
                role_user["content"] = temp[0]
                role_assistant["content"] = temp[1]
                t["messages"]= [role_system,role_user,role_assistant]
                k.append(json.dumps(t,ensure_ascii=False)) # 仮で置く
            # 辞書型は参照性があるため、一度json型からstr型に変換する 
    random_sentence = random.sample(k, 3) # ランダムに3文抽出する
    for i in k:
        if i in random_sentence:
            test.append(i)
        else:
            data.append(i)

for i in range(len(data)):
    data_end.append(json.loads(data[i])) # json型に元の戻す

for i in range(len(test)):
    test_end.append(json.loads(test[i])) 

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