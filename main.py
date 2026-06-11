import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkintermapview



class MuseumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Zarządzania Muzeami")
        self.root.geometry("400x250")
        self.root.resizable(False, False)

        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Logowanie do systemu", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.login_frame, text="Login:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.entry_login = tk.Entry(self.login_frame)
        self.entry_login.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.login_frame, text="Hasło:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.entry_haslo = tk.Entry(self.login_frame, show="*")
        self.entry_haslo.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self.login_frame, text="Zaloguj", width=15, command=self.login).grid(row=3, column=0, columnspan=2, pady=20)

    def login(self):
        login = self.entry_login.get()
        haslo = self.entry_haslo.get()

        if login == "admin" and haslo == "admin":
            self.login_frame.destroy()
            self.show_main_screen()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login lub hasło!")

    def show_main_screen(self):
        self.root.geometry("1200x700")
        self.root.resizable(True, True)

        # Tworzenie panelu z zakładkami
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Tworzenie ramek dla poszczególnych zakładek
        self.tab_muzea = ttk.Frame(self.notebook)
        self.tab_magazyny = ttk.Frame(self.notebook)
        self.tab_pracownicy = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_muzea, text="🏛️ Muzea")
        self.notebook.add(self.tab_magazyny, text="📦 Magazyny")
        self.notebook.add(self.tab_pracownicy, text="👥 Pracownicy")

        self.build_tab_layout(self.tab_muzea, "Lista Muzeów")
        self.build_tab_layout(self.tab_magazyny, "Lista Magazynów")
        self.build_tab_layout(self.tab_pracownicy, "Lista Pracowników")

    def build_tab_layout(self, parent_frame, title):

        left_frame = tk.Frame(parent_frame, width=250)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text=title, font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))

        filter_frame = tk.Frame(left_frame)
        filter_frame.pack(fill="x", pady=5)
        tk.Label(filter_frame, text="Szukaj:").pack(side="left")
        tk.Entry(filter_frame).pack(side="left", fill="x", expand=True, padx=(5, 0))


        listbox = tk.Listbox(left_frame)
        listbox.pack(fill="both", expand=True, pady=5)


        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Dodaj").pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Edytuj").pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Usuń").pack(side="left", expand=True, fill="x", padx=1)


        mid_frame = tk.Frame(parent_frame, width=300)
        mid_frame.pack(side="left", fill="y", padx=10, pady=10)


        mid_frame.pack_propagate(False)

        tk.Label(mid_frame, text="Szczegóły / Formularz", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 15))

        tk.Label(mid_frame, text="[Miejsce na pola formularza]", fg="gray").pack(pady=50)


        right_frame = tk.Frame(parent_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        map_widget = tkintermapview.TkinterMapView(right_frame, corner_radius=5)
        map_widget.pack(fill="both", expand=True)

        map_widget.set_position(52.0693, 19.4803)
        map_widget.set_zoom(6)


if __name__ == "__main__":
    root = tk.Tk()
    app = MuseumApp(root)
    root.mainloop()