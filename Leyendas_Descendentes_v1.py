import pygame
import sys
import math
import random

#queda:
#Menu principal
#Al implementar las pociones no se pueden usar y no se por que 
#Implementar el menu inventario para poder utilizar pociones y demas en mitad de la bajada
#Crear la clase EnemigoAumentado para crear Bosses (Ultimo mensaje de ChatGpt)(va a costar mas de lo pensado)
#cambiar todos los puntos por sus respectivos aspectos finales
#Maximo piso alcanzado 11 ida y vuelta,al llegar al piso 11 a los enemigos les cuesta avanzar y pillarte
#Arreglar el bug de tener mas vida q la barra de vida al comer comida de la cantinera
#Implementar la armadura


class Heroe:
    def __init__(self):
        self.velocidad = 5
        self.size = 20
        self.daño = 10
        self.nivel = 1
        self.vida = 100
        self.vida_maxima = 100
        self.armadura = 0
        self.color = (255, 255, 255)
        self.posicion = [width // 2, height // 2]
        self.angulo = 0
        self.proyectiles = []
        self.experiencia = 0
        self.experiencia_necesaria = 100
        self.inventario = {"Gema":0,
                           "Oro": 0,
                           "Pocion": 0}
        self.regeneracionVida = 50
        

    def subir_nivel(self):
        self.nivel += 1
        self.experiencia = 0
        self.experiencia_necesaria *= 2
        self.aumentar_atributos()
    
    def aumentar_atributos(self):
        self.vida_maxima +=20
        self.vida += 20
        self.daño += 5
        self.velocidad += 1
        self.armadura +=1

    def recibir_experiencia(self, screen, cantidad):
        self.experiencia += cantidad
        if self.experiencia >= self.experiencia_necesaria:
            self.subir_nivel()

    def mover(self, keys):
        if keys[pygame.K_w]:
            self.posicion[1] -= self.velocidad
        if keys[pygame.K_s]:
            self.posicion[1] += self.velocidad
        if keys[pygame.K_a]:
            self.posicion[0] -= self.velocidad
        if keys[pygame.K_d]:
            self.posicion[0] += self.velocidad

    def apuntar(self, mouse_pos):
        dx = mouse_pos[0] - self.posicion[0]
        dy = mouse_pos[1] - self.posicion[1]
        self.angulo = math.atan2(dy, dx)

    def disparar(self):
        proyectil = Proyectil(self.posicion.copy(), self.angulo, self.daño)
        self.proyectiles.append(proyectil)

    def actualizar_proyectiles(self):
        for proyectil in self.proyectiles:
            proyectil.actualizar()
            if not (0 <= proyectil.posicion[0] <= width and 0 <= proyectil.posicion[1] <= height):
                self.proyectiles.remove(proyectil)

    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, (self.posicion[0], self.posicion[1], self.size, self.size))

        for proyectil in self.proyectiles:
            proyectil.Dibujar(screen)
    def dibujar_barra_vida(self, screen):
        barra_vida_ancho =  200
        barra_vida_altura = 10
        barra_vida_color = (0,255,0)
        
        longitud_vida_actual = (self.vida/self.vida_maxima)* barra_vida_ancho
        barra_x = width //2 - barra_vida_ancho//2
        barra_y = height - 50 
        pygame.draw.rect(screen, barra_vida_color,(barra_x, barra_y, longitud_vida_actual, barra_vida_altura))
        pygame.draw.rect(screen, (255, 255, 255), (barra_x, barra_y,barra_vida_ancho,barra_vida_altura), 2)
    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            return True
        return False

    def dibujar_barra_experiencia(self, screen):
        barra_exp_ancho = 200
        barra_exp_altura = 10
        barra_exp_color = (0, 0, 255)

        longitud_exp_actual = (self.experiencia / self.experiencia_necesaria) * barra_exp_ancho
        barra_exp_x = width // 2 - barra_exp_ancho // 2
        barra_exp_y = height - 30
        pygame.draw.rect(screen, barra_exp_color, (barra_exp_x, barra_exp_y, longitud_exp_actual, barra_exp_altura))
        pygame.draw.rect(screen, (255, 255, 255), (barra_exp_x, barra_exp_y, barra_exp_ancho, barra_exp_altura), 2)
    
    def agregar_al_inventario(self, gema):
        self.inventario["Gema"] += gema.valor
    
    def usarPocion(self):
        if self.inventario["Pocion"] > 0 :
            self.vida += self.regeneracionVida
            if self.vida >= self.vida_maxima:
                self.vida = self.vida_maxima
            self.inventario["Pocion"] -= 1



