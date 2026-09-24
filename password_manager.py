import secrets
from cryptography.fernet import Fernet
import os
import json


def losowe_haslo(dlugosc: int = 16) -> str:
    import secrets
    znaki = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    haslo = ""
    for i in range (dlugosc):
        haslo += secrets.choice(znaki)
    return haslo

def generuj_klucz() -> bytes:
    return Fernet.generate_key()

def zaszyfruj_haslo(haslo: str, klucz: bytes) -> bytes:
    f = Fernet(klucz)
    return f.encrypt(haslo.encode())

def odszyfrowuj_haslo(zaszyfrowane_haslo: bytes, klucz: bytes) -> str:
    f = Fernet(klucz)
    return f.decrypt(zaszyfrowane_haslo).decode()

def zapisz_klucz_do_pliku(klucz: bytes, nazwa_pliku: str):
    with open(nazwa_pliku, "wb") as f:
        f.write(klucz)

def wczytaj_klucz_z_pliku(nazwa_pliku: str) -> bytes:
    with open(nazwa_pliku, "rb") as f:
        return f.read()

def inicjalizuj_klucz(nazwa_pliku: str = "secret.key") -> bytes:
    if os.path.exists(nazwa_pliku):
        print("Znaleziono istniejący klucz szyfrujący.")
        return wczytaj_klucz_z_pliku(nazwa_pliku)
    
    else:
        print("Nie znaleziono klucza. Generowanie nowego...")
        nowy_klucz = generuj_klucz()
        zapisz_klucz_do_pliku(nowy_klucz, nazwa_pliku)
        return nowy_klucz

def zapisz_baze(dane: dict, nazwa_pliku: str = "baza.json"):
    with open(nazwa_pliku, "w") as f:
        json.dump(dane, f, indent=4)

def wczytaj_baze(nazwa_pliku: str = "baza.json") -> dict:
    if os.path.exists(nazwa_pliku):
        with open(nazwa_pliku, "r") as f:
            return json.load(f)
    else:
        return {}

def main():
    print("Inicjalizacja menedżera haseł...")
    klucz = inicjalizuj_klucz("secret.key")
    baza_hasel = wczytaj_baze("baza.json")
    
    while True:
        print("\n=== MENEDŻER HASEŁ ===")
        print("1. Wygeneruj i zapisz nowe hasło")
        print("2. Odczytaj zapisane hasło")
        print("3. Zakończ program")
        
        wybor = input("Wybierz opcję (1/2/3): ")
        
        if wybor == '1':
            serwis = input("Podaj nazwę serwisu (np. GitHub): ")
            haslo = losowe_haslo(16)
            

            zaszyfrowane_bajty = zaszyfruj_haslo(haslo, klucz)
            baza_hasel[serwis] = zaszyfrowane_bajty.decode("utf-8")
            zapisz_baze(baza_hasel, "baza.json")
            
            print(f"[+] Wygenerowano i bezpiecznie zapisano hasło dla: {serwis}")
            
        elif wybor == '2':
            serwis = input("Podaj nazwę serwisu: ")
            
            if serwis in baza_hasel:

                zaszyfrowany_tekst = baza_hasel[serwis]
                odszyfrowane = odszyfrowuj_haslo(zaszyfrowany_tekst.encode("utf-8"), klucz)
                
                print(f"[!] Twoje hasło do {serwis} to: {odszyfrowane}")
            else:
                print("[-] Brak takiego serwisu w bazie!")
                
        elif wybor == '3':
            print("Zamykanie")
            break 
            
        else:
            print("[-] Nieprawidłowy wybór, spróbuj ponownie.")


if __name__ == "__main__":
    main()