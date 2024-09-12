
## NB: Je m'excuse pour les répétitions inutiles. J'essaie de rendre mon code plus clair.
## Bonne lecture


from browser import document, html,window
from components import defineCustomElements, createElement

defineCustomElements("ligne-disque", "/components/LigneDisque/", "TR")

donnees = [
    {"Nom": "Disque1", "Partition": "C:", "Volume": "500", "Libre": "200", "Occupe": "300"},
    {"Nom": "Disque2", "Partition": "D:", "Volume": "1000", "Libre": "600", "Occupe": "400"},
]

def ajouter_ligne(nom, partition, volume, libre, occupe):
    ligne = html.TR(Id="ligne_" + nom)
    ligne <= html.TD(nom)
    ligne <= html.TD(partition)
    ligne <= html.TD(f"{volume} Go")
    ligne <= html.TD(f"{libre} Go")
    ligne <= html.TD(f"{occupe} Go")
    document["lignes"].appendChild(ligne)


def click_creer(ev):
    document["dialogue"].showModal()

def confirmer_ajout(event):
    # Récuperation des valeurs du formulaire
    nom = document["nom_input"].value
    partition = document["partition_input"].value
    volume =int( document["volume_input"].value)
    libre =int( document["libre_input"].value)
    occupe = volume-libre  

    # ajout de ligne dans le tableau
    ajouter_ligne(nom, partition, volume, libre, occupe)

    # Mise à jour des données
    nouveau_disque = {"Nom": nom, "Partition": partition, "Volume": volume, "Libre": libre, "Occupe": occupe}
    donnees.append(nouveau_disque)

    # Mise à jour des options dans les menus déroulants
    for select_id in ["disque_select2", "disque_select3", "disque_select4", "disque_select5"]:
        document[select_id] <= html.OPTION(nom, value=nom)

    
    document["dialogue"].close()

################################################################################
def click_modifier(ev):
    document["dialogue2"].showModal()

def confirmer_modification(event):
    # Récupération des valeurs modifiées
    selected_nom = document["disque_select2"].value  
    new_partition = document["partition_input"].value
    new_volume = int(document["volume_input"].value)
    new_libre = int(document["libre_input"].value)
    new_occupe = new_volume-new_libre

    # Mise à jour de la ligne correspondante dans le tableau
    ligne_id = "ligne_" + selected_nom
    if ligne_id in document:
        ligne = document[ligne_id]
        ligne.clear()
        ligne <= html.TD(selected_nom)
        ligne <= html.TD(new_partition)
        ligne <= html.TD(f"{new_volume} Go")
        ligne <= html.TD(f"{new_libre} Go")
        ligne <= html.TD(f"{new_occupe} Go")

    # Mise à jour des données
    for disque in donnees:
        if disque["Nom"] == selected_nom:
            disque["Partition"] = new_partition
            disque["Volume"] = new_volume
            disque["Libre"] = new_libre
            disque["Occupe"] = new_occupe

    document["dialogue2"].close()

def confirmer_modification_nom(event):
    selected_nom = document["disque_select2"].value  # Le disque à modifier
    nouveau_nom = document["nouveau_nom_input"].value  # Le nouveau nom

    # Mise à jour de la ligne dans le tableau
    ligne_id = "ligne_" + selected_nom
    if ligne_id in document:
        ligne = document[ligne_id]
        ligne.clear()
        ligne <= html.TD(nouveau_nom)
        # Reconstruire le reste de la ligne avec les mêmes valeurs
        disque = next(d for d in donnees if d["Nom"] == selected_nom)
        disque["Nom"] = nouveau_nom
        for cle in ["Partition", "Volume", "Libre", "Occupe"]:
            ligne <= html.TD(f"{disque[cle]} Go" if cle in ["Volume", "Libre", "Occupe"] else disque[cle])

    # Mise à jour des données
    for disque in donnees:
        if disque["Nom"] == selected_nom:
            disque["Nom"] = nouveau_nom

    # Mise à jour des options dans les menus déroulants
    for option in document.select('option'):
        if option.value == selected_nom:
            option.text = nouveau_nom
            option.value = nouveau_nom

    document["dialogue6"].close()

document["confirmer6"].bind("click", confirmer_modification_nom)

################################################################################
def click_modifier_nom(ev):
    document["dialogue6"].showModal()

document["confirmer2"].bind("click", click_modifier_nom)  

def confirmer_modification_nom(event):
    selected_nom = document["disque_select2"].value  # Obtenez le nom du disque sélectionné pour modification
    nouveau_nom = document["newnom"].value  # Récupérez le nouveau nom du champ de saisie

    # Mise à jour de la ligne dans le tableau
    ligne_id = "ligne_" + selected_nom
    if ligne_id in document:
        ligne = document[ligne_id]
        ligne.clear()
        ligne <= html.TD(nouveau_nom)
        # Reconstruire le reste de la ligne avec les mêmes valeurs
        disque = next(d for d in donnees if d["Nom"] == selected_nom)
        disque["Nom"] = nouveau_nom
        for cle in ["Partition", "Volume", "Libre", "Occupe"]:
            ligne <= html.TD(f"{disque[cle]} Go" if cle in ["Volume", "Libre", "Occupe"] else disque[cle])

    # Mise à jour des données et des options dans les menus 
    for disque in donnees:
        if disque["Nom"] == selected_nom:
            disque["Nom"] = nouveau_nom

    for option in document.select('option'):
        if option.value == selected_nom:
            option.text = nouveau_nom
            option.value = nouveau_nom

    document["dialogue6"].close()

