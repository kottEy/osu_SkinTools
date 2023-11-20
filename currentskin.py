import os
import customtkinter
import tkinter as tk
import sqlite3
from osu import Osu
from cursor import CursorFrame


FONT_TYPE = 15
APPDIR = os.getcwd()
dbname = 'osu_dir.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()


class CurrentSkinFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="CurrentSkin", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        self.setup_form()


    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(0, weight=1)

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")
        self.currentskin = Osu.get_currskin(self)
        CursorFrame.save_skincursor(self)
        if len(self.currentskin) >= 10:
            self.currentskin = self.currentskin[:10]
            self.currentskin += ' ...'

        self.label2 = customtkinter.CTkLabel(self, text=self.currentskin, font=(FONT_TYPE, 15))
        self.label2.grid(row=1, column=0, padx=20, sticky="w")

        self.button_select = customtkinter.CTkButton(self, text="Select from Explorer", fg_color="#444", hover_color="#333", command=self.btn_select_callback)
        self.button_select.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.button_update = customtkinter.CTkButton(self, text="⟳", width=50, command=self.update_currskin)
        self.button_update.grid(row=1, column=1, padx=20, pady=5, sticky="e")

    
    def update_currskin(self):
        cur.execute("DELETE FROM osu_currskin")
        conn.commit()
        self.currentskin = Osu.get_currskin(self)
        CursorFrame.save_skincursor(self)
        if len(self.currentskin) >= 10:
            self.currentskin = self.currentskin[:10]
            self.currentskin += ' ...'
        self.label2.configure(text=self.currentskin)
        self.label2.grid(row=1, column=0, padx=20, sticky="w")


    def btn_select_callback(self):
        cur.execute("DELETE FROM osu_currskin")
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
                cur.execute("INSERT INTO osu_currskin VALUES (?)", (skin_path, ))
                conn.commit()
                CursorFrame.save_skincursor(self)
                if len(self.currentskin) >= 10:
                    self.currentskin = os.path.basename(os.path.dirname(f"{skin_path}/skin.ini"))[:10]
                    self.currentskin += ' ...'
                self.label2.configure(text=self.currentskin)
            else:
                tk.messagebox.showerror(title="Skin Tools", message="Failed to get skin")


    def select_skin(self):
        osu_dir = Osu.get_osudir(self)
        skin_path = tk.filedialog.askdirectory(initialdir = osu_dir)
        if len(skin_path) != 0:
            return skin_path
        else:
            # ファイル選択がキャンセルされた場合
            return None

