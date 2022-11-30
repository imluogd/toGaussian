import sqlite3
import re
level= "M06-2X/MG3S"
print("now turn to PR")
prod_string=input("please enter the structure(PRx) you want to process:")
prod_list=prod_string.split(sep=',')
result_list2=[]
for item in prod_list: result_list2.append(item.strip())
print(result_list2)

name_list = []
geom_list = []
conn = sqlite3.connect('prod.db')
print ("processing PR ...")
cursur = conn.cursor()
select_result = cursur.execute("SELECT name, geom FROM prod")
for line in select_result:
    processed_name = (line[0]).split(sep="_")[0]
    if processed_name in prod_list:   
        name_list.append(processed_name)
        geom_list.append(line[1])

for str in geom_list:
    index_of_sub = geom_list.index(str)
    geom_list[index_of_sub]=re.sub(r'-5','-5.00000',str)
print(geom_list,geom_list[0])

for item in name_list:
    index=name_list.index(item)#我们处理到第几个了？
    file_name = item+'.gjf'
    with open(file_name,'w+') as f:
        f.write("# "+level+" opt freq(calcfc)\n")
        f.write('\n');f.write(item+'\n\n');f.write('0 1\n');f.write(geom_list[index]);f.write('\n\n')