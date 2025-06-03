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
        self.vies = [[0 for _ in range(NB_COLONNES)] for _ in range(NB_LIGNES)]
        self.etape = 0

        self.setup_interface()
        self.afficher_monde()

    def setup_interface(self):
        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Menu
        self.frame_gauche = tk.Frame(self.frame_principal, width=200, bg="#f0f0f0")
        self.frame_gauche.pack(side=tk.LEFT, fill=tk.Y)

        self.label_menu = tk.Label(self.frame_gauche, text="Règles", font=("Arial", 14), bg="#f0f0f0")
        self.label_menu.pack(pady=10)

        self.var_apocalypse = tk.BooleanVar()
        self.var_esperance = tk.BooleanVar()
        self.var_gravite = tk.BooleanVar()
        self.var_attraction = tk.BooleanVar()
        self.var_collision = tk.BooleanVar()

        regles = [
            ("Apocalypse", self.var_apocalypse),
            ("Espérance de vie", self.var_esperance),
            ("Gravité", self.var_gravite),
            ("Attraction", self.var_attraction),
            ("Collision", self.var_collision),
        ]
        for texte, var in regles:
            tk.Checkbutton(self.frame_gauche, text=texte, variable=var, bg="#f0f0f0").pack(anchor=tk.W, padx=10)

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
        self.vies = [[random.randint(5, 8) if self.monde[y][x] else 0 for x in range(NB_COLONNES)] for y in range(NB_LIGNES)]
        self.etape = 0
        self.label_etape.config(text="Étape : 0")
        self.afficher_monde()

    def afficher_monde(self):
        self.canvas.delete("all")
        for y in range(NB_LIGNES):
            for x in range(NB_COLONNES):
                couleur = "black" if self.monde[y][x] else "white"
                self.canvas.create_rectangle(
                    x * TAILLE_CASE, y * TAILLE_CASE,
                    (x + 1) * TAILLE_CASE, (y + 1) * TAILLE_CASE,
                    fill=couleur, outline="gray"
                )

    def on_case_click(self, event):
        col = event.x // TAILLE_CASE
        lig = event.y // TAILLE_CASE
        if 0 <= col < NB_COLONNES and 0 <= lig < NB_LIGNES:
            self.monde[lig][col] = 1 - self.monde[lig][col]
            self.vies[lig][col] = random.randint(5, 8) if self.var_esperance.get() and self.monde[lig][col] else 0
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
                        if self.monde[y][x]:
                            self.vies[y][x] -= 1
                            if self.vies[y][x] <= 0:
                                self.monde[y][x] = 0

            if self.var_gravite.get():
                for y in reversed(range(1, NB_LIGNES)):
                    for x in range(NB_COLONNES):
                        if self.monde[y - 1][x]:
                            if not self.var_collision.get() or self.monde[y][x] == 0:
                                self.monde[y][x] = self.monde[y - 1][x]
                                self.vies[y][x] = self.vies[y - 1][x]
                                self.monde[y - 1][x] = 0
                                self.vies[y - 1][x] = 0

            if self.var_attraction.get():
                new_monde = [row[:] for row in self.monde]
                new_vies = [row[:] for row in self.vies]

                for y in range(NB_LIGNES):
                    for x in range(NB_COLONNES):
                        if self.monde[y][x] == 1:
                            closest = self.find_closest_active(x, y)
                            if closest:
                                dx = closest[0] - x
                                dy = closest[1] - y
                                move_x = x + (1 if dx > 0 else -1 if dx < 0 else 0)
                                move_y = y + (1 if dy > 0 else -1 if dy < 0 else 0)
                                if 0 <= move_x < NB_COLONNES and 0 <= move_y < NB_LIGNES:
                                    if not self.var_collision.get() or self.monde[move_y][move_x] == 0:
                                        new_monde[move_y][move_x] = 1
                                        new_vies[move_y][move_x] = self.vies[y][x]
                                        new_monde[y][x] = 0
                                        new_vies[y][x] = 0
                self.monde = new_monde
                self.vies = new_vies

        self.afficher_monde()

    def find_closest_active(self, x0, y0, rayon=2):
        min_dist = float("inf")
        target = None
        for dy in range(-rayon, rayon + 1):
            for dx in range(-rayon, rayon + 1):
                if dx == 0 and dy == 0:
                    continue
                x = x0 + dx
                y = y0 + dy
                if 0 <= x < NB_COLONNES and 0 <= y < NB_LIGNES and self.monde[y][x] == 1:
                    dist = abs(dx) + abs(dy)
                    if dist < min_dist:
                        min_dist = dist
                        target = (x, y)
        return target

# Lancement
if __name__ == "__main__":
    root = tk.Tk()
    app = Monde2D(root)
    root.mainloop()
