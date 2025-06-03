import tkinter as tk
import random

# Configuration
TAILLE_MONDE = 50
TAILLE_CASE = 15

class Monde1D:
    def __init__(self, root):
        self.root = root
        self.root.title("Monde 1D")

        self.monde = [0] * TAILLE_MONDE

        self.canvas = tk.Canvas(root, width=TAILLE_MONDE * TAILLE_CASE, height=TAILLE_CASE)
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self.on_case_click)  # Événement clic gauche

        self.bouton = tk.Button(root, text="Init", command=self.init_monde)
        self.bouton.pack()

        self.afficher_monde()

    def init_monde(self):
        self.monde = [random.randint(0, 1) for _ in range(TAILLE_MONDE)]
        self.afficher_monde()

    def afficher_monde(self):
        self.canvas.delete("all")
        for i, val in enumerate(self.monde):
            couleur = "black" if val == 1 else "white"
            x0 = i * TAILLE_CASE
            x1 = x0 + TAILLE_CASE
            self.canvas.create_rectangle(x0, 0, x1, TAILLE_CASE, fill=couleur, outline="gray")

    def on_case_click(self, event):
        index = event.x // TAILLE_CASE
        if 0 <= index < TAILLE_MONDE:
            self.monde[index] = 1 - self.monde[index]  # Inversion
            self.afficher_monde()

# Lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = Monde1D(root)
    root.mainloop()
