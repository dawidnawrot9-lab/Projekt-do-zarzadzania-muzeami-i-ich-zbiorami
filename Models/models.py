class Muzeum:
    def __init__(self, uid: int, nazwa: str, lokalizacja: str, lat: float, lon: float):
        self.id = uid
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        return {
            "id": self.id,
            "nazwa": self.nazwa,
            "lokalizacja": self.lokalizacja,
            "lat": self.lat,
            "lon": self.lon
        }


class Magazyn:
    def __init__(self, uid: int, muzeum_id: int, nazwa: str, lokalizacja: str, lat: float, lon: float):
        self.id = uid
        self.muzeum_id = muzeum_id
        self.nazwa = nazwa
        self.lokalizacja = lokalizacja
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        return {
            "id": self.id,
            "muzeum_id": self.muzeum_id,
            "nazwa": self.nazwa,
            "lokalizacja": self.lokalizacja,
            "lat": self.lat,
            "lon": self.lon
        }


class Pracownik:
    def __init__(self, uid: int, muzeum_id: int, imie: str, nazwisko: str, lokalizacja: str, lat: float, lon: float):
        self.id = uid
        self.muzeum_id = muzeum_id
        self.imie = imie
        self.nazwisko = nazwisko
        self.lokalizacja = lokalizacja
        self.lat = lat
        self.lon = lon

    def to_dict(self):
        return {
            "id": self.id,
            "muzeum_id": self.muzeum_id,
            "imie": self.imie,
            "nazwisko": self.nazwisko,
            "lokalizacja": self.lokalizacja,
            "lat": self.lat,
            "lon": self.lon
        }