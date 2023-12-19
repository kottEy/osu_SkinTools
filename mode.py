import os
import customtkinter


FONT_TYPE = 15
APPDIR = os.getcwd()


class ChangeModeFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fonts = (FONT_TYPE, 15)
        self.setup_form()

    
    def setup_form(self):
        # 行方向のマスのレイアウト設定
        self.grid_rowconfigure(0, weight=1)
        # 列方向のマスのレイアウト設定
        self.grid_columnconfigure(3, weight=1)

        self.button_mode1 = customtkinter.CTkButton(self, text="●", width=28, fg_color="#444", hover_color="#333", command=lambda : self.change_page(self.master.master.page_cursor))
        self.button_mode1.grid(row=0, column=0, pady=10)
        self.button_mode2 = customtkinter.CTkButton(self, text="♪", width=28, fg_color="#444", hover_color="#333", command=lambda : self.change_page(self.master.master.page_hitsounds))
        self.button_mode2.grid(row=1, column=0, pady=10)

    
    def change_page(self, page):
        #画面遷移
        page.tkraise()