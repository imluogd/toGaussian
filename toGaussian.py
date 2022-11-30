import sqlite3
import re
# 首先选择精度 CCSD(T)用orca?
#print("please select calculation level :")
# print("选择面板，需补充")
level = "M06-2X/MG3S"
# dic={}精度字典,需要补充

# 输入处理
todo_string = input("please enter the structure(MINx) you want to process:")
todo_list = todo_string.split(sep=',')
result_list = []
for item in todo_list:
    result_list.append(item.strip())
print(result_list)

# 先处理MIN
conn = sqlite3.connect('min.db')
print("processing MIN ...")
cursur = conn.cursor()
# id是否需要？--不需要，实在需要可以从name中取
select_result = cursur.execute("SELECT name, geom FROM min")


geom_list = []
name_list = []
# with open('test.txt','w+') as f:#如果该文件已存在则打开文件，原有内容会被删除。如果该文件不存在，创建新文件
for line in select_result:
    # print(line[0],line[1],sep='\n')
    if line[0] in result_list:
        #print("in !")
        # 可以保证一一对应，即名字与结构总是对得上，不会出现顺序错乱的情况，即便python会自动把生成的列表排序？为什么
        name_list.append(line[0])
        geom_list.append(line[1])  # 总之测试过是可以的，因为名字和结构是在一个循环写的
        # else:
        #print(line[0],'CAN NOT FOUND, PLEASE CHECK min.db')
    # f.write(str(name_list))
    # f.write('\n')
    # f.write(str(geom_list)) #写到文件里是方便查看，在控制台输出内容太多显示不全
# print(name_list)
for item in name_list:
    index = name_list.index(item)  # 我们处理到第几个了？
    file_name = item+'.gjf'
    with open(file_name, 'w+') as f:
        f.write("# "+level+" opt freq(calcfc)\n")
        f.write('\n')
        f.write(item+'\n\n')
        f.write('0 1\n')
        f.write(geom_list[index])
        f.write('\n\n')
# now process prod.db
print("now turn to PROD")
prod_string = input("please enter the structure(PRODx) you want to process:")
prod_list = prod_string.split(sep=',')
result_list2 = []
for item in prod_list:
    result_list2.append(item.strip())
print(result_list2)

name_list.clear()  # 清空两个含有min信息的列表
geom_list.clear()

conn = sqlite3.connect('prod.db')
print("processing PR ...")
cursur = conn.cursor()
select_result = cursur.execute("SELECT name, geom FROM prod")
for line in select_result:
    processed_name = (line[0]).split(sep="_")[0]
    if processed_name in prod_list:
        name_list.append(processed_name)
        geom_list.append(line[1])

#! ! ! 发现处理prod时，生成的坐标中会有整数‘5’，应为浮点数，于是将5替换为5.00000
for str in geom_list:
    index_of_sub = geom_list.index(str)
    geom_list[index_of_sub] = re.sub(r'-5', '-5.00000', str)

# print(name_list,geom_list)
for item in name_list:
    index = name_list.index(item)  # 我们处理到第几个了？
    file_name = item+'.gjf'
    with open(file_name, 'w+') as f:
        f.write("# "+level+" opt freq(calcfc)\n")
        f.write('\n')
        f.write(item+'\n\n')
        f.write('0 1\n')
        f.write(geom_list[index])
        f.write('\n\n')
# 一般要高精度计算的结构都会存在，就不提示没有了
