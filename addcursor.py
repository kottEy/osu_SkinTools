import os
import shutil
import customtkinter
from tkinterdnd2 import TkinterDnD, DND_ALL
from PIL import Image
from cursor import CursorFrame


FONT_TYPE = 15
APPDIR = os.getcwd()


class AddCursorFrame(customtkinter.CTkFrame, TkinterDnD.DnDWrapper):
    def __init__(self, *args, header_name="Add cursor", type="cursor", **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name
        self.type = type
        self.setup_form()

    
    def get_path(self, event):
        self.file = str(event.data).replace('{', '')
        self.file = str(self.file).replace('}', '')
        image = customtkinter.CTkImage(light_image=Image.open(fp=self.file), size=[25, 25])
        
        self.label2.grid(row=1, column=1, padx=(55, 0))
        self.label2.configure(text="", image=image)

        self.button_apply = customtkinter.CTkButton(self, text="Add", command=self.add_cursor, width=50, height=20)
        self.button_apply.grid(row=1, column=3, padx=(0, 16), pady=(5, 2))
        self.button_cancel = customtkinter.CTkButton(self, text="Cancel", command=self.cancel_cursor, width=50, height=20)
        self.button_cancel.grid(row=2, column=3, padx=(0, 16), pady=(0, 5))


    def add_cursor(self):
        new_file = self.duplicate_rename(f"{APPDIR}/images/{self.type}/{self.type}.png")
        shutil.copy(self.file, new_file)
        self.change_label()
        self.button_apply.destroy()
        self.button_cancel.destroy()
        CursorFrame.update_file_list(self, f"{APPDIR}\\images\\{self.type}\\")


    def cancel_cursor(self):
        self.change_label()
        self.button_apply.destroy()
        self.button_cancel.destroy()

    
    def change_label(self):
        self.label2.destroy()
        self.label2 = customtkinter.CTkLabel(self, text="Drop files here.", font=self.fonts)
        if self.type == "cursor":
            self.label2.grid(row=1, column=1, padx=20, sticky="ew")
        else:
            self.label2.grid(row=1, column=1, padx=(5, 20), sticky="ew")
        


    def duplicate_rename(self, file_path):
        if os.path.exists(file_path):
            name, ext = os.path.splitext(file_path)
            i = 1
            while True:
                new_name = "{} ({}){}".format(name, i, ext)
                if not os.path.exists(new_name):
                    return new_name
                i += 1
        else:
            return file_path
        

    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(2, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(2, weight=1)

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")

        self.label2 = customtkinter.CTkLabel(self, text="Drop files here.", font=self.fonts)
        if self.type == "cursor":
            self.label2.grid(row=1, column=1, padx=20, sticky="ew")
        else:
            self.label2.grid(row=1, column=1, padx=(5, 20), sticky="ew")
        self.entryWidget = customtkinter.CTkLabel(self, text="")
        self.entryWidget.grid(row=2, column=1, padx=20, sticky="ew")
        self.entryWidget.drop_target_register(DND_ALL)
        self.entryWidget.dnd_bind("<<Drop>>", self.get_path)

