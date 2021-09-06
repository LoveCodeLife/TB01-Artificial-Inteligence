import pygame
import math
import random
import sys
import time



class Nodo():
    def __init__(self, pariente=None, posicion=None):
        self.pariente = pariente
        self.posicion = posicion

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.posicion == otro.posicion


def A_asterisc(mapa, inicio, meta):
    Nodo_inicio = Nodo(None, inicio)
    Nodo_inicio.g = Nodo_inicio.h = Nodo_inicio.f = 0
    Nodo_fin = Nodo(None, meta)
    Nodo_fin.g = Nodo_fin.h = Nodo_fin.f = 0
    lista_abierta = []
    lista_cerrada = []
    lista_abierta.append(Nodo_inicio)
    while len(lista_abierta) > 0:
        Nodo_actual = lista_abierta[0]
        index_actual = 0
        for index, item in enumerate(lista_abierta):
            if item.f < Nodo_actual.f:
                Nodo_actual = item
                index_actual = index

        lista_abierta.pop(index_actual)
        lista_cerrada.append(Nodo_actual)

        if Nodo_actual == Nodo_fin:
            path = []
            current = Nodo_actual
            while current is not None:
                path.append(current.posicion)
                current = current.pariente
            return path[::-1] #Truco para obtener el reves de la lista

        sucesores = []
        for pos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  #Se validó para todos los casos

            Nodo_posicion = (Nodo_actual.posicion[0] + pos[0], Nodo_actual.posicion[1] + pos[1])
            if Nodo_posicion[0] > (len(mapa) - 1) or Nodo_posicion[0] < 0 or Nodo_posicion[1] > \
                    (len(mapa[len(mapa) - 1]) - 1) or Nodo_posicion[1] < 0:
                continue

            if mapa[Nodo_posicion[0]][Nodo_posicion[1]] != 0:
                continue

            nuevo = Nodo(Nodo_actual, Nodo_posicion)

            sucesores.append(nuevo)

        for sucesor in sucesores:

            for hijo in lista_cerrada:
                if sucesor == hijo:
                    continue

            # f() = g() + h()
            sucesor.g = Nodo_actual.g + 1
            sucesor.h = math.sqrt(((sucesor.posicion[0] - Nodo_fin.posicion[0]) ** 2) + (
                        (sucesor.posicion[1] - Nodo_fin.posicion[1]) ** 2))
            sucesor.f = sucesor.g + sucesor.h

            for nodo_abierto in lista_abierta:
                if sucesor == nodo_abierto and sucesor.g > nodo_abierto.g:
                    continue

            lista_abierta.append(sucesor)


##########################
class Serpiente():
    def __init__(self, x, y):
        self.posicion = [x, y]
        self.cuerpo = [[x, y], [x - 10, y], [x - 20, y]]
        self.direccion = "Derecha"
        self.change_dir = self.direccion

    def cambiar_direccion(self, direccion):
        if direccion == "Derecha" and not self.direccion == "Izquierda":
            self.direccion = "Derecha"
        if direccion == "Izquierda" and not self.direccion == "Derecha":
            self.direccion = "Izquierda"
        if direccion == "Arriba" and not self.direccion == "Abajo":
            self.direccion = "Arriba"
        if direccion == "Abajo" and not self.direccion == "Arriba":
            self.direccion = "Abajo"

    def mover(self, comida_pos):
        if self.direccion == "Derecha":
            self.posicion[0] += 10
        if self.direccion == "Izquierda":
            self.posicion[0] -= 10
        if self.direccion == "Arriba":
            self.posicion[1] -= 10
        if self.direccion == "Abajo":
            self.posicion[1] += 10
        self.cuerpo.insert(0, list(self.posicion))
        if self.posicion == comida_pos:
            return 1  # True
        else:
            self.cuerpo.pop()
            return 0  # False

    def Colision(self):
        x = self.posicion[0]
        y = self.posicion[1]
        #limites del mapa
        if x > 690 or x < 0:
            return 1
        elif y > 690 or y < 0:
            return 1
        return 0

    def getHeadPos(self):
        return self.posicion

    def getBody(self):
        return self.cuerpo


class comida_generador():
    def __init__(self):
        self.posicion = [random.randrange(1, 70) * 10,
                         random.randrange(1, 50) * 10]
        self.isFoodOnScreen = True

    def comida_spawn(self):
        if self.isFoodOnScreen == False:
            self.posicion = [random.randrange(1, 70) * 10,
                             random.randrange(1, 50) * 10]
            self.isFoodOnScreen = True
        return self.posicion

    def setFoodOnScreen(self, b):
        self.isFoodOnScreen = b


