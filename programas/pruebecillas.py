dna_string = "AACGTTAAACCGGTAATAATTCCCTTTTCGAACGTTAGCCACAHGAGAGAGTTTGAACGCAAAAACCCCCCTCA"

# Queremos coger los primeros 5 fragmentos de 10 caracteres.
# Los índices en cada uno de esos fragmentos son:
# 1er fragmento: 0 1 2 3 4 5 6 7 8 9
# 2o fragmento: 10 11 12 13 14 15 16 17 18 19
# 3er fragmento 20 21 22 23 24 25 26 27 28 29
# ...
# El primer valor de un range es el primer indice, el segundo es donde para y el tercero es
# lo que se incrementa i en cada salto. Así que con el range del for de abajo, se dan 5 saltos
# en los que i vale: 0, 10, 20, 30, 40. Que son justamente los indices donde comienzan los
# fragmentos que queemos y desde los que tengo que coger 10 caracteres:
for i in range(0, 40, 10):
    print(f"principio del fragmento {i} final del fragmento {i+10-1}")
    fragment = dna_string[i:i+10]
    print(f"Longitud del fragmento {len(fragment)}, Fragmento: {fragment}")

