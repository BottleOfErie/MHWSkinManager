import os

# file="D:\\SJBox\\SJBox\\temp\\nativePC"
# old_name="501_0000"
# new_name="115_0001"

class PathFile:
	def __init__(self,dir,name):
		self.dir=dir
		self.name=name
		self.full=os.path.join(dir,name)
	def __str__(self):
		return f"{self.dir}[{self.name}]"
	def __repr__(self) -> str:
		return self.__str__()

def traverse(file,func):
	lst=[PathFile(file,item) for item in os.listdir(file)]
	while len(lst)>0:
		f=lst.pop(0)
		func(f)
		if os.path.isdir(f.full):
			lst.extend([PathFile(f.full,item) for item in os.listdir(f.full)])

def rename(f,old_name,new_name):
	if old_name in f.name:
		print(f)
		nm=os.path.join(f.dir,f.name.replace(old_name,new_name))
		os.rename(f.full,nm)
		f.full=nm

def batch_rename(file,old_name,new_name):
	print(old_name+"->"+new_name)
	traverse(file,lambda f:rename(f,old_name,new_name))

if __name__=="__main__":
	file=input("dir:")
	old_name=input("old:")
	new_name=input("new:")
	batch_rename(file,old_name,new_name)