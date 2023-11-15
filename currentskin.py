import customtkinter
from osu import Osu

FONT_TYPE = 15

class CurrentSkinFrame(customtkinter.CTkFrame):
    def __init__(self, *args, header_name="CurrentSkin", **kwargs):
        super().__init__(*args, **kwargs)

        self.fonts = (FONT_TYPE, 15)
        self.header_name = header_name

        # フォームのセットアップをする
        self.setup_form()


    def setup_form(self):
        # 行方向のマスのレイアウトを設定する。リサイズしたときに一緒に拡大したい行をweight 1に設定。
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウトを設定する
        self.grid_columnconfigure(0, weight=1)

        # ラベルを表示
        self.label = customtkinter.CTkLabel(self, text=self.header_name, font=(FONT_TYPE, 11))
        self.label.grid(row=0, column=0, padx=20, sticky="w")
        
        self.currentskin = Osu.get_currskin(self)
        self.label2 = customtkinter.CTkLabel(self, text=self.currentskin, font=(FONT_TYPE, 15))
        self.label2.grid(row=1, column=0, padx=20, sticky="w")

        self.button_update = customtkinter.CTkButton(self, text="⟳", width=50, command=self.update_curskin)
        self.button_update.grid(row=1, column=1, padx=20, pady=5, sticky="w")

    
    def update_curskin(self):
        self.currentskin = Osu.get_currskin(self)
        #self.label2 = customtkinter.CTkLabel(self, text=self.currentskin, font=self.fonts)
        self.label2.configure(text=self.currentskin)
        self.label2.grid(row=1, column=0, padx=20, sticky="w")