from __future__ import annotations

import installer

from tkinter import *
from tkinter.font import Font
from tkinter.ttk import Treeview
from win32api import GetSystemMetrics
from PIL import Image as PILImage, ImageTk
import time, random, sys, os
import tkinter.messagebox as messagebox
import connect,resize
from PersonalWidgets import PopingToplevel

#Applications
import H.Apps.Gestionnaire.gestion_tache as gestion_tache
import H.Apps.admintools.admintool as admintool
import H.Apps.BooleCalc.boolecalc as boolecalc
import H.Apps.Conversions.main as Conv
import H.Apps.desktools.tools as tools
import H.Apps.explorateur.exploreur as exploreur
import H.Apps.Space_Invaders.main as SpaceInvade
import H.Apps.Terminal._cmd_ as _cmd_
import H.Apps.word.main as word

def welcome_text():
    dic = {
        'Mon':'Lundi',
        'Tue':'Mardi',
        'Wed':'Mercredi',
        'Thu':'Jeudi',
        'Fri':'Vendredi',
        'Sat':'Samedi',
        'Sun':'Dimanche',

        'Jan':'janvier',
        'Feb':'février',
        'Mar':'mars',
        'Apr':'avril',
        'May':'mai',
        'Jun':'juin',
        'Jul':'juillet',
        'Aug':'âout',
        'Sep':'septembre',
        'Oct':'octobre',
        'Nov':'novembre',
        'Dec':'décembre'
    }

    today = time.asctime().split()
    sentence = "Bienvenue\n"+dic[today[0]]+' '+today[2]+' '+dic[today[1]]+' '+today[4]+'\n'+today[3]
    return sentence

class Session:
    def __init__(self,id):
        self.id=id
        self.last_dir = os.getcwd()+r'\H\Users\\'+id
        self.path = r'H\Users\\'+id
        self.pref=connect.get_preferances(self.id)[0]

class IMG:
    def __init__(self,file:str,can:Canvas) -> None:
        self.file=file
        self.canvas=can
        self.possible = {
            'icone':ImageTk.PhotoImage(resize.cached_resize(75,1,self.file)),
            'Vignette':ImageTk.PhotoImage(resize.cached_resize(20,1,self.file)),
            'list':ImageTk.PhotoImage(resize.cached_resize(15,1,self.file)),
            }
    
    def add(self,n:str,h:int|float):
        self.possible[n]=ImageTk.PhotoImage(resize.cached_resize(h,1,self.file))
    
    def __call__(self, w):
        return self.possible[w]
    
class Background:
    def __init__(self,canvas:Canvas,link):
        self.canvas=canvas
        resize.resize(GetSystemMetrics(0),0,link,link)
        self.link=link.split('\\')[-1]
        self.bg_image =  ImageTk.PhotoImage(PILImage.open(link))
        self.bg_display = self.canvas.create_image(self.bg_image.width()/2,GetSystemMetrics(1)/(2),image=self.bg_image,anchor="center")
    
    def change(self,link):
        resize.resize(GetSystemMetrics(0),0,link,link)
        #self.canvas.delete(self.bg_display)
        self.bg_image =  ImageTk.PhotoImage(PILImage.open(link))
        self.link=link.split('\\')[-1]
        self.canvas.itemconfigure(self.bg_display,image=self.bg_image,anchor="center")
        self.canvas.coords(self.bg_display,self.bg_image.width()/2,GetSystemMetrics(1)/(2))
    
    def height(self):
        return self.bg_image.height()

