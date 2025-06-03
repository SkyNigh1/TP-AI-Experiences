import tkinter as tk
import random

# Configuration
NB_LIGNES = 30
NB_COLONNES = 50
TAILLE_CASE = 20

class Monde2D:
    def __init__(self, root):
        self.root = root
        self.root.title("Monde 2D")
        self.root.attributes("-fullscreen", True)

        self.monde = [[0 for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
        self.vies = [[0 for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]  # Pour espérance de vie
        self.etape = 0

        self.setup_interface()
        self.afficher_monde()

    def setup_interface(self):
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Menu à gauche
        self.frame_gauche = tk.Frame(self.frame_principal, width=200, bg="#f0f0f0")
        self.frame_gauche.pack(side=tk.LEFT, fill=tk.Y)

        self.label_menu = tk.Label(self.frame_gauche, text="Règles", font=("Arial", 14), bg="#f0f0f0")
        self.label_menu.pack(pady=10)

        self.var_apocalypse = tk.BooleanVar()
        self.check_apocalypse = tk.Checkbutton(
            self.frame_gauche, text="Apocalypse", variable=self.var_apocalypse, bg="#f0f0f0"
        )
        self.check_apocalypse.pack(anchor=tk.W, padx=10)

        self.var_esperance = tk.BooleanVar()
        self.check_esperance = tk.Checkbutton(
            self.frame_gauche, text="Espérance de vie", variable=self.var_esperance, bg="#f0f0f0"
        )
        self.check_esperance.pack(anchor=tk.W, padx=10)

        self.var_gravite = tk.BooleanVar()
        self.check_gravite = tk.Checkbutton(
            self.frame_gauche, text="Gravité", variable=self.var_gravite, bg="#f0f0f0"
        )
        self.check_gravite.pack(anchor=tk.W, padx=10)

        self.label_etape = tk.Label(self.frame_gauche, text="Étape : 0", bg="#f0f0f0")
        self.label_etape.pack(pady=(30, 10))

        self.bouton_next = tk.Button(self.frame_gauche, text="Next", command=self.next_step)
        self.bouton_next.pack(pady=5)

        self.bouton_init = tk.Button(self.frame_gauche, text="Init", command=self.init_monde)
        self.bouton_init.pack(pady=5)

        self.bouton_quitter = tk.Button(self.frame_gauche, text="Quitter", command=self.root.quit)
        self.bouton_quitter.pack(pady=20)

        # Canevas
        largeur = NB_COLONNES * TAILLE_CASE
        hauteur = NB_LIGNES * TAILLE_CASE
        self.canvas = tk.Canvas(self.frame_principal, width=largeur, height=hauteur)
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_case_click)

    def init_monde(self):
        self.monde = [[random.randint(0, 1) for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
        self.vies = [[random.randint(5, 8) if self.monde[y][x] == 1 else 0 for x in range(NB_COLONNES)] for y in range(NB_LIGNES)]
        self.etape = 0
        self.label_etape.config(text="Étape : 0")
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
            self.vies[lig][col] = random.randint(5, 8) if self.var_esperance.get() and self.monde[lig][col] == 1 else 0
            self.afficher_monde()

    def next_step(self):
        self.etape += 1
        self.label_etape.config(text=f"Étape : {self.etape}")

        if self.var_apocalypse.get():
            self.monde = [[0 for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
            self.vies = [[0 for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
        else:
            if self.var_esperance.get():
                for y in range(NB_LIGNES):
                    for x in range(NB_COLONNES):
                        if self.monde[y][x] == 1:
                            self.vies[y][x] -= 1
                            if self.vies[y][x] <= 0:
                                self.monde[y][x] = 0

            if self.var_gravite.get():
                for y in reversed(range(1, NB_LIGNES)):
                    for x in range(NB_COLONNES):
                        self.monde[y][x] = self.monde[y - 1][x]
                        self.vies[y][x] = self.vies[y - 1][x]
                # Première ligne devient blanche
                for x in range(NB_COLONNES):
                    self.monde[0][x] = 0
                    self.vies[0][x] = 0

        self.afficher_monde()

# Lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = Monde2D(root)
    root.mainloop()
