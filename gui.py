import tkinter as tk
import core
from PIL import ImageTk,Image
from os import startfile

def get_part_label(root,parts):
    frame=tk.Frame(root)
    for i in range(5):
        label=tk.Label(frame,text=core.cloth_parts[i])
        if parts[i]:
            label.config(fg="green")
        else:
            label.config(fg="red")
        label.pack(side=tk.LEFT)
    return frame

imagesize=500
tkimageobj=None
noneimage=Image.open("./none.jpg").resize((imagesize,imagesize))

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MHW skin manager")
        self.choosed_cloth=None
        self.choosed_clothid=None
        self.create_cloth_panel()
        self.create_clothid_panel()
        self.create_main_panel()
    def create_main_panel(self):
        frame=tk.Frame(self,width=200,height=400)
        self.cloth_frame=tk.Frame(frame,height=200)
        self.cloth_frame.pack()
        self.clothid_frame=tk.Frame(frame,height=200)
        self.clothid_frame.pack()
        self.button_frame=tk.Frame(frame,height=200)
        tk.Button(self.button_frame,text="Refresh",command=self.load_cloth_list).pack(side=tk.LEFT)
        tk.Button(self.button_frame,text="Mark",command=self.mark_or_demark).pack(side=tk.LEFT)
        tk.Button(self.button_frame,text="Ignore",command=self.ignore_or_not).pack(side=tk.LEFT)
        tk.Button(self.button_frame,text="Checkfile",command=self.start_dir).pack(side=tk.LEFT)
        tk.Button(self.button_frame,text="Change",command=self.rename).pack(side=tk.LEFT)
        tk.Button(self.button_frame,text="Deploy",command=core.cloth_deploy_all).pack(side=tk.LEFT)
        self.button_frame.pack()
        frame.pack()
    def clear_cloth_frame(self):
        for widget in self.cloth_frame.winfo_children():
            widget.destroy()
    def clear_clothid_frame(self):
        for widget in self.clothid_frame.winfo_children():
            widget.destroy()
    def show_cloth(self,item:core.Cloth):
        self.clear_cloth_frame()
        name=tk.Label(self.cloth_frame,text="Name:"+item.name)
        if item.marked:
            name.configure(fg="green")
        if item.ignored:
            name.configure(bg="red")
        name.pack()
        tk.Label(self.cloth_frame,text="Usage:"+str(core.clothid[item.id])).pack()
        tk.Label(self.cloth_frame,text="Author:"+str(item.author)).pack()
        get_part_label(self.cloth_frame,item.parts).pack()
        global tkimageobj
        if(not item.preview==None):
            ratio=min(imagesize/item.preview.width,imagesize/item.preview.height)
            tkimageobj=ImageTk.PhotoImage(item.preview.resize((int(item.preview.width*ratio),int(item.preview.height*ratio))))
            tk.Label(self.cloth_frame,image=tkimageobj,height=imagesize,width=imagesize).pack()
        else:
            tkimageobj=ImageTk.PhotoImage(noneimage)
            tk.Label(self.cloth_frame,image=tkimageobj,height=imagesize,width=imagesize).pack()
    def show_clothid(self,item:core.Clothid):
        self.clear_clothid_frame()
        tk.Label(self.clothid_frame,text="Name:"+item.name).pack()
        tk.Label(self.clothid_frame,text="Id:"+item.id).pack()
        get_part_label(self.clothid_frame,item.parts).pack()
        tk.Label(self.clothid_frame,text="Usage:"+str(item.usage)).pack()
        
    def load_cloth_list(self):
        curidx=self.cloth_list.yview()[0]
        self.cloth_list.delete(0,tk.END)
        for i in range(len(core.cloths)):
            self.cloth_list.insert(tk.END,core.cloths[i])
            if core.cloths[i].marked:
                self.cloth_list.itemconfigure(i,fg="green")
            if core.cloths[i].ignored:
                self.cloth_list.itemconfigure(i,bg="red")
        self.cloth_list.yview_moveto(curidx)
    def choose_cloth(self,id):
        self.choosed_cloth=core.cloths[id]
        self.show_cloth(core.cloths[id])
    def create_cloth_panel(self):
        frame=tk.Frame(self)
        self.cloth_list=tk.Listbox(frame,width=25)
        self.cloth_list.bind('<Double-Button-1>',lambda evt:self.choose_cloth(self.cloth_list.curselection()[0]))
        self.load_cloth_list()
        sb=tk.Scrollbar(frame,command=self.cloth_list.yview)
        self.cloth_list.config(yscrollcommand=sb.set)
        self.cloth_list.pack(side=tk.LEFT,fill=tk.BOTH)
        sb.pack(side=tk.RIGHT,fill=tk.BOTH)
        frame.pack(side=tk.LEFT)
    def load_clothid_list(self):
        curidx=self.clothid_list.yview()[0]
        self.clothid_list.delete(0,tk.END)
        self.clothid_text_list.clear()
        i=0
        for item in core.clothid.keys():
            self.clothid_list.insert(tk.END,core.clothid[item])
            if len(core.clothid[item].usage)>1:
                self.clothid_list.itemconfigure(i,bg="red")
            self.clothid_text_list.append(item)
            i=i+1
        self.clothid_list.yview_moveto(curidx)
    def choose_clothid(self,id):
        self.choosed_clothid=core.clothid[self.clothid_text_list[id]]
        self.show_clothid(core.clothid[self.clothid_text_list[id]])
    def rename(self):
        if self.choosed_cloth==None or self.choosed_clothid==None:
            return
        core.cloth_change(self.choosed_cloth,self.choosed_clothid)
        self.show_cloth(self.choosed_cloth)
        self.show_clothid(self.choosed_clothid)
        self.load_cloth_list()
        self.load_clothid_list()
    def mark_or_demark(self):
        if self.choosed_cloth==None:
            return
        self.choosed_cloth.marked=not self.choosed_cloth.marked
        self.show_cloth(self.choosed_cloth)
        self.load_cloth_list()
    def ignore_or_not(self):
        if self.choosed_cloth==None:
            return
        if self.choosed_cloth.ignored:
            core.clothid[self.choosed_cloth.id].add_usage(self.choosed_cloth)
        if not self.choosed_cloth.ignored:
            core.clothid[self.choosed_cloth.id].remove_usage(self.choosed_cloth)
        self.choosed_cloth.ignored=not self.choosed_cloth.ignored
        self.show_cloth(self.choosed_cloth)
        self.load_cloth_list()
        self.load_clothid_list()
    def start_dir(self):
        if self.choosed_cloth==None:
            return
        startfile(self.choosed_cloth.source)
    def create_clothid_panel(self):
        frame=tk.Frame(self)
        self.clothid_list=tk.Listbox(frame,width=25)
        self.clothid_text_list=[]
        self.clothid_list.bind('<Double-Button-1>',lambda evt:self.choose_clothid(self.clothid_list.curselection()[0]))
        self.load_clothid_list()
        sb=tk.Scrollbar(frame,command=self.clothid_list.yview)
        self.clothid_list.config(yscrollcommand=sb.set)
        self.clothid_list.pack(side=tk.LEFT,fill=tk.BOTH)
        sb.pack(side=tk.RIGHT,fill=tk.BOTH)
        frame.pack(side=tk.RIGHT)


if __name__=="__main__":
    app=App()
    app.mainloop()