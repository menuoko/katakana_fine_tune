import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

ans = {}
ans_t = {}
gaikoku_go = 0
xml_data = ''
flag = 0
# core_SUWからカタカナ語を含む文章を抽出し、一度それらの文章をtxtファイルに変換し保存する
with open('./core_SUW.txt',encoding="utf-8") as f:
    flag = 0
    for line in f:
        l = line.split("	")
        if(l[15] == "外"):
            gaikoku_go += 1
            judge = l[-2] # 後ろから2番目を格納
            if (l[0] == "PB" or l[0] == "LB"):
                t = './{0}/{1}/{2}.txt'.format(l[0],l[1][0:3],l[1])
            elif(l[0] == "OC" or l[0] == "OY"):
                t = './{0}/{1}/{2}.txt'.format(l[0],l[1][0:4],l[1])
            else:
                t = './{0}/{1}.txt'.format(l[0],l[1])
                ''' # BeautifulSoup でxmlタグを無視して文章を抽出
                with open(path, 'r', encoding='utf-8') as file:
                    xml_data = file.read()
                soup = BeautifulSoup(xml_data, 'lxml')
                text = soup.get_text(separator="\n")
                '''
            with open(t, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            for line in lines:
                if flag == 1:
                    flag = 0
                    break
                if judge in line:
                    if judge not in ans_t:
                        ans_t[judge] = []
                    ans[line] = l[1]
                    ans_t[judge].append(line.strip())
                    flag = 1

name = []

# 各カタカナ語を含む文章が5つ以上ある場合、その単語を抽出する
with open("./tango.txt","w",encoding="utf-8") as o:
    for key, value in ans_t.items():
        value = set(value)
        if len(value) >= 5:
            ex = ": "
            print(*key,sep="",file=o,end="\n")

# 抽出単語数計算 (網羅率計算)
cnt = 0
for key, value in ans_t.items():
    ex = ": "
    v = str(len(value))
    cnt += len(value)

print(cnt)              # 抽出した単語数 32226
print(gaikoku_go)       # 全体の単語数   36338