class Proyectil:
    def __init__(self, posicion, angulo, daño):
        self.velocidad = 10
        self.radio = 5
        self.color = (255, 255, 0)
        self.posicion = posicion
        self.velocidad_x = self.velocidad * math.cos(angulo)
        self.velocidad_y = self.velocidad * math.sin(angulo)
        self.daño = daño

    def actualizar(self):
        self.posicion[0] += self.velocidad_x
        self.posicion[1] += self.velocidad_y

    def Dibujar(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.posicion[0]), int(self.posicion[1])), self.radio)
    
    def verificar_colision_enemigo(self, enemigo):
        distancia = math.sqrt((self.posicion[0] - enemigo.posicion[0])**2 + (self.posicion[1] - enemigo.posicion[1])**2)
        if distancia < enemigo.size / 2 + self.radio:  # Colisión si la distancia entre el proyectil y el centro del enemigo es menor que la suma de los radios
            enemigo.recibir_danio(self.daño)
            if self.vida <= 0:
                enemigo.vida = 0  # Asegurarse de que la vida no sea negativa
                enemigo.eliminar()
            return True
        return False



class Enemigo:
    def __init__(self, width, height):
        self.velocidad = 2
        self.size = 20
        self.daño = 5
        self.vida_maxima = 20
        self.vida = self.vida_maxima
        self.color = (255, 0, 0)
        self.posicion = [random.randint(0, width - self.size), random.randint(0, height - self.size)]
        self.objetivo = None  # Punto objetivo al que se moverá el enemigo
        self.experiencia_base = 5
        self.nivel = 1

    def subir_nivel(self):
        self.nivel += 1
        self.vida_maxima +=10
        self.vida = self.vida_maxima
        self.experiencia_base += 2

    def mover_hacia_heroe(self, heroe_posicion):
        dx = heroe_posicion[0] - self.posicion[0]
        dy = heroe_posicion[1] - self.posicion[1]
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia != 0:
            direccion_x = dx / distancia
            direccion_y = dy / distancia

            self.posicion[0] += self.velocidad * direccion_x
            self.posicion[1] += self.velocidad * direccion_y
    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        

    def eliminar(self):
            enemigos.remove(self)

    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, (self.posicion[0], self.posicion[1], self.size, self.size))

    def manejar_colision_heroe(self, heroe):
        distancia = math.sqrt((self.posicion[0] - heroe.posicion[0])**2 + (self.posicion[1] - heroe.posicion[1])**2)
        if distancia < heroe.size / 2 + self.size / 2:
            # Colisión con el héroe
            heroe.vida -= self.daño
            if heroe.vida < 0:
                heroe.vida = 0

            # Separarse en la misma dirección pero en sentido contrario
            dx = self.posicion[0] - heroe.posicion[0]
            dy = self.posicion[1] - heroe.posicion[1]
            distancia = math.sqrt(dx**2 + dy**2)
            
            if distancia != 0:
                direccion_x = dx / distancia
                direccion_y = dy / distancia

                separacion = 150
                self.posicion[0] += separacion * direccion_x
                self.posicion[1] += separacion * direccion_y
    
    def otorgar_experiencia(self):
        return self.experiencia_base * self.nivel
    def generar_gema(self):
        tipo = "Gema"
        valor = random.randint(0 , 10)
        return Gema(tipo, valor)

class EnemigoConNivel(Enemigo):
    def __init__(self, width, height, nivel):
        super().__init__(width,height)
        self.nivel=nivel
        self.size = 20
        self.daño = 5 + nivel
        self.vida_maxima = (20 + nivel * 0.5)
        self.vida = self.vida_maxima
        self.experiencia_base += nivel
        self.velocidad = 2 + 0.1*nivel
