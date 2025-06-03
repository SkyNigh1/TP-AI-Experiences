import tkinter as tk
import random

# Configuration du monde
TAILLE_MONDE = 50  # nombre de cases
TAILLE_CASE = 15   # taille d'une case en pixels

class Monde1D:
    def __init__(self, root):
        self.root = root
        self.root.title("Monde 1D")
        
        # Tableau représentant le monde (0 = blanc, 1 = noir)
        self.monde = [0] * TAILLE_MONDE

        # Canvas pour afficher les cases
        self.canvas = tk.Canvas(root, width=TAILLE_MONDE * TAILLE_CASE, height=TAILLE_CASE)
        self.canvas.pack(pady=10)

        # Bouton Init
        self.bouton = tk.Button(root, text="Init", command=self.init_monde)
        self.bouton.pack()

        # Affichage initial
        self.afficher_monde()

    def init_monde(self):
        # Remplir le tableau avec des 0 ou 1 aléatoires
        self.monde = [random.randint(0, 1) for _ in range(TAILLE_MONDE)]
        self.afficher_monde()

    def afficher_monde(self):
        self.canvas.delete("all")  # Effacer l'ancien affichage
        for i, val in enumerate(self.monde):
            couleur = "black" if val == 1 else "white"
            x0 = i * TAILLE_CASE
            x1 = x0 + TAILLE_CASE
            self.canvas.create_rectangle(x0, 0, x1, TAILLE_CASE, fill=couleur, outline="gray")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = Monde1D(root)
    root.mainloop()
