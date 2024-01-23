import batch_remane
import shutil
import os

goodname=""
filedir=""
replacer=""

lst=[]

def check(f:batch_remane.PathFile):
    return f.name==goodname

def replace(f:batch_remane.PathFile):
    if check(f):
        lst.append(f)

def rename0(file:batch_remane.PathFile,i:int):
    return os.path.join(file.dir,file.name+'-'+str(i))

def old_rename(file:batch_remane.PathFile):
    i=1
    while os.path.exists(rename0(file,i)):
        i=i+1
    print(f"{file.full}->{rename0(file,i)}")
    os.rename(file.full,rename0(file,i))

goodname=input("Name:")
filedir=input("TargetDirectory:")
batch_remane.traverse(filedir,replace)
print(lst)
replacer=input("Replacer:")
print(replacer,os.stat(replacer).st_size)
for item in lst:
    print(item,os.stat(item.full).st_size)
    choice=input("Replace?(Y/n)")
    if choice.lower()=='y':
        old_rename(item)
        shutil.copy(replacer,item.full)