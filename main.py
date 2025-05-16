import os
import ast
from fltk import *
from random import shuffle
import sys


def cree_carte(nb,bool):
    carte = [[None] * nb for _ in range(nb)]
    if bool:
        for i in range(nb):
            for j in range(nb):
                if i == 0 or i == nb-1 or j == 0 or j == nb-1:
                    carte[i][j] = 'SSSS'
    return carte


def cree_dico(chemin):
    dico = {}
    liste_elem = os.listdir(chemin)
    for elem in liste_elem:
        dico[elem[:4]] = chemin + elem
    return dico


def emplacement_valide(grille, i, j, nom_tuile):
    if grille[i][j] is not None:
        return False
    if i > 0 and grille[i-1][j] is not None:
        if grille[i-1][j][2] != nom_tuile[0]:
            return False
    if j < len(grille[0]) - 1 and grille[i][j+1] is not None:
        if grille[i][j+1][3] != nom_tuile[1]:
            return False
    if i < len(grille) - 1 and grille[i+1][j] is not None:
        if grille[i+1][j][0] != nom_tuile[2]:
            return False
    if j > 0 and grille[i][j-1] is not None:
        if grille[i][j-1][1] != nom_tuile[3]:
            return False
    return True


def tuiles_possibles(grille, i, j, dico):
    if grille[i][j] is not None:
        return []
    else:
        tab = []
        for nom in dico:
            if emplacement_valide(grille, i, j, nom):
                tab.append(nom)
    return tab


def quadrillage(nb):
    cord_x_y = hauteur_fenetre() // nb
    for i in range(nb - 1):
        ligne(cord_x_y, 0, cord_x_y, hauteur_fenetre())
        ligne(0, cord_x_y, largeur_fenetre(), cord_x_y)
        cord_x_y += hauteur_fenetre() // nb


