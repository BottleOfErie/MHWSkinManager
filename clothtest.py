import batch_remane
import subprocess
import os
import shutil

tempfolder="./temp"
tempfile="./tempfile"
deploy_location=""
old_id=[]
files=[]
new_id=""
nativePC=""

class DeployFile:
    def __init__(self,path):
        self.path=path
        self.deploy_path=deploy_location+path[len(nativePC):]
        self.isdir=os.path.isdir(path)
        self.exist=os.path.exists(self.deploy_path)
        self.remove_flag=False
        self.replace_flag=False

if not os.path.isdir(tempfolder):
    os.mkdir(tempfolder)


def unzip(file):
    shutil.rmtree(tempfolder)
    os.mkdir(tempfolder)
    _=subprocess.Popen(f"bz x {file} {tempfolder}")
    _.wait()
    return _.poll()==0

def dfs1(f:batch_remane.PathFile):
    if f.name[0]=='p' and f.name[1]=='l' and len(f.name)!=2:
        old_id.append(f.name[2:])
    elif f.name=="nativePC":
        global nativePC
        nativePC=f.full

def dfs2(f:batch_remane.PathFile):
    files.append(DeployFile(f.full))

def analyze():
    global nativePC
    nativePC=""
    global old_id
    old_id=[]
    batch_remane.traverse(tempfolder,dfs1)
    if nativePC=="":
        print("No nativePC folder!")
        return
    if len(old_id)!=1:
        print(f"clothID count:{len(old_id)}({str(old_id)})!")
        return
    batch_remane.batch_rename(nativePC,old_id[0],new_id)
    global files
    files=[]
    batch_remane.traverse(nativePC,dfs2)

def deploy():
    for dpfile in files:
        if dpfile.isdir:
            if not dpfile.exist:
                os.mkdir(dpfile.deploy_path)
                dpfile.remove_flag=True
        else:
            if dpfile.exist:
                dpfile.replace_flag=True
                shutil.move(dpfile.deploy_path,tempfile)
            shutil.move(dpfile.path,dpfile.deploy_path)
            if os.path.exists(tempfile):
                shutil.move(tempfile,dpfile.path)
    return

def undo_deploy():
    for dpfile in reversed(files):
        if dpfile.isdir:
            if dpfile.remove_flag:
                os.rmdir(dpfile.deploy_path)
        else:
            os.remove(dpfile.deploy_path)
            if dpfile.replace_flag==True:
                shutil.move(dpfile.path,dpfile.deploy_path)
    return

if __name__=="__main__":
    deploy_location=input("nativePC:")
    new_id=input("ClothID to replace:")
    target=input("zipfile:")
    while len(target)!=0:
        print("========Unzip")
        unzip(target)
        print("========Analyze")
        analyze()
        print("========Deploy")
        deploy()
        target=input("zipfile:")
        print("========Undo")
        undo_deploy()