class EnemigoAumentado(Enemigo):
    def __init__(self, widht, height):
        super().__init__(widht, height)
        self.size = 50
        self.daño = 20
        self.vida_maxima = 2000
        self.vida = self.vida_maxima
        self.experiencia_base = 40
        self.color = (255,255,0)

class Mazmorra:
    def __init__(self):
        self.piso_actual = 0
        self.enemigos_mazmorra_actual = 0
        self.enemigos_por_piso = 0
        self.enemigos_maximos_por_piso = 10
        self.intervalo_enemigos = 2500
        self.nivel_base_enemigos = 1
        self.pisos_para_subir_nivel_base = 15
        self.objetivos_enemigos_alcanzados = False
        self.pueblo = True
        self.pisoBoss = 10
        
    def incrementar_piso(self):
        self.piso_actual += 1
        self.enemigos_mazmorra_actual = 0
        self.enemigos_maximos_por_piso += 2
        self.enemigos_por_piso += 10
        self.intervalo_enemigos -= 100

        if self.piso_actual % self.pisos_para_subir_nivel_base == 0 and not self.pueblo:
            self.nivel_base_enemigos += 1

        self.objetivos_enemigos_alcanzados = False
        self.pueblo = False

    
    def reducir_piso(self):
        self.piso_actual -= 1
        self.enemigos_mazmorra_actual = 0
        self.enemigos_maximos_por_piso-= 2
        self.enemigos_por_piso -= 10
        self.intervalo_enemigos +=100
        self.objetivos_enemigos_alcanzados = False
        if self.piso_actual <= 0:
            self.pueblo = True
        else: 
            self.pueblo = False

    def crear_enemigo(self):
        nivel_enemigo = random.randint(self.nivel_base_enemigos, heroe.nivel)
        if self.piso_actual % self.pisoBoss != 0 :
            return EnemigoConNivel(width, height, nivel_enemigo)
        else:
            return EnemigoAumentado(width, height)
    
    
class Portal:
    def __init__(self, tipo, x, y, destino):
        self.tipo = tipo #Subir o bajar
        self.rect = pygame.Rect(x, y, 30,30)
        self.destino = destino
    
    def Dibujar(self, screen):
        pygame.draw.rect(screen,(0, 128, 255), self.rect)
    
    def verificar_colision_heroe(self, heroe):
        return self.rect.colliderect(pygame.Rect(heroe.posicion[0], heroe.posicion[1],heroe.size, heroe.size))
    def usarPortal(self, mazmorra):
        if self.tipo == "subir":
            mazmorra.incrementar_piso()
        if self.tipo == "bajar" and mazmorra.piso_actual > 0:
            mazmorra.reducir_piso()
    
