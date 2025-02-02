import requests,json,os
from io import StringIO
from tkinter.filedialog import askdirectory
import tkinter.messagebox as messagebox
from tkinter import *
import tkinter.ttk as ttk
from win32com.client import Dispatch
import tkinter.scrolledtext as scrolledtext



class App(Tk):
    def __init__(self):
        super().__init__()
        self.base = r"https://raw.githubusercontent.com/Pr0methee/Fractalus-apps/main/"

        self.geometry("500x250")
        self.resizable(False, False)
        #self.iconbitmap("logo.ico")
        self.title("Downloading Fractalus")
        lab = Label(self, text="Connection to web server...")
        lab.place(x=5, y=0)
        self.d = json.load(StringIO(requests.get(self.base + "install.json").content.decode().replace('{"--début--"}', '').replace('{"--fin--"}', '')))
        self.lab=lab
        self.copyright()

    def copyright(self):
        self.lab['text'] = "Welcome, you are about to download the Fractalus virtual machine.\n Please read the following and confirm you agree with the terms."
        text = scrolledtext.ScrolledText(self,wrap=WORD)
        text.place(x=5,y=35,width = 490,height=175)

        text.insert("0.0", """BSD 3-Clause License

Copyright (c) 2024, Valentin Novo (Pr0methee)

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""")
        text.config(state='disabled')

        Checkbutton(self,text="I have read and I accept the terms.",command=self.check).place(x=5,y=220)
        self.btn = Button(self,text="Continue",state='disabled',command=self.first)
        self.btn.place(x=225,y=220)

    def check(self):
        if self.btn['state'] == 'disabled':
            self.btn['state'] = 'normal'
        else:
            self.btn['state'] = 'disabled'

    def first(self):
        for k,v in self.children.copy().items():
            if v != self.lab :
                v.destroy()

        self.lab['text'] = "Where do you want to install Fractalus?"
        self.ent = Entry(self, width=50)
        self.dir = StringVar(self, os.getcwd())
        c = ttk.Combobox(self, state='readonly', textvariable=self.dir, width=50)
        c.place(x=5, y=25)
        c.bind("<Button-1>", self.change)

        self.btn = Button(self, text="Continue", command=self.next)
        self.btn.place(x=220, y=100)
        self.update()

    def next(self):
        if not os.path.isdir(self.dir.get()) :
            messagebox.showwarning("Warning","Directory does not exist")
            return

        for k,v in self.children.copy().items():
            if k =='!label':
                v['text']="Installing ..."
            else:
                v.destroy()

        self.pb = ttk.Progressbar(self,orient=HORIZONTAL,length=500,mode='determinate')
        self.pb.place(x=0, y=25)

        self.download()

    def download(self):
        self.update()

        n=100/(len(self.d["Heart_description"]['content'])+len(self.d["Wallpapers_description"]['content'])+sum(len(v) for v in self.d["Necessary Apps"].values())+2)
        self.pb['value'] = 0
        try:
            os.mkdir(self.dir.get()+"\\Fractalus")
            os.mkdir(self.dir.get()+"\\Fractalus\\H")
            os.mkdir(self.dir.get()+"\\Fractalus\\H\\Apps")
            os.mkdir(self.dir.get()+"\\Fractalus\\H\\Wallpapers")

            self.pb['value'] +=n
            self.update()

            rep =requests.get(self.base + "logo.ico").content
            with open(self.dir.get()+"\\Fractalus\\logo.ico","wb+") as f:
                f.write(rep)
            self.pb['value'] += n
            self.update()

            for th in self.d['Heart_description']['content']:
                rep =requests.get(self.base+self.d["Heart_description"]['location']+"/"+th).content
                with open(self.dir.get()+"\\Fractalus\\"+th,"wb+") as f:
                    f.write(rep)
                self.pb['value'] += n
                self.update()

            for th in self.d['Wallpapers_description']['content']:
                rep =requests.get(self.base+self.d["Wallpapers_description"]['location']+"/"+th).content
                with open(self.dir.get()+"\\Fractalus\\H\\Wallpapers\\"+th,"wb+") as f:
                    f.write(rep)
                self.pb['value'] += n
                self.update()

            for th in self.d['Necessary Apps']:
                os.mkdir(self.dir.get()+"\\Fractalus\\H\\Apps\\"+th)
                for elt in self.d['Necessary Apps'][th]:
                    rep = requests.get(self.base+th+"/"+elt).content
                    with open(self.dir.get()+"\\Fractalus\\H\\Apps\\"+th+"\\"+elt,"wb+") as f:
                        f.write(rep)
                    self.pb['value'] += n
                    self.update()

            self.finish()
        except Exception as err:
            messagebox.showerror("Error while downloading","Process failed due to the following error : "+str(err))
            self.first()

    def finish(self):
        self.pb.destroy()
        self.lab['text']="Instalation has finished without troubles !"
        self.intvar = IntVar(self)
        self.intvar.set(0)
        if os.path.exists(r"C:\Windows\System32\cmd.exe"):
            Label(self,text='Do you want to create a shortcut on your desktop for Fractalus ?').place(x=5,y=15)
            Radiobutton(self,text="Yes",variable=self.intvar,value=1).place(x=5, y=35)
            Radiobutton(self, text="No", variable=self.intvar, value=0).place(x=5, y=60)
        else :
            Label(self,text="Click Finish to close").place(x=5,y=15)

        self.btn = Button(self,text="Finish",command=self.close)
        self.btn.place(x=229,y=100)

    def close(self):
        if self.intvar.get()==1:
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortcut(desktop+"\\Fractalus.lnk")
            shortcut.TargetPath =r"C:\Windows\System32\cmd.exe"
            shortcut.Arguments='/c cd %s & python %s'%(self.dir.get()+"\\Fractalus",self.dir.get()+"\\Fractalus\\launcher.py")
            shortcut.WorkingDirectory = ''
            shortcut.IconLocation = self.dir.get()+"\\Fractalus\\logo.ico"
            shortcut.save()

        messagebox.showinfo("Summary","Fractalus has been installed correctly !\n You can launch it using the file : %s"%(self.dir.get()+"\\Fractalus\\launcher.py"))
        self.destroy()

    def change(self,*evt):
        r = askdirectory(initialdir=self.ent.get())
        if os.path.exists(r):self.dir.set(r)

if __name__ == '__main__':
    app=App()
    app.mainloop()