from sqlalchemy.orm import sessionmaker
from model import Klientas, Uzsakymas, Paslauga, PaslaugosUzsakymas, engine


session = sessionmaker(bind=engine)()

def vartotojo_pasirinkimas():
    print("===[ Klientai Paslauga ]===")
    print("1 | įrašyti klientą")
    print("2 | įrašyti paslaugą")
    print("3 | įrašyti užsakymą")
    print("4 | įrašyti paslaugos užsakymą")
    print("5 | perziureti paslaugos užsakymus")
    print("6 | peržiūrėti kliento užsakymus")
    print("7 | keisti kliento duomenis")
    print("8 | peržiurėti visų paslaugų 'užsakytas' užsakymus")
    print("0 | išeiti")
    pasirinkimas = input("Pasirinkite: ")
    return pasirinkimas

def irasyti_klienta():
    vardas = input("Vardas: ")
    pavarde = input("Pavardė: ")
    adresas = input("Adresas: ")
    el_pastas = input("El. paštas: ")
    telefonas = int(input("Telefono numeris: "))
    klientas = Klientas(vardas=vardas, pavarde=pavarde, adresas=adresas, el_pastas=el_pastas, telefonas=telefonas)
    session.add(klientas)
    session.commit()
    print(klientas)

def irasyti_paslauga():
    pavadinimas = input("Paslaugos pavadinimas: ")
    kaina = float(input("Paslaugos kaina: "))
    paslauga = Paslauga(pavadinimas=pavadinimas, kaina=kaina)
    session.add(paslauga)
    session.commit()
    print(paslauga)

def irasyti_uzsakyma():
    perziureti_visus_klientus()
    kliento_ID = int(input("Įveskite kliento ID: "))
    statusas = input("Užsakymo statusas: ")
    uzsakymas = Uzsakymas(kliento_id=kliento_ID, statusas=statusas)
    session.add(uzsakymas)
    session.commit()

def irasyti_paslaugos_užsakyma():
    perziureti_visus_uzsakymus()
    uzsakymo_ID = int(input("Įveskite užsakymo ID: "))
    perziureti_visas_paslaugas()
    paslaugos_ID = int(input("Įveskite paslaugos ID: "))
    bandiniu_kiekis = int(input("Kiek bandinių: "))
    paslaugos_uzsakymas = PaslaugosUzsakymas(bandiniu_kiekis=bandiniu_kiekis, uzsakymo_id=uzsakymo_ID, paslaugos_id=paslaugos_ID)
    session.add(paslaugos_uzsakymas)
    session.commit()

def perziureti_visus_klientus():
    klientai = session.query(Klientas).all()
    for klientas in klientai:
        print(f'{klientas.id} - {klientas.vardas} {klientas.pavarde}, adresas: {klientas.adresas}, el.pastas: {klientas.el_pastas}, telefonas: {klientas.telefonas}')

def perziureti_visus_uzsakymus():
    uzsakymai = session.query(Uzsakymas).all()
    for uzsakymas in uzsakymai:
        print(f'{uzsakymas.id} užsakytas: {uzsakymas.data}, užsakymo statusas: {uzsakymas.statusas}, užsakovas - {uzsakymas.klientas.vardas} {uzsakymas.klientas.pavarde}')

def perziureti_visas_paslaugas():
    paslaugos = session.query(Paslauga).all()
    for paslauga in paslaugos:
        print(f'{paslauga.id} {paslauga.pavadinimas}, paslaugos kaina {paslauga.kaina}')

def kliento_duomenu_redagavimas(klientas, **pakeitimai):
    for field, value in pakeitimai.items():
        if value:
            setattr(klientas, field, value)
    session.commit()
    print(klientas)

def kliento_pakeitimai(klientas):
    print(klientas)
    print("Įveskite vertes arba nieko jei norite palikti senus duomenis")
    pakeitimai = {
        "vardas": input("Vardas: "),
        "pavarde": input("Pavarde: "),
        "adresas": input("Adresas: "),
        "el_pastas": input("El.pastas: "),
        "telefonas": input("Telefonas: "),
    }
    return pakeitimai

def klientas_pagal_id():
    perziureti_visus_klientus()
    try:
        id = int(input("Kliento ID: "))
    except ValueError:
        print("Klaida! ID turi būti skaičius")
    else:
        return session.query(Klientas).get(id)

def perziureti_visu_paslaugu_uzsakytus_uzsakymus():
    paslaugos_uzsakymai = session.query(PaslaugosUzsakymas).all()
    for paslaugos_uzsakymas in paslaugos_uzsakymai:
        if paslaugos_uzsakymas.uzsakymas.statusas == "Užsakytas":
            print(f'{paslaugos_uzsakymas.id} bandinių kiekis: {paslaugos_uzsakymas.bandiniu_kiekis}, užsakyta paslauga: {paslaugos_uzsakymas.paslauga.pavadinimas}, užsakovas - {paslaugos_uzsakymas.uzsakymas.klientas.vardas} {paslaugos_uzsakymas.uzsakymas.klientas.pavarde}')

def perziuteri_kliento_uzsakymus():
    perziureti_visus_klientus()
    try:
        klientas = session.query(Klientas).get(int(input("Įveskite kliento Id: ")))
    except ValueError:
        print("Klaida! Kliento ID turi buti skaičius")
    else:
        if klientas is None:
            print("Neteisingai įvestas kliento ID!")
        else:
            if len(klientas.uzsakymai) > 0:
                for kliento_uzsakymai in klientas.uzsakymai:
                    print(f'{kliento_uzsakymai.id} --- {kliento_uzsakymai.klientas.vardas} {kliento_uzsakymai.klientas.pavarde}, uzsakymo statusas: {kliento_uzsakymai.statusas}, užsakytas: {kliento_uzsakymai.data}')
            else:
                print("Šis asmuo užsakymų neturi") 

def perziureti_paslaugos_uzsakymus():
    perziureti_visas_paslaugas()
    try:
        paslauga = session.query(Paslauga).get(int(input("Įveskite paslaugos Id: ")))
    except ValueError:
        print("Klaida! paslaugos ID turi buti skaičius")
    else:
        if paslauga is None:
            print("Neteisingas paslaugos ID")
        else:
            if len(paslauga.paslaugos_uzsakymai) > 0:
                for paslaugos_uzsakymai in paslauga.paslaugos_uzsakymai:
                    print(f'Bandinių kiekis: {paslaugos_uzsakymai.bandiniu_kiekis} užsisakė: {paslaugos_uzsakymai.uzsakymas.klientas.vardas} {paslaugos_uzsakymai.uzsakymas.klientas.pavarde} ')
            else:
                print("Ši paslauga užsakymų neturi")


while True:
    pasirinkimas = vartotojo_pasirinkimas()
    if pasirinkimas == "0" or pasirinkimas == "":
        break
    elif pasirinkimas == "1":
       irasyti_klienta()
    elif pasirinkimas == "2":
        irasyti_paslauga()
    elif pasirinkimas == "3":
        irasyti_uzsakyma()
    elif pasirinkimas == "4":
        irasyti_paslaugos_užsakyma()
    elif pasirinkimas == "5":
        perziureti_paslaugos_uzsakymus()
    elif pasirinkimas == "6":
        perziuteri_kliento_uzsakymus()
    elif pasirinkimas == "7":
        klientas = klientas_pagal_id()
        kliento_duomenu_redagavimas(klientas, **kliento_pakeitimai(klientas))
    elif pasirinkimas == "8":
        perziureti_visu_paslaugu_uzsakytus_uzsakymus()
    else:
        print(f"Klaida! Blogas pasirinkimas {pasirinkimas}")