def affichage_menu_tuile(nb):
    taille_case = largeur_fenetre() // nb
    decalage = taille_case // 3
    rectangle(taille_case // 2, taille_case // 2, largeur_fenetre() - taille_case // 2, hauteur_fenetre() - taille_case // 2, couleur="black", remplissage="gray", tag="menu_tuile")
    rectangle(taille_case - decalage, taille_case - decalage, (largeur_fenetre() - taille_case) + decalage, (hauteur_fenetre() - taille_case) + decalage, couleur="white", remplissage="white", tag="menu_tuile")


def affichage_tuile(tuiles_possibles, dico, nb, nb_tuiles_par_ligne=12):
    global zones_tuiles_menu
    zones_tuiles_menu = []
    taille_case = largeur_fenetre() // nb
    decalage = taille_case // 3
    x1 = taille_case - decalage
    y1 = taille_case - decalage
    x2 = (largeur_fenetre() - taille_case) + decalage
    y2 = (hauteur_fenetre() - taille_case) + decalage
    largeur_rect = x2 - x1
    hauteur_rect = y2 - y1
    n = nb_tuiles_par_ligne
    espacement = 10
    tuile_w = (largeur_rect - (n + 1) * espacement) // n
    tuile_h = tuile_w
    max_lignes = (hauteur_rect + espacement) // (tuile_h + espacement)
    total_h = max_lignes * tuile_h + (max_lignes + 1) * espacement
    start_y = y1 + (hauteur_rect - total_h) // 2
    if len(tuiles_possibles) == 0:
        texte(largeur_fenetre()//2, hauteur_fenetre()//2, "Aucune tuile disponible. La carte ne peut pas être terminée.", ancrage="center", taille=12, tag="texte")
        attente(1)
        efface("menu_tuile")
        efface("texte")
    for index, tuile in enumerate(tuiles_possibles):
        ligne = index // n
        if ligne >= max_lignes:
            break
        col = index % n
        x = x1 + espacement + col * (tuile_w + espacement)
        y = start_y + ligne * (tuile_h + espacement)
        rectangle(x, y, x + tuile_w, y + tuile_h, couleur="black", tag="menu_tuile")
        image(x + tuile_w // 2, y + tuile_h // 2, dico[tuile], tag="menu_tuile",
              ancrage="center", largeur=taille_case//2, hauteur=taille_case//2)
        zones_tuiles_menu.append((x, y, x + tuile_w, y + tuile_h, tuile))


def choix_tuile(nb, tuiles_possibles, dico):
    affichage_menu_tuile(nb)
    affichage_tuile(tuiles_possibles, dico, nb)
    mise_a_jour()
    while True:
        ev = attend_ev()
        if type_ev(ev) == "ClicGauche":
            x, y = abscisse(ev), ordonnee(ev)
            for x1, y1, x2, y2, nom in zones_tuiles_menu:
                if x1 <= x <= x2 and y1 <= y <= y2:
                    efface("menu_tuile")
                    return nom


def placer_tuiles(grille, i, j, nom_tuile, dico, nb):
    taille_case = largeur_fenetre() // nb
    grille[i][j] = nom_tuile
    x = j * taille_case + taille_case // 2
    y = i * taille_case + taille_case // 2
    # Ajout d'un tag unique basé sur les coordonnées
    image(x, y, dico[nom_tuile], ancrage="center", 
          largeur=taille_case, hauteur=taille_case, 
          tag=f"tuile_{i}_{j}")  # <-- Modification ici
    return grille


def grille_pleine(grille):
    for elt in grille:
        if None in elt:
            return False
    return True


def solveur(grille, dico):
    if grille_pleine(grille):
        return True
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] is None:
                lst_tuiles = tuiles_possibles(grille, i, j, dico)
                shuffle(lst_tuiles)
                for t in lst_tuiles:
                    grille[i][j] = t
                    placer_tuiles(grille, i, j, t, dico, len(grille))
                    mise_a_jour()
                    if solveur(grille, dico):
                        return True
                    grille[i][j] = None
                return False
    return False

def sauvegarde(carte, nb):

    save_folder_path = "sauvegarde"
    os.makedirs(save_folder_path, exist_ok=True)

    save_file_path = os.path.join(save_folder_path, "sauvegarde_partie.txt")

    try:
        with open(save_file_path, 'w', encoding='utf-8') as fichier:
            fichier.write(str(carte) + '\n')
            fichier.write(str(nb) + '\n')
        print(f"Sauvegarde réussie dans {save_file_path}")


    except Exception as e:
        print("Erreur lors de la sauvegarde :", e)



def ouvrir_sauvegarde():
    save_file_path = os.path.join("sauvegarde", "sauvegarde_partie.txt")

    # Vérifie si le fichier existe
    if not os.path.exists(save_file_path):
        print("Aucune sauvegarde trouvée.")
        return None, None

    try:
        with open(save_file_path, 'r', encoding='utf-8') as fichier:
            lignes = fichier.readlines()
            carte_str = lignes[0].strip()
            nb_str = lignes[1].strip()

            carte = ast.literal_eval(carte_str)
            nb = int(nb_str)

            print("Sauvegarde chargée avec succès.")
            return carte, nb

    except Exception as e:
        print("Erreur lors du chargement de la sauvegarde :", e)
        return None, None



def main(bool):
    cree_fenetre(600, 600)
    dico = cree_dico("tuiles/")

    if bool:
        nb = 10
        carte = cree_carte(nb, True)
        
    else:
        carte, nb = ouvrir_sauvegarde()
       
    sys.setrecursionlimit((nb ** 2) * 2)
    
    quadrillage(nb)
    
    for i in range(nb):
        for j in range(nb):
            if carte[i][j] is not None:
                placer_tuiles(carte, i, j, carte[i][j], dico, nb)



    while True:
        ev = donne_ev()
        tev = type_ev(ev)
        if tev == "Quitte":
            ferme_fenetre()
            break
        if tev == "ClicGauche":
            taille_case = largeur_fenetre() // nb
            colonne = abscisse_souris() // taille_case
            ligne = ordonnee_souris() // taille_case
            tuiles_dispo = tuiles_possibles(carte, ligne, colonne, dico)
            affichage_menu_tuile(nb)
            affichage_tuile(tuiles_dispo, dico, nb)
            nom_tuile = choix_tuile(nb, tuiles_dispo, dico)
            carte = placer_tuiles(carte, ligne, colonne, nom_tuile, dico, nb)

        if tev == "ClicDroit":  
            taille_case = largeur_fenetre() // nb
            colonne = abscisse_souris() // taille_case
            ligne = ordonnee_souris() // taille_case
            if 0 <= ligne < nb and 0 <= colonne < nb:
                if carte[ligne][colonne] is not None:
                    # Suppression graphique et logique
                    efface(f"tuile_{ligne}_{colonne}")
                    carte[ligne][colonne] = None

        if tev == "Touche":
            if touche(ev) == "s":
                solveur(carte, dico)
            if touche(ev)== "r":
                ferme_fenetre()
                main(True)
            if touche(ev)=="e":
                sauvegarde(carte,nb)
    
                
                

        mise_a_jour()