class App(Tk):
    def __init__(self):
        super().__init__()

        self.wm_attributes("-fullscreen",1)

        n =random.randint(12,22)
        self.eol=0
               
        self.CANVAS = Canvas(self, width=GetSystemMetrics(0),height=GetSystemMetrics(1),borderwidth=0,highlightthickness=0,bg='black')
        self.CANVAS.pack(expand=True,fill=BOTH)

        self.bg=Background(self.CANVAS,rf"H\Wallpapers\fond{n}.jpg")

        self.etat=''

        #icones
        self.ADMIN_PARA = IMG(r"H\Apps\admintools\admin_para2.jpg",self.CANVAS)#ImageTk.PhotoImage(PILImage.open(r"H\Apps\admintools\admin_para2.jpg"))
        self.TERMINAL = IMG(r"H\Apps\Terminal\Terminal.png",self.CANVAS)
        self.GESTIONNAIRE = IMG(r"H\Apps\Gestionnaire\gestionnaire_taches.jpg",self.CANVAS)
        self.BOOLECALC = IMG(r"H\Apps\BooleCalc\BooleCalculator.png",self.CANVAS)
        self.SI = IMG(r"H\Apps\Space_Invaders\icon_si.png",self.CANVAS)
        self.CONVERT =IMG(r"H\Apps\Conversions\icon_convert.png",self.CANVAS)
        self.EXPLORATEUR = IMG(r"H\Apps\explorateur\explorateur.png",self.CANVAS)
        self.LOVELACECODE = IMG(r"H\Apps\word\LovelaceCode.png",self.CANVAS)


        self.welcome_screen()

    def welcome_screen(self):
        self.etat='w'
        self.date = self.CANVAS.create_text(400,GetSystemMetrics(1)-200,text=welcome_text(), font=Font(family="Helvetica",weight='bold',size=42),fill='white')
        self.update_date()
        self.bind_all("<Key>",self.changes)
        self.bind_all("<Button>",self.changes)
    
    def changes(self,event):
        if self.etat=='w':
            self.login_screen()
    
    def end_button_action(self):
        try:
            self.chooser.poping()
        except:
            self.chooser = CloseChooser(self,self.end,self.userchange)

    def ask_destroy(self):
        if messagebox.askyesnocancel("Exit ?","Êtes vous sur de vouloir éteindre le programme ?") is True:
            self.eol=0
            for child in self.children.copy().values():
                if type(child)==admintool.AdminInterface:
                    try:child.f.end()#si une fenetre Formulaire est ouverte : l'arrêter.
                    except:pass
            self.destroy()
            self.eol=1
            sys.exit()

    def login_screen(self):
        self.etat='l'
        for i in range(500):
            self.CANVAS.move(self.date,0,-2)
            self.update()
            self.update_idletasks()
        self.CANVAS.delete(self.date)

        

        self.end_btn = Button(self,text="I/O", fg="black",bg='#c80000', activebackground="red", command=self.ask_destroy)
        if GetSystemMetrics(1)/2+self.bg.height()/2> GetSystemMetrics(1):
            self.end_btn.place(x=GetSystemMetrics(0)-25,y=GetSystemMetrics(1)-25)
        else:
            self.end_btn.place(x=GetSystemMetrics(0)-25,y=GetSystemMetrics(1)/2+self.bg.height()/2-25)

        self.frame = Frame(self,height=200,width=250, borderwidth= 5, relief=RIDGE,bg='white')
        self.frame.pack(pady=270)
        self.frame.pack_propagate(False)

        self.can=Canvas(self.frame, height=75,width=75,borderwidth=0,bg='white',highlightthickness=0)
        self.can.pack()

        self.img=ImageTk.PhotoImage(PILImage.open(r"H\Apps\desktools\buste_.gif"))
        self.can.create_image(0,0,image=self.img,anchor="nw")
        self.sousframe_nom=Frame(self.frame)
        self.sousframe_nom.pack()

        self.lab_nom =Label(self.sousframe_nom,text="Identifiant :",bg='white')
        self.lab_nom.pack(side=LEFT)
        self.entry_nom = Entry(self.sousframe_nom,relief=SOLID)
        self.entry_nom.pack(side=RIGHT)
        self.entry_nom.focus()
        

        self.sousframe_password = Frame(self.frame)
        self.sousframe_password.pack()

        self.lab_pass = Label(self.sousframe_password,text="Mot de passe :",bg='white')
        self.lab_pass.pack(side=LEFT)
        self.entry_pass = Entry(self.sousframe_password, show='•',relief=SOLID)
        self.entry_pass.pack(side=RIGHT)
        self.entry_pass.bind('<Return>',self.connexion)

        self.entry_nom.bind('<Return>',lambda arg:self.entry_pass.focus())

        self.btn = Button(self.frame,text="⟹", relief=GROOVE, bg='#004080', fg='white', font=Font(self,family="Helvetica",weight='bold'), activebackground='#0055aa', activeforeground="white", command=self.connexion)
        self.btn.pack(side=RIGHT, padx=10)

        self.canvas_frame = self.CANVAS.create_window(GetSystemMetrics(0)//2,GetSystemMetrics(1)//2,window=self.frame)
    
    def run(self):
        while not self.eol:
            self.update()
            try:
                self.ges.update()
            except TclError as err:
                break
            except AttributeError as err:
                pass

    def update_date(self):
        if self.etat == 'w':
            self.CANVAS.itemconfig(self.date,text=welcome_text())
            self.after(10**3,self.update_date)
    
    def connexion(self,*arg):
        if connect.connect(self.entry_nom.get(),self.entry_pass.get()):
            self.session = Session(self.entry_nom.get())
            self.princ_screen()
        else:
            messagebox.showerror("Oups...","Le mot de passe ou l'identifiant est incorrect...",parent=self)
    
    def princ_screen(self):
        user =self.entry_nom.get()
        self.CANVAS.delete(self.canvas_frame)
        word.initialize(self.session)

        self.bg.change(r"H\Wallpapers\\"+self.session.pref[1])
        self.end_btn['command']=self.end_button_action

        self.frame.destroy()
        ask = [
            lambda files,master:exploreur.openfile(master,files,self.session.path),
            lambda files,master:exploreur.savefile(master,files,self.session.path),
        ]

        self.ges=gestion_tache.GestionApps(self)
        self.ges.add("Terminal",lambda master:_cmd_.CMD(master,self.session.path,self.session.path),self.TERMINAL)
        self.ges.add("Boole Calculator",lambda master:boolecalc.Calculator(master),self.BOOLECALC)
        self.ges.add("Space Invaders",lambda master:SpaceInvade.Jeu(master),self.SI)
        self.ges.add("Explorateur",lambda master: exploreur.Explorateur(master,self.session.last_dir,self.session.last_dir,{os.getcwd()+'\\':""},self.ges.open_file),self.EXPLORATEUR)
        self.ges.add("Lovelace Code",lambda master,link='': word.App(master,link,ask),self.LOVELACECODE)
        self.ges.add("Convertisseur",lambda master: Conv.run(master),self.CONVERT)
        
        self.ges.add_hide("Horloge",lambda master:tools.Clock(master))
        self.ges.add_hide("Batterie",lambda master:tools.Battery(master))
        self.ges.add_hide("Opener",lambda master:exploreur.BackgroundsOpener(master,self.bg))

        self.ges.add_infos("Lovelace Code",word.FILES[0][1])
        self.ges.start()

        self.b=ImageTk.PhotoImage(PILImage.open(r"H\Apps\desktools\bat.png"))
        self.h = ImageTk.PhotoImage(PILImage.open(r"H\Apps\desktools\horloge.png"))
        self.k = ImageTk.PhotoImage(PILImage.open(r"H\Apps\desktools\koch.png"))
        self.b_displayed=self.CANVAS.create_image(GetSystemMetrics(0)-35,GetSystemMetrics(1)-22.5,image=self.b,anchor='nw',tag='b')
        self.h_displayed=self.CANVAS.create_image(GetSystemMetrics(0)-75,GetSystemMetrics(1)-22.5,image=self.h,anchor='nw',tag='h')
        self.k_displayed=self.CANVAS.create_image(35,GetSystemMetrics(1)-22.5,image=self.k,anchor='nw',tag='k')


        if user=='admin':
            self.ges.add("Paramètres Administrateur",lambda master:admintool.AdminInterface(master),self.ADMIN_PARA)

        self.CANVAS.tag_bind("b",'<Button-1>',lambda *args:self.ges.open('Batterie'))
        self.CANVAS.tag_bind("h",'<Button-1>',lambda *args:self.ges.open('Horloge'))
        self.CANVAS.tag_bind("k",'<Button-1>',lambda evt:self.ges.show(self))
        self.CANVAS.bind("<Button-3>",lambda *evt:self.ges.open("Opener"))
        self.ges.draw()
        if GetSystemMetrics(1)/2+self.bg.height()/2>=GetSystemMetrics(1):
            self.end_btn.place_configure(x=0,y=GetSystemMetrics(1)-25)
        else:
            self.end_btn.place_configure(x=0,y=GetSystemMetrics(1)/2+self.bg.height()/2-25)
    
    def userchange(self,*args):
        connect.change_bg(self.session.id,self.bg.link)
        for couple in word.save_pref().items():
            connect.change_in_pref(self.session.id,couple[0],couple[1])
        n =random.randint(12,22)
        self.ges.end()
        self.end_btn.destroy()
        self.CANVAS.delete(self.b_displayed,self.k_displayed,self.h_displayed)
        del self.ges,self.b_displayed,self.k_displayed,self.h_displayed
        self.bg.change(rf"H\Wallpapers\fond{n}.jpg")
        self.welcome_screen()
    
    def end(self):
        connect.change_bg(self.session.id,self.bg.link)
        for couple in word.save_pref().items():
            connect.change_in_pref(self.session.id,couple[0],couple[1])
        self.destroy()

class CloseChooser(PopingToplevel):
    def __init__(self, master,com1,com2):
        super().__init__(master)
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW",self.destroy)
        self.transient(master)
        self.title("") 
        self.update_idletasks()
        self.overrideredirect(1)

        self.commands=[com1,com2]

        self.tree = Treeview(self,show='tree')
        self.tree.pack()

        self.power =ImageTk.PhotoImage(PILImage.open("H\Apps\desktools\power.png"))
        self.change=ImageTk.PhotoImage(PILImage.open("H\Apps\desktools\change.png"))
        self.tree.insert('',END,text="Eteindre",image=self.power)
        self.tree.insert('',END,text="Changer d'utilisateur",image=self.change)
        
        self.geometry("150x45+0+"+str(GetSystemMetrics(1)-70))

        self.bind("<Configure>",lambda *args:self.geometry("150x45+0+"+str(GetSystemMetrics(1)-70)))
        self.bind("<Leave>",lambda *args:self.destroy)
        self.tree.bind('<<TreeviewSelect>>',self.do)

    def do(self,event):
        proc = self.tree.item(self.tree.focus())['text']
        if proc=='Eteindre':
            self.commands[0]()
        else:
            self.commands[1]()
            self.destroy()
    
if __name__=='__main__':
    logiciel = App()
    logiciel.run()
    sys.exit()