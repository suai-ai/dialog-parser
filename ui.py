import tkinter
import customtkinter

# customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
# customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# app = customtkinter.CTk()  # create CTk window like you do with the Tk window
# app.geometry("400x240")

# def button_function():
#     print("button pressed")

# # Use CTkButton instead of tkinter Button
# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# app.mainloop()


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("blue")


class ListItem(customtkinter.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)
        # self.grid(padx=10, pady=10, sticky="ew")
        # self.grid(row=i, column=0)
        self.text = text
        self.label = customtkinter.CTkLabel(self, text=self.text)
        self.label.pack(side=tkinter.LEFT, expand=True)
        self.button = customtkinter.CTkButton(
            self, text="X", command=self.delete)
        # self.button.pack(side=tkinter.RIGHT)
        # segemented_button_var = customtkinter.StringVar(value="Человек")  # set initial value

        # segemented_button = customtkinter.CTkComboBox(master=self,
        #                                       values=["Человек", "Женщина", "Боевой вертолет"],
        #                                       variable=segemented_button_var)
        # segemented_button.pack(padx=20, pady=10, side=tkinter.RIGHT)
        segemented_button = customtkinter.CTkOptionMenu(
            master=self,
            values=[
                "[ неизвестно ]", "Человек", "Женщина"],
            command=lambda x: print(text, x))
        segemented_button.pack(padx=10, pady=10, side=tkinter.RIGHT)
        self.pack(fill=tkinter.X, padx=10, pady=5, expand=True)

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
        frame1.grid(row=0, column=0, sticky="nsew", padx=4, pady=4)

        list_items = []
        for i in range(30):
            list_items.append(ListItem(frame1, "Item " + str(i)))
            # customtkinter.CTkLabel(master=frame1, text=f"Item {i}"))
            # list_items[i].grid(row=i, column=0, sticky="nsew", padx=4, pady=4)

        # right column
        frame2 = customtkinter.CTkFrame(master=self.tab_1)
        frame2.grid(row=0, column=1, sticky="nsew", padx=4, pady=4)

        # bottom row
        frame3 = customtkinter.CTkFrame(master=self.tab_1)
        frame3.grid(row=1, column=0, columnspan=2,
                    sticky="nsew", padx=4, pady=4)

        # bottom row buttons
        self.button = customtkinter.CTkButton(
            master=frame3, text="CTkButton", command=self.pick_file)
        self.button.grid(row=1, column=0, sticky="nsew")

        self.button2 = customtkinter.CTkButton(
            master=frame3, text="CTkButton2", command=self.pick_file)
        self.button2.grid(row=1, column=1, sticky="nsew")

    def pick_file(self):
        dialog = customtkinter.CTkInputDialog(
            text="Type a filename", title="Telegram export file")
        file = dialog.get_input()
        print(file)
        try:
            with open(file) as f:
                print("File found")
        except FileNotFoundError:
            print("File not found")


if __name__ == "__main__":
    app = App()
    app.mainloop()
