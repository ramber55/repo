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


# Clase Fruta --------------------------
class Fruta:
    
    def __init__(self, tipo, tamanio):
        self.tipo = tipo
        self.tamanio = tamanio

    def __str__(self):
        txt = "{} de tamaño {}"
        return txt.format(tiposFruta[self.tipo], tamanio_fruta[self.tamanio])

    def __eq__(self, other):
        return self.tipo == other.tipo and self.tamanio == other.tamanio


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


# Clase Frutero --------------------------
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

    # puedo por haber definido __eq__ en Fruta:
    def fruta_en_frutero2(self, fruta):
        return fruta in self.frutas

    def sacar_fruta(self, fruta):
        self.frutas.remove(fruta)

    def __iter__(self):
        return iter(self.frutas)

    def __len__(self):
        return len(self.frutas)


# main ------------------------------------------------
# IMPRIMIR -------------
print("Here we go ...")
manzana1 = Manzana(medio)
manzana2 = Manzana(pequenio)
# Puedo imprimir una fruta porque he definido __str__
print("una manzana:", manzana2)
pera1 = Pera(grande)
frutero = Frutero()
frutero.meter_fruta(manzana1)
frutero.meter_fruta(manzana2)
frutero.meter_fruta(pera1)
# Puedo imprimir el frutero porque he definido __str__
print("Frutero:", frutero)

# OPERADORES -------------
print("A ver si hay una", Manzana(medio))
esta = frutero.fruta_en_frutero(Manzana(medio))
esta2 = frutero.fruta_en_frutero2(Manzana(medio))
if esta:
    print("Metodo1: Hay.")
else:
    print("Metodo1: No hay.")

if esta2:
    print("Metodo2: Hay.")
else:
    print("Metodo2: No hay.")

print("A ver si hay un", Aguacate(grande))
esta = frutero.fruta_en_frutero(Aguacate(grande))
esta2 = frutero.fruta_en_frutero2(Aguacate(grande))
if esta:
    print("Metodo1: Hay.")
else:
    print("Metodo1: No hay.")

if esta2:
    print("Metodo2: Hay.")
else:
    print("Metodo2: No hay.")

# RECORRIENDO (iterador) -------------
for fruta in frutero:
    print("Fruta", fruta)

fruta10 = Aguacate(pequenio)
fruta11 = Aguacate(pequenio)
fruta12 = Pera(grande)

# __eq__
if fruta10 == fruta11:
    print(fruta10, "y", fruta11, "son iguales")
else:
    print(fruta10, "y", fruta11, "son diferentes")

if fruta10 == fruta12:
    print(fruta10, "y", fruta12, "son iguales")
else:
    print(fruta10, "y", fruta12, "son diferentes")

print("El frutero tiene", len(frutero), "piezas")

frutero.meter_fruta(fruta10)
frutero.meter_fruta(fruta11)
frutero.meter_fruta(fruta12)
print("El frutero ahora tiene", len(frutero), "piezas")
for fruta in frutero:
    print("Fruta", fruta)

# OPERADORES ------------- __len__()
# y como esta __eq__ puedo usar remove(fruta) directamente
print("-----------------------------------------------------")
frutero.sacar_fruta(Pera(grande))
print("El frutero ahora tiene", len(frutero), "piezas")
for fruta in frutero:
    print("Fruta", fruta)
print("-----------------------------------------------------")
frutero.sacar_fruta(Pera(grande))
print("El frutero ahora tiene", len(frutero), "piezas")
for fruta in frutero:
    print("Fruta", fruta)

print("adios")
