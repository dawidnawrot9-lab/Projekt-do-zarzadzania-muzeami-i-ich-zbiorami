import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
import Models.data_manager as data_manager
import utils
from Models.models import Muzeum, Magazyn, Pracownik


class MuseumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("System Zarządzania Muzeami")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        self.data = data_manager.load_data()
        self.show_login_screen()

    def show_login_screen(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(expand=True)

        tk.Label(self.login_frame, text="Logowanie do systemu", font=("Arial", 16, "bold")).grid(row=0, column=0,
                                                                                                 columnspan=2, pady=20)

        tk.Label(self.login_frame, text="Login:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.entry_login = tk.Entry(self.login_frame)
        self.entry_login.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(self.login_frame, text="Hasło:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.entry_haslo = tk.Entry(self.login_frame, show="*")
        self.entry_haslo.grid(row=2, column=1, pady=5, padx=5)

        tk.Button(self.login_frame, text="Zaloguj", width=15, command=self.login).grid(row=3, column=0, columnspan=2,
                                                                                       pady=20)

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

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        self.tab_muzea = ttk.Frame(self.notebook)
        self.tab_magazyny = ttk.Frame(self.notebook)
        self.tab_pracownicy = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_muzea, text="🏛️ Muzea")
        self.notebook.add(self.tab_magazyny, text="📦 Magazyny")
        self.notebook.add(self.tab_pracownicy, text="👥 Pracownicy")

        self.build_muzea_tab()
        self.build_magazyny_tab()
        self.build_pracownicy_tab()

    def build_muzea_tab(self):
        left_frame = tk.Frame(self.tab_muzea, width=250)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text="Lista Muzeów", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))

        filter_frame = tk.Frame(left_frame)
        filter_frame.pack(fill="x", pady=5)
        tk.Label(filter_frame, text="Szukaj:").pack(side="left")
        self.muzea_search_entry = tk.Entry(filter_frame)
        self.muzea_search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.muzea_search_entry.bind("<KeyRelease>", self.filter_muzea)

        self.muzea_listbox = tk.Listbox(left_frame)
        self.muzea_listbox.pack(fill="both", expand=True, pady=5)
        self.muzea_listbox.bind("<<ListboxSelect>>", self.on_muzeum_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Dodaj", command=self.add_muzeum).pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Edytuj", command=self.update_muzeum).pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Usuń", command=self.delete_muzeum).pack(side="left", expand=True, fill="x", padx=1)

        mid_frame = tk.Frame(self.tab_muzea, width=300)
        mid_frame.pack(side="left", fill="y", padx=10, pady=10)
        mid_frame.pack_propagate(False)

        tk.Label(mid_frame, text="Formularz Muzeum", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 15))

        tk.Label(mid_frame, text="Nazwa:").pack(anchor="w")
        self.muzeum_nazwa_entry = tk.Entry(mid_frame, width=40)
        self.muzeum_nazwa_entry.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Lokalizacja (Miejscowość):").pack(anchor="w")
        self.muzeum_lokalizacja_entry = tk.Entry(mid_frame, width=40)
        self.muzeum_lokalizacja_entry.pack(pady=(0, 10))

        right_frame = tk.Frame(self.tab_muzea)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.muzea_map = tkintermapview.TkinterMapView(right_frame, corner_radius=5)
        self.muzea_map.pack(fill="both", expand=True)
        self.muzea_map.set_position(52.0693, 19.4803)
        self.muzea_map.set_zoom(6)

        self.refresh_muzea_list()
        self.refresh_muzea_map()

    def build_magazyny_tab(self):
        tk.Label(self.tab_magazyny, text="W budowie...").pack(pady=50)

    def build_pracownicy_tab(self):
        tk.Label(self.tab_pracownicy, text="W budowie...").pack(pady=50)

    def refresh_muzea_list(self, filter_text=""):
        self.muzea_listbox.delete(0, tk.END)
        for m in self.data["muzea"]:
            if filter_text.lower() in m["nazwa"].lower() or filter_text.lower() in m["lokalizacja"].lower():
                self.muzea_listbox.insert(tk.END, f"[{m['id']}] {m['nazwa']} ({m['lokalizacja']})")

    def refresh_muzea_map(self, filter_text=""):
        self.muzea_map.delete_all_marker()
        for m in self.data["muzea"]:
            if filter_text.lower() in m["nazwa"].lower() or filter_text.lower() in m["lokalizacja"].lower():
                self.muzea_map.set_marker(m["lat"], m["lon"], text=m["nazwa"])

    def filter_muzea(self, event):
        szukana_fraza = self.muzea_search_entry.get()
        self.refresh_muzea_list(szukana_fraza)
        self.refresh_muzea_map(szukana_fraza)

    def on_muzeum_select(self, event):
        selection = self.muzea_listbox.curselection()
        if not selection:
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        muzeum = next((m for m in self.data["muzea"] if m["id"] == muzeum_id), None)
        if muzeum:
            self.muzeum_nazwa_entry.delete(0, tk.END)
            self.muzeum_nazwa_entry.insert(0, muzeum["nazwa"])

            self.muzeum_lokalizacja_entry.delete(0, tk.END)
            self.muzeum_lokalizacja_entry.insert(0, muzeum["lokalizacja"])

            self.muzea_map.set_position(muzeum["lat"], muzeum["lon"])
            self.muzea_map.set_zoom(12)

    def get_next_muzeum_id(self):
        if not self.data["muzea"]:
            return 1
        return max(m["id"] for m in self.data["muzea"]) + 1

    def add_muzeum(self):
        nazwa = self.muzeum_nazwa_entry.get().strip()
        lokalizacja = self.muzeum_lokalizacja_entry.get().strip()

        if not nazwa or not lokalizacja:
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola!")
            return

        nowe_id = self.get_next_muzeum_id()
        wspolrzedne = utils.get_coordinates(lokalizacja)

        nowe_muzeum = Muzeum(nowe_id, nazwa, lokalizacja, wspolrzedne[0], wspolrzedne[1])
        self.data["muzea"].append(nowe_muzeum.to_dict())
        data_manager.save_data(self.data)

        self.refresh_muzea_list()
        self.refresh_muzea_map()
        self.muzeum_nazwa_entry.delete(0, tk.END)
        self.muzeum_lokalizacja_entry.delete(0, tk.END)

    def update_muzeum(self):
        selection = self.muzea_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz muzeum z listy do edycji!")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        nazwa = self.muzeum_nazwa_entry.get().strip()
        lokalizacja = self.muzeum_lokalizacja_entry.get().strip()

        if not nazwa or not lokalizacja:
            messagebox.showwarning("Błąd", "Wypełnij wszystkie pola!")
            return

        for m in self.data["muzea"]:
            if m["id"] == muzeum_id:
                m["nazwa"] = nazwa
                if m["lokalizacja"] != lokalizacja:
                    wspolrzedne = utils.get_coordinates(lokalizacja)
                    m["lokalizacja"] = lokalizacja
                    m["lat"] = wspolrzedne[0]
                    m["lon"] = wspolrzedne[1]
                break

        data_manager.save_data(self.data)
        self.filter_muzea(None)

    def delete_muzeum(self):
        selection = self.muzea_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz muzeum z listy do usunięcia!")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        self.data["muzea"] = [m for m in self.data["muzea"] if m["id"] != muzeum_id]
        data_manager.save_data(self.data)

        self.filter_muzea(None)
        self.muzeum_nazwa_entry.delete(0, tk.END)
        self.muzeum_lokalizacja_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MuseumApp(root)
    root.mainloop()