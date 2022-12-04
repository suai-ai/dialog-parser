import tkinter
import customtkinter
from tkinter import filedialog as fd

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
# Themes: "blue" (standard), "green", "dark-blue"


class ListItem(customtkinter.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)
        self.text = text
        self.checkbox = customtkinter.CTkCheckBox(self, text=self.text)
        self.checkbox.pack(side=tkinter.LEFT, padx=10,
                           pady=10, expand=True, fill=tkinter.BOTH)
        # self.label = customtkinter.CTkLabel(self, text=self.text)
        # self.label.pack(side=tkinter.LEFT)
        self.button = customtkinter.CTkButton(
            self, text="?", width=30, command=self.delete, font=("Arial", 16))
        # SEGMENTED BUTTON
        # segemented_button = customtkinter.CTkOptionMenu(
        #     master=self,
        #     values=[
        #         "[ неизвестно ]", "Человек", "Женщина"],
        #     command=lambda x: print(text, x))
        # segemented_button.pack(padx=10, pady=10, side=tkinter.RIGHT)

        # RADIO BUTTON
        self.gender = tkinter.IntVar(value=0)
        radio_button_u = customtkinter.CTkRadioButton(
            width=20, fg_color=["#2CC985", "#2FA572"], hover_color=["#0C955A", "#106A43"],
            master=self, text="", command=lambda x: print(text, x), variable=self.gender, value=0)
        radio_button_m = customtkinter.CTkRadioButton(
            width=20, fg_color=["#3B8ED0", "#1F6AA5"], hover_color=["#36719F", "#144870"],
            master=self, text="", command=lambda x: print(text, x), variable=self.gender, value=1)
        radio_button_w = customtkinter.CTkRadioButton(
            width=20, fg_color=["#d13b9f", "#a61f79"], hover_color=['#9e367b', '#701451'],
            master=self, text="", command=lambda x: print(text, x), variable=self.gender, value=2)

        self.button.pack(side=tkinter.RIGHT, padx=10, pady=10)
        radio_button_w.pack(padx=0, pady=10, side=tkinter.RIGHT)
        radio_button_m.pack(padx=0, pady=10, side=tkinter.RIGHT)
        radio_button_u.pack(padx=0, pady=10, side=tkinter.RIGHT)
        self.pack(fill=tkinter.X, padx=0, pady=(0, 1))

    def get_gender(self):
        return self.text

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

        # segemented_button_var = customtkinter.StringVar(
        #     value="Value 1")  # set initial value

        # segemented_button = customtkinter.CTkSegmentedButton(
        #     master=self.tab_2,
        #     font=("Arial", 16),
        #     border_width=5,
        #     corner_radius=8,
        #     values=["Value 1", "Value 2", "Value 3"],
        #     variable=segemented_button_var
        # )
        # segemented_button.pack(padx=20, pady=10)

        # Dialogs Merge Tool is not implemented yet warning
        warning = customtkinter.CTkLabel(
            self.tab_2, text="Dialogs Merge Tool is not implemented yet, uwu :3", font=("Arial", 20))
        warning.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # ------ GENDER CLASSIFICATION TAB ------

        # two columns with 40% and 60% width
        self.tab_1.rowconfigure(0, weight=1)
        self.tab_1.rowconfigure(1, weight=0)
        self.tab_1.grid_columnconfigure(0, weight=6)
        self.tab_1.grid_columnconfigure(1, weight=4)

        # left column
        frame1 = customtkinter.CTkFrame(master=self.tab_1)
        frame1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        frame11 = customtkinter.CTkFrame(master=frame1)
        frame11.pack(fill=tkinter.X, padx=0, pady=0)

        list_items = []
        for i in range(10):
            list_items.append(ListItem(frame11, "Item " + str(i)))

        # right column
        frame2 = customtkinter.CTkFrame(master=self.tab_1)
        frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # bottom row
        frame3 = customtkinter.CTkFrame(master=self.tab_1)
        frame3.grid(row=1, column=0, columnspan=2,
                    sticky="nsew", padx=5, pady=5)

        # bottom row buttons
        self.button = customtkinter.CTkButton(
            master=frame3, text="<< Prev page", command=self.pick_file, width=80, bg_color="transparent")
        self.button.pack(padx=10, pady=10, side=tkinter.LEFT)
        # self.button.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.page_label = customtkinter.CTkLabel(
            master=frame3, text="Page 1 of 1")
        self.page_label.pack(padx=10, pady=0, side=tkinter.LEFT)
        # self.page_label.grid(row=1, column=1, sticky="nsew", padx=0, pady=10)

        self.button2 = customtkinter.CTkButton(
            master=frame3, text="Next page >>", command=self.pick_file, width=80)
        self.button2.pack(padx=10, pady=10, side=tkinter.LEFT)
        # self.button2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.pick_file_btn = customtkinter.CTkButton(
            master=frame3, text="Pick file", command=self.pick_file, width=80)
        self.pick_file_btn.pack(padx=10, pady=10, side=tkinter.RIGHT)
        # self.button2.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.path_label = customtkinter.CTkLabel(
            master=frame3, text="No file selected")
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
