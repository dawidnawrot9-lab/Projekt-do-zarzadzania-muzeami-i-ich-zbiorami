import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
from Models import data_manager
from Models.models import Muzeum, Magazyn, Pracownik
import utils


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
        self.update_comboboxes()

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

        self.muzea_listbox = tk.Listbox(left_frame, exportselection=False)
        self.muzea_listbox.pack(fill="both", expand=True, pady=5)
        self.muzea_listbox.bind("<<ListboxSelect>>", self.on_muzeum_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Dodaj", command=self.add_muzeum).pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Zapisz zmiany", command=self.update_muzeum).pack(side="left", expand=True, fill="x",
                                                                                    padx=1)
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
        self.muzeum_lokalizacja_entry.pack(pady=(0, 20))

        tk.Button(mid_frame, text="Pokaż zasoby muzeum", command=self.show_museum_resources, bg="#d9d9d9").pack(
            fill="x", pady=5)

        right_frame = tk.Frame(self.tab_muzea)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.muzea_map = tkintermapview.TkinterMapView(right_frame, corner_radius=5)
        self.muzea_map.pack(fill="both", expand=True)
        self.muzea_map.set_position(52.0693, 19.4803)
        self.muzea_map.set_zoom(6)

        self.refresh_muzea_list()
        self.refresh_muzea_map()

    def build_magazyny_tab(self):
        left_frame = tk.Frame(self.tab_magazyny, width=250)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text="Lista Magazynów", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))

        filter_frame = tk.Frame(left_frame)
        filter_frame.pack(fill="x", pady=5)
        tk.Label(filter_frame, text="Szukaj:").pack(side="left")
        self.magazyny_search_entry = tk.Entry(filter_frame)
        self.magazyny_search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.magazyny_search_entry.bind("<KeyRelease>", self.filter_magazyny)

        self.magazyny_listbox = tk.Listbox(left_frame, exportselection=False)
        self.magazyny_listbox.pack(fill="both", expand=True, pady=5)
        self.magazyny_listbox.bind("<<ListboxSelect>>", self.on_magazyn_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Dodaj", command=self.add_magazyn).pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Zapisz zmiany", command=self.update_magazyn).pack(side="left", expand=True, fill="x",
                                                                                     padx=1)
        tk.Button(btn_frame, text="Usuń", command=self.delete_magazyn).pack(side="left", expand=True, fill="x", padx=1)

        mid_frame = tk.Frame(self.tab_magazyny, width=300)
        mid_frame.pack(side="left", fill="y", padx=10, pady=10)
        mid_frame.pack_propagate(False)

        tk.Label(mid_frame, text="Formularz Magazynu", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 15))

        tk.Label(mid_frame, text="Przypisz do Muzeum:").pack(anchor="w")
        self.magazyn_muzeum_combo = ttk.Combobox(mid_frame, width=37, state="readonly")
        self.magazyn_muzeum_combo.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Nazwa Magazynu:").pack(anchor="w")
        self.magazyn_nazwa_entry = tk.Entry(mid_frame, width=40)
        self.magazyn_nazwa_entry.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Lokalizacja (Miejscowość):").pack(anchor="w")
        self.magazyn_lokalizacja_entry = tk.Entry(mid_frame, width=40)
        self.magazyn_lokalizacja_entry.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Dzieła sztuki (np. po przecinku):").pack(anchor="w")
        self.magazyn_dziela_entry = tk.Entry(mid_frame, width=40)
        self.magazyn_dziela_entry.pack(pady=(0, 10))

        right_frame = tk.Frame(self.tab_magazyny)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.magazyny_map = tkintermapview.TkinterMapView(right_frame, corner_radius=5)
        self.magazyny_map.pack(fill="both", expand=True)
        self.magazyny_map.set_position(52.0693, 19.4803)
        self.magazyny_map.set_zoom(6)

        self.refresh_magazyny_list()
        self.refresh_magazyny_map()

    def build_pracownicy_tab(self):
        left_frame = tk.Frame(self.tab_pracownicy, width=250)
        left_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(left_frame, text="Lista Pracowników", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))

        filter_frame = tk.Frame(left_frame)
        filter_frame.pack(fill="x", pady=5)
        tk.Label(filter_frame, text="Szukaj:").pack(side="left")
        self.pracownicy_search_entry = tk.Entry(filter_frame)
        self.pracownicy_search_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))
        self.pracownicy_search_entry.bind("<KeyRelease>", self.filter_pracownicy)

        self.pracownicy_listbox = tk.Listbox(left_frame, exportselection=False)
        self.pracownicy_listbox.pack(fill="both", expand=True, pady=5)
        self.pracownicy_listbox.bind("<<ListboxSelect>>", self.on_pracownik_select)

        btn_frame = tk.Frame(left_frame)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="Dodaj", command=self.add_pracownik).pack(side="left", expand=True, fill="x", padx=1)
        tk.Button(btn_frame, text="Zapisz zmiany", command=self.update_pracownik).pack(side="left", expand=True,
                                                                                       fill="x", padx=1)
        tk.Button(btn_frame, text="Usuń", command=self.delete_pracownik).pack(side="left", expand=True, fill="x",
                                                                              padx=1)

        mid_frame = tk.Frame(self.tab_pracownicy, width=300)
        mid_frame.pack(side="left", fill="y", padx=10, pady=10)
        mid_frame.pack_propagate(False)

        tk.Label(mid_frame, text="Formularz Pracownika", font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 15))

        tk.Label(mid_frame, text="Przypisz do Muzeum:").pack(anchor="w")
        self.pracownik_muzeum_combo = ttk.Combobox(mid_frame, width=37, state="readonly")
        self.pracownik_muzeum_combo.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Imię:").pack(anchor="w")
        self.pracownik_imie_entry = tk.Entry(mid_frame, width=40)
        self.pracownik_imie_entry.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Nazwisko:").pack(anchor="w")
        self.pracownik_nazwisko_entry = tk.Entry(mid_frame, width=40)
        self.pracownik_nazwisko_entry.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Lokalizacja (Miejscowość):").pack(anchor="w")
        self.pracownik_lokalizacja_entry = tk.Entry(mid_frame, width=40)
        self.pracownik_lokalizacja_entry.pack(pady=(0, 10))

        tk.Label(mid_frame, text="Stanowisko:").pack(anchor="w")
        self.pracownik_stanowisko_entry = tk.Entry(mid_frame, width=40)
        self.pracownik_stanowisko_entry.pack(pady=(0, 10))

        right_frame = tk.Frame(self.tab_pracownicy)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.pracownicy_map = tkintermapview.TkinterMapView(right_frame, corner_radius=5)
        self.pracownicy_map.pack(fill="both", expand=True)
        self.pracownicy_map.set_position(52.0693, 19.4803)
        self.pracownicy_map.set_zoom(6)

        self.refresh_pracownicy_list()
        self.refresh_pracownicy_map()

    def update_comboboxes(self):
        muzea_list = [f"[{m['id']}] {m['nazwa']}" for m in self.data["muzea"]]
        self.magazyn_muzeum_combo['values'] = muzea_list
        self.pracownik_muzeum_combo['values'] = muzea_list

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

    def show_museum_resources(self):
        selection = self.muzea_listbox.curselection()
        if not selection:
            messagebox.showinfo("Informacja", "Wybierz muzeum z listy, aby zobaczyć jego zasoby.")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        muzeum = next((m for m in self.data["muzea"] if m["id"] == muzeum_id), None)

        res_window = tk.Toplevel(self.root)
        res_window.title(f"Zasoby: {muzeum['nazwa']}")
        res_window.geometry("800x400")

        mag_frame = tk.Frame(res_window)
        mag_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        tk.Label(mag_frame, text="Przypisane Magazyny i Dzieła", font=("Arial", 11, "bold")).pack(anchor="w")
        mag_listbox = tk.Listbox(mag_frame)
        mag_listbox.pack(fill="both", expand=True)

        prac_frame = tk.Frame(res_window)
        prac_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        tk.Label(prac_frame, text="Przypisani Pracownicy", font=("Arial", 11, "bold")).pack(anchor="w")
        prac_listbox = tk.Listbox(prac_frame)
        prac_listbox.pack(fill="both", expand=True)

        for mag in self.data["magazyny"]:
            if mag["muzeum_id"] == muzeum_id:
                dziela = mag.get("dziela", "Brak danych")
                mag_listbox.insert(tk.END, f"{mag['nazwa']} ({mag['lokalizacja']}) - Zbiory: {dziela}")

        for prac in self.data["pracownicy"]:
            if prac["muzeum_id"] == muzeum_id:
                stanowisko = prac.get("stanowisko", "Brak stanowiska")
                prac_listbox.insert(tk.END, f"{prac['imie']} {prac['nazwisko']} - {stanowisko} ({prac['lokalizacja']})")

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
        self.update_comboboxes()
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
        self.update_comboboxes()

    def delete_muzeum(self):
        selection = self.muzea_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz muzeum z listy do usunięcia!")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        self.data["muzea"] = [m for m in self.data["muzea"] if m["id"] != muzeum_id]

        self.data["magazyny"] = [mag for mag in self.data["magazyny"] if mag["muzeum_id"] != muzeum_id]
        self.data["pracownicy"] = [p for p in self.data["pracownicy"] if p["muzeum_id"] != muzeum_id]

        data_manager.save_data(self.data)

        self.filter_muzea(None)
        self.filter_magazyny(None)
        self.filter_pracownicy(None)
        self.update_comboboxes()
        self.muzeum_nazwa_entry.delete(0, tk.END)
        self.muzeum_lokalizacja_entry.delete(0, tk.END)

    def refresh_magazyny_list(self, filter_text=""):
        self.magazyny_listbox.delete(0, tk.END)
        for mag in self.data["magazyny"]:
            if filter_text.lower() in mag["nazwa"].lower() or filter_text.lower() in mag["lokalizacja"].lower():
                self.magazyny_listbox.insert(tk.END, f"[{mag['id']}] {mag['nazwa']} ({mag['lokalizacja']})")

    def refresh_magazyny_map(self, filter_text=""):
        self.magazyny_map.delete_all_marker()
        for mag in self.data["magazyny"]:
            if filter_text.lower() in mag["nazwa"].lower() or filter_text.lower() in mag["lokalizacja"].lower():
                self.magazyny_map.set_marker(mag["lat"], mag["lon"], text=mag["nazwa"])

    def filter_magazyny(self, event):
        szukana_fraza = self.magazyny_search_entry.get()
        self.refresh_magazyny_list(szukana_fraza)
        self.refresh_magazyny_map(szukana_fraza)

    def on_magazyn_select(self, event):
        selection = self.magazyny_listbox.curselection()
        if not selection:
            return

        item_text = self.magazyny_listbox.get(selection[0])
        magazyn_id = int(item_text.split("]")[0][1:])

        magazyn = next((mag for mag in self.data["magazyny"] if mag["id"] == magazyn_id), None)
        if magazyn:
            self.magazyn_nazwa_entry.delete(0, tk.END)
            self.magazyn_nazwa_entry.insert(0, magazyn["nazwa"])

            self.magazyn_lokalizacja_entry.delete(0, tk.END)
            self.magazyn_lokalizacja_entry.insert(0, magazyn["lokalizacja"])

            self.magazyn_dziela_entry.delete(0, tk.END)
            self.magazyn_dziela_entry.insert(0, magazyn.get("dziela", ""))

            muzeum = next((m for m in self.data["muzea"] if m["id"] == magazyn["muzeum_id"]), None)
            if muzeum:
                self.magazyn_muzeum_combo.set(f"[{muzeum['id']}] {muzeum['nazwa']}")
            else:
                self.magazyn_muzeum_combo.set("")

            self.magazyny_map.set_position(magazyn["lat"], magazyn["lon"])
            self.magazyny_map.set_zoom(12)

    def get_next_magazyn_id(self):
        if not self.data["magazyny"]:
            return 1
        return max(mag["id"] for mag in self.data["magazyny"]) + 1

    def add_magazyn(self):
        muzeum_str = self.magazyn_muzeum_combo.get()
        nazwa = self.magazyn_nazwa_entry.get().strip()
        lokalizacja = self.magazyn_lokalizacja_entry.get().strip()
        dziela = self.magazyn_dziela_entry.get().strip()

        if not muzeum_str or not nazwa or not lokalizacja:
            messagebox.showwarning("Błąd", "Wypełnij wymagane pola i wybierz muzeum!")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])
        nowe_id = self.get_next_magazyn_id()
        wspolrzedne = utils.get_coordinates(lokalizacja)

        nowy_magazyn = Magazyn(nowe_id, muzeum_id, nazwa, lokalizacja, wspolrzedne[0], wspolrzedne[1], dziela)
        self.data["magazyny"].append(nowy_magazyn.to_dict())
        data_manager.save_data(self.data)

        self.refresh_magazyny_list()
        self.refresh_magazyny_map()

        self.magazyn_nazwa_entry.delete(0, tk.END)
        self.magazyn_lokalizacja_entry.delete(0, tk.END)
        self.magazyn_dziela_entry.delete(0, tk.END)
        self.magazyn_muzeum_combo.set("")

    def update_magazyn(self):
        selection = self.magazyny_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz magazyn z listy do edycji!")
            return

        item_text = self.magazyny_listbox.get(selection[0])
        magazyn_id = int(item_text.split("]")[0][1:])

        muzeum_str = self.magazyn_muzeum_combo.get()
        nazwa = self.magazyn_nazwa_entry.get().strip()
        lokalizacja = self.magazyn_lokalizacja_entry.get().strip()
        dziela = self.magazyn_dziela_entry.get().strip()

        if not muzeum_str or not nazwa or not lokalizacja:
            messagebox.showwarning("Błąd", "Wypełnij wymagane pola i wybierz muzeum!")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])

        for mag in self.data["magazyny"]:
            if mag["id"] == magazyn_id:
                mag["muzeum_id"] = muzeum_id
                mag["nazwa"] = nazwa
                mag["dziela"] = dziela
                if mag["lokalizacja"] != lokalizacja:
                    wspolrzedne = utils.get_coordinates(lokalizacja)
                    mag["lokalizacja"] = lokalizacja
                    mag["lat"] = wspolrzedne[0]
                    mag["lon"] = wspolrzedne[1]
                break

        data_manager.save_data(self.data)
        self.filter_magazyny(None)

    def delete_magazyn(self):
        selection = self.magazyny_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz magazyn z listy do usunięcia!")
            return

        item_text = self.magazyny_listbox.get(selection[0])
        magazyn_id = int(item_text.split("]")[0][1:])

        self.data["magazyny"] = [mag for mag in self.data["magazyny"] if mag["id"] != magazyn_id]
        data_manager.save_data(self.data)

        self.filter_magazyny(None)
        self.magazyn_nazwa_entry.delete(0, tk.END)
        self.magazyn_lokalizacja_entry.delete(0, tk.END)
        self.magazyn_dziela_entry.delete(0, tk.END)
        self.magazyn_muzeum_combo.set("")

    def refresh_pracownicy_list(self, filter_text=""):
        self.pracownicy_listbox.delete(0, tk.END)
        for p in self.data["pracownicy"]:
            if filter_text.lower() in p["imie"].lower() or filter_text.lower() in p[
                "nazwisko"].lower() or filter_text.lower() in p["lokalizacja"].lower():
                self.pracownicy_listbox.insert(tk.END, f"[{p['id']}] {p['imie']} {p['nazwisko']} ({p['lokalizacja']})")

    def refresh_pracownicy_map(self, filter_text=""):
        self.pracownicy_map.delete_all_marker()
        for p in self.data["pracownicy"]:
            if filter_text.lower() in p["imie"].lower() or filter_text.lower() in p[
                "nazwisko"].lower() or filter_text.lower() in p["lokalizacja"].lower():
                self.pracownicy_map.set_marker(p["lat"], p["lon"], text=f"{p['imie']} {p['nazwisko']}")

    def filter_pracownicy(self, event):
        szukana_fraza = self.pracownicy_search_entry.get()
        self.refresh_pracownicy_list(szukana_fraza)
        self.refresh_pracownicy_map(szukana_fraza)

    def on_pracownik_select(self, event):
        selection = self.pracownicy_listbox.curselection()
        if not selection:
            return

        item_text = self.pracownicy_listbox.get(selection[0])
        pracownik_id = int(item_text.split("]")[0][1:])

        pracownik = next((p for p in self.data["pracownicy"] if p["id"] == pracownik_id), None)
        if pracownik:
            self.pracownik_imie_entry.delete(0, tk.END)
            self.pracownik_imie_entry.insert(0, pracownik["imie"])

            self.pracownik_nazwisko_entry.delete(0, tk.END)
            self.pracownik_nazwisko_entry.insert(0, pracownik["nazwisko"])

            self.pracownik_lokalizacja_entry.delete(0, tk.END)
            self.pracownik_lokalizacja_entry.insert(0, pracownik["lokalizacja"])

            self.pracownik_stanowisko_entry.delete(0, tk.END)
            self.pracownik_stanowisko_entry.insert(0, pracownik.get("stanowisko", ""))

            muzeum = next((m for m in self.data["muzea"] if m["id"] == pracownik["muzeum_id"]), None)
            if muzeum:
                self.pracownik_muzeum_combo.set(f"[{muzeum['id']}] {muzeum['nazwa']}")
            else:
                self.pracownik_muzeum_combo.set("")

            self.pracownicy_map.set_position(pracownik["lat"], pracownik["lon"])
            self.pracownicy_map.set_zoom(12)

    def get_next_pracownik_id(self):
        if not self.data["pracownicy"]:
            return 1
        return max(p["id"] for p in self.data["pracownicy"]) + 1

    def add_pracownik(self):
        muzeum_str = self.pracownik_muzeum_combo.get()
        imie = self.pracownik_imie_entry.get().strip()
        nazwisko = self.pracownik_nazwisko_entry.get().strip()
        lokalizacja = self.pracownik_lokalizacja_entry.get().strip()
        stanowisko = self.pracownik_stanowisko_entry.get().strip()

        if not muzeum_str or not imie or not nazwisko or not lokalizacja:
            messagebox.showwarning("Błąd", "Wypełnij wymagane pola i wybierz muzeum!")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])
        nowe_id = self.get_next_pracownik_id()
        wspolrzedne = utils.get_coordinates(lokalizacja)

        nowy_pracownik = Pracownik(nowe_id, muzeum_id, imie, nazwisko, lokalizacja, wspolrzedne[0], wspolrzedne[1],
                                   stanowisko)
        self.data["pracownicy"].append(nowy_pracownik.to_dict())
        data_manager.save_data(self.data)

        self.refresh_pracownicy_list()
        self.refresh_pracownicy_map()

        self.pracownik_imie_entry.delete(0, tk.END)
        self.pracownik_nazwisko_entry.delete(0, tk.END)
        self.pracownik_lokalizacja_entry.delete(0, tk.END)
        self.pracownik_stanowisko_entry.delete(0, tk.END)
        self.pracownik_muzeum_combo.set("")

    def update_pracownik(self):
        selection = self.pracownicy_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz pracownika z listy do edycji!")
            return

        item_text = self.pracownicy_listbox.get(selection[0])
        pracownik_id = int(item_text.split("]")[0][1:])

        muzeum_str = self.pracownik_muzeum_combo.get()
        imie = self.pracownik_imie_entry.get().strip()
        nazwisko = self.pracownik_nazwisko_entry.get().strip()
        lokalizacja = self.pracownik_lokalizacja_entry.get().strip()
        stanowisko = self.pracownik_stanowisko_entry.get().strip()

        if not muzeum_str or not imie or not nazwisko or not lokalizacja:
            messagebox.showwarning("Błąd", "Wypełnij wymagane pola i wybierz muzeum!")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])

        for p in self.data["pracownicy"]:
            if p["id"] == pracownik_id:
                p["muzeum_id"] = muzeum_id
                p["imie"] = imie
                p["nazwisko"] = nazwisko
                p["stanowisko"] = stanowisko
                if p["lokalizacja"] != lokalizacja:
                    wspolrzedne = utils.get_coordinates(lokalizacja)
                    p["lokalizacja"] = lokalizacja
                    p["lat"] = wspolrzedne[0]
                    p["lon"] = wspolrzedne[1]
                break

        data_manager.save_data(self.data)
        self.filter_pracownicy(None)

    def delete_pracownik(self):
        selection = self.pracownicy_listbox.curselection()
        if not selection:
            messagebox.showwarning("Błąd", "Wybierz pracownika z listy do usunięcia!")
            return

        item_text = self.pracownicy_listbox.get(selection[0])
        pracownik_id = int(item_text.split("]")[0][1:])

        self.data["pracownicy"] = [p for p in self.data["pracownicy"] if p["id"] != pracownik_id]
        data_manager.save_data(self.data)

        self.filter_pracownicy(None)
        self.pracownik_imie_entry.delete(0, tk.END)
        self.pracownik_nazwisko_entry.delete(0, tk.END)
        self.pracownik_lokalizacja_entry.delete(0, tk.END)
        self.pracownik_stanowisko_entry.delete(0, tk.END)
        self.pracownik_muzeum_combo.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = MuseumApp(root)
    root.mainloop()