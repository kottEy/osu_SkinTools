import os
import sys
import re
import glob
import sqlite3
import tkinter as tk
import os


class Osu():
    def get_osudir(self):

        dbname = 'osu_dir.db'

        conn = sqlite3.connect(dbname)

        cur = conn.cursor()
        #osu.exeの位置が登録されているか確認
        cur.execute("SELECT path FROM client")

        for r in cur:
            pass
        try:
            file_path = r[0]

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
    

    def get_currskin(self):
        dbname = 'osu_dir.db'
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()
        # osuフォルダのディレクトリを取得する
        try:
            file_path = Osu.get_osudir(self)
            file_path = str(file_path).replace('osu!.exe', '')
            dir = os.getcwd()
            # 現在のスキンを取得する
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
            return curr_skin
        except:
            cur.execute("DELETE FROM client")
            conn.commit()
            tk.messagebox.showerror(title="Skin Tools", message="osu!.[user].cfgが見つかりませんでした。")
            sys.exit()

    

    def file_read(self):
        # ファイル選択ダイアログを表示する
        current_dir = os.path.abspath(os.path.dirname(__file__))
        tk.messagebox.showinfo(title="Skin Tools", message="Please select osu!.exe")
        file_path = tk.filedialog.askopenfilename(filetypes=[("exeファイル","*.exe")],initialdir=current_dir)

        if len(file_path) != 0:
            return file_path
        else:
            # ファイル選択がキャンセルされた場合
            return None    