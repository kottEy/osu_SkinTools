import os
import sqlite3
import subprocess
import sys
import tkinter.messagebox
import customtkinter
from cursor import CursorFrame, CursorTrailFrame
from collection import CollectionFrame
from currentskin import CurrentSkinFrame
from addcursor import AddCursorFrame, AddCursorTrailFrame
from updater import Updater


FONT_TYPE = "meiryo"
APPDIR = os.getcwd()

dbname = 'osu_dir.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS client (path varchar NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS osu_currskin (path varchar)")
cur.execute("DELETE FROM osu_currskin")
conn.commit()

mkdir = {"./images/cursor",
         "./images/cursortrail",
         "./images/collections"}
for d in mkdir:
    try:
        os.makedirs(d)
    except:
        pass


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.fonts = (FONT_TYPE, 15)

        self.setup_form()

    
    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # フォームサイズ設定
        self.geometry("727x600")
        self.maxsize(727, 600)
        self.minsize(727, 600)
        self.title("osu! Skin Tools")
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(1, weight=1)

        self.read_current_skin_frame = CurrentSkinFrame(master=self, header_name="Current Skin")
        self.read_current_skin_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.read_collection = CollectionFrame(master=self, header_name="Collection")
        self.read_collection.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.read_cursor_frame = CursorFrame(master=self, header_name="Cursor")
        self.read_cursor_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.read_cursortrail_frame = CursorTrailFrame(master=self, header_name="Cursor Trail")
        self.read_cursortrail_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.read_addcursor_frame = AddCursorFrame(master=self, header_name="Add Cursor")
        self.read_addcursor_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.read_addcursortrail_frame = AddCursorTrailFrame(master=self, header_name="Add Cursor Trail")
        self.read_addcursortrail_frame.grid(row=2, column=1, padx=20, pady=20, sticky="ew")


if __name__ == "__main__":
    # アプリの更新検知
    ud = Updater()
    if ud.check_update():
        is_update = tkinter.messagebox.askquestion("更新しますか?", f"{ud.latest_version}の更新プログラムが見つかりました。\nアップデートしますか?")
        if is_update == "yes":
            subprocess.Popen("updater.exe", close_fds=True)
            sys.exit()
    # アプリケーション実行
    app = App()
    try:
        app.iconbitmap('./osu_SkinTools_logo.ico')
    except:
        pass
    app.mainloop()
