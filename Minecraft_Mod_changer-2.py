import os,tkinter,json,sys,ctypes,subprocess,re,requests,threading

def Exit_and_Run_Minecraft():
    S.root.destroy()
    Devloper_mode=True
    if Devloper_mode ==False:
        if __name__ == "__main__":
            subprocess.call("C:\XboxGames\Minecraft Launcher\Content\Minecraft.exe")

def read(pathway):
    file=open(pathway,"r")
    information=file.read()
    return information
    
def write(Pathway,information):
    file=open(Pathway,"w",)
    file.write(information)
  
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

#x = requests.get("https://cdn.modrinth.com/data/AANobbMI/versions/rAfhHfow/sodium-fabric-mc1.19.2-0.4.4%2Bbuild.18.jar")
#file=open("C:/Users/alexf/AppData/Roaming/.minecraft/mods/test","wb",)
#file.write(x.content)

class System():
    def __init__(self):
        user32 = ctypes.windll.user32
        window_x_half=round(user32.GetSystemMetrics(0)/4)
        window_y_half=round(user32.GetSystemMetrics(1)/4)
        
        self.root = tkinter.Tk()
        self.root.title("Minecraft Mod Updater by Alex")
        
        self.root.geometry(str(window_x_half)+"x"+str(window_y_half))
        
        self.root.resizable(0,0)
        self.root.protocol("WM_DELETE_WINDOW",Exit_and_Run_Minecraft)
        
        self.current_modpack,self.Mod_Pathway,self.Minecraft_Pathway="Unknown","Unknown","Unknown"

        del sys.modules["ctypes"]
    def Change_current_mod(self):
        os.rename(self.Mod_Pathway,self.Minecraft_Pathway+self.current_modpack)
        new_choice = variable.get()
        os.rename(self.Minecraft_Pathway+new_choice,self.Mod_Pathway)
        write("Current_modpack.txt",new_choice)
        self.current_modpack=new_choice

        mylist.delete(0, "end")
        self.find_Minecraft_Mods()

    def find_Minecraft_Mod_Packs(self):
        Minecraft_Mod_Pack_List=[self.current_modpack]
        Minecraft_Mod_Pack_List_Unchekced=os.listdir(self.Minecraft_Pathway)

        for A in range(len(Minecraft_Mod_Pack_List_Unchekced)):
            unchecked=Minecraft_Mod_Pack_List_Unchekced[A].lower()
            isdir=os.path.isdir(self.Minecraft_Pathway+Minecraft_Mod_Pack_List_Unchekced[A])
            if unchecked.find("mod")!=-1 and unchecked!="mods" and isdir==True:
                Minecraft_Mod_Pack_List.append(Minecraft_Mod_Pack_List_Unchekced[A])
     
        return Minecraft_Mod_Pack_List
        
    def find_Minecraft_Mods(self):
        number_of_non_mods=0
        pathway=self.Mod_Pathway+"z-modpacktype.txt"
        
        try:
            current_pack=read(pathway)
            if current_pack=="":
                current_pack=None
                self.fabric,self.forge,self.quilt=0,0,0
        except FileNotFoundError:
            write(pathway,information="unknown")
            current_pack=None
            self.fabric,self.forge,self.quilt=0,0,0

        Current_mods=os.listdir(self.Mod_Pathway[:-1])
        for I in range(len(Current_mods)):
            if Current_mods[I][-4:]== ".jar" and os.path.isdir(self.Mod_Pathway+Current_mods[I])!=True:
                
                current_mod=Current_mods[I].lower()
                threading.Thread(target=update_mod, args=(current_mod,)).start()
                
                if current_pack==None:
                    current_pack=mod_type(current_mod)
                    mod_version(current_mod)

                   
                Letters=list(Current_mods[I][:-4])
                R,G,B=0,0,0
             
                numb=0
                for J in range(len(Letters)):
                    if numb==0:
                        R=R+ord(Letters[J])
                        numb=1
                        if R >=256:
                            R=R-256    
                    elif numb==1:
                        G=G+ord(Letters[J])
                        numb=2
                        if G >=256:
                            G=G-256
                    else:
                        B=B+ord(Letters[J])
                        numb=0
                        if B >=256:
                            B=B-256
                            
                
                mylist.insert("end",Current_mods[I][:-4])  
                mylist.itemconfig(I-number_of_non_mods, {'fg':rgb_hack((R,G,B)),'bg':'black'})
            else:
                number_of_non_mods=number_of_non_mods+1

        print(current_pack)  
        nub=I+1
        if current_pack==True:
            print("fabric")
        elif current_pack==False:
            print("quilt")
        elif self.fabric>self.forge and self.fabric>self.quilt:#fabric byists
            print("fabric")
        elif self.forge>self.fabric and self.fabric>self.quilt:
            print("forge")
        elif self.quilt>self.fabric and self.quilt>self.forge:
            print("quilt")
            
