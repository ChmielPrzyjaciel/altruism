import random
import math
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os


class Fenotyp:
    def __init__(self):
        # lista zapisuje kolejne akcja jakie podejmuje dany gracz
        self.lista = []
        # listaP zapisuje kolejne akcje jakie podejmuje przeciwnik
        self.listaP = []
        # wynik_suma zlicza sume punktow zebranych przez danego gracza
        self.wynik_suma = 0


# akcja to decyzja podjeta przez gracza
# 0 - zdrada
# 1 - wspolpraca

# zawsze wspolpracuje
class Frajer(Fenotyp):
    def taktyka(self):
        akcja = 1
        self.lista.append(akcja)
        return akcja


# zawsze zdradza
class Zdrajca(Fenotyp):
    def taktyka(self):
        akcja = 0
        self.lista.append(akcja)
        return akcja


# losowe decyzje
class Losowy(Fenotyp):
    def taktyka(self):
        akcja = random.randint(0, 1)
        self.lista.append(akcja)
        return akcja


# powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy
class WetZaWet(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i - 1]
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy, czasem wybacza (10%)
class Wybaczalski(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i - 1]
        else:
            akcja = 1
        r = random.randint(0, 10)
        if akcja == 0 and r == 0:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy, czasem wybacza (20%)
class WybaczalskiBardziej(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i - 1]
        else:
            akcja = 1
        r = random.randint(0, 5)
        if akcja == 0 and r == 0:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy, czasem wybacza (5%)
class WybaczalskiMniej(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i - 1]
        else:
            akcja = 1
        r = random.randint(0, 20)
        if akcja == 0 and r == 0:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# jesli ktos go zdradzi, obraza sie na zawsze, zaczyna od wspolpracy
class Obrazalski(Fenotyp):
    def taktyka(self):
        akcja = 1
        if len(self.listaP) > 0:
            for k in range(0, len(self.listaP)):
                if self.listaP[k] == 0:
                    akcja = 0
        self.lista.append(akcja)
        return akcja


# jesli ktos go zdradzi, obraza sie na prawie zawsze (10% ze wybaczy tak o), zaczyna od wspolpracy
class ObrazalskiCoWybacza(Fenotyp):
    def taktyka(self):
        r = random.randint(0, 10)
        if r == 0:
            self.lista = []
            self.listaP = []
        akcja = 1
        if len(self.listaP) > 0:
            for k in range(0, len(self.listaP)):
                if self.listaP[k] == 0:
                    akcja = 0
        self.lista.append(akcja)
        return akcja


