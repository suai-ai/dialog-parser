import tkinter
import customtkinter
from tkinter import filedialog as fd
from functools import partial
from new_message_mod import TelegramFile
from math import ceil
import json
from tqdm import tqdm

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
# Themes: "blue" (standard), "green", "dark-blue"


def get_page(page, page_size, lst):
    return lst[page * page_size: page * page_size + page_size]


class ListItem(customtkinter.CTkFrame):
    def __init__(self, master, chat, info):
        self.chat = chat
        super().__init__(master)
        if self.chat.type_ == "saved_messages":
            self.chat.name = "Сохраненные сообщения"
        elif not self.chat.name:
            self.chat.name = f"bot_{self.chat.id_}"
        self.need_export = tkinter.BooleanVar(value=True)

        self.grid_columnconfigure(0, weight=1)

        self.checkbox = customtkinter.CTkCheckBox(
            self, text=self.chat.name, variable=self.need_export, onvalue=True, offvalue=False)
        self.checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.checkbox.select()

        self.button = customtkinter.CTkButton(
            self, text="?", width=30, command=info, font=("Arial", 16))

        # RADIO BUTTON
        self.gender = tkinter.IntVar(value=0)
        radio_button_u = customtkinter.CTkRadioButton(
            width=20, fg_color=["#2CC985", "#2FA572"], hover_color=["#0C955A", "#106A43"],
            master=self, text="", command=lambda: print(self.chat.name, self.get_gender()), variable=self.gender, value=0)
        radio_button_m = customtkinter.CTkRadioButton(
            width=20, fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"],
            master=self, text="", command=lambda: print(self.chat.name, self.get_gender()), variable=self.gender, value=1)
        radio_button_w = customtkinter.CTkRadioButton(
            width=20, fg_color=["#d13b9f", "#a61f79"], hover_color=['#9e367b', '#701451'],
            master=self, text="", command=lambda: print(self.chat.name, self.get_gender()), variable=self.gender, value=2)

        self.button.grid(row=0, column=4, padx=10, pady=10)
        radio_button_w.grid(row=0, column=3, padx=0, pady=10, sticky="ns")
        radio_button_m.grid(row=0, column=2, padx=0, pady=10, sticky="ns")
        radio_button_u.grid(row=0, column=1, padx=0, pady=10, sticky="ns")
        # self.pack(fill=tkinter.X, padx=0, pady=(0, 1))

    def get_gender(self) -> str:
        # prnt_chat()
        return ["unknown", "male", "female"][self.gender.get()]

    def to_json(self):
        self.chat.need_export = self.need_export.get()
        self.chat.gender = self.get_gender()
        return self.chat.dict()
        # print(self.chat.dict())


class Settings:
    def __init__(self):
        self.filter_bots = tkinter.BooleanVar(value=True)
        self.preview_count = tkinter.IntVar(value=10)
        self.default_filename = tkinter.StringVar(value="chats.json")


