import tkinter as tk
from tkinter import ttk, messagebox
from Models import data_manager
from Views.gui_muzea import MuzeaTab
from Views.gui_magazyny import MagazynyTab
from Views.gui_pracownicy import PracownicyTab


class MuseumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Zarządzania Muzeami")
        self.root.geometry("450x300")
        self.root.resizable(False, False)
        self.data = data_manager.load_data()

        self.bg_main = "#2b2a27"
        self.bg_panel = "#383633"
        self.text_color = "#e6e1d5"
        self.accent_color = "#8b2e2e"
        self.list_bg = "#42403c"

        self.root.configure(bg=self.bg_main)
        self.setup_styles()
        self.show_login_screen()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure(".", background=self.bg_main, foreground=self.text_color, font=("Helvetica", 10))

        self.style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.bg_panel, foreground=self.text_color, padding=[15, 8],
                             borderwidth=0, font=("Helvetica", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.accent_color)])

        self.style.configure("TFrame", background=self.bg_main)

        self.style.configure("TLabel", background=self.bg_main, foreground=self.text_color)

        self.style.configure("TButton", background=self.list_bg, foreground=self.text_color, borderwidth=0, padding=6,
                             font=("Helvetica", 10, "bold"))
        self.style.map("TButton", background=[("active", self.accent_color)])

        self.style.configure("TEntry", fieldbackground=self.list_bg, foreground="white", borderwidth=0, padding=5)

        self.style.configure("TCombobox", fieldbackground=self.list_bg, background=self.list_bg, foreground="white",
                             borderwidth=0, padding=5)
        self.style.map("TCombobox", fieldbackground=[("readonly", self.list_bg)],
                       selectbackground=[("readonly", self.accent_color)])

        self.style.configure("TLabelframe", background=self.bg_main, foreground=self.text_color,
                             bordercolor=self.list_bg)
        self.style.configure("TLabelframe.Label", background=self.bg_main, foreground=self.accent_color,
                             font=("Helvetica", 12, "bold"))

    def show_login_screen(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(expand=True, fill="both", padx=40, pady=40)

        ttk.Label(self.login_frame, text="SYSTEM LOGOWANIA", font=("Helvetica", 16, "bold"),
                  foreground=self.accent_color).pack(pady=(0, 20))

        ttk.Label(self.login_frame, text="Login:").pack(anchor="w")
        self.entry_login = ttk.Entry(self.login_frame, width=40)
        self.entry_login.pack(pady=(0, 10), fill="x")

        ttk.Label(self.login_frame, text="Hasło:").pack(anchor="w")
        self.entry_haslo = ttk.Entry(self.login_frame, show="*", width=40)
        self.entry_haslo.pack(pady=(0, 20), fill="x")

        ttk.Button(self.login_frame, text="ZALOGUJ", command=self.login).pack(fill="x")

    def login(self):
        login = self.entry_login.get()
        haslo = self.entry_haslo.get()

        if login == "admin" and haslo == "admin":
            self.login_frame.destroy()
            self.show_main_screen()
        else:
            messagebox.showerror("Błąd autoryzacji", "Odmowa dostępu. Nieprawidłowe dane.")

    def show_main_screen(self):
        self.root.geometry("1300x750")
        self.root.resizable(True, True)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)

        self.tab_muzea = ttk.Frame(self.notebook)
        self.tab_magazyny = ttk.Frame(self.notebook)
        self.tab_pracownicy = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_muzea, text=" MUZEA ")
        self.notebook.add(self.tab_magazyny, text=" MAGAZYNY ZBIORÓW ")
        self.notebook.add(self.tab_pracownicy, text=" PRACOWNICY ")

        self.muzea_handler = MuzeaTab(self.tab_muzea, self)
        self.magazyny_handler = MagazynyTab(self.tab_magazyny, self)
        self.pracownicy_handler = PracownicyTab(self.tab_pracownicy, self)

        self.update_all_views()

    def create_custom_listbox(self, parent):
        lb = tk.Listbox(parent, exportselection=False, bg=self.list_bg, fg="white",
                        selectbackground=self.accent_color, selectforeground="white",
                        relief="flat", borderwidth=0, highlightthickness=1, highlightbackground=self.bg_panel,
                        font=("Helvetica", 10))
        return lb

    def update_all_views(self):
        self.muzea_handler.filter_muzea(None)
        self.magazyny_handler.filter_magazyny(None)
        self.pracownicy_handler.filter_pracownicy(None)

        muzea_list = [f"[{m['id']}] {m['nazwa']}" for m in self.data["muzea"]]
        self.magazyny_handler.magazyn_muzeum_combo['values'] = muzea_list
        self.pracownicy_handler.pracownik_muzeum_combo['values'] = muzea_list


if __name__ == "__main__":
    root = tk.Tk()
    app = MuseumApp(root)
    root.mainloop()