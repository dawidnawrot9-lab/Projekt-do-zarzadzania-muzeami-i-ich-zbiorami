import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
from Models import data_manager
from Models.models import Magazyn
import utils


class MagazynyTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.build_tab()

    def build_tab(self):
        left_frame = ttk.Frame(self.parent, width=280)
        left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        ttk.Label(left_frame, text="Rejestr Magazynów", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))

        self.magazyny_search_entry = ttk.Entry(left_frame)
        self.magazyny_search_entry.pack(fill="x", pady=5)
        self.magazyny_search_entry.bind("<KeyRelease>", self.filter_magazyny)

        self.magazyny_listbox = self.app.create_custom_listbox(left_frame)
        self.magazyny_listbox.pack(fill="both", expand=True, pady=5)
        self.magazyny_listbox.bind("<<ListboxSelect>>", self.on_magazyn_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Dodaj", command=self.add_magazyn).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(btn_frame, text="Zapisz", command=self.update_magazyn).pack(side="left", expand=True, fill="x",
                                                                               padx=2)
        ttk.Button(btn_frame, text="Usuń", command=self.delete_magazyn).pack(side="left", expand=True, fill="x", padx=2)

        mid_frame = ttk.Frame(self.parent, width=320)
        mid_frame.pack(side="left", fill="y", padx=5, pady=10)
        mid_frame.pack_propagate(False)

        form_frame = ttk.LabelFrame(mid_frame, text=" Karta Magazynu ")
        form_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Label(form_frame, text="Przynależność (Muzeum):").pack(anchor="w", padx=10, pady=(15, 2))
        self.magazyn_muzeum_combo = ttk.Combobox(form_frame, state="readonly")
        self.magazyn_muzeum_combo.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Nazwa obiektu:").pack(anchor="w", padx=10, pady=(0, 2))
        self.magazyn_nazwa_entry = ttk.Entry(form_frame)
        self.magazyn_nazwa_entry.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Lokalizacja (Miejscowość):").pack(anchor="w", padx=10, pady=(0, 2))
        self.magazyn_lokalizacja_entry = ttk.Entry(form_frame)
        self.magazyn_lokalizacja_entry.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Wykaz dzieł/eksponatów:").pack(anchor="w", padx=10, pady=(0, 2))
        self.magazyn_dziela_entry = ttk.Entry(form_frame)
        self.magazyn_dziela_entry.pack(fill="x", padx=10, pady=(0, 15))

        right_frame = ttk.Frame(self.parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        self.magazyny_map = tkintermapview.TkinterMapView(right_frame, corner_radius=12)
        self.magazyny_map.pack(fill="both", expand=True)
        self.magazyny_map.set_position(52.0693, 19.4803)
        self.magazyny_map.set_zoom(6)

        self.refresh_magazyny_list()
        self.refresh_magazyny_map()

    def refresh_magazyny_list(self, filter_text=""):
        self.magazyny_listbox.delete(0, tk.END)
        for mag in self.app.data["magazyny"]:
            if filter_text.lower() in mag["nazwa"].lower() or filter_text.lower() in mag["lokalizacja"].lower():
                self.magazyny_listbox.insert(tk.END, f"[{mag['id']}] {mag['nazwa']} ({mag['lokalizacja']})")

    def refresh_magazyny_map(self, filter_text=""):
        self.magazyny_map.delete_all_marker()
        for mag in self.app.data["magazyny"]:
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

        magazyn = next((mag for mag in self.app.data["magazyny"] if mag["id"] == magazyn_id), None)
        if magazyn:
            self.magazyn_nazwa_entry.delete(0, tk.END)
            self.magazyn_nazwa_entry.insert(0, magazyn["nazwa"])

            self.magazyn_lokalizacja_entry.delete(0, tk.END)
            self.magazyn_lokalizacja_entry.insert(0, magazyn["lokalizacja"])

            self.magazyn_dziela_entry.delete(0, tk.END)
            self.magazyn_dziela_entry.insert(0, magazyn.get("dziela", ""))

            muzeum = next((m for m in self.app.data["muzea"] if m["id"] == magazyn["muzeum_id"]), None)
            if muzeum:
                self.magazyn_muzeum_combo.set(f"[{muzeum['id']}] {muzeum['nazwa']}")
            else:
                self.magazyn_muzeum_combo.set("")

            self.magazyny_map.set_position(magazyn["lat"], magazyn["lon"])
            self.magazyny_map.set_zoom(12)

    def get_next_magazyn_id(self):
        if not self.app.data["magazyny"]:
            return 1
        return max(mag["id"] for mag in self.app.data["magazyny"]) + 1

    def add_magazyn(self):
        muzeum_str = self.magazyn_muzeum_combo.get()
        nazwa = self.magazyn_nazwa_entry.get().strip()
        lokalizacja = self.magazyn_lokalizacja_entry.get().strip()
        dziela = self.magazyn_dziela_entry.get().strip()

        if not muzeum_str or not nazwa or not lokalizacja:
            messagebox.showwarning("Braki w formularzu", "Wypełnij wymagane pola i wskaż przydział.")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])
        nowe_id = self.get_next_magazyn_id()
        wspolrzedne = utils.get_coordinates(lokalizacja)

        nowy_magazyn = Magazyn(nowe_id, muzeum_id, nazwa, lokalizacja, wspolrzedne[0], wspolrzedne[1], dziela)
        self.app.data["magazyny"].append(nowy_magazyn.to_dict())
        data_manager.save_data(self.app.data)

        self.refresh_magazyny_list()
        self.refresh_magazyny_map()

        self.magazyn_nazwa_entry.delete(0, tk.END)
        self.magazyn_lokalizacja_entry.delete(0, tk.END)
        self.magazyn_dziela_entry.delete(0, tk.END)
        self.magazyn_muzeum_combo.set("")

    def update_magazyn(self):
        selection = self.magazyny_listbox.curselection()
        if not selection:
            messagebox.showwarning("Braki w formularzu", "Zaznacz pozycję w rejestrze, którą chcesz zaktualizować.")
            return

        item_text = self.magazyny_listbox.get(selection[0])
        magazyn_id = int(item_text.split("]")[0][1:])

        muzeum_str = self.magazyn_muzeum_combo.get()
        nazwa = self.magazyn_nazwa_entry.get().strip()
        lokalizacja = self.magazyn_lokalizacja_entry.get().strip()
        dziela = self.magazyn_dziela_entry.get().strip()

        if not muzeum_str or not nazwa or not lokalizacja:
            messagebox.showwarning("Braki w formularzu", "Wypełnij wymagane pola i wskaż przydział.")
            return

        muzeum_id = int(muzeum_str.split("]")[0][1:])

        for mag in self.app.data["magazyny"]:
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

        data_manager.save_data(self.app.data)
        self.filter_magazyny(None)

    def delete_magazyn(self):
        selection = self.magazyny_listbox.curselection()
        if not selection:
            messagebox.showwarning("Braki w formularzu", "Zaznacz pozycję w rejestrze do usunięcia.")
            return

        item_text = self.magazyny_listbox.get(selection[0])
        magazyn_id = int(item_text.split("]")[0][1:])

        self.app.data["magazyny"] = [mag for mag in self.app.data["magazyny"] if mag["id"] != magazyn_id]
        data_manager.save_data(self.app.data)

        self.filter_magazyny(None)
        self.magazyn_nazwa_entry.delete(0, tk.END)
        self.magazyn_lokalizacja_entry.delete(0, tk.END)
        self.magazyn_dziela_entry.delete(0, tk.END)
        self.magazyn_muzeum_combo.set("")