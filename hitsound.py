import os
import glob
import sqlite3
import shutil
import tkinter as tk
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

        # Addタブ
        self.entry = customtkinter.CTkEntry(self.tabview.tab("追加"), placeholder_text="", state="readonly",width=126)
        self.entry.grid(row=1, column=0, padx=(20, 0), sticky="ew")

        self.button_select = customtkinter.CTkButton(self.tabview.tab("追加"), width=40, text="Open", fg_color="#444", hover_color="#333", command=self.btn_select_callback)
        self.button_select.grid(row=1, column=1, padx=(0, 20), sticky="w")

        self.button_add = customtkinter.CTkButton(self.tabview.tab("追加"), text="Add", fg_color="#444", width=50, state="readonly", command=self.add_hitsounds)
        self.button_add.grid(row=1, column=2, padx=(0, 10), pady=5, sticky="w")


    def combobox_callback(self, choice):
        self.button_apply.configure(state='normal', fg_color='#1f6AA5')
        self.choice = choice


    def select_hitsounds(self):
        hitsounds_path = tk.filedialog.askdirectory(initialdir = self.osu_dir)
        if len(hitsounds_path) != 0:
            return hitsounds_path
        else:
            # ファイル選択がキャンセルされた場合
            return None
        
    
    def btn_select_callback(self):
            self.hs_path = self.select_hitsounds()
            if self.hs_path != None:
                text = str(os.path.split(self.hs_path)[1])
                self.entry.configure(state="normal", placeholder_text=text)
                self.entry.configure(state="readonly")
                self.button_add.configure(state="normal", fg_color='#1f6AA5')
    

    def add_hitsounds(self):
        try:
            self.hs_path
        except:
            return
        
        if self.hs_path != None:
            try:
                os.makedirs(f"./hitsounds/{os.path.split(self.hs_path)[1]}")
            except:
                pass
            types = ('mp3', 'wav', 'ogg')
            files = []
            for t in types:
                files +=  glob.glob(fr"{self.hs_path}/*-hit*.*" + t)
                files +=  glob.glob(fr"{self.hs_path}/*-slider*.*" + t)
            for f in files:
                try:
                    shutil.copy(f, f'./hitsounds/{os.path.split(self.hs_path)[1]}/{os.path.split(f)[1]}')
                except:
                    pass
            self.get_hitsounds()
            self.combobox.configure(values=self.hitsounds_array)
            self.entry.configure(state="normal", placeholder_text="")
            self.entry.configure(state="readonly")
            self.button_add.configure(state="readonly", fg_color='#444')
                    

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
                shutil.copy(f'./hitsounds/{self.choice}/{os.path.split(f)[1]}', f'{osu_dir}Skins\\{curr_skin}\\{os.path.split(f)[1]}')
            except:
                pass


    def get_hitsounds(self):
        self.hitsounds_array = []
        dir = "./hitsounds/"
        for d in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, d)):
                self.hitsounds_array.append(d)