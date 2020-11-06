# coding:utf-8
#↑日本語表示に必要
#csvファイルに書き出すため
import csv
import subprocess
import os
from subprocess import check_output


#WER,CER関数
def wer(r, h):

#initialisation 初期化
    import numpy
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
	    for j in range(len(h)+1):
	        if i == 0:
                       d[0][j] = j
	        elif j == 0:
                       d[i][0] = i


# computation 計算

    for i in range(1, len(r)+1):
            for j in range(1, len(h)+1):
                if r[i-1] == h[j-1]:
                   d[i][j] = d[i-1][j-1]
                else:
                    substitution = d[i-1][j-1] + 1
                    insertion    = d[i][j-1] + 1
                    deletion     = d[i-1][j] + 1
                    d[i][j] = min(substitution, insertion, deletion)

    return d[len(r)][len(h)]


#書き込むCSVファイルのパスを指定
csv_pass = "/home/yamamoto/dataset/google_dataset/wer_test.csv"

#正解テキストファイルのパスを指定
with open('/home/yamamoto/dataset/google_dataset/google_seikai.txt', 'r') as f:
     seikai_list = f.readlines()

#比較テキストファイルのフォルダを指定
hikaku_pass = "/home/yamamoto/dataset/google_dataset/properly_mukakou_text/"
ls = "ls -v "
ls += hikaku_pass
ls_out = check_output(ls.split()).decode("utf-8")
hikaku_list = ls_out.split('\n')
hikaku_list = hikaku_list[:-1]


#hikaku_list　比較ファイル名一覧
#hikaku_file  比較ファイル名
#hikaku_line  比較するテキスト

hikaku_pass += "/"

#要素数、次元数
WER_list = [[0 for i in range(len(hikaku_list))] for j in range(3)]

#比較ファイル数だけループ
for num in range(len(hikaku_list)):
    ave_WER = 0
    ave_CER = 0
    WER_0 = 0
    seikai_line = seikai_list[num]

    #比較するテキストファイルのパス
    hikaku_file = hikaku_pass
    hikaku_file += str(hikaku_list[num])
  
    #比較するテキストファイルの中身を読み込み
    with open(hikaku_file, 'r') as f:
         hikaku = f.readlines() 

    #比較ファイルの行数だけループ     
    for gyo_num in range(len(hikaku)):
        hikaku_line = hikaku[gyo_num]
        
        #CERの導出のために1文字を１単語扱いする
        hikaku_line_cer = (hikaku_line.replace(' ', '')).replace('',' ')
        seikai_line_cer = (seikai_line.replace(' ', '')).replace('',' ')

        #WERの導出
        different_WER = wer(seikai_line.split(),hikaku_line.split())
        word_len = len(seikai_line.split())
        WER = 100 * (different_WER / word_len)
        
        #CER計算
        different_CER = wer(seikai_line_cer.split(),hikaku_line_cer.split())
        cha_len = len(seikai_line_cer.split())
        CER = 100 * (different_CER/cha_len) 

        #平均の導出
        ave_CER = ave_CER + CER
        ave_WER = ave_WER + WER
        if round(WER, 1) == 0:
           WER_0 = WER_0 + 1

    WER_list[0][num] = round(ave_WER/len(hikaku),1)
    WER_list[1][num] = round(ave_CER/len(hikaku),1)
    WER_list[2][num] = round(100*(WER_0/len(hikaku)),1)
    print("{}個目のファイルのWER導出完了".format(num+1))
    print("比較したのはこの2つ")
    print(hikaku_list[num])
    print(seikai_line)
print("{}個のファイルのWER導出完了".format(num+1))

#csvファイルへ書き込み

with open(csv_pass, 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(WER_list) # 2次元配列を書き込み
