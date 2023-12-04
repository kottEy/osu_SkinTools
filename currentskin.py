import os
import re
import sys
import glob
import shutil
import customtkinter
import tkinter as tk
import sqlite3


dbname = 'osu_dir.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
FONT_TYPE = 15
APPDIR = os.getcwd()


class CurrentSkinFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="CurrentSkin", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name
        cur.execute('SELECT path FROM client')
        for r in cur:
            self.osu_dir = r[0]
        self.setup_form()


    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(0, weight=1)

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")
        self.currentskin = self.get_currskin()
        self.save_skincursor()
        if len(self.currentskin) >= 10:
            self.currentskin = self.currentskin[:10]
            self.currentskin += ' ...'

        self.label2 = customtkinter.CTkLabel(self, text=self.currentskin, font=(FONT_TYPE, 15))
        self.label2.grid(row=1, column=0, padx=20, sticky="w")

        self.button_select = customtkinter.CTkButton(self, text="Select from Explorer", fg_color="#444", hover_color="#333", command=self.btn_select_callback)
        self.button_select.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.button_update = customtkinter.CTkButton(self, text="⟳", width=50, command=self.update_currskin)
        self.button_update.grid(row=1, column=1, padx=20, pady=5, sticky="e")


    def get_currskin(self):
        dbname = 'osu_dir.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        # osuフォルダのディレクトリを取得
        try:
            cur.execute("SELECT path FROM client")
            for r in cur:
                file_path = r[0]
                file_path = str(file_path).replace('osu!.exe', '')
            dir = os.getcwd()
            # 現在のスキンを取得
            os.chdir(file_path)
            for file in glob.glob(f"{file_path}osu!.*.cfg"):
                cfg_file = file
            with open(cfg_file, encoding="utf-8") as f:
                for line in f:
                    if re.search(r'^Skin = *', line):
                        curr_skin = line.replace('Skin = ', '')
                        curr_skin = curr_skin.replace('\n', '')
                        break
            os.chdir(dir)
            cur.execute("INSERT INTO currskin VALUES(?)", (curr_skin, ))
            conn.commit()
            return curr_skin
        except:
            cur.execute("DELETE FROM client")
            conn.commit()
            tk.messagebox.showerror(title="Skin Tools", message="osu!.[user].cfgが見つかりませんでした。")
            sys.exit()

    
    def update_currskin(self):
        cur.execute("DELETE FROM currskin")
        conn.commit()
        self.currentskin = self.get_currskin()
        self.save_skincursor()
        if len(self.currentskin) >= 10:
            currentskin = self.currentskin[:10]
            currentskin += ' ...'
        self.label2.configure(text=currentskin)
        self.label2.grid(row=1, column=0, padx=20, sticky="w")


    def save_skincursor(self):
        try:
            os.makedirs(f"./images/{self.currentskin}")
        except:
            return
        osu_dir = str(self.osu_dir).replace('osu!.exe', '')
        file_name = {f'{osu_dir}Skins\\{self.currentskin}\\cursor.png',
                        f'{osu_dir}Skins\\{self.currentskin}\\cursor@2x.png',
                        f'{osu_dir}Skins\\{self.currentskin}\\cursortrail.png', 
                        f'{osu_dir}Skins\\{self.currentskin}\\cursortrail@2x.png'} 
        for f in file_name:
            try:
                shutil.copy(f, f'./images/{self.currentskin}/')
            except:
                pass


    def select_skin(self):
        skin_path = tk.filedialog.askdirectory(initialdir = self.osu_dir)
        if len(skin_path) != 0:
            return skin_path
        else:
            # ファイル選択がキャンセルされた場合
            return None


    def btn_select_callback(self):
            cur.execute("DELETE FROM currskin")
            conn.commit()
            skin_path = self.select_skin()
            if skin_path != None:
                os.chdir(skin_path)
                os.chdir('../../')
                files = os.listdir(str(os.getcwd()))
                flag = False
                for f in files:
                    if f == "osu!.exe":
                        flag = True
                os.chdir(APPDIR)
                if flag == True:
                    self.currentskin = os.path.basename(os.path.dirname(f"{skin_path}/skin.ini"))
                    self.save_skincursor()
                    if len(self.currentskin) >= 10:
                        currentskin = f'{self.currentskin[:10]}...'
                    else:
                        currentskin = self.currentskin
                    self.label2.configure(text=currentskin)
                    cur.execute("INSERT INTO currskin VALUES (?)", (self.currentskin, ))
                    conn.commit()
                else:
                    tk.messagebox.showerror(title="Skin Tools", message="Failed to get skin")