import subprocess
from subprocess import check_output

#dire_name deepspeechに入力する音声ファイルが入ったすべてのディレクトリ名
#onsei_pass 現在入力しているの音声ファイルのディレクトリ名
#file_name onsei_passが示すディレクトリの中身一覧


rute_pass = "/home/yamamoto/dataset/google_dataset/saikai/"
ls = "ls -v "
ls += rute_pass
ls_out = check_output(ls.split()).decode("utf-8")

dire_name = ls_out.split('\n')
dire_name = dire_name[:-1]


for dire_num in range(len(dire_name)):
    rute_pass = "/home/yamamoto/dataset/google_dataset/saikai/"
    rute_pass += dire_name[dire_num]
    onsei_pass = rute_pass

    ls = "ls -v "
    ls = ls.split()
    ls.append(onsei_pass)
    all_file = check_output(ls).decode("utf-8")
    file_name = all_file.split('\n')
    file_name = file_name[:-1]

    out_file = "/home/yamamoto/dataset/google_dataset/moto_mukakou_text/"  
    out_file += dire_name[dire_num]
    out_file += ".txt"
    f = open(out_file, 'a')
    f.close() 

    for onsei in file_name:
        deepcommand = "deepspeech --model /home/yamamoto/onsei/deepspeech-0.4.1-models/output_graph.pb --alphabet /home/yamamoto/onsei/deepspeech-0.4.1-models/alphabet.txt --audio "
        deepspeech = deepcommand.split()
        add = onsei_pass
        add += "/"
        add += str(onsei) 
        deepspeech.append(add)
        out_text = check_output(deepspeech).decode("utf-8")
        print(onsei)
        print(out_text)
        f = open(out_file, 'a')
        f.write(out_text)
