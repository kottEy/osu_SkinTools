import os
import sys
import sqlite3
import tkinter as tk
import os


class Osu():
    def __init__(self) -> None:
        pass

    def get_osudir(self):

        dbname = 'osu_dir.db'

        conn = sqlite3.connect(dbname)

        cur = conn.cursor()
        #osu.exeの位置が登録されているか確認
        cur.execute("SELECT path FROM client")

        for r in cur:
            file_path = r[0]
        try:
            file_path
        except:
            file_path = Osu.file_read(self)
            if file_path != None:
                if "osu!/osu!.exe" in file_path:
                        pass
                else:
                    sys.exit()
            else:
                sys.exit()
            cur.execute("INSERT INTO client VALUES (?)", (file_path, ))
            conn.commit()

        return file_path
    

    def file_read(self):
        # ファイル選択ダイアログを表示
        current_dir = os.path.abspath(os.path.dirname(__file__))
        tk.messagebox.showinfo(title="Skin Tools", message="Please select osu!.exe")
        file_path = tk.filedialog.askopenfilename(filetypes=[("exeファイル","*.exe")],initialdir=current_dir)

        if len(file_path) != 0:
            return file_path
        else:
            # ファイル選択がキャンセルされた場合
            return None    