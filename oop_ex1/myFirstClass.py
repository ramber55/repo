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

# Clases -----------------------------------------------------------


class Fruta:
    
    def __init__(self, tipo, tamanio):
        self.tipo = tipo
        self.tamanio = tamanio

    def __str__(self):
        txt = "{} de tamaño {}"
        return txt.format(tiposFruta[self.tipo], tamanioFruta[self.tamanio])


class Manzana (Fruta):

    def __init__(self, tamanio):
        super().__init__(manzana, tamanio)


class Pera(Fruta):

    def __init__(self, tamanio):
        super().__init__(pera, tamanio)


class Platano(Fruta):

    def __init__(self, tamanio):
        super().__init__(platano, tamanio)


class Aguacate(Fruta):

    def __init__(self, tamanio):
        super().__init__(aguacate, tamanio)


class Mandarina(Fruta):

    def __init__(self, tamanio):
        super().__init__(mandarina, tamanio)


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


# main ------------------------------------------------
print("Here we go ...")
manzana1 = Manzana(medio)
manzana2 = Manzana(pequenio)
print("una manzana:", manzana2)
pera1 = Pera(grande)
frutero = Frutero()
frutero.meter_fruta(manzana1)
frutero.meter_fruta(manzana2)
frutero.meter_fruta(pera1)
