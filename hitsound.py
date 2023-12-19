import os
import glob
import sqlite3
import shutil
import customtkinter


dbname = 'osu_dir.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
FONT_TYPE = 15
APPDIR = os.getcwd()


class HitSoundsFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Collection", osu_dir, **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name
        self.osu_dir = osu_dir
        self.setup_form()


    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(0, weight=1)

        # ラベルを表示
        self.tabview = customtkinter.CTkTabview(master=self, width=250, height=30)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="e")

        self.tabview.add("選択")
        self.tabview.add("追加")

        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        # Selectタブ
        self.get_hitsounds()

        self.combobox = customtkinter.CTkComboBox(self.tabview.tab("選択"), width=150, height=28, values=self.hitsounds_array, state='readonly', command=self.combobox_callback)
        self.combobox.set("Select hitsounds")
        self.combobox.grid(row=1, column=0, padx=20, sticky="ew")

        self.button_apply = customtkinter.CTkButton(self.tabview.tab("選択"), text="Apply", fg_color="#444", width=50, state='readonly', command=self.apply_hitsounds)
        self.button_apply.grid(row=1, column=1, padx=(20, 10), pady=5, sticky="w")

        # Add
        self.button_add = customtkinter.CTkButton(self.tabview.tab("追加"), width=231, text="Add hitsounds from current skin", command=self.add_hitsounds)
        self.button_add.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")


    def combobox_callback(self, choice):
        self.button_apply.configure(state='normal', fg_color='#1f6AA5')
        self.choice = choice


    def add_hitsounds(self):
        cur.execute('SELECT name FROM currskin')
        for r in cur:
            curr_skin = r[0]
        try:
            os.makedirs(f"./hitsounds/{curr_skin}")
        except:
            pass
        osu_dir = str(self.osu_dir).replace('osu!.exe', '')
        types = ('mp3', 'wav', 'ogg')
        files = []
        for t in types:
            files +=  glob.glob(fr"{osu_dir}Skins/{curr_skin}/*-hit*.*" + t)
            files +=  glob.glob(fr"{osu_dir}Skins/{curr_skin}/*-slider*.*" + t)
        for f in files:
            try:
                shutil.copy(f'{osu_dir}Skins\\{curr_skin}\\{os.path.split(f)[1]}', f'./hitsounds/{curr_skin}/{os.path.split(f)[1]}')
            except:
                pass
        self.get_hitsounds()
        self.combobox.configure(values=self.hitsounds_array)
                    

    def apply_hitsounds(self):
        cur.execute('SELECT name FROM currskin')
        for r in cur:
            curr_skin = r[0]
        try:
            self.choice
        except:
            return
        osu_dir = str(self.osu_dir).replace('osu!.exe', '')
        types = ('mp3', 'wav', 'ogg')
        files = []
        delfiles = []
        for t in types:
            files +=  glob.glob(fr"./hitsounds/{self.choice}/*-hit*.*" + t)
            files +=  glob.glob(fr"./hitsounds/{self.choice}/*-slider*.*" + t)
            delfiles +=  glob.glob(fr"{osu_dir}Skins/{curr_skin}/*-hit*.*" + t)
            delfiles +=  glob.glob(fr"{osu_dir}Skins/{curr_skin}/*-slider*.*" + t)
        for df in delfiles:
            try:
                os.remove(df)
            except:
                pass
        for f in files:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{os.path.split(f)[1]}')
            except:
                pass
            try:
                shutil.copy(f'./hitsounds/{self.choice}/{os.path.split(f)[1]}', f'{osu_dir}Skins\\{curr_skin}\\{os.path.split(f)[1]}')
            except:
                pass


    def get_hitsounds(self):
        self.hitsounds_array = []
        dir = "./hitsounds/"
        for d in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, d)):
                self.hitsounds_array.append(d)