class Pueblo:
    def __init__(self):
        self.portal_subir_piso = Portal('subir', width // 2, height - 100, 1)
        self.posicion_heroe = [width//2,height//2]
    
    def dibujar_pueblo(self, screen):
        self.portal_subir_piso.Dibujar(screen)
    
    def verificar_colision_portal(self, heroe):
        return self.portal_subir_piso.verificar_colision_heroe(heroe)
    
class Gema:
    def __init__(self, tipo, valor):
        self.color = (128,0,128)
        self.tipo = tipo
        self.valor = valor 
    
class Recepcionista:
    def __init__(self):
        self.color = (130,170, 227)
        self.rect = pygame.Rect(random.randint(0, width),random.randint(0, height), 30,30)
    
    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def verificar_colision_heroe(self, heroe):
        return self.rect.colliderect(pygame.Rect(heroe.posicion[0], heroe.posicion[1], heroe.size, heroe.size))
    
    def interactuar(self, heroe):
        gemas = heroe.inventario["Gema"]
        mensaje = f"Tienes {gemas} gemas. ¿Quieres venderlas ? (s/n)"
        ventana_dialogo = VentanaDialogos()
        ventana_dialogo.mostrarDialogos(screen, mensaje)

        respuesta = None
        while respuesta not  in ["s", "n"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        respuesta = "s"
                        break
                    elif event.key == pygame.K_n:
                        respuesta = "n"
                        break

        if respuesta.lower() == "s":
            heroe.inventario["Oro"] += heroe.inventario["Gema"]
            heroe.inventario["Gema"] = 0
            heroe.contador_gemas = 0
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)
        else:
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)
            
class Herrero:
    def __init__(self):
        self.color = (128,128,128)
        self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 30, 30)
        self.precio = {"Armas": 10,
                       "Armadura": 10,
                       "Botas": 10}
    
    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def verificar_colision_heroe(self, heroe):
        return self.rect.colliderect(pygame.Rect(heroe.posicion[0], heroe.posicion[1], heroe.size, heroe.size))
    
    def interactuar(self, heroe):
        dinero = heroe.inventario["Oro"]
        mensaje = f"Tienes {dinero}. Puedes mejorar Daño(d), vida(a), velocidad (v) o no (n)"
        ventana_dialogo = VentanaDialogos()
        ventana_dialogo.mostrarDialogos(heroe, mensaje)
        respuesta = None
        while respuesta not in ["a", "d", "v", "n"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        respuesta = "a"
                        break
                    elif event.key == pygame.K_d:
                        respuesta = "d"
                        break
                    elif event.key == pygame.K_v:
                        respuesta = "v"
                        break
                    elif event.key == pygame.K_n:
                        respuesta = "n"
                        break
        if respuesta.lower() == "a":
            heroe.vida_maxima +=1
            heroe.inventario["Oro"] -= self.precio["Armadura"]
            self.precio["Armadura"] += 5
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)
            
        elif respuesta.lower() == "d" :
            heroe.daño +=1
            heroe.inventario["Oro"] -= self.precio["Armas"]
            self.precio["Armas"] += 5
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)
            
        elif respuesta.lower() == "v":
            heroe.velocidad += 0.5
            heroe.inventario["Oro"] -= self.precio["Botas"]
            self.precio["Botas"] += 5
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)

        elif respuesta.lower() == "n":
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)   

class Cantinero:
    def __init__(self):
        self.color = (0, 201, 87)
        self.rect = pygame.Rect(random.randint(0, width),random.randint(0, height), 30,30)
        self.comida = {"Gambas": 10, "Macarrones": 60}
    
    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def verificar_colision_heroe(self, heroe):
        return self.rect.colliderect(pygame.Rect(heroe.posicion[0], heroe.posicion[1], heroe.size, heroe.size))
    
    def interactuar(self, heroe):
        dinero = heroe.inventario["Oro"]
        mensaje = f"Tienes {heroe.vida} puntos de vida.Quieres algun plato: 1{self.comida["Gambas"]}€ Plato de gambas (10) 2 {self.comida["Macarrones"]} € Macarrones (50)"
        ventana_dialogo = VentanaDialogos()
        ventana_dialogo.mostrarDialogos(screen, mensaje)

        respuesta = None
        while respuesta not in ["1", "2", "n"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        respuesta = "1"
                        break
                    elif event.key == pygame.K_2:
                        respuesta = "2"
                        break
                    elif event.key == pygame.K_n:
                        respuesta = "n"
                        break

        if respuesta == "1":
            heroe.vida += 10
            heroe.inventario["Oro"] -= self.comida["Gambas"]
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)
        elif respuesta == "2":
            heroe.vida += 50
            heroe.inventario["Oro"] -= self.comida["Macarrones"]
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)
        else:
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)

class Analista:
    def __init__(self):
        self.color = (0, 0, 139)  # Color azul oscuro
        self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 30, 30)

    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def verificar_colision_heroe(self, heroe):
        return self.rect.colliderect(pygame.Rect(heroe.posicion[0], heroe.posicion[1], heroe.size, heroe.size))

    def interactuar(self, heroe):
        mensaje = f"Atributos del héroe:\n"  \
                  f"Nivel: {heroe.nivel} \n" \
                  f"Velocidad: {heroe.velocidad} \n" \
                  f"Vida: {heroe.vida} \n" \
                  f"Vida Máxima: {heroe.vida_maxima} \n" \
                  f"Daño: {heroe.daño} \n" \
                  f"Armadura: {heroe.armadura}\n"
         
        ventana_dialogo = VentanaDialogos()
        ventana_dialogo.mostrarDialogos(heroe, mensaje)

