import tkinter
import customtkinter
from tkinter import filedialog as fd
from functools import partial

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
# Themes: "blue" (standard), "green", "dark-blue"


class ListItem(customtkinter.CTkFrame):
    def __init__(self, master, text, info):
        super().__init__(master)
        self.text = text
        self.checkbox = customtkinter.CTkCheckBox(self, text=self.text)
        self.checkbox.pack(side=tkinter.LEFT, padx=10,
                           pady=10, expand=True, fill=tkinter.BOTH)
        # self.label = customtkinter.CTkLabel(self, text=self.text)
        # self.label.pack(side=tkinter.LEFT)
        self.button = customtkinter.CTkButton(
            self, text="?", width=30, command=info, font=("Arial", 16))

        def print_self(): return print(self.text, self.grnder)
        # RADIO BUTTON
        self.gender = tkinter.IntVar(value=0)
        radio_button_u = customtkinter.CTkRadioButton(
            width=20, fg_color=["#2CC985", "#2FA572"], hover_color=["#0C955A", "#106A43"],
            master=self, text="", command=lambda: print(self.text, self.get_gender()), variable=self.gender, value=0)
        radio_button_m = customtkinter.CTkRadioButton(
            width=20, fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"],
            master=self, text="", command=lambda: print(self.text, self.get_gender()), variable=self.gender, value=1)
        radio_button_w = customtkinter.CTkRadioButton(
            width=20, fg_color=["#d13b9f", "#a61f79"], hover_color=['#9e367b', '#701451'],
            master=self, text="", command=lambda: print(self.text, self.get_gender()), variable=self.gender, value=2)

        self.button.pack(side=tkinter.RIGHT, padx=10, pady=10)
        radio_button_w.pack(padx=0, pady=10, side=tkinter.RIGHT)
        radio_button_m.pack(padx=0, pady=10, side=tkinter.RIGHT)
        radio_button_u.pack(padx=0, pady=10, side=tkinter.RIGHT)
        self.pack(fill=tkinter.X, padx=0, pady=(0, 1))

    def get_gender(self) -> str:
        return ["Неизвестно", "Мужской", "Женский"][self.gender.get()]

    def delete(self):
        self.destroy()


class App(customtkinter.CTk):
    def __init__(self):
        self.height = 700
        self.width = 1100
        super().__init__()
        self.geometry(f"{self.width}x{self.height}")

        tabview = customtkinter.CTkTabview(self)
        tabview.pack(padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        self.tab_1 = tabview.add("Gender Classification")
        self.tab_2 = tabview.add("Dialogs Merge Tool")
        # self.tab_3 = tabview.add("Settings")
        # tabview.set("Dialogs Merge Tool")

        # Dialogs Merge Tool is not implemented yet warning
        warning_label = customtkinter.CTkLabel(
            self.tab_2, text="Dialogs Merge Tool is not implemented yet, uwu :3", font=("Arial", 20))
        warning_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # ------ GENDER CLASSIFICATION TAB ------

        self.tab_1.grid_rowconfigure(0, weight=1)
        self.tab_1.grid_rowconfigure(1, weight=0)
        self.tab_1.grid_columnconfigure(0, weight=1)
        self.tab_1.grid_columnconfigure(1, weight=1)

        # left column
        left_frame = customtkinter.CTkFrame(master=self.tab_1)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        list_frame = customtkinter.CTkFrame(master=left_frame)
        list_frame.pack(fill=tkinter.X, padx=0, pady=0)

        list_items = []
        for i in range(10):
            list_items.append(ListItem(list_frame, "Item " +
                              str(i), partial(self.show_preview, i)))

        self.textbox = customtkinter.CTkTextbox(
            master=self.tab_1, font=("Arial", 16))
        self.textbox.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.textbox.configure(state=tkinter.DISABLED)

        # bottom row
        bottom_frame = customtkinter.CTkFrame(master=self.tab_1)
        bottom_frame.grid(row=1, column=0, columnspan=2,
                          sticky="nsew", padx=5, pady=5)

        # pagination
        self.prev_btn = customtkinter.CTkButton(
            master=bottom_frame, text="<< Prev page", command=self.pick_file, width=80, bg_color="transparent")
        self.prev_btn.pack(padx=10, pady=10, side=tkinter.LEFT)

        self.page_label = customtkinter.CTkLabel(
            master=bottom_frame, text="Page 1 of 1")
        self.page_label.pack(padx=10, pady=0, side=tkinter.LEFT)

        self.next_btn = customtkinter.CTkButton(
            master=bottom_frame, text="Next page >>", command=self.pick_file, width=80)
        self.next_btn.pack(padx=10, pady=10, side=tkinter.LEFT)

        # file pick button and label
        self.pick_file_btn = customtkinter.CTkButton(
            master=bottom_frame, text="Pick file", command=self.pick_file, width=80)
        self.pick_file_btn.pack(padx=10, pady=10, side=tkinter.RIGHT)

        self.path_label = customtkinter.CTkLabel(
            master=bottom_frame, text="No file selected")
        self.path_label.pack(
            padx=0, pady=10, side=tkinter.RIGHT, anchor=tkinter.W)

    def pick_file(self):
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
                with open(self.json_file) as f:
                    print(f"File {self.json_file} found")
                    filesize = round(len(f.read()) / 1024**2, 2)
                    self.path_label.configure(
                        text=f"{self.json_file} ({filesize} Mb)")

            except FileNotFoundError:
                print(f"File {self.json_file} not found")
                self.path_label.configure(text="File not found")

    def show_preview(self, id):
        print(f"Showing preview for item {id}")
        # TODO: get random messages from json file from person with id,
        # TODO: show them in preview window

        # все совпадения с реальными людьми случайны
        users = [
            "Rayan Gosling",
            "Johny Depp",
            "Tom Cruise",
            "Brad Pitt",
            "Leonardo DiCaprio",
            "Will Smith",
            "yyyyylia"
        ]

        messages = [
            {"text": "Привет!", "from": "Вы", "t": "3:00"},
            {"text": "Привет", "from": users[id % len(users)], "t": "3:01"},
            {"text": "Как ты?", "from": "Вы", "t": "3:02"},
            {"text": "Все хорошо",
                "from": users[id % len(users)], "t": "3:03"},
            {"text": "Нам нужно поговорить.", "from": "Вы", "t": "3:04"},
            {"text": "У меня нет времени",
                "from": users[id % len(users)], "t": "3:05"},
        ]

        text = "\n\n".join(
            [f"({m['t']}) {m['from']}: {m['text']}" for m in messages])
        text = f"Total messages: {len(messages) ** (11 - id) + 1234}\nPreview:\n\n" + text

        self.textbox.configure(state=tkinter.NORMAL)
        self.textbox.delete("1.0", tkinter.END)
        self.textbox.insert(tkinter.END, text)
        self.textbox.configure(state=tkinter.DISABLED)


if __name__ == "__main__":
    app = App()
    app.mainloop()
