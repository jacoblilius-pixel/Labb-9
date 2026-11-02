from linked9 import LinkedQ

atomer = """ H   He  Li  Be  B   C   N   O   F   Ne  Na  Mg  Al  Si  P   S   Cl  Ar  K   Ca  Sc  Ti  V   Cr
Mn  Fe  Co  Ni  Cu  Zn  Ga  Ge  As  Se  Br  Kr  Rb  Sr  Y   Zr  Nb  Mo  Tc  Ru  Rh  Pd  Ag  Cd
In  Sn  Sb  Te  I   Xe  Cs  Ba  La  Ce  Pr  Nd  Pm  Sm  Eu  Gd  Tb  Dy  Ho  Er  Tm  Yb  Lu  Hf
Ta  W   Re  Os  Ir  Pt  Au  Hg  Tl  Pb  Bi  Po  At  Rn  Fr  Ra  Ac  Th  Pa  U   Np  Pu  Am  Cm
Bk  Cf  Es  Fm  Md  No  Lr  Rf  Db  Sg  Bh  Hs  Mt  Ds  Rg  Cn  Fl  Lv """

atomlista = atomer.split()

class Syntaxfel(Exception):
    pass

def LETTER(ordkö):
    """Kontroll stor bokstav syntax"""
    ordet = ordkö.peek()
    if not ordet.isupper():
        raise Syntaxfel("Saknad stor bokstav vid radslutet")
    if 'A' <= ordet <= 'Z':
        ordkö.dequeue()
    else:
        raise Syntaxfel("Saknad stor bokstav vid radslutet")

def letter(ordkö):
    """Kontroll liten bokstav"""
    ordet = ordkö.peek()
    if 'a' <= ordet <= 'z':
        ordkö.dequeue()
    else:
        raise Syntaxfel("Saknad liten bokstav vid radslutet")

def num(ordkö):
    """Kontroll syntax nummer, lyfter fel om likvärdig med 0 eller 1"""
    ordet = ordkö.dequeue()
    if ordet == "0":
        raise Syntaxfel("För litet tal vid radslutet")
    if ordet == "1":
        if ordkö.isEmpty() or not ordkö.peek().isdigit():
            raise Syntaxfel("För litet tal vid radslutet")
    while not ordkö.isEmpty() and ordkö.peek().isdigit():
        ordkö.dequeue()

def readatom(ordkö):
    """Säkerställer syntax för atom"""
    stor = ordkö.peek()
    LETTER(ordkö)
    atomnamn = stor
    if not ordkö.isEmpty():
        if ordkö.peek().islower():
            liten = ordkö.peek()
            letter(ordkö)
            atomnamn += liten
    if not atomnamn in atomlista:
        raise Syntaxfel("Okänd atom vid radslutet")

def readgroup(ordkö):
    """Syntax för grupp"""
    if ordkö.peek().isalpha():
        readatom(ordkö)
        if not ordkö.isEmpty() and ordkö.peek().isdigit():
            num(ordkö)
    elif ordkö.peek() == '(':
        ordkö.dequeue()
        readmol(ordkö)
        if ordkö.isEmpty() or ordkö.peek() != ')':
            raise Syntaxfel("Saknad högerparentes vid radslutet")
        ordkö.dequeue()
        if not ordkö.isEmpty() and ordkö.peek().isdigit():
            num(ordkö)
        else:
            raise Syntaxfel("Saknad siffra vid radslutet")
    else:
        raise Syntaxfel("Felaktig gruppstart vid radslutet")

def molekyl(mening):
    """Lägger indata i kö och returnerar kön"""
    ordkö = LinkedQ()
    for tecken in mening:
        ordkö.enqueue(tecken)
    return ordkö

def sträng(ordkö):
    """Returnerar rest vid felaktig inmatning"""
    rest = ""
    while not ordkö.isEmpty():
        rest += ordkö.dequeue()
    return rest

def readmol(ordkö):
    """read mol"""
    readgroup(ordkö)
    while not ordkö.isEmpty() and ordkö.peek() != ')':
        readmol(ordkö)

def readformel(ordkö):
    readmol(ordkö)
    if not ordkö.isEmpty():
        raise Syntaxfel("Felaktig gruppstart vid radslutet")

def main():
    while True:
        mening = input()
        ordkö = molekyl(mening)
        if mening == "#":
            break
        try:
            readformel(ordkö)
            print("Formeln är syntaktiskt korrekt")

        except Syntaxfel as fel:
            rest = sträng(ordkö)
            if rest:
                print(str(fel) + " " + rest)
            else:
                print(fel)

if __name__ == "__main__":
    main()