# powtarza 2 ostatnie ruchy przeciwnika, ale szybciej wybacza, zaczyna od wspolpracy
class WetZa2Wety(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 1:
            i = len(self.listaP)
            if self.listaP[i - 1] == 0 and self.listaP[i - 2] == 0:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# powtarza 3 ostatnie ruchy przeciwnika, ale szybciej wybacza, zaczyna od wspolpracy
class WetZa3Wety(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 2:
            i = len(self.listaP)
            if self.listaP[i - 1] == 0 and self.listaP[i - 2] == 0 and self.listaP[i - 3] == 0:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# powtarza 2 ostatnie ruchy przeciwnika, wybacza gdy przeciwnik 2 razy bedzie wspolpracowal, zaczyna od wspolpracy
class WetZa2Wety2(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 2:
            i = len(self.listaP)
            if (self.listaP[i - 1] + self.listaP[i - 2] + self.listaP[i - 3]) <= 1:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# wspolpracuje jesli przeciwnik wpolpracuje przynajmniej w 50% pzrzypadkow
class Podejrzany(Fenotyp):
    def taktyka(self):
        akcja = 1
        if len(self.listaP) > 0:
            suma = 0
            for k in range(0, len(self.listaP)):
                suma += self.listaP[k]
            if suma < len(self.listaP) / 2:
                akcja = 0
        self.lista.append(akcja)
        return akcja


# daje ruch przeciwny do tego ktory dal przeciwnik. Zaczyna od zdrady
class Fajtlapa(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = 1 - self.listaP[i - 1]
        else:
            akcja = 0
        self.lista.append(akcja)
        return akcja


# zaczyna od wspolpracy, jesli ktos 3 razy wspolpracuje to zdradza, jesli kto 2 razy niewspolpracuje tez zdradza
class Kocur(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 2:
            i = len(self.listaP)
            if self.listaP[i - 1] == 0 and self.listaP[i - 2] == 0:
                akcja = 0
            elif self.listaP[i - 1] == 1 and self.listaP[i - 2] == 1 and self.listaP[i - 3] == 1:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja


# zdradza 2 na 3 razy
class Chytrus(Fenotyp):
    def taktyka(self):
        r = random.randint(0, 3)
        if r == 0:
            akcja = 1
        else:
            akcja = 0
        return akcja


# wspolpracuje w 60% przypadkow. Ma przechytrzyc podejrzanego!
class Wojownik(Fenotyp):
    def taktyka(selfself):
        r = random.randint(0,100)
        if r >= 40:
            akcja = 1
        else:
            akcja = 0
        return akcja


# funkcja pojedynku
def pojedynek(A, B, pomylka=1):
    a = A.taktyka()
    b = B.taktyka()
    A.listaP.append(b)
    B.listaP.append(a)

    # ta instrukcja warunkowa odpowiada za to, ze czasem dobre intencje beda zle odbierane przez przeciwnika
    # szansa na takie zle odebranie wynosi 1/pomylka
    if random.randint(0, pomylka) == 0 and pomylka != 1:
        if random.randint(0, 2) == 0:
            if len(A.listaP) > 0:
                A.listaP.pop()
            A.listaP.append(0)
        else:
            if len(B.listaP) > 0:
                B.listaP.pop()
            B.listaP.append(0)

    if a == 0 and b == 0:
        A.wynik_suma += 1
        B.wynik_suma += 1
    elif a == 0 and b == 1:
        A.wynik_suma += 5
    elif a == 1 and b == 0:
        B.wynik_suma += 5
    else:
        A.wynik_suma += 3
        B.wynik_suma += 3

# funkcja zliczajaca liczbe osobnikow o danym fenotypie w danym pokoleniu
def zliczanie(lista, Fenotyp):
    licznik = 0
    for i in range(0, len(pop)):
        if isinstance(pop[i], Fenotyp):
            licznik += 1
    lista.append(licznik)


g1 = WetZaWet()
g2 = WetZa2Wety()
g3 = Wybaczalski()
g4 = Zdrajca()
g5 = Obrazalski()
g6 = ObrazalskiCoWybacza()
g7 = Losowy()
g8 = Frajer()
g9 = WetZa3Wety()
g10 = WetZa2Wety2()
g11 = WybaczalskiMniej()
g12 = WybaczalskiBardziej()
g13 = Podejrzany()
g14 = Fajtlapa()
g15 = Kocur()
g16 = Chytrus()
g17 = Wojownik()

# populacja = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17]

# for i in range(0,100):
#    pojedynek(g7, g15, 1)

# print(g7.lista)
# print(g15.lista)
# print("Wynik A: ", g7.wynik_suma)
# print("Wynik B: ", g15.wynik_suma)

fenotypy = [WetZaWet, WetZa2Wety, Wybaczalski, Zdrajca, Obrazalski, ObrazalskiCoWybacza, Losowy, Frajer, WetZa3Wety,
            WetZa2Wety2, WybaczalskiMniej, WybaczalskiBardziej, Podejrzany, Fajtlapa, Kocur, Chytrus, Wojownik]

fenotypy_niezmienione = [WetZaWet, WetZa2Wety, Wybaczalski, Zdrajca, Obrazalski, ObrazalskiCoWybacza, Losowy, Frajer, WetZa3Wety,
            WetZa2Wety2, WybaczalskiMniej, WybaczalskiBardziej, Podejrzany, Fajtlapa, Kocur, Chytrus, Wojownik]

# listy zliczajace obiekty danej klasy w danym pokoleniu
fenotypy_listy = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

liczba_pokolen = 30
liczba_osobnikow = 30  # P0
pojemnosc_srodowiska = 60  # K
szybkosc_wzrostu = 0.21  # B
pomylka = 20

# funkcja ktora wypluwa liczbe osob w populacji
def wielkosc_populcji(P0, K, B, t):
    P = round(K/(1+(K/P0-1)*(math.e)**(-B*t)))
    return P

# parametr czasu, pokazuje ktore mamy pokolenie w funkcji wielkosci populacji (pewnie mozna to uproscic do zmiennej i z pierwszej petli for)
t = 0

# lista x przyjmuje nr kolejnych pokolen. Lista y przyjmuje kolejne wartosci liczby populacji
x=[]
y=[]

for i in range(0, liczba_pokolen):
    pop = []
    lista_nazw = []
    lista_wynikow = []

    print("\n Pokolenie nr.", i, ". Liczba osobnikow: ", wielkosc_populcji(liczba_osobnikow, pojemnosc_srodowiska, szybkosc_wzrostu, t))

    x.append(t)
    y.append(wielkosc_populcji(liczba_osobnikow, pojemnosc_srodowiska, szybkosc_wzrostu, t))

    for i in range(0, wielkosc_populcji(liczba_osobnikow, pojemnosc_srodowiska, szybkosc_wzrostu, t)):
        losowa_klasa = random.choice(fenotypy)  # Losowanie klasy
        nazwa = f"{losowa_klasa.__name__}_{i + 1}"  # Losowa nazwa obiektu
        nowy_obiekt = losowa_klasa()  # Tworzenie obiektu danej losowej klasy
        pop.append(nowy_obiekt)  # Dodawanie obiektu do listy
        lista_nazw.append(nazwa)

    t += 1

    for i in range(1, len(pop)):
        j = 0
        while j < i:
            for k in range(0, 200):
                pojedynek(pop[i], pop[j], pomylka)
            # print(pop[i].lista)
            # print(pop[j].lista)
            # print("Wynik ", {pop[i]},": ", pop[i].wynik_suma)
            # print("Wynik ", {pop[j]}, ": ", pop[j].wynik_suma, "\n")
            pop[i].lista = []
            pop[j].lista = []
            pop[i].listaP = []
            pop[j].listaP = []
            j += 1

    for i in range(0, len(pop)):
        # print("Wynik ", lista_nazw[i], ": ", pop[i].wynik_suma)
        lista_wynikow.append(pop[i].wynik_suma)

    # Sortowanie trzech list na podstawie wartości w pierwszej liście
    posortowane = sorted(zip(lista_wynikow, lista_nazw, pop), reverse=True)

    # Rozdzielanie posortowanych wartości na trzy listy
    lista_wynikow, lista_nazw, pop = zip(*posortowane)

    for i in range(0, len(pop)):
        print("Wynik ", lista_nazw[i], ": ", lista_wynikow[i])

    # Prowizoryczne rozprzestrzenianie sie zwycieskiego genotypu
    for i in range(0, 2):
        fenotypy.append(pop[0].__class__)
        fenotypy.append(pop[1].__class__)
        fenotypy.append(pop[2].__class__)
        fenotypy.append(pop[3].__class__)
        fenotypy.append(pop[4].__class__)
    for i in range(0, 2):
        fenotypy.append(pop[5].__class__)
        fenotypy.append(pop[6].__class__)
        fenotypy.append(pop[7].__class__)
        fenotypy.append(pop[8].__class__)
        fenotypy.append(pop[9].__class__)
    for i in range(0, 1):
        fenotypy.append(pop[10].__class__)
        fenotypy.append(pop[11].__class__)
        fenotypy.append(pop[12].__class__)
        fenotypy.append(pop[13].__class__)
        fenotypy.append(pop[14].__class__)
        fenotypy.append(pop[15].__class__)
        fenotypy.append(pop[16].__class__)
        fenotypy.append(pop[17].__class__)

    for i in range(0, len(fenotypy_listy)):
        zliczanie(fenotypy_listy[i], fenotypy[i])

# rysowanie wykresu
plt.figure(figsize=(11.5, 6)) # dopasowanie wielkosci okna
plt.plot(x, y, label="Populacja")
for i in range(0, len(fenotypy_listy)):
    plt.plot(x, fenotypy_listy[i], label=f'{fenotypy[i].__name__}')
    plt.legend(fenotypy)

plt.xlabel('Pokolenie')
plt.ylabel('Liczba osobnikow')
plt.title('Zmiana liczby populacji')

# dopasowanie wielkosci ramki tak zeby miescila sie tez legenda
plt.subplots_adjust(left=0.1, right=0.75)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# tworzenie folderu do zapisu wykresu i jego zapis
subfolder_name = "wykresy"

if not os.path.exists(subfolder_name): # Sprawdzenie, czy podfolder istnieje, i utworzenie go, jeśli nie istnieje
    os.makedirs(subfolder_name)

subfolder_path = os.path.join(os.getcwd(), subfolder_name)
nr_pliku = random.randint(0,1000000)
wykres_name = f"wykres_{nr_pliku}.png" # Zapisywanie pliku z odpowiednią nazwą
wykres_path = os.path.join(subfolder_path, wykres_name) # Pełna ścieżka do pliku wykresu w podfolderze

plt.savefig(wykres_path)


folder_wyniki = "wyniki"

if not os.path.exists(folder_wyniki):
    os.makedirs(folder_wyniki)

pdf_name = f"wyniki_{nr_pliku}.pdf"
pdf_path = os.path.join(folder_wyniki, pdf_name)

# Tworzenie pliku PDF
c = canvas.Canvas(pdf_path, pagesize=A4)
c.setFillColor(colors.black)
c.setFont("Helvetica", 20)
c.drawString(50, 805, "Wyniki")

c.setFillColor(colors.black)
c.setFont("Helvetica", 10)
c.drawString(50, 780, "Fenotypy:")
c.setFont("Helvetica", 7)
c.drawString(50, 760, "WetZaWet - zaczyna od wspolpracy, nastepnie powtarza ostatni ruch przeciwnika")
c.drawString(50, 750, "Wetza2Wety - jak WetZaWet, ale zdradza po 2 zdradach")
c.drawString(50, 740, "Wybaczalski - jak WetZaWet, ale w 1 na 10 przypadkow wybacza")
c.drawString(50, 730, "Zdrajca - zawsze zdradza")
c.drawString(50, 720, "Obrazalski - zaczyna od wspolpracy, jesli ktos go zdradzi obraza sie na zawsze")
c.drawString(50, 710, "ObrazalskiCowybacza - jak obrazalski, ale czasem wybacza")
c.drawString(50, 700, "Losowy - jego decyzje sa losowe")
c.drawString(50, 690, "Frajer - zawsze wspolpracuje")
c.drawString(50, 680, "WetZa3Wety - jak WetZaWet, ale zdradza po 3 zdradach")
c.drawString(50, 670, "WetZa3Wety2 - jak WetZaWet3, ale zaczyna wspolpracowac kiedy przeciwnik 2 razy bedzie wspolpracowal")
c.drawString(50, 660, "Wybaczalski Mniej - jak WetZaWet, ale w 1 na 20 przypadkow wybacza")
c.drawString(50, 650, "Wybaczalski Bardziej - jak WetZaWet, ale w 1 na 5 przypadkow wybacza")
c.drawString(50, 640, "Wybaczalski Mniej - jak WetZaWet, ale w 1 na 20 przypadkow wybacza")
c.drawString(50, 630, "Wybaczalski Bardziej - jak WetZaWet, ale w 1 na 5 przypadkow wybacza")
c.drawString(50, 620, "Podejrzany - wspolpracuje jesli przeciwnik wpolpracuje przynajmniej w 50% pzrzypadkow")
c.drawString(50, 610, "Fajtlapa - zaczyna od zrady, daje ruch przeciwny do ostatniego ruchu przeciwnika")
c.drawString(50, 600, "Kocur - zaczyna od wspolpracy, jesli ktos 3 razy wspolpracuje lub 2 razy niewspolpracuje to zdradza")
c.drawString(50, 590, "Chytrus - zdradza 2 na 3 razy")
c.drawString(50, 580, "Wojownik - wspolpracuje w 60% przypadkow")
c.setFont("Helvetica", 9)
c.drawString(50, 560, f"Poczatkowa liczba osobnikow: {liczba_osobnikow}")
c.drawString(50, 542, f"Pojemnosc srodowiska: {pojemnosc_srodowiska}")
c.drawString(50, 524, f"Liczba pokolen: {liczba_pokolen}")
c.drawString(50, 506, f"Szybkosc wzrostu populacji: {szybkosc_wzrostu}")
c.drawString(50, 488, f"Szansa na pomylke: {round(100/pomylka)} %")

c.drawImage(wykres_path, 10, 150, width=585, height=350)

wyniki_koncowe = []

for i in range (0, len(fenotypy_niezmienione)):
    a = fenotypy_listy[i]
    wyniki_koncowe.append(a[liczba_pokolen-1])

# Sortowanie trzech list na podstawie wartości w pierwszej liście
posortowane_2 = sorted(zip(wyniki_koncowe, fenotypy_niezmienione), reverse=True, key=lambda x: x[0])

# Rozdzielanie posortowanych wartości na trzy listy
wyniki_koncowe, fenotypy_niezmienione = zip(*posortowane_2)

for i in range(0,5):
    c.drawString(50, 120-i*15, f"{i+1}. {fenotypy_niezmienione[i].__name__}: {wyniki_koncowe[i]} osobnikow.")

c.save()

plt.show()