from fltk import *
from main import main
import os


cree_fenetre(800, 400)
image(400, 200, 'Rollit.png', ancrage='center', tag='im')


while True:
    ev = donne_ev()
    tev = type_ev(ev)

    if tev == "Quitte":
        ferme_fenetre()
        break

    if tev == "ClicGauche":
        x, y = abscisse(ev), ordonnee(ev)
        
        if 335 <= x <= 465 and 230 <= y <= 286:
            print("générer")
            ferme_fenetre()
            main(True)
            break
            
        if 335 <= x <= 465 and 315 <= y <= 370:
            print("importer")
            ferme_fenetre()
            main(False)  # partie sauvegardée
            break

    mise_a_jour() 