import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

import collections
import math
import os
import queue
from concurrent.futures import ThreadPoolExecutor

queue = queue.Queue()


def entropy_calc(text):
    entropy = 0
    for key,value in collections.Counter(text).items():
        probability = value/len(text)
        entropy += (-probability)*math.log2(probability)
    return entropy


class Application(tk.Tk):
    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Tk", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)

        ttk.Style().configure("TButton", padding=1, relief="flat",background="#ccc")

        self.frame_1 = ttk.Frame(self)
        self.frame_2 = ttk.Frame(self)
        self.frame_3  = ttk.Frame(self)
        self.frame_4 = ttk.Frame(self,height=20,width=20)

        self.path_lable = ttk.Label(self.frame_1,text="请输入路径")
        self.path_entry_1 = ttk.Entry(self.frame_1)
        self.file_path_button = ttk.Button(self.frame_2,text="请选择文件",command=self.get_file_path)
        self.dir_path_button = ttk.Button(self.frame_2,text="请选择目录",command=self.get_dir_path)
        self.start_button = ttk.Button(self.frame_3,text="计算",command=self.get_entropy)
        # self.combox = ttk.Combobox(self.frame_3,height=40,width=60)
        self.Text = tk.Text(self.frame_4,width=100,height=19)


        self.path_lable.pack(side='left',padx=1,anchor='ne',pady=20)
        self.path_entry_1.pack(side='left',padx=1,anchor='ne',pady=20)
        self.file_path_button.pack(side='left',anchor='ne',pady=20,padx=1)
        self.dir_path_button.pack(side='left',anchor='ne',pady=20,padx=0.9)
        self.start_button.pack(side="top",pady=20)
        self.Text.pack()

        self.frame_1.pack()
        self.frame_2.pack()
        self.frame_3.pack()
        self.frame_4.pack()

    def get_file_path(self):
        self.file_path = filedialog.askopenfilename(title="请选择文件")
        self.path_entry_1.delete(0,tk.END)
        self.path_entry_1.insert(0,self.file_path)

    def get_dir_path(self):
        self.dir_path = filedialog.askdirectory(title="请选择目录")
        self.path_entry_1.delete(0,tk.END)
        self.path_entry_1.insert(0,self.dir_path)

    def get_entropy(self):
        text_list = []
        path = self.path_entry_1.get()
        if path == "":
            messagebox.showerror("error","请输入文件路径")

        if not os.path.exists(path):
            messagebox.showerror("error","该文件不存在")
            raise FileNotFoundError("该文件路径不存在")
        
        if os.path.isfile(path):
            try:
                with open(path,'rb+') as file:
                    file = file.read()
                print(f"{path}的熵是{entropy_calc(file)}")
                self.Text.delete("0.0",tk.END)
                self.Text.insert("1.0",f"{path}的熵是{entropy_calc(file)}\n")
            except PermissionError:
                self.Text.insert("1.0",f"{path}读取错误\n")
                pass


            
        
        if os.path.isdir(path):
            try:
                self.Text.delete("0.0",tk.END)
                for root,dir,file in os.walk(path):
                    for file in file:
                        file_path = os.path.join(root,file)
                        print(file_path)
                        queue.put(file_path)
            except PermissionError:
                pass

            def get_file_entropy(path):
                try:
                    with open(path,"rb+") as file:
                        file = file.read()
                    a = f"{path}的熵值是{entropy_calc(file)}\n\n"
                    
                    # print(f"{file_path}的熵值是{entropy_calc(file)}\n\n")
                    text_list.append(a)
                except PermissionError:
                    pass

            with ThreadPoolExecutor() as pool:
                while not queue.empty():
                    pool.submit(get_file_entropy,queue.get())
            
        if text_list:
            for text in text_list:
                self.Text.insert("1.0",text)
                # print(text)
                pass     

    
if __name__ == "__main__":
    app = Application()
    app.title("entropy-gui")
    app.wm_geometry(f"300x500+{int(app.winfo_screenheight()/2)}+{int(app.winfo_screenmmwidth()/2)}")
    app.mainloop()