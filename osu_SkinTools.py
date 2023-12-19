import os
import sqlite3
import subprocess
import sys
import tkinter.messagebox
import customtkinter
from osu import Osu
from cursor import CursorFrame
from collection import CollectionFrame
from currentskin import CurrentSkinFrame
from addcursor import AddCursorFrame
from mode import ChangeModeFrame
from hitsound import HitSoundsFrame
from updater import Updater


FONT_TYPE = "meiryo"
APPDIR = os.getcwd()

dbname = 'osu_dir.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS client (path varchar NOT NULL)")
cur.execute("CREATE TABLE IF NOT EXISTS currskin (name varchar)")
cur.execute("DELETE FROM currskin")
conn.commit()

mkdir = {"./images/cursor",
         "./images/cursortrail",
         "./images/collections",
         "./hitsounds"
         }
for d in mkdir:
    try:
        os.makedirs(d)
    except:
        pass


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        customtkinter.CTk.__init__(self, *args, **kwargs)
        self.fonts = (FONT_TYPE, 15)
        self.setup_form()

    
    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # フォームサイズ設定
        self.geometry("770x600")
        self.maxsize(770, 600)
        self.minsize(770, 600)
        self.title("osu! Skin Tools")
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(0, weight=1)

        osu_dir = Osu.get_osudir(self)


        # Cursor Tool
        self.page_cursor = customtkinter.CTkFrame(self, fg_color="#242424")
        self.page_cursor.grid(row=0, column=0, sticky="nsew")

        self.read_current_skin_frame = CurrentSkinFrame(master=self.page_cursor, header_name="Current skin", osu_dir=osu_dir)
        self.read_current_skin_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.read_collection = CollectionFrame(master=self.page_cursor, header_name="Collection", osu_dir=osu_dir)
        self.read_collection.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.read_cursor_frame = CursorFrame(master=self.page_cursor, header_name="Cursor", type="cursor", osu_dir=osu_dir)
        self.read_cursor_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.read_cursortrail_frame = CursorFrame(master=self.page_cursor, header_name="Cursortrail", type="cursortrail", osu_dir=osu_dir)
        self.read_cursortrail_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.read_addcursor_frame = AddCursorFrame(master=self.page_cursor, header_name="Add cursor", type="cursor")
        self.read_addcursor_frame.grid(row=2, column=0, padx=20, pady=20, sticky="sew")

        self.read_addcursortrail_frame = AddCursorFrame(master=self.page_cursor, header_name="Add cursortrail", type="cursortrail")
        self.read_addcursortrail_frame.grid(row=2, column=1, padx=20, pady=20, sticky="sew")

        self.read_mode_frame = ChangeModeFrame(master=self.page_cursor)
        self.read_mode_frame.grid(row=1, column=2, padx=(0, 20))
        
        
        # HitSound Tool
        self.page_hitsounds = customtkinter.CTkFrame(self, fg_color="#242424")
        self.page_hitsounds.grid(row=0, column=0, sticky="nsew")

        self.read_current_skin_frame = CurrentSkinFrame(master=self.page_hitsounds, header_name="Current skin", osu_dir=osu_dir)
        self.read_current_skin_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.read_addhitsound_frame = HitSoundsFrame(master=self.page_hitsounds, header_name="Hitsounds", osu_dir=osu_dir)
        self.read_addhitsound_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.read_mode_frame2 = ChangeModeFrame(master=self.page_hitsounds)
        self.read_mode_frame2.grid(row=1, column=2, padx=(0, 20), pady=(109, 0))

        self.page_cursor.tkraise()


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
