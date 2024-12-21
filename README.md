# 実行環境
python 3.11.7

# 共有データ
本研究はBCCWJ(Balanced Corpus of Contemporary
Written Japanese) [https://clrd.ninjal.ac.jp/bccwj] よりデータセットの作成を行っているが、規約によりBCCWJ内のデータの公開は著作権の観点から禁止されている。
そのため共有データはBCCWJより抽出した際の対象単語名(カタカナ語)のみとなる。

# 利用方法
-fine_tune_process/analysis.py
BCCWJからカタカタ語を含む文章を抽出し、それらの文をBeautifulSoupによってxmlから文字列形式に変換し、txtファイルに一度保存する。また抽出した単語を含む文が5つ以上ある場合はその単語をtango.txtに出力する。
-fine_tune_process/make_fine_data.py
対象単語を選別したファイル(source/circle.txt)とsource/circle下の各対象単語ごとに語義をラベル付けしたファイルを読み込み、訓練データ、テストデータを作る。実験1,7用

-fine_tune_process/make_fine_data2.py
実験2～6、実験8用のファイル

-experiment/test.py
実験1、実験7で使用する
fine-tuning前と後でテストデータに関する出力を得る。

-experiment_zero/test.py
実験2～6、実験8で使用する
fine-tuning前と後でテストデータに関する出力を得る。