def mod_type(current_mod):
    Fabric_mod=current_mod.find("fabric")
    Forge_mod=current_mod.find("froge")
    Quilt_mod=current_mod.find("quilt")                        
    if current_mod.find("fabric-api")!=-1:
        return True #farbic
    elif current_mod.find("qfapi")!=-1: 
        return False #quilt
    else:
        if Fabric_mod!=-1:
            S.fabric+=+1
        if Forge_mod!=-1:
            S.forge+=+1
        if Quilt_mod!=-1:
            S.quilt+=1
    
def mod_version(current_mod):
    a=re.sub('\D', '',current_mod)
    #print(a)

def update_mod(Current_mod):
    s=Current_mod[:-4].replace("fabric","").replace("build","").replace("mc","").replace(".","").replace("+","").replace("-","").replace("v","").replace("forge","").replace("quilt","")
    test=re.sub(r'[0-9]+', '', s)

    link_pref="https://modrinth.com/mod/"+test
    if requests.get(link_pref).status_code==200:
         req=requests.get(link_pref+"/versions").content
         write("test",str(req))
    else:
         print(test+"\n")

    
def find_Minecaft_pathway():
    try:
        import getpass
        pathway="C:/Users/"+getpass.getuser()+"/AppData/Roaming/.minecraft/"
        del sys.modules["getpass"]
        return pathway
    except:
        print("your computer should not exist")


S=System()

try:
    S.Minecraft_Pathway=read("pathway.txt")  
except FileNotFoundError:
    S.Minecraft_Pathway=find_Minecaft_pathway()
    write("pathway.txt",information=S.Minecraft_Pathway)
    
S.Mod_Pathway=S.Minecraft_Pathway+"mods/"
if os.path.isdir(S.Minecraft_Pathway)==False:
    print(S.Mod_Pathway)
    os.makedirs(S.Mod_Pathway)

try:
    S.current_modpack=read("Current_modpack.txt")
except FileNotFoundError:
    S.current_modpack="orginal_mod"
    write("Current_modpack.txt",information="orginal_mod")

file=open(S.Minecraft_Pathway+"launcher_profiles.json")
Minecraft_profiles=json.load(file)
file.close()

#print(Minecraft_profiles)

Minecraft_Mod_Pack_List=S.find_Minecraft_Mod_Packs()

variable = tkinter.StringVar(S.root)
variable.set(Minecraft_Mod_Pack_List[0])

refresh = tkinter.Button(S.root, text="Refresh",command=S.find_Minecraft_Mod_Packs())
refresh.config(width=10, font=('Helvetica', 12))
refresh.pack(side="right",anchor="ne")

opt = tkinter.OptionMenu(S.root, variable, *Minecraft_Mod_Pack_List,command=lambda x:S.Change_current_mod())
opt.config(width=110, font=('Helvetica', 12),text=Minecraft_Mod_Pack_List)
opt.pack(side="top",anchor="nw")

scrollbar = tkinter.Scrollbar(S.root)
scrollbar.pack( side = "right",fill = "y",anchor="e")
mylist = tkinter.Listbox(S.root, yscrollcommand = scrollbar.set ,width=100)

S.find_Minecraft_Mods()
scrollbar.config( command = mylist.yview )
mylist.pack( side = "right", fill = "both",anchor="s" )

S.root.mainloop()