class Mapa:
    mapa = []

    def __init__(self):
        for i in range(70): # va 50 y abajo tbn
            self.fil = []
            for j in range(70):
                self.fil.append(0)
            self.mapa.append(self.fil)

    def getMapa(self):
        return self.mapa

    '''
    El score está definido para la IA
    El score2 para el jugador
    '''
    def gameOver(self, score, score2):
        resultado = ""
        if (score == score2):
            resultado = "EMPATE!"
        if (score > score2):
            resultado = "GANADOR: Inteligencia Artificial"
        if (score < score2):
            resultado = "GANADOR: Humano"

        pygame.display.set_caption(resultado)

        Fin = True
        while Fin:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    Fin = False
        pygame.quit()
        sys.exit()




def main():
    # Mapa (Matriz)
    MAPA = Mapa()
    mapa = MAPA.getMapa()

    # Mapa (Pygame)
    window = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('A* Algorithm')
    fps = pygame.time.Clock()

    # Comida
    foodSpawner = comida_generador()

    # IA
    snake = Serpiente(0,0)
    score = 0
    inicio = (int(snake.getHeadPos()[0] / 10), int(snake.getHeadPos()[1] / 10))
    objetivo = (int(foodSpawner.comida_spawn()[0] / 10), int(foodSpawner.comida_spawn()[1] / 10))

    # Humano
    snake2 = Serpiente(0,20)
    score2 = 0

    window.fill(pygame.Color(178,255,255))

    while True:
        camino = A_asterisc(mapa, inicio, objetivo)
        snake_x = snake.getHeadPos()[0]
        snake_y = snake.getHeadPos()[1]
        # IA
        for (x, y) in camino:
            if x > snake_x:
                snake.cambiar_direccion('Derecha')
            if x < snake_x:
                snake.cambiar_direccion('Izquierda')
            if y > snake_y:
                snake.cambiar_direccion('Abajo')
            if y < snake_y:
                snake.cambiar_direccion('Arriba')
            snake_x = x
            snake_y = y
        # Humano
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mapa.gameOver()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake2.cambiar_direccion('Derecha')
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake2.cambiar_direccion('Izquierda')
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake2.cambiar_direccion('Arriba')
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake2.cambiar_direccion('Abajo')
                if event.key == pygame.K_q: #opcional
                    score2 +=1




        comida_pos = foodSpawner.comida_spawn()  # Retorna posicion de la comida

        # IA
        if (snake.mover(comida_pos) == 1):  # Si hay colision
            score += 1
            foodSpawner.setFoodOnScreen(False)
        # Humano
        if (snake2.mover(comida_pos) == 1):  # Si hay colision
            score2 += 1
            foodSpawner.setFoodOnScreen(False)

        window.fill(pygame.Color(225, 225, 225))

        for x in range(70):
            for y in range(70):
                if (mapa[x][y] == 0):
                    pygame.draw.rect(window, pygame.Color(194, 186, 186),
                                     pygame.Rect(x * 10, y * 10, 10, 10), 1)  # x,y,ancho,alto
                if (mapa[x][y] == 1):
                    pygame.draw.rect(window, pygame.Color(0, 0, 0),
                                     pygame.Rect(x * 10, y * 10, 10, 10), 1)  # x,y,ancho,alto
        # IA
        for pos in snake.getBody():
            pygame.draw.rect(window, pygame.Color(203, 50, 52),
                             pygame.Rect(pos[0], pos[1], 10, 10))  # x,y,ancho,alto
        # Humano
        for pos in snake2.getBody():
            pygame.draw.rect(window, pygame.Color(0, 0, 0),
                             pygame.Rect(pos[0], pos[1], 10, 10))  # x,y,ancho,alto

        # Dibujar Comida
        pygame.draw.rect(window, pygame.Color(0, 143, 57),
                         pygame.Rect(comida_pos[0], comida_pos[1], 10, 10))
        # IA
        if (snake.Colision() == 1):
            MAPA.gameOver(score, score2)
        # Humano
        if (snake2.Colision() == 1):
            MAPA.gameOver(score, score2)

        # Puntaje
        pygame.display.set_caption("IA | Puntaje :" + str(score) + "Humano | Puntaje :" + str(score2))
        pygame.display.flip()
        fps.tick(24)

        # Nodo
        inicio = (int(snake.getHeadPos()[0] / 10), int(snake.getHeadPos()[1] / 10))
        objetivo = (int(comida_pos[0] / 10), int(comida_pos[1] / 10))


if __name__ == '__main__':
    main()

