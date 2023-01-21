import pyxel
import random
#
#
#
#Bienvenue sur Unduck Pressure, un jeu original par le groupe CPT .
#
# Vous êtes un sous-marin, chargé d’une cargaison de canards. Vous devez survivre dans un environnempent sous-marin. Pour cela, vous vous servirez des canards pour atteindre vos advesaires et les éliminer.
#
# A chaque adversaire éliminé, vous gagnez des points.
#
# Si vous entrez en collision avec un de vos adversaires, vous perdez une vie. Vous disposez de 3 vies.
#
# Bonne chance !
#
#
#Controles:
# Z = Haut
# Q = Gauche
# S = Bas
# D = Droite
# Espace = Tirer
#
#
#
#
#
#self.x et .y sont les coordonnées du sous-marin
#
class Jeu():
    def __init__(self):
        pyxel.init(128, 128, title="Un jeu trop bien", quit_key=pyxel.KEY_M)
        pyxel.load("2.pyxres")
        pyxel.playm(0, 0, True)
        self.x = 32
        self.y = 32
        self.speed = 1
        self.tir_liste = []
        self.mechant_liste = []
        self.pv = 3
        self.point = 0
        self.shooting_delay = 15
        self.spawn_rate = 30
        self.speed_mechant = 0.5
        self.boss_liste = []
        self.boss_point_spawn = 0
        self.status = 0
        #status :
        #0 = Menu start
        #1 = Jeu
        #2 = Mort
        pyxel.run(self.update, self.draw)
    def run(self):
        pyxel.run(self.update, self.draw)
#commande de mouvements
    def mouvements(self):
        if pyxel.btn(pyxel.KEY_D):
            self.x += self.speed
        if pyxel.btn(pyxel.KEY_Q):
            self.x -= self.speed
        if pyxel.btn(pyxel.KEY_Z):
            self.y -= self.speed
        if pyxel.btn(pyxel.KEY_S):
            self.y += self.speed

    def move_check(self):
        if self.x > (128 - 16):
            self.x = (128 - 16)
        if self.x < 0:
            self.x = 0
        if self.y > (128 - 10 - 16):
            self.y = (128 - 10 - 16)
        if self.y < 8:
            self.y = 8

#definition des tirs
    def tir(self):
        if pyxel.btnp(pyxel.KEY_SPACE, 0, 15):
            self.tir_liste.append([self.x, self.y])
            self.shooting_delay = 15
        for tir in self.tir_liste:
            tir[0] += 2

#creation, explosion des méchants
    def spawn_mechant(self):
        if pyxel.frame_count%self.spawn_rate == 0:
            self.mechant_liste.append([134, random.randint(20, 100)])
        for mechant in self.mechant_liste:
            mechant[0] -= self.speed_mechant
    def explosion_mechant(self):
        for mechant in self.mechant_liste:
            if mechant[1] <= self.y+6 and mechant[1]+6 >= self.y and mechant[0] <= self.x + 16 and mechant[0] + 7 >= self.x:
                self.pv -= 1
                self.mechant_liste.remove(mechant)
    def tri_mechants(self):
        for tir in self.tir_liste:
            for mechant in self.mechant_liste:
                if mechant[1] <= tir[1]+7 and mechant[1]+7 >= tir[1] and mechant[0] <= tir[0] + 7 and mechant[0] + 7 >= tir[0]:
                    self.mechant_liste.remove(mechant)
                    self.tir_liste.remove(tir)
                    self.point += 10
                    # self.boss_point_spawn += 100
    # def spawn_boss(self):
    #     if self.boss_point_spawn == 300:
    #         self.boss_point_spawn -= 200
    #     if self.boss_point_spawn == 200:
    #         self.boss_liste.append([128, 50, 10])
    #     for boss in self.boss_liste:
    #         boss[0] -= 1
    def thib(self):
        if self.pv <= 0:
            self.status = 2
    def start(self):
        if pyxel.btn(pyxel.KEY_RETURN):
            self.status = 1
    def harder(self):
        if self.point != 0:
            if self.point%50 == 0:
                if self.spawn_rate >= 1.1:
                    self.spawn_rate -= 1
                if self.speed_mechant <= 1:
                    self.speed_mechant += 0.05
#------------------------------------
#UPDATE
#------------------------------------
    def update(self):
        if self.status == 0:
            self.start()
        if self.status == 1:
            self.mouvements()
            self.move_check()
            self.tir()
            self.spawn_mechant()
            self.explosion_mechant()
            self.thib()
            self.tri_mechants()
            self.harder()
            # self.spawn_boss()

#------------------------------------
#DRAW
#------------------------------------
    def draw(self):
        pyxel.cls(0)
        if self.status == 0:
            pyxel.text(50, 50, "START", pyxel.frame_count%15)
            pyxel.text(20, 60, "PRESS ENTER TO START", pyxel.frame_count%15)
        elif self.status == 1:
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            for tir in self.tir_liste:
                if tir[0] > 134:
                    self.tir_liste.remove(tir)
            for tir in self.tir_liste:
                pyxel.blt(tir[0], tir[1], 0, 0, 73, 6, 6, 0)
            for mechant in self.mechant_liste:
                if mechant[0] < -8:
                    self.mechant_liste.remove(mechant)
            for mechant in self.mechant_liste:
                pyxel.blt(mechant[0], mechant[1], 0, 9, 73, 7, 6, 0)
            #pyxel.rect(self.x%pyxel.width, self.y%pyxel.width, 8, 8, 1)
            pyxel.blt(self.x, self.y, 0, 16, 82, 16, 9, 0)
            pyxel.blt(0, 0, 0, 32, 65, 8, 7, 0)
            self.pv = str(self.pv)
            self.point = str(self.point)
            pyxel.text(10, 0, self.pv, 0)
            pyxel.text(30, 0, self.point + "   POINT", 0)
            self.pv = int(self.pv)
            self.point = int(self.point)
            for boss in self.boss_liste:
                pyxel.blt(boss[0], boss[1], 0, 32, 83, 17, 9, 0)
        elif self.status == 2:
            pyxel.text(50, 50, "GAME OVER", pyxel.frame_count%15)
            pyxel.text(50, 60, "YOU LOSE", pyxel.frame_count%15)
Jeu()