class Alquimista:
    def __init__(self):
        self.color = (182,102,210)
        self.rect = pygame.Rect(random.randint(0, width), random.randint(0, height), 30, 30)

    def Dibujar(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def verificar_colision_heroe(self, heroe):
        return self.rect.colliderect(pygame.Rect(heroe.posicion[0], heroe.posicion[1], heroe.size, heroe.size))
    
    def interactuar(self, heroe):
        mensaje = "Vendo pociones de vida a buen precio 100 € (s/n)"
        ventana_dialogo = VentanaDialogos()
        ventana_dialogo.mostrarDialogos(heroe, mensaje)
        respuesta = None
        while respuesta not in ["s", "n"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        respuesta = "s"
                        break
                    elif event.key == pygame.K_n:
                        respuesta = "n"
                        break
        if respuesta.lower() == "s":
            heroe.inventario["Pocion"] += 1
            heroe.inventario["Oro"] -= 100
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)

        else:
            self.rect.x = random.randint(0, width)
            self.rect.y = random.randint(0, height)                
        


       
class VentanaDialogos:
    def __init__(self, ):
        self.rect= pygame.Rect(width, height, 300, 150)
        self.color_fondo = (0,0,0)
        self.color_borde = (0,0,0)
        self.color_texto = (255,255,255)
        self.front = pygame.font.Font(None, 24)
        

    def mostrarDialogos(self, heroe, mensaje):
        
        texto_superficie = self.front.render(mensaje, True, self.color_texto)
        rect_texto = texto_superficie.get_rect(center=(self.rect.width + 100 , self.rect.height//2))

        pygame.draw.rect(screen, self.color_fondo, self.rect)
        pygame.draw.rect(screen, self.color_borde, self.rect, 2)
        screen.blit(texto_superficie, rect_texto)


# Inicializar Pygame
pygame.init()

# Obtener el tamaño de la pantalla
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Leyendas Descendentes")

# Inicializar el bucle principal
heroe = Heroe()
enemigos = []
clock = pygame.time.Clock()
pausa = False
mazmorra = Mazmorra()
pueblo = Pueblo()
recepcionista = Recepcionista()
analista = Analista()
herrero = Herrero()
barman = Cantinero()
alquimista = Alquimista()
npcs = [recepcionista, analista, herrero, barman, alquimista]
portales =[pueblo.portal_subir_piso,
           Portal('bajar', width//2,20,mazmorra.piso_actual- 1 )]
#iniciar los intervalos para que aparezcan enemigos:
tiempo_ultima_aparicion = pygame.time.get_ticks()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pausa = not pausa
            elif event.type == pygame.K_1:
                heroe.usarPocion()
        elif pausa and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            continuar_button_rect = pygame.Rect(width // 2 -100, height//2-50, 200,40)
            salir_button_rect = pygame.Rect(width // 2 - 100, height //2 + 50,200, 40)
            if continuar_button_rect.collidepoint(mouse_pos):
                pausa =False
            elif salir_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
        
    if not pausa:
        # Lógica del juego y actualizaciones aquí
        keys = pygame.key.get_pressed()
        heroe.mover(keys)

        for enemigo in enemigos:
            enemigo.mover_hacia_heroe(heroe.posicion)
            enemigo.manejar_colision_heroe(heroe)
        
        
        proyectiles_a_eliminar = []
        for proyectil in heroe.proyectiles:
            proyectil.actualizar()
            for enemigo in enemigos:
                if proyectil.verificar_colision_enemigo(enemigo):
                    proyectiles_a_eliminar.append(proyectil)
                    heroe.recibir_experiencia(screen, enemigo.otorgar_experiencia())

                    gema = enemigo.generar_gema()
                    heroe.agregar_al_inventario(gema)
                    mazmorra.enemigos_mazmorra_actual += 1
    
        for proyectil in proyectiles_a_eliminar:
            heroe.proyectiles.remove(proyectil)
        
        if heroe.recibir_daño(0):
            pygame.quit()
            sys.exit()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_1:
                    heroe.usarPocion()
                
        
        #aparicion de enemigos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultima_aparicion >= mazmorra.intervalo_enemigos and len(enemigos) < mazmorra.enemigos_maximos_por_piso and mazmorra.piso_actual > 0 :
            enemigos.append(mazmorra.crear_enemigo())
            tiempo_ultima_aparicion = tiempo_actual

        if mazmorra.enemigos_mazmorra_actual >= mazmorra.enemigos_por_piso:
            mazmorra.objetivos_enemigos_alcanzados = True
            if mazmorra.objetivos_enemigos_alcanzados:
                for portal in portales:
                    portal.Dibujar(screen)
                    if portal.verificar_colision_heroe(heroe):
                        portal.usarPortal(mazmorra)
        
        # Apuntar y disparar al hacer clic izquierdo
        mouse_pos = pygame.mouse.get_pos()
        heroe.apuntar(mouse_pos)

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] == 1:
            heroe.disparar()



        # Dibujar en pantalla
        screen.fill((0, 0, 0))
        heroe.Dibujar(screen)

        for enemigo in enemigos:
            enemigo.Dibujar(screen)

        heroe.dibujar_barra_vida(screen)
        heroe.dibujar_barra_experiencia(screen)
        cont = pygame.font.Font(None, 24)
        info_gema = cont.render(f"Gemas:{heroe.inventario["Gema"]} Oro: {heroe.inventario["Oro"]} Pociones: {heroe.inventario["Pocion"]}", True , (255,255,255))
        screen.blit(info_gema, (100, height - 60))
        pygame.draw.circle(screen, (128,0,128), (60,  height - 60), 15)
        if mazmorra.pueblo:
            for npc in npcs:
                npc.Dibujar(screen)
                if npc.verificar_colision_heroe(heroe):
                    npc.interactuar(heroe)

        font = pygame.font.Font(None, 24)
        info_piso = font.render(f"Piso: {mazmorra.piso_actual} - Enemigos: {mazmorra.enemigos_mazmorra_actual}/{mazmorra.enemigos_por_piso}", True, (255, 255, 255))
        screen.blit(info_piso, (10, 10))
        if mazmorra.objetivos_enemigos_alcanzados:
            for portal in portales:
                portal.Dibujar(screen)

        if mazmorra.pueblo:
            pueblo.dibujar_pueblo(screen)
            if pueblo.verificar_colision_portal(heroe):
                portales.usarPortal(mazmorra)

    if pausa:
        # Si está en pausa, dibujar el fondo oscuro y los botones del menú de pausa
        pygame.draw.rect(screen, (0, 0, 0, 128), (0, 0, width, height))  # Fondo oscuro y translúcido

        # Botones del menú de pausa
        font = pygame.font.Font(None, 24)

        continuar_button = pygame.Rect(width // 2 - 100, height // 2 - 50, 200, 40)
        pygame.draw.rect(screen, (255, 255, 255), continuar_button)
        continuar_text = font.render("Continuar", True, (0, 0, 0))
        screen.blit(continuar_text, (width // 2 - 80, height // 2 - 40))

        configuracion_button = pygame.Rect(width // 2 - 100, height // 2, 200, 40)
        pygame.draw.rect(screen, (255, 255, 255), configuracion_button)
        configuracion_text = font.render("Configuración", True, (0, 0, 0))
        screen.blit(configuracion_text, (width // 2 - 110, height // 2 + 10))

        salir_button = pygame.Rect(width // 2 - 100, height // 2 + 50, 200, 40)
        pygame.draw.rect(screen, (255, 255, 255), salir_button)
        salir_text = font.render("Salir", True, (0, 0, 0))
        screen.blit(salir_text, (width // 2 - 45, height // 2 + 60))

            

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del bucle
    clock.tick(100)  # 60 fotogramas por segundo
