# Tipos de Frutas
tiposFruta = ("manzana", "pera", "plátano", "aguacate", "mandarina")
manzana = 0
pera = 1
platano = 2
aguacate = 3
mandarina = 4
# Tamaño
tamanio_fruta = ("pequeño", "medio", "grande")
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
        return txt.format(tiposFruta[self.tipo], tamanio_fruta[self.tamanio])


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
            contenido += str(fruta) + "\n"
        return contenido

    def meter_fruta(self, fruta):
        self.frutas.append(fruta)

    def fruta_en_frutero(self, fruta):
        tipo_fruta = fruta.tipo
        tamanio_fruta = fruta.tamanio
        for fruta_en_frutero in self.frutas:
            if fruta_en_frutero.tipo == tipo_fruta and fruta_en_frutero.tamanio == tamanio_fruta:
                return True
        return False

    def sacar_fruta(self, fruta):
        tipo_fruta = fruta.tipo
        tamanio_fruta = fruta.tamanio
        for fruta_en_frutero in self.frutas:
            if fruta_en_frutero.tipo == tipo_fruta and fruta_en_frutero.tamanio == tamanio_fruta:
                return True
        return False


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
print("Frutero:", frutero)

print("A ver si hay una", Manzana(medio))
esta = frutero.fruta_en_frutero(Manzana(medio))
if esta:
    print("Hay.")
else:
    print("No hay.")

print("A ver si hay un", Aguacate(grande))
esta = frutero.fruta_en_frutero(Aguacate(grande))
if esta:
    print("Hay.")
else:
    print("No hay.")
