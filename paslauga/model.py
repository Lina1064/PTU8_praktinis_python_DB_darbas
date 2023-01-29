from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

engine = create_engine('sqlite:///data/paslauga.db')
Base = declarative_base()

class Klientas(Base):
    __tablename__ = "klientas"
    id = Column(Integer, primary_key=True)
    vardas = Column(String)
    pavarde = Column(String)
    adresas = Column(String)
    el_pastas = Column(String)
    telefonas = Column(Integer)
    uzsakymai = relationship("Uzsakymas", back_populates="klientas")

    def __init__(self, vardas, pavarde, adresas, el_pastas, telefonas):
        self.vardas = vardas
        self.pavarde = pavarde
        self.adresas = adresas
        self.el_pastas = el_pastas
        self.telefonas = telefonas
    
    def __repr__(self):
        return f'{self.id}: {self.vardas} {self.pavarde}, adresas: {self.adresas}, el. pastas: {self.el_pastas} tefefonas: {self.telefonas}' 

class Uzsakymas(Base):
    __tablename__ = "uzsakymas"
    id = Column(Integer, primary_key=True)
    data = Column(DateTime, default = datetime.utcnow)
    kliento_id = Column(Integer, ForeignKey("klientas.id"))
    statusas = Column(String)
    klientas = relationship("Klientas", back_populates="uzsakymai")
    paslaugos_uzsakymas = relationship("PaslaugosUzsakymas", back_populates="uzsakymas")

    def __init__(self, kliento_id, statusas):
        self.kliento_id = kliento_id
        self.statusas = statusas
    
    def __repr__(self):
        return f'{self.id}, {self.data}, užsakymo statusas: {self.statusas}'

class Paslauga(Base):
    __tablename__ = "paslauga"
    id = Column(Integer, primary_key=True)
    pavadinimas = Column(String)
    kaina = Column(Float)
    paslaugos_uzsakymai = relationship("PaslaugosUzsakymas", back_populates="paslauga")

    def __init__(self, pavadinimas, kaina):
        self.pavadinimas = pavadinimas
        self.kaina = kaina

    def __repr__(self):
        return f'{self.id}, {self.pavadinimas}, {self.kaina}'

class PaslaugosUzsakymas(Base):
    __tablename__ = "paslaugos_uzsakymas"
    id = Column(Integer, primary_key=True)
    bandiniu_kiekis = Column(Integer)
    uzsakymo_id = Column(Integer, ForeignKey("uzsakymas.id"))
    paslaugos_id = Column(Integer, ForeignKey("paslauga.id"))
    uzsakymas = relationship("Uzsakymas", back_populates="paslaugos_uzsakymas")
    paslauga = relationship("Paslauga", back_populates="paslaugos_uzsakymai")

    def __init__(self, bandiniu_kiekis, uzsakymo_id, paslaugos_id):
        self.bandiniu_kiekis = bandiniu_kiekis
        self.uzsakymo_id = uzsakymo_id
        self.paslaugos_id = paslaugos_id
    
    def __repr__(self):
        return f'{self.id}, {self.bandiniu_kiekis}, {self.uzsakymo_id}, {self.paslaugos_id}'


if __name__=="__main__":
    Base.metadata.create_all(engine)