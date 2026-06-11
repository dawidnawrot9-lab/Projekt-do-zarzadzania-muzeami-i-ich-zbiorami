import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
from Models import data_manager
from Models.models import Pracownik
import utils


class PracownicyTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.build_tab()

    def build_tab(self):
        left_frame = ttk.Frame(self.parent, width=280)
        left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        ttk.Label(left_frame, text="Wykaz Personelu", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))

        self.pracownicy_search_entry = ttk.Entry(left_frame)
        self.pracownicy_search_entry.pack(fill="x", pady=5)
        self.pracownicy_search_entry.bind("<KeyRelease>", self.filter_pracownicy)

        self.pracownicy_listbox = self.app.create_custom_listbox(left_frame)
        self.pracownicy_listbox.pack(fill="both", expand=True, pady=5)
        self.pracownicy_listbox.bind("<<ListboxSelect>>", self.on_pracownik_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Dodaj", command=self.add_pracownik).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(btn_frame, text="Zapisz", command=self.update_pracownik).pack(side="left", expand=True, fill="x",
                                                                                 padx=2)
        ttk.Button(btn_frame, text="Usuń", command=self.delete_pracownik).pack(side="left", expand=True, fill="x",
                                                                               padx=2)

        mid_frame = ttk.Frame(self.parent, width=320)
        mid_frame.pack(side="left", fill="y", padx=5, pady=10)
        mid_frame.pack_propagate(False)

        form_frame = ttk.LabelFrame(mid_frame, text=" Akta Pracownicze ")
        form_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Label(form_frame, text="Przydział (Muzeum):").pack(anchor="w", padx=10, pady=(15, 2))
        self.pracownik_muzeum_combo = ttk.Combobox(form_frame, state="readonly")
        self.pracownik_muzeum_combo.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Imię:").pack(anchor="w", padx=10, pady=(0, 2))
        self.pracownik_imie_entry = ttk.Entry(form_frame)
        self.pracownik_imie_entry.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Nazwisko:").pack(anchor="w", padx=10, pady=(0, 2))
        self.pracownik_nazwisko_entry = ttk.Entry(form_frame)
        self.pracownik_nazwisko_entry.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Lokalizacja (Miejscowość):").pack(anchor="w", padx=10, pady=(0, 2))
        self.pracownik_lokalizacja_entry = ttk.Entry(form_frame)
        self.pracownik_lokalizacja_entry.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Stanowisko / Stopień:").pack(anchor="w", padx=10, pady=(0, 2))
        self.pracownik_stanowisko_entry = ttk.Entry(form_frame)
        self.pracownik_stanowisko_entry.pack(fill="x", padx=10, pady=(0, 15))

        right_frame = ttk.Frame(self.parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        self.pracownicy_map = tkintermapview.TkinterMapView(right_frame, corner_radius=12)
        self.pracownicy_map.pack(fill="both", expand=True)
        self.pracownicy_map.set_position(52.0693, 19.4803)
        self.pracownicy_map.set_zoom(6)

        self.refresh_pracownicy_list()
        self.refresh_pracownicy_map()

    def refresh_pracownicy_list(self, filter_text=""):
        self.pracownicy_listbox.delete(0, tk.END)
        for p in self.app.data["pracownicy"]:
            if filter_text.lower() in p["imie"].lower() or filter_text.lower() in p[
                "nazwisko"].lower() or filter_text.lower() in p["lokalizacja"].lower():
                self.pracownicy_listbox.insert(tk.END, f"[{p['id']}] {p['imie']} {p['nazwisko']} ({p['lokalizacja']})")

    def refresh_pracownicy_map(self, filter_text=""):
        self.pracownicy_map.delete_all_marker()
        for p in self.app.data["pracownicy"]:
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

        pracownik = next((p for p in self.app.data["pracownicy"] if p["id"] == pracownik_id), None)
        if pracownik:
            self.pracownik_imie_entry.delete(0, tk.END)
            self.pracownik_imie_entry.insert(0, pracownik["imie"])

            self.pracownik_nazwisko_entry.delete(0, tk.END)
            self.pracownik_nazwisko_entry.insert(0, pracownik["nazwisko"])

            self.pracownik_lokalizacja_entry.delete(0, tk.END)
            self.pracownik_lokalizacja_entry.insert(0, pracownik["lokalizacja"])

            self.pracownik_stanowisko_entry.delete(0, tk.END)
            self.pracownik_stanowisko_entry.insert(0, pracownik.get("stanowisko", ""))

            muzeum = next((m for m in self.app.data["muzea"] if m["id"] == pracownik["muzeum_id"]), None)
            if muzeum:
                self.pracownik_muzeum_combo.set(f"[{muzeum['id']}] {muzeum['nazwa']}")
            else:
                self.pracownik_muzeum_combo.set("")

            self.pracownicy_map.set_position(pracownik["lat"], pracownik["lon"])
            self.pracownicy_map.set_zoom(12)

    def get_next_pracownik_id(self):
        if not self.app.data["pracownicy"]:
            return 1
        return max(p["id"] for p in self.app.data["pracownicy"]) + 1

    def add_pracownik(self):
        muzeum_str = self.pracownik_muzeum_combo.get()
        imie = self.pracownik_imie_entry.get().strip()
        nazwisko = self.pracownik_nazwisko_entry.get().strip()
        lokalizacja = self.pracownik_lokalizacja_entry.get().strip()
        stanowisko = self.pracownik_stanowisko_entry.get().strip()

        if not muzeum_str or not imie or not nazwisko or not lokalizacja:
            messagebox.showwarning("Braki w formularzu", "Wypełnij wymagane pola i wskaż przydział.")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])
        nowe_id = self.get_next_pracownik_id()
        wspolrzedne = utils.get_coordinates(lokalizacja)

        nowy_pracownik = Pracownik(nowe_id, muzeum_id, imie, nazwisko, lokalizacja, wspolrzedne[0], wspolrzedne[1],
                                   stanowisko)
        self.app.data["pracownicy"].append(nowy_pracownik.to_dict())
        data_manager.save_data(self.app.data)

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
            messagebox.showwarning("Braki w formularzu", "Zaznacz pozycję w rejestrze, którą chcesz zaktualizować.")
            return

        item_text = self.pracownicy_listbox.get(selection[0])
        pracownik_id = int(item_text.split("]")[0][1:])

        muzeum_str = self.pracownik_muzeum_combo.get()
        imie = self.pracownik_imie_entry.get().strip()
        nazwisko = self.pracownik_nazwisko_entry.get().strip()
        lokalizacja = self.pracownik_lokalizacja_entry.get().strip()
        stanowisko = self.pracownik_stanowisko_entry.get().strip()

        if not muzeum_str or not imie or not nazwisko or not lokalizacja:
            messagebox.showwarning("Braki w formularzu", "Wypełnij wymagane pola i wskaż przydział.")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])

        for p in self.app.data["pracownicy"]:
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

        data_manager.save_data(self.app.data)
        self.filter_pracownicy(None)

    def delete_pracownik(self):
        selection = self.pracownicy_listbox.curselection()
        if not selection:
            messagebox.showwarning("Braki w formularzu", "Zaznacz pozycję w rejestrze do usunięcia.")
            return

        item_text = self.pracownicy_listbox.get(selection[0])
        pracownik_id = int(item_text.split("]")[0][1:])

        self.app.data["pracownicy"] = [p for p in self.app.data["pracownicy"] if p["id"] != pracownik_id]
        data_manager.save_data(self.app.data)

        self.filter_pracownicy(None)
        self.pracownik_imie_entry.delete(0, tk.END)
        self.pracownik_nazwisko_entry.delete(0, tk.END)
        self.pracownik_lokalizacja_entry.delete(0, tk.END)
        self.pracownik_stanowisko_entry.delete(0, tk.END)
        self.pracownik_muzeum_combo.set("")