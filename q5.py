import tkinter as tk
import random

# Configuration
NB_LIGNES = 20
NB_COLONNES = 30
TAILLE_CASE = 20

class Monde2D:
    def __init__(self, root):
        self.root = root
        self.root.title("Monde 2D")

        self.monde = [[0 for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
        self.etape = 0  # Compteur d'étapes

        largeur = NB_COLONNES * TAILLE_CASE
        hauteur = NB_LIGNES * TAILLE_CASE
        self.canvas = tk.Canvas(root, width=largeur, height=hauteur)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_case_click)

        self.bouton_init = tk.Button(root, text="Init", command=self.init_monde)
        self.bouton_init.pack()

        # Ligne inférieure : étiquette et bouton "Next"
        bas_frame = tk.Frame(root)
        bas_frame.pack(pady=10)

        self.label_etape = tk.Label(bas_frame, text="Étape : 0")
        self.label_etape.pack(side=tk.LEFT, padx=10)

        self.bouton_next = tk.Button(bas_frame, text="Next", command=self.next_step)
        self.bouton_next.pack(side=tk.LEFT)

        self.afficher_monde()

    def init_monde(self):
        self.monde = [[random.randint(0, 1) for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
        self.etape = 0  # Réinitialise l'étape
        self.label_etape.config(text="Étape : 0")  # Met à jour le label
        self.afficher_monde()

    def afficher_monde(self):
        self.canvas.delete("all")
        for y in range(NB_LIGNES):
            for x in range(NB_COLONNES):
                couleur = "black" if self.monde[y][x] == 1 else "white"
                x0 = x * TAILLE_CASE
                y0 = y * TAILLE_CASE
                x1 = x0 + TAILLE_CASE
                y1 = y0 + TAILLE_CASE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=couleur, outline="gray")

    def on_case_click(self, event):
        col = event.x // TAILLE_CASE
        lig = event.y // TAILLE_CASE
        if 0 <= col < NB_COLONNES and 0 <= lig < NB_LIGNES:
            self.monde[lig][col] = 1 - self.monde[lig][col]
            self.afficher_monde()

    def next_step(self):
        self.etape += 1
        self.label_etape.config(text=f"Étape : {self.etape}")

# Lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = Monde2D(root)
    root.mainloop()
