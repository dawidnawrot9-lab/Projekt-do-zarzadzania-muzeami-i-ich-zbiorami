import tkinter as tk
from tkinter import ttk, messagebox
import tkintermapview
from Models import data_manager
from Models.models import Muzeum
import utils


class MuzeaTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.build_tab()

    def build_tab(self):
        left_frame = ttk.Frame(self.parent, width=280)
        left_frame.pack(side="left", fill="y", padx=(10, 5), pady=10)

        ttk.Label(left_frame, text="Rejestr Muzeów", font=("Helvetica", 12, "bold"),
                  foreground=self.app.text_color).pack(anchor="w", pady=(0, 5))

        self.muzea_search_entry = ttk.Entry(left_frame)
        self.muzea_search_entry.pack(fill="x", pady=5)
        self.muzea_search_entry.bind("<KeyRelease>", self.filter_muzea)

        self.muzea_listbox = self.app.create_custom_listbox(left_frame)
        self.muzea_listbox.pack(fill="both", expand=True, pady=5)
        self.muzea_listbox.bind("<<ListboxSelect>>", self.on_muzeum_select)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Dodaj", command=self.add_muzeum).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(btn_frame, text="Zapisz", command=self.update_muzeum).pack(side="left", expand=True, fill="x",
                                                                              padx=2)
        ttk.Button(btn_frame, text="Usuń", command=self.delete_muzeum).pack(side="left", expand=True, fill="x", padx=2)

        mid_frame = ttk.Frame(self.parent, width=320)
        mid_frame.pack(side="left", fill="y", padx=5, pady=10)
        mid_frame.pack_propagate(False)

        form_frame = ttk.LabelFrame(mid_frame, text=" Karta Obiektu ")
        form_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Label(form_frame, text="Nazwa placówki:").pack(anchor="w", padx=10, pady=(15, 2))
        self.muzeum_nazwa_entry = ttk.Entry(form_frame)
        self.muzeum_nazwa_entry.pack(fill="x", padx=10, pady=(0, 15))

        ttk.Label(form_frame, text="Lokalizacja (Miejscowość):").pack(anchor="w", padx=10, pady=(0, 2))
        self.muzeum_lokalizacja_entry = ttk.Entry(form_frame)
        self.muzeum_lokalizacja_entry.pack(fill="x", padx=10, pady=(0, 25))

        ttk.Button(form_frame, text="Przeglądaj powiązane zasoby", command=self.show_museum_resources).pack(fill="x",
                                                                                                            padx=10,
                                                                                                            pady=5)

        right_frame = ttk.Frame(self.parent)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

        self.muzea_map = tkintermapview.TkinterMapView(right_frame, corner_radius=12)
        self.muzea_map.pack(fill="both", expand=True)
        self.muzea_map.set_position(52.0693, 19.4803)
        self.muzea_map.set_zoom(6)

        self.refresh_muzea_list()
        self.refresh_muzea_map()

    def refresh_muzea_list(self, filter_text=""):
        self.muzea_listbox.delete(0, tk.END)
        for m in self.app.data["muzea"]:
            if filter_text.lower() in m["nazwa"].lower() or filter_text.lower() in m["lokalizacja"].lower():
                self.muzea_listbox.insert(tk.END, f"[{m['id']}] {m['nazwa']} ({m['lokalizacja']})")

    def refresh_muzea_map(self, filter_text=""):
        self.muzea_map.delete_all_marker()
        for m in self.app.data["muzea"]:
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

        muzeum = next((m for m in self.app.data["muzea"] if m["id"] == muzeum_id), None)
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
            messagebox.showinfo("Brak wyboru", "Zaznacz muzeum na liście, aby wyświetlić przypisane do niego zasoby.")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        muzeum = next((m for m in self.app.data["muzea"] if m["id"] == muzeum_id), None)

        res_window = tk.Toplevel(self.app.root)
        res_window.title(f"Zasoby obiektu: {muzeum['nazwa']}")
        res_window.geometry("850x450")
        res_window.configure(bg=self.app.bg_main)

        mag_frame = ttk.Frame(res_window)
        mag_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        ttk.Label(mag_frame, text="Rejestr Magazynów i Eksponatów", font=("Helvetica", 11, "bold"),
                  foreground=self.app.accent_color).pack(anchor="w", pady=(0, 5))
        mag_listbox = self.app.create_custom_listbox(mag_frame)
        mag_listbox.pack(fill="both", expand=True)

        prac_frame = ttk.Frame(res_window)
        prac_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)
        ttk.Label(prac_frame, text="Wykaz Personelu", font=("Helvetica", 11, "bold"),
                  foreground=self.app.accent_color).pack(anchor="w", pady=(0, 5))
        prac_listbox = self.app.create_custom_listbox(prac_frame)
        prac_listbox.pack(fill="both", expand=True)

        for mag in self.app.data["magazyny"]:
            if mag["muzeum_id"] == muzeum_id:
                dziela = mag.get("dziela", "Brak danych")
                mag_listbox.insert(tk.END, f"{mag['nazwa']} ({mag['lokalizacja']})")
                mag_listbox.insert(tk.END, f"  ↳ Zbiory: {dziela}")
                mag_listbox.insert(tk.END, "")

        for prac in self.app.data["pracownicy"]:
            if prac["muzeum_id"] == muzeum_id:
                stanowisko = prac.get("stanowisko", "Brak stopnia")
                prac_listbox.insert(tk.END, f"{prac['imie']} {prac['nazwisko']} ({prac['lokalizacja']})")
                prac_listbox.insert(tk.END, f"  ↳ Funkcja: {stanowisko}")
                prac_listbox.insert(tk.END, "")

    def get_next_muzeum_id(self):
        if not self.app.data["muzea"]:
            return 1
        return max(m["id"] for m in self.app.data["muzea"]) + 1

    def add_muzeum(self):
        nazwa = self.muzeum_nazwa_entry.get().strip()
        lokalizacja = self.muzeum_lokalizacja_entry.get().strip()

        if not nazwa or not lokalizacja:
            messagebox.showwarning("Braki w formularzu", "Wypełnij wszystkie wymagane pola rejestru.")
            return

        nowe_id = self.get_next_muzeum_id()
        wspolrzedne = utils.get_coordinates(lokalizacja)

        nowe_muzeum = Muzeum(nowe_id, nazwa, lokalizacja, wspolrzedne[0], wspolrzedne[1])
        self.app.data["muzea"].append(nowe_muzeum.to_dict())
        data_manager.save_data(self.app.data)

        self.refresh_muzea_list()
        self.refresh_muzea_map()
        self.app.update_all_views()
        self.muzeum_nazwa_entry.delete(0, tk.END)
        self.muzeum_lokalizacja_entry.delete(0, tk.END)

    def update_muzeum(self):
        selection = self.muzea_listbox.curselection()
        if not selection:
            messagebox.showwarning("Braki w formularzu", "Zaznacz pozycję w rejestrze, którą chcesz zaktualizować.")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        nazwa = self.muzeum_nazwa_entry.get().strip()
        lokalizacja = self.muzeum_lokalizacja_entry.get().strip()

        if not nazwa or not lokalizacja:
            messagebox.showwarning("Braki w formularzu", "Wypełnij wszystkie wymagane pola rejestru.")
            return

        for m in self.app.data["muzea"]:
            if m["id"] == muzeum_id:
                m["nazwa"] = nazwa
                if m["lokalizacja"] != lokalizacja:
                    wspolrzedne = utils.get_coordinates(lokalizacja)
                    m["lokalizacja"] = lokalizacja
                    m["lat"] = wspolrzedne[0]
                    m["lon"] = wspolrzedne[1]
                break

        data_manager.save_data(self.app.data)
        self.filter_muzea(None)
        self.app.update_all_views()

    def delete_muzeum(self):
        selection = self.muzea_listbox.curselection()
        if not selection:
            messagebox.showwarning("Braki w formularzu", "Zaznacz pozycję w rejestrze do usunięcia.")
            return

        item_text = self.muzea_listbox.get(selection[0])
        muzeum_id = int(item_text.split("]")[0][1:])

        self.app.data["muzea"] = [m for m in self.app.data["muzea"] if m["id"] != muzeum_id]
        self.app.data["magazyny"] = [mag for mag in self.app.data["magazyny"] if mag["muzeum_id"] != muzeum_id]
        self.app.data["pracownicy"] = [p for p in self.app.data["pracownicy"] if p["muzeum_id"] != muzeum_id]

        data_manager.save_data(self.app.data)

        self.app.update_all_views()
        self.muzeum_nazwa_entry.delete(0, tk.END)
        self.muzeum_lokalizacja_entry.delete(0, tk.END)