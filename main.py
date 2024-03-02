import random

class Fenotyp:
    def __init__(self):
        #lista zapisuje kolejne akcja jakie podejmuje dany gracz
        self.lista = []
        #listaP zapisuje kolejne akcje jakie podejmuje przeciwnik
        self.listaP = []
        #wynik_suma zlicza sume punktow zebranych przez danego gracza
        self.wynik_suma = 0


#akcja to decyzja podjeta przez gracza
# 0 - zdrada
# 1 - wspolpraca

#zawsze wspolpracuje
class Frajer(Fenotyp):
    def taktyka(self):
        akcja = 1
        self.lista.append(akcja)
        return akcja

#zawsze zdradza
class Zdrajca(Fenotyp):
    def taktyka(self):
        akcja = 0
        self.lista.append(akcja)
        return akcja

#losowe decyzje
class Losowy(Fenotyp):
    def taktyka(self):
        akcja = random.randint(0, 1)
        self.lista.append(akcja)
        return akcja

#powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy
class WetZaWet(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i-1]
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy, czasem wybacza (10%)
class Wybaczalski(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i-1]
        else:
            akcja = 1
        r = random.randint(0, 10)
        if akcja == 0 and r == 0:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy, czasem wybacza (20%)
class WybaczalskiBardziej(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i-1]
        else:
            akcja = 1
        r = random.randint(0, 5)
        if akcja == 0 and r == 0:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#powtarza ostatni ruch przeciwnika, zaczyna od wspolpracy, czasem wybacza (5%)
class WybaczalskiMniej(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = self.listaP[i-1]
        else:
            akcja = 1
        r = random.randint(0, 20)
        if akcja == 0 and r == 0:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#jesli ktos go zdradzi, obraza sie na zawsze, zaczyna od wspolpracy
class Obrazalski(Fenotyp):
    def taktyka(self):
        akcja = 1
        if len(self.listaP) > 0:
            for k in range(0, len(self.listaP)):
                if self.listaP[k] == 0:
                    akcja = 0
        self.lista.append(akcja)
        return akcja

#jesli ktos go zdradzi, obraza sie na prawie zawsze (10% ze wybaczy tak o), zaczyna od wspolpracy
class ObrazalskiCoWybacza(Fenotyp):
    def taktyka(self):
        r = random.randint(0,10)
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

#powtarza 2 ostatnie ruchy przeciwnika, ale szybciej wybacza, zaczyna od wspolpracy
class WetZa2Wety(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 1:
            i = len(self.listaP)
            if self.listaP[i-1]==0 and self.listaP[i-2]==0:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#powtarza 3 ostatnie ruchy przeciwnika, ale szybciej wybacza, zaczyna od wspolpracy
class WetZa3Wety(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 2:
            i = len(self.listaP)
            if self.listaP[i-1]==0 and self.listaP[i-2]==0 and self.listaP[i-3]==0:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#powtarza 2 ostatnie ruchy przeciwnika, wybacza gdy przeciwnik 2 razy bedzie wspolpracowal, zaczyna od wspolpracy
class WetZa2Wety2(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 2:
            i = len(self.listaP)
            if (self.listaP[i-1] + self.listaP[i-2] + self.listaP[i-3])<=1:
                akcja = 0
            else:
                akcja = 1
        else:
            akcja = 1
        self.lista.append(akcja)
        return akcja

#wspolpracuje jesli przeciwnik wpolpracuje przynajmniej w 50% pzrzypadkow
class Podejrzany(Fenotyp):
    def taktyka(self):
        akcja = 1
        if len(self.listaP) > 0:
            suma = 0
            for k in range(0, len(self.listaP)):
                suma += self.listaP[k]
            if suma < len(self.listaP)/2:
                akcja = 0
        self.lista.append(akcja)
        return akcja

#daje ruch przeciwny do tego ktory dal przeciwnik. Zaczyna od zdrady
class Fajtlapa(Fenotyp):
    def taktyka(self):
        if len(self.listaP) > 0:
            i = len(self.listaP)
            akcja = 1-self.listaP[i - 1]
        else:
            akcja = 0
        self.lista.append(akcja)
        return akcja

#zaczyna od wspolpracy, jesli ktos 3 razy wspolpracuje to zdradza, jesli kto 2 razy niewspolpracuje tez zdradza
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

#zdradza 2 na 3 razy
class Chytrus(Fenotyp):
    def taktyka(self):
        r = random.randint(0,3)
        if r == 0:
            self.lista = []
            self.listaP = []
            akcja = 1
        else:
            akcja = 0
        return akcja

#funkcja pojedynku
def pojedynek(A, B, pomylka=1):
    a = A.taktyka()
    b = B.taktyka()
    A.listaP.append(b)
    B.listaP.append(a)

    #ta instrukcja warunkowa odpowiada za to, ze czasem dobre intencje beda zle odbierane przez przeciwnika
    #szansa na takie zle odebranie wynosi 1/pomylka
    if random.randint(0,pomylka)==0 and pomylka != 1:
        if random.randint(0,2)==0:
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

# populacja = [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16]

#for i in range(0,100):
#    pojedynek(g7, g15, 1)

#print(g7.lista)
#print(g15.lista)
#print("Wynik A: ", g7.wynik_suma)
#print("Wynik B: ", g15.wynik_suma)

fenotypy=[WetZaWet, WetZa2Wety, Wybaczalski, Zdrajca, Obrazalski, ObrazalskiCoWybacza, Losowy, Frajer, WetZa3Wety, WetZa2Wety2,
          WybaczalskiMniej, WybaczalskiBardziej, Podejrzany, Fajtlapa, Kocur, Chytrus]

liczba_pokolen = 30
for i in range(0,liczba_pokolen):
    pop = []
    lista_nazw = []
    lista_wynikow = []

    print("\n Pokolenie nr.", i+1)

    for i in range(0, 30):
        losowa_klasa = random.choice(fenotypy)  # Losowanie klasy
        nazwa = f"{losowa_klasa.__name__}_{i + 1}"  # Losowa nazwa obiektu
        nowy_obiekt = losowa_klasa()  # Tworzenie obiektu danej losowej klasy
        pop.append(nowy_obiekt)  # Dodawanie obiektu do listy
        lista_nazw.append((nazwa))

    for i in range(1, len(pop)):
        j = 0
        while j < i:
            for k in range(0, 200):
                pojedynek(pop[i], pop[j], 20)
            # print(pop[i].lista)
            # print(pop[j].lista)
            # print("Wynik ", {pop[i]},": ", pop[i].wynik_suma)
            # print("Wynik ", {pop[j]}, ": ", pop[j].wynik_suma, "\n")
            pop[i].lista = []
            pop[j].lista = []
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
    for i in range(0,5):
        fenotypy.append(pop[1].__class__)
        fenotypy.append(pop[2].__class__)
        fenotypy.append(pop[3].__class__)
    for i in range(0,3):
        fenotypy.append(pop[4].__class__)
        fenotypy.append(pop[5].__class__)
        fenotypy.append(pop[6].__class__)
        fenotypy.append(pop[7].__class__)
        fenotypy.append(pop[8].__class__)
    for i in range(0,1):
        fenotypy.append(pop[9].__class__)
        fenotypy.append(pop[10].__class__)
        fenotypy.append(pop[11].__class__)
        fenotypy.append(pop[12].__class__)
        fenotypy.append(pop[13].__class__)
        fenotypy.append(pop[14].__class__)
        fenotypy.append(pop[15].__class__)