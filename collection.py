import os
import sqlite3
import shutil
import customtkinter
import tkinter as tk


dbname = 'osu_dir.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
FONT_TYPE = 15
APPDIR = os.getcwd()


class CollectionFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="Collection", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name
        cur.execute('SELECT path FROM client')
        for r in cur:
            self.osu_dir = r[0]
        self.setup_form()
    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(1, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(0, weight=1)

        self.tabview = customtkinter.CTkTabview(master=self, height=30)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 10))

        self.tabview.add("選択")
        self.tabview.add("追加")

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        # Selectタブ
        self.get_collections()
        self.combobox = customtkinter.CTkComboBox(self.tabview.tab("選択"), width=150, height=28, values=self.collection_array, state='readonly', command=self.combobox_callback)
        self.combobox.set("Select collection")
        self.combobox.grid(row=1, column=0, padx=20, sticky="ew")

        self.button_apply = customtkinter.CTkButton(self.tabview.tab("選択"), text="Apply", fg_color="#444", width=50, state='readonly', command=self.apply_collection)
        self.button_apply.grid(row=1, column=1, padx=20, pady=5, sticky="w")

        # Addタブ
        self.entry_add = customtkinter.CTkEntry(self.tabview.tab("追加"), width=150, height=28)
        self.entry_add.grid(row=1, column=0, padx=20, sticky="ew")

        self.button_add = customtkinter.CTkButton(self.tabview.tab("追加"), text="Add", width=50, command=self.add_collection)
        self.button_add.grid(row=1, column=1, padx=20, pady=5, sticky="w")


    def combobox_callback(self, choice):
        self.button_apply.configure(state='normal', fg_color='#1f6AA5')
        self.choice = choice


    def add_collection(self):
        cur.execute('SELECT name FROM currskin')
        for r in cur:
            curr_skin = r[0]
        name = self.entry_add.get()
        try:
            os.makedirs(f"./images/collections/{name}")
        except:
            tk.messagebox.showerror(title="Skin Tools", message="Failed to create folder.")
        osu_dir = str(self.osu_dir).replace('osu!.exe', '')
        os.chdir(osu_dir)
        os.chdir(APPDIR)
        file_name = {'cursor.png',
                     'cursor@2x.png',
                     'cursortrail.png',
                     'cursortrail@2x.png',
                     'cursormiddle.png',
                     'cursormiddle@2x.png'
                    }
        for f in file_name:
            try:
                shutil.copy(f'{osu_dir}Skins\\{curr_skin}\\{f}', f'./images/collections/{name}/{f}')
            except:
                pass
        self.get_collections()
        self.combobox.configure(values=self.collection_array)
        

    def apply_collection(self):
        cur.execute('SELECT name FROM currskin')
        for r in cur:
            curr_skin = r[0]
        try:
            self.choice
        except:
            return
        osu_dir = str(self.osu_dir).replace('osu!.exe', '')
        file_name = {'cursor.png',
                     'cursor@2x.png',
                     'cursortrail.png',
                     'cursortrail@2x.png',
                     'cursormiddle.png',
                     'cursormiddle@2x.png'
                    }
        for f in file_name:
            try:
                os.remove(f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass
            try:
                shutil.copy(f'./images/collections/{self.choice}/{f}', f'{osu_dir}Skins\\{curr_skin}\\{f}')
            except:
                pass


    def get_collections(self):
        self.collection_array = []
        dir = "./images/collections/"
        for d in os.listdir(dir):
            if os.path.isdir(os.path.join(dir, d)):
                self.collection_array.append(d)