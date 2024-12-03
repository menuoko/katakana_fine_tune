before_score = 0
after_score = 0

# 手作業で正解不正解の判定を行ったcheck.txtを読み込み、その正解率を確認する
with open("./check.txt","r",encoding="utf-8") as q: 
    list = []
    for line in q:
        line = line.rstrip('\n')
        list = line.split(" ")
        before_score += int(list[2])
        after_score += int(list[3])

print("ファインチューニング前 : {0}({1}/120)\n".format(before_score / 120,before_score))
print("ファインチューニング後 : {0}({1}/120)\n".format(after_score / 120,after_score))
