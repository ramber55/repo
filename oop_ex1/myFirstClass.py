print("first class")

# Tipos de Frutas
tiposFruta = ("manzana", "pera", "plátano", "aguacate", "mandarina")
manzana = 0
pera = 1
platano = 2
aguacate = 3
mandarina = 4
# Tamaño
tamanioFruta = ("pequeño", "medio", "grande")
pequenio = 0
medio = 1
grande = 2


class Fruta:
    
    def __init__(self, tipo, tamanio):
        self.tipo = tipo
        self.tamanio = tamanio

    def __str__(self):
        return f"{self.tipo} de tamaño {self.tamanio}"


class Frutero:

    def __init__(self):
        self.frutas = []

    def __str__(self):
        contenido = ""
        for fruta in self.frutas:
            contenido += " " + str(fruta)
        return contenido

    def meter_fruta(self, fruta):
        self.frutas.append(fruta)

