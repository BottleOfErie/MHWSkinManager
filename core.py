
import os.path
import batch_remane
from PIL import Image
from distutils.dir_util import copy_tree

source_path="./source"
deploy_path='./deploy'
cloth_parts=["helm","body","arm","wst","leg"]
authors=["mangie","AragakiSama"]

cloths=[]
clothid={}
files={}


class Clothid:
    def __init__(self,line) -> None:
        lst=line.split(",")
        self.name=lst[0]
        self.id=lst[1]
        if lst[2]=='A\n':
            self.parts=[True,True,True,True,True]
        else:
            self.parts=[False,False,False,False,False]
            for i in lst[2]:
                if i !='\n':
                    self.parts[int(i)]=True
        self.usage=[]
    def add_usage(self,cloth):
        self.usage.append(cloth)
    def remove_usage(self,cloth):
        self.usage.remove(cloth)
    def __str__(self) -> str:
        return f"{self.name}:{len(self.usage)}"
    def __repr__(self) -> str:
        return self.__str__()

with open("./clothes.txt","r",encoding="utf-8") as file:
    for line in file:
        tmp=Clothid(line)
        clothid[tmp.id]=tmp


class Cloth:
    def __init__(self,source,absolute=False):
        if absolute:
            self.name="Unknown"
            self.source=source
        else:
            self.name=source
            self.source=os.path.join(source_path,source)
        self.count=0
        self.parts=[False,False,False,False,False]
        self.islegal=False
        self.id=[]
        self.author=[]
        self.marked=False
        self.ignored=False
        self.preview=None
        self.init_source()
    def test_file(self,f:batch_remane.PathFile):
        if not os.path.isdir(f.full):
            if not f.full[len(self.source):] in files.keys():
                files[f.full[len(self.source):]]=[]
            files[f.full[len(self.source):]].append(self)
        for item in authors:
            if not item in self.author and item in f.name:
                self.author.append(item)
        if f.name[0]=='p' and f.name[1]=='l' and f.name[2:] in clothid.keys():
            self.id.append(f.name[2:])
            self.count=self.count+1
        elif os.path.isdir(f.full) and f.name in cloth_parts:
            self.parts[cloth_parts.index(f.name)]=True
            
    def init_source(self):
        nativePC=os.path.join(self.source,"nativePC")
        if not os.path.isdir(nativePC):
            return
        batch_remane.traverse(nativePC,lambda f:self.test_file(f))
        if self.count>1 or len(self.id)!=1:
            return
        self.id=self.id[0]
        clothid[self.id].add_usage(self)
        for item in os.listdir(self.source):
            if item.split(".")[-1].lower() in ["png","jpg"]:
                self.preview=Image.open(os.path.join(self.source,item))
            if item=="ignored_mark":
                self.ignored=True
        self.islegal=True
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.__str__()

for item in os.listdir(source_path):
    tmp=Cloth(item)
    if tmp.islegal:
        cloths.append(tmp)
        if tmp.preview==None:
            print("no preview:"+item)
    else:
        print("illegal:"+item)

def cloth_change(origin:Cloth,to:Clothid):
    clothid[origin.id].remove_usage(origin)
    to.add_usage(origin)
    batch_remane.batch_rename(origin.source,origin.id,to.id)
    origin.id=to.id

def cloth_deploy(cloth:Cloth):
    copy_tree(os.path.join(cloth.source,"nativePC"),deploy_path)

def cloth_ignore(cloth:Cloth):
    markpath=os.path.join(cloth.source,"ignored_mark")
    if cloth.ignored:
        clothid[cloth.id].add_usage(cloth)
        os.remove(markpath)
    else:
        clothid[cloth.id].remove_usage(cloth)
        open(markpath,"x").close()
    cloth.ignored=not cloth.ignored

def cloth_deploy_all():
    for i in cloths:
        if not i.ignored:
            cloth_deploy(i)

if __name__=="__main__":
    for item in files.keys():
        if len(files[item])>1:
            print(item,files[item])