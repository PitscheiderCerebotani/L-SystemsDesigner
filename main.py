import turtle #Libreria per l'utilizzo della turtle
import json #Libreria per la gestione dei Json
import os #Libreria per la gestione di file
import fnmatch #Libreria simile a Regex per controllare corrispondenze (usata per controllare se i file sono Json)

#Creazione della classe simbolo per l'alfabeto
class Simbolo:
    def __init__(self, avanzamento: int, rotazione: float, inchiostro: bool, regola: str):
        self.avanzamento: int = avanzamento
        self.rotazione: float = rotazione
        self.inchiostro: bool = inchiostro
        self.regola: str = regola


    def esecuzioneSimbolo(self, pen: turtle, moltiplicatoreAvanzamento: float):
        pen.left(self.rotazione)
        pen.forward(self.avanzamento * (moltiplicatoreAvanzamento))
        if (self.inchiostro):
            pen.pendown()
        elif (self.inchiostro == False):
            pen.penup()


#Funzione di rappresentazione con supporto a bracketed OL-Systems
def rappresentazione (sviluppo: str, alfabeto, pen: turtle, moltiplicatoreAvanzamento: float, velocita: int):
        pen.speed(velocita)
        pila = []
        for simbolo in sviluppo:
            if simbolo == "[":
                pila.append({
                    "xCorrente": pen.xcor(),
                    "yCorrente": pen.ycor(),
                    "rotazioneCorrente": pen.heading()
                })
            elif simbolo == "]":
                riferimentiCorrenti = pila.pop()
                pen.setpos(riferimentiCorrenti["xCorrente"], riferimentiCorrenti["yCorrente"])
                pen.setheading(riferimentiCorrenti["rotazioneCorrente"])

            alfabeto[simbolo].esecuzioneSimbolo(pen, moltiplicatoreAvanzamento)


#Funzione di sviluppo della stringa assioma in base alle regole dell'alfabeto
def sviluppoAssioma(alfabeto, assioma: str, iterazioni: int):
    sviluppo = assioma
    for i in range(iterazioni):
        oldSviluppo = sviluppo[:]
        sviluppo = ""
        for simbolo in oldSviluppo:
            sviluppo += alfabeto[simbolo].regola
    while alfabeto[sviluppo[0]].rotazione!=0 and alfabeto[sviluppo[0]].avanzamento==0:
        sviluppo = sviluppo[1:]
    return sviluppo


#Controlli sull'alfabeto
def checkAlfabeto(alfabeto):
    check = True
    for simbolo in alfabeto:
        if len(simbolo)!=1:
            check = False
        if type(alfabeto[simbolo].avanzamento) != int:
            check = False
        if type(alfabeto[simbolo].rotazione) != float and type(alfabeto[simbolo].rotazione) != int:
            check = False
        if type(alfabeto[simbolo].inchiostro) != bool and alfabeto[simbolo].inchiostro != None:
            check = False
        if type(alfabeto[simbolo].regola) != str:
            check = False

    return check


#Controlli sulla validita delle regole (in particolare controlla che per ogni simbolo di una regola esista un simbolo nell'alfabeto)
def checkRegole(alfabeto):
    check = True
    for simbolo in alfabeto:
        for carattere in alfabeto[simbolo].regola:
            if not carattere in alfabeto:
                check = False

    return check

#Controlli sulla validita dell'assioma (in particolare controlla che per ogni simbolo dell'assioma esista un simbolo nell'alfabeto)
def checkAssioma(assioma: str, alfabeto):
    check = True
    for carattere in assioma:
        if not carattere in alfabeto:
            check = False

    return check

#Controlli sui parametri di rappresentazione (in particolare sui tipi)
def checkRappresentazione(moltiplicatoreAvanzamento, velocita, iterazione, angoloIniziale):
    check = True
    if type(moltiplicatoreAvanzamento)!=float and type(moltiplicatoreAvanzamento)!=int:
        check = False
    if type(velocita) != int:
        check = False
    if type(iterazione) != int:
        check = False
    if iterazione<0:
        check = False
    if type(angoloIniziale) != float and type(angoloIniziale) != int:
        check = False

    return check

#funzione che avvia tutti i controlli precedenti
def checkParametri(assioma: str, alfabeto, moltiplicatoreAvanzamento: float, velocita: int, iterazione: int, angoloIniziale: float):
    check = False
    if checkAlfabeto(alfabeto) and checkRegole(alfabeto) and checkAssioma(assioma, alfabeto) and checkRappresentazione(moltiplicatoreAvanzamento, velocita, iterazione, angoloIniziale):
        check = True

    return check



def main():

    #Caricamento dei file nella cartella Modelli e filtraggio su quelli con estensione Json
    directory = os.getcwd() + "/Modelli/"
    elencoFile = os.listdir(directory)
    elencoFileJson = []
    for file in elencoFile:
        if fnmatch.fnmatch(file, '*.json'):
            elencoFileJson += [file]


    if len(elencoFileJson) != 0:

        #Scelta del modello da caricare
        iFile = -1

        print("Inserire il numero associato al file JSON da caricare:")
        for i in range(len(elencoFileJson)):
            print((i+1), "-", elencoFileJson[i])
        iFile = int(input("\nFile da caricare: "))-1

        if (iFile>=0 and iFile<len(elencoFileJson)):
            file = elencoFileJson[iFile]

            with open(directory + file, "r") as file:
                parametri = json.load(file)


            #Mappatura dei dizionari JSON con la classe Simbolo
            alfabeto = { }

            for voce in parametri["alfabeto"]:
                chiave = voce
                valore = Simbolo(
                    parametri["alfabeto"][voce]["avanzamento"],
                    parametri["alfabeto"][voce]["rotazione"],
                    parametri["alfabeto"][voce]["inchiostro"],
                    parametri["alfabeto"][voce]["regola"]
                )
                alfabeto[chiave] = valore

            #Mappatura degli altri parametri
            assioma = parametri["assioma"]
            moltiplicatoreAvanzamento = parametri["moltiplicatoreAvanzamento"]
            velocita = parametri["velocita"]
            iterazione = parametri["iterazione"]
            angoloIniziale = parametri["angoloIniziale"]


            #Controllo dei parametri
            if checkParametri(assioma, alfabeto, moltiplicatoreAvanzamento, velocita, iterazione, angoloIniziale):
                sviluppo = sviluppoAssioma(alfabeto, assioma, iterazione)
                print("Sviluppo:")
                print(sviluppo)

                #Esecuzione della rappresentazione (richiede try e except, altrimenti non funziona)
                try:
                    pen = turtle.Turtle()
                    turtle.tracer(0)
                    pen.hideturtle()
                    pen.left(angoloIniziale)
                    rappresentazione(sviluppo, alfabeto, pen, moltiplicatoreAvanzamento, velocita)
                    turtle.update()
                    turtle.exitonclick()
                    turtle.bye()
                except:
                    pass

            else:
                print("\nParametri non validi!")

        else:
            print("\nIndice selezionato non valido!")
    else:
        print("\nNessun file JSON trovato!")


#Ciclo di ripetizione del programma
uscita = "1"
while uscita!="0":
    main()
    uscita = input("\nDigitare 0 per uscire, o un carattere per continuare: ")