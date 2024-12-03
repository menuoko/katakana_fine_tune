from openai import OpenAI
import openai
import json
import settings

# API_KEYの読み込み
openai.organization = settings.OK
openai.api_key = settings.AK
client = OpenAI(api_key=openai.api_key)

# テストデータのパスの指定
test_path = './test.jsonl'

# 変数
prompt = []              # プロンプトを格納
answer = []              # 正解を格納
a = []                   # ファインチューニング後のモデルを用いたプロンプトに対する回答を格納
b = []                   # ファインチューニング前のモデルを用いたプロンプトに対する回答を格納
name = []                # 各対象単語の名前を格納

# テストデータを読み込み
with open(test_path, 'r', encoding='utf-8') as file:
    test = [json.loads(line) for line in file]

# 手作業で条件を満たした単語を選定し、記述したファイルを読み込む
with open("./source/circle.txt","r",encoding="utf-8") as q:
    for line in q:
        if line.rstrip('\n')[0] != "△" and line.rstrip('\n')[0] != "×":
            name.append(line.rstrip('\n'))

# 指定したファイルから各対象単語に対応した選択肢を抽出する(goo辞書 https://dictionary.goo.ne.jp/ からスクレイピングしたもの)
pivot = 0
for word in name:
    path = "./source/choices/" + word + ".txt"
    k = []
    choices = "" # 選択肢の文字列
    with open(path,'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            k.append(line)
    for i in k:
        if choices != "":
            choices =choices + "," +  i
        else:
            choices = i

    # 3文ごとにsystemのcontentに選択肢を追加 ランダムに各単語(40語)から3文ずつテストデータとして利用しているため
    for i in range(pivot, pivot + 3):
        test[i]["messages"][0]["content"] = str(test[i]["messages"][0]["content"]) + "なお次の選択肢から一番近い意味を選んでください。" + choices
        prompt.append([test[i]["messages"][0],test[i]["messages"][1]])
        answer.append([test[i]["messages"][2]])
    pivot += 3
print("The prompts were completed.\n")

# ファインチューニング前のモデルを利用 gpt-4o-mini
cnt = 0
for item in prompt:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,                          # temperatureは0.9に指定
        messages=item
    )
    answer_to_prompt = "{0}. 出力:{1}\n正解:{2}\n".format(cnt+1,response.choices[0].message.content, answer[cnt][0]['content'])
    cnt += 1
    b.append(answer_to_prompt)
print("The before files were completed.\n")

# ファインチューニング後のモデルを利用
cnt = 0
for item in prompt:
    response = client.chat.completions.create(
        model = "", # ここでファインチューニング後のモデルを指定
        temperature=0.9,
        messages=item
    )
    p = "{0}. 出力:{1}\n正解:{2}\n".format(cnt+1,response.choices[0].message.content, answer[cnt][0]['content'])
    cnt += 1
    a.append(p)
print("The after files were completed.\n")

with open("./before.txt",'w', encoding='utf-8') as f:
        for t in b:
            print(*t,sep="",file=f,end="\n")

with open("./after.txt",'w', encoding='utf-8') as f:
        for t in a:
            print(*t,sep="",file=f,end="\n")