import random

class Jeu:
    def __init__(self, largeur, hauteur, bombes, premier_clic=(0,0)):
        self.largeur = largeur
        self.hauteur = hauteur
        self.nbombes = bombes
        self.grille = self.generer_grille(premier_clic)
        self.cases_devoilees = []

    def generer_grille(self, premier_clic):
        grille=[]
        grille_sans_bombe=[]
        for i in range(self.largeur*self.hauteur):
            grille += [0]
            grille_sans_bombe += [i]

        del grille_sans_bombe[premier_clic[0] + self.largeur * premier_clic[1]]

        for bombe in range(self.nbombes):
            nouvelle_bombe = random.choice(grille_sans_bombe)
            grille_sans_bombe.remove(nouvelle_bombe)
            grille[nouvelle_bombe] = -1

        for case in range(self.largeur*self.hauteur):
            if grille[case] == -1:
                continue
            for i in (-1, 0, 1):
                if ((case + i) // self.largeur) != (case // self.largeur):
                    continue
                for j in (-self.largeur, 0, self.largeur):
                    if ((case + j) // self.largeur) // self.hauteur != 0 or (i, j) == (0, 0):
                        continue
                    if grille[case + i + j] == -1:
                        grille[case] += 1

        return grille

    def devoiler(self, case):
        self.cases_devoilees += [case]
        liste_a_devoiler = []
        if self.grille[case] == 0:
            liste_a_devoiler += self.devoiler_cases_vides(case)
        if self.grille[case] == -1:
            for case in range(self.largeur*self.hauteur):
                if case not in self.cases_devoilees and self.grille[case] == -1:
                    liste_a_devoiler += [case]

        return liste_a_devoiler

    def devoiler_cases_vides(self, case):
        liste_cases = []
        for i in (-1, 0, 1):
            if ((case + i) // self.largeur) != (case // self.largeur):
                continue
            for j in (-self.largeur, 0, self.largeur):
                if ((case + j) // self.largeur) // self.hauteur != 0 or (i, j) == (0, 0):
                    continue
                if (case + i + j) not in self.cases_devoilees:
                    self.cases_devoilees += [case + i + j]
                    liste_cases += [case + i + j]
                    if self.grille[case + i + j] == 0:
                        liste_cases += self.devoiler_cases_vides(case + i + j)

        return liste_cases