class App(customtkinter.CTk):
    def __init__(self):
        self.height = 700
        self.width = 1100
        self.chats = []
        self.chats_page = 0
        self.chats_per_page = 10
        self.chats_pages = 0
        self.json_file = None

        super().__init__()
        self.title("Huynya App 3000 - v0.1 - with love by CyberPotato")
        self.geometry(f"{self.width}x{self.height}")

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        self.tab_1 = tabview.add("Gender Classification")
        self.tab_2 = tabview.add("Dialogs Merge Tool")
        self.tab_3 = tabview.add("Settings")
        # tabview.set("Settings")

        # Dialogs Merge Tool is not implemented yet warning
        warning_label = customtkinter.CTkLabel(
            self.tab_2, text="Dialogs Merge Tool is not implemented yet, uwu :3", font=("Arial", 20))
        warning_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # ------ SETTINGS TAB ------
        self.settings = Settings()

        center_frame = customtkinter.CTkFrame(self.tab_3, width=500)
        # center frame by X
        center_frame.place(relx=0.5, rely=0.1,
                           anchor=tkinter.CENTER, relwidth=0.5)
        center_frame.grid_columnconfigure(1, weight=1)

        # Filter bots label
        filter_bots_label = customtkinter.CTkLabel(
            center_frame, text="Exclude bots")
        filter_bots_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Filter bots switch
        filter_bots_switch = customtkinter.CTkSwitch(
            center_frame, variable=self.settings.filter_bots, onvalue=True, offvalue=False, text=None)
        filter_bots_switch.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        # set filter_bots_switch to True
        filter_bots_switch.select()

        # Preview count
        preview_count_label = customtkinter.CTkLabel(
            center_frame, text="Preview len")
        preview_count_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        preview_count_slider = customtkinter.CTkSlider(
            center_frame, from_=10, to=50, number_of_steps=4, variable=self.settings.preview_count)
        preview_count_slider.grid(
            row=0, column=1, padx=10, pady=10, sticky="ew")

        # slider value label
        self.preview_count_value_label = customtkinter.CTkLabel(
            center_frame, textvariable=self.settings.preview_count)
        self.preview_count_value_label.grid(
            row=0, column=2, padx=(0, 20), pady=10, sticky="w")

        # ------ GENDER CLASSIFICATION TAB ------

        self.tab_1.grid_rowconfigure(0, weight=1)
        self.tab_1.grid_rowconfigure(1, weight=0)
        self.tab_1.grid_columnconfigure(0, weight=1, uniform="group1")
        self.tab_1.grid_columnconfigure(1, weight=1, uniform="group1")

        # left column
        left_frame = customtkinter.CTkFrame(master=self.tab_1)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.list_frame = customtkinter.CTkFrame(master=left_frame)

        self.textbox = customtkinter.CTkTextbox(
            master=self.tab_1, font=("Arial", 16), wrap=tkinter.WORD)
        self.textbox.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.textbox.configure(state=tkinter.DISABLED)

        # bottom row
        bottom_frame = customtkinter.CTkFrame(master=self.tab_1)
        bottom_frame.grid(row=1, column=0, columnspan=2,
                          sticky="nsew", padx=5, pady=5)

        # pagination
        self.prev_btn = customtkinter.CTkButton(
            master=bottom_frame,
            text="<< Prev page",
            command=partial(self.update_list, -1),
            width=80,
        )
        self.prev_btn.pack(padx=10, pady=10, side=tkinter.LEFT)

        self.page_label = customtkinter.CTkLabel(
            master=bottom_frame, text="Page 1 of 1")
        self.page_label.pack(padx=10, pady=0, side=tkinter.LEFT)

        self.next_btn = customtkinter.CTkButton(
            master=bottom_frame, text="Next page >>", command=partial(self.update_list, 1), width=80)
        self.next_btn.pack(padx=10, pady=10, side=tkinter.LEFT)

        self.save_file_btn = customtkinter.CTkButton(
            master=bottom_frame, text="Save file", command=self.save_file, width=80)
        self.save_file_btn.pack(padx=(5, 10), pady=10, side=tkinter.RIGHT)

        # file pick button and label
        self.pick_file_btn = customtkinter.CTkButton(
            master=bottom_frame, text="Load file", command=self.pick_file, width=80)
        self.pick_file_btn.pack(padx=(10, 5), pady=10, side=tkinter.RIGHT)

        # self.file_refr_btn = customtkinter.CTkButton(
        #     master=bottom_frame, text="Update File", command=self.parse_file, width=80)
        # self.file_refr_btn.pack(padx=10, pady=10, side=tkinter.RIGHT)

        self.path_label = customtkinter.CTkLabel(
            master=bottom_frame, text="No file selected")
        self.path_label.pack(
            padx=0, pady=10, side=tkinter.RIGHT, anchor=tkinter.W)

        self.update_list()

    def update_list(self, inc=0):
        self.chats_page += inc
        self.chats_page = max(0, min(self.chats_page, self.chats_pages - 1))
        self.page_label.configure(
            text=f"Page {self.chats_page + 1 if self.chats_pages else 0} of {self.chats_pages}")

        if len(self.chats) > 0:
            self.list_frame.pack(fill=tkinter.X, padx=0, pady=0)

        # undo pack
        for chat in self.chats:
            chat.pack_forget()
        for i in get_page(self.chats_page, self.chats_per_page, self.chats):
            i.pack(fill=tkinter.X, padx=0, pady=(0, 1))

    def pick_file(self):
        print(self.settings.filter_bots.get(),
              self.settings.preview_count.get())
        filetypes = (
            ('Json files', '*.json'),
            ('All files', '*.*')
        )

        self.json_file = fd.askopenfilename(
            title='Open a file',
            initialdir='.',
            filetypes=filetypes)

        if self.json_file:
            try:
                with open(self.json_file, encoding='utf-8') as f:
                    print(f"File {self.json_file} found")
                    filesize = round(len(f.read()) / 1024**2, 2)
                    self.path_label.configure(
                        text=f"{self.json_file} ({filesize} Mb)")
                self.parse_file()

            except FileNotFoundError:
                print(f"File {self.json_file} not found")
                self.path_label.configure(text="File not found")

    def save_file(self):
        f_name = fd.asksaveasfilename(defaultextension=".json",
                                      initialfile=self.settings.default_filename.get())
        if f_name is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        export = []
        for chat in tqdm(self.chats):
            if chat.need_export:
                export.append(chat.to_json())
        text2save = json.dumps(export, indent=1, ensure_ascii=False)

        with open(f_name, 'w', encoding='utf-8') as f:
            f.write(text2save)

    def show_preview(self, text):
        self.textbox.configure(state=tkinter.NORMAL)
        self.textbox.delete("1.0", tkinter.END)
        self.textbox.insert(tkinter.END, text)
        self.textbox.configure(state=tkinter.DISABLED)

    def parse_file(self):
        if not self.json_file:
            print("No file selected")
            return
        print("Parsing file... ", end="")
        self.data = TelegramFile.parse_file(self.json_file).chats.list
        print("Done")

        if self.settings.filter_bots.get():
            self.data = [i for i in self.data if i.name]

        for chat in self.data:
            preview = chat.messages[-10:]
            preview = "\n\n".join(
                [f"[ {m.date_.replace('T', ' ')} ]\n{m.from_}: "
                 f"{m.text if type(m.text) == str else (' '.join((i if type(i) == str else i.text) for i in m.text))}"
                 for m in preview])
            chat.preview = preview
            chat.total_messages = len(chat.messages)

        self.chats = []
        for chat in self.data:
            self.chats.append(
                ListItem(
                    master=self.list_frame,
                    chat=chat,
                    info=partial(self.show_preview, chat.preview)
                )
            )

        self.chats_pages = ceil(len(self.chats) / self.chats_per_page)
        self.update_list()


if __name__ == "__main__":
    app = App()
    app.mainloop()
