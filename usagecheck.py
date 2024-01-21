import os

dct={}
count={}

with open("./clothes.txt","r",encoding="utf-8") as file:
	for line in file:
		if line[0]=='x':
			line=line[1:]
		lst=line.split(',')
		dct[lst[1]]=line
		count[lst[1]]=0
file2=input('f_equip:')
for f in os.listdir(file2):
	for i in dct.keys():
		if i in f:
			count[i]=count[i]+1
# for i in dct.keys():
# 	if count[i]==0:
# 		print(dct[i])
with open("./clothes.txt","w",encoding="utf-8") as file:
	for i in dct.keys():
		if count[i]==0:
			file.write(dct[i])
		else:
			file.write("x"+dct[i])