document["confirmer6"].bind("click", confirmer_modification_nom)

###########################################################################
def click_supprimer(ev):
    document["dialogue3"].showModal()

def supprimer_disque(event):
    # Récupération du nom du disque sélectionné
    selected_nom = document["disque_select3"].value 

    # Suppression de la ligne correspondante dans le tableau
    ligne_id = "ligne_" + selected_nom
    if ligne_id in document:
        document[ligne_id].remove()

    # Suppression du disque de la liste des données
    global donnees
    donnees = [disque for disque in donnees if disque["Nom"] != selected_nom]

    # Suppression de l'option du disque dans tous les menus déroulants
    for option in document.select('option'):
        if option.value == selected_nom:
            option.remove()

    document["dialogue3"].close()

 ###########################################################################
def click_chiffrer(ev):
    document["dialogue4"].showModal()

def chiffrement_cesar(texte, decalage):
    resultat = ''
    for char in texte:
        if char.isupper(): 
            resultat += chr((ord(char) - ord('A') + decalage) % 26 + ord('A'))
        elif char.islower(): 
            resultat += chr((ord(char) - ord('a') + decalage) % 26 + ord('a'))
        else: 
            resultat += char
    return resultat

def confirmer_chiffrement(event):
    # Récupération du nom du disque sélectionné
    selected_nom = document["disque_select4"].value

    # Trouver le disque correspondant dans les données
    disque = next(d for d in donnees if d["Nom"] == selected_nom)

    # Chiffrement du nom
    nom_chiffre = chiffrement_cesar(disque["Nom"], 3) 

    # Mise à jour de la ligne dans le tableau
    ligne_id = "ligne_" + selected_nom
    if ligne_id in document:
        ligne = document[ligne_id]
        ligne.clear()
        ligne <= html.TD(nom_chiffre)
        # Reconstruire le reste de la ligne avec les mêmes valeurs
        disque["Nom"] = nom_chiffre
        for cle in ["Partition", "Volume", "Libre", "Occupe"]:
            ligne <= html.TD(f"{disque[cle]} Go" if cle in ["Volume", "Libre", "Occupe"] else disque[cle])

    # Mise à jour des données et des options dans les menus 
    for option in document.select('option'):
        if option.value == selected_nom:
            option.text = nom_chiffre
            option.value = nom_chiffre

    document["dialogue4"].close()

document["confirmer4"].bind("click", confirmer_chiffrement)
########################################################################
def click_dechiffrer(v):
    document["dialogue5"].showModal()

def dechiffrement_cesar(texte_chiffre, decalage):
    return chiffrement_cesar(texte_chiffre, -decalage)

def confirmer_dechiffrement(event):
    # Récupération du nom du disque sélectionné
    selected_nom = document["disque_select5"].value

    # Trouver le disque correspondant dans les données
    disque = next(d for d in donnees if d["Nom"] == selected_nom)

    # Déchiffrement du nom
    nom_dechiffre = dechiffrement_cesar(disque["Nom"], 3)  

    # Mise à jour de la ligne dans le tableau
    ligne_id = "ligne_" + disque["Nom"]
    if ligne_id in document:
        ligne = document[ligne_id]
        ligne.clear()
        ligne <= html.TD(nom_dechiffre)
        # Reconstruire le reste de la ligne avec les mêmes valeurs
        for cle in ["Partition", "Volume", "Libre", "Occupe"]:
            ligne <= html.TD(f"{disque[cle]} Go" if cle in ["Volume", "Libre", "Occupe"] else disque[cle])

    # Mise à jour des données
    disque["Nom"] = nom_dechiffre

    # Mise à jour des options dans les menus déroulants
    for option in document.select('option'):
        if option.value == selected_nom:
            option.text = nom_dechiffre
            option.value = nom_dechiffre

    document["dialogue5"].close()

document["confirmer5"].bind("click", confirmer_dechiffrement)   

###########################################################################
def refresh(ev):
    document.location.reload()

def fermer(ev):
    window.close()

###########################################################################

document["creer"].bind("click", click_creer)
document["confirmer"].bind("click", confirmer_ajout)
document["modifier"].bind("click", click_modifier)
document["Supprimer"].bind("click", click_supprimer)
document["confirmer3"].bind("click", supprimer_disque)
document["chiffre"].bind("click", click_chiffrer)
document["dechiffrer"].bind("click", click_dechiffrer)
document["accueil"].bind("click", refresh)
document["quitter"].bind("click", fermer)

###############################################################################
for disque in donnees:
    ajouter_ligne(disque["Nom"], disque["Partition"], disque["Volume"], disque["Libre"], disque["Occupe"])
    for select_id in ["disque_select2", "disque_select3", "disque_select4", "disque_select5"]:
        document[select_id] <= html.OPTION(disque["Nom"], value=disque["Nom"])



######################################################J'avais pas complement fini mon travail.
######################################################J'avais encore beaucoup plus d'idées.
######################################################je continuerai personnellement mon code pour finir mes idées.
################################# FIN #######################################################