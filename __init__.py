import os

lst=[]

file1=input('clothes.txt:')
with open(file1,"r",encoding="utf-8") as file:
	for line in file:
		if line[0]=='1':
			line=line[1:len(line)]
		lst.append(line)
print(lst)
file2=input('f_equip:')
for f in os.listdir(file2):
	for i in range(len(lst)):
		if f in lst[i] and lst[i][0]!='1':
			lst[i]='1'+lst[i]
with open(file1,"w",encoding="utf-8") as file:
	for line in lst:
		file.write(line)