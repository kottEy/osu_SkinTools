import os
import sqlite3
import customtkinter
from cursor import CursorFrame, CursorTrailFrame
from currentskin import CurrentSkinFrame
from addcursor import AddCursorFrame, AddCursorTrailFrame

FONT_TYPE = "meiryo"

APPDIR = os.getcwd()

dbname = 'osu_dir.db'

conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS client (path varchar NOT NULL)")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        # メンバー変数の設定
        self.fonts = (FONT_TYPE, 15)

        # フォームのセットアップをする
        self.setup_form()

    
    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # フォームサイズ設定
        self.geometry("727x550")
        self.maxsize(727, 550)
        self.minsize(727, 550)
        self.title("osu! Skin Tool")
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(1, weight=1)

        self.read_current_skin_frame = CurrentSkinFrame(master=self, header_name="Current Skin")
        self.read_current_skin_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        self.read_cursor_frame = CursorFrame(master=self, header_name="Cursor")
        self.read_cursor_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        self.read_cursortrail_frame = CursorTrailFrame(master=self, header_name="Cursor Trail")
        self.read_cursortrail_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.read_addcursor_frame = AddCursorFrame(master=self, header_name="Add Cursor")
        self.read_addcursor_frame.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

        self.read_addcursortrail_frame = AddCursorTrailFrame(master=self, header_name="Add Cursor Trail")
        self.read_addcursortrail_frame.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

if __name__ == "__main__":
    # アプリケーション実行
    app = App()
    app.mainloop()
