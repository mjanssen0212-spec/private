import numpy as np


def toYUV(r, g, b):
    y = np.dot(0.299, r) + np.dot(0.587, g) + np.dot(0.114, b)

    u = (b - y) * 0.493
    v = (r - y) * 0.877

    print(f"Y: {y}\n U: {u}\n V: {v}")

    return y,u,v


def prepare(r,g,b):
    y,u,v = toYUV(r,g,b)

    y = np.round(np.dot(y, 255)-128)
    u = np.round(np.dot((u+0.436), 255) / 0.872 - 128)
    v = np.round(np.dot((v+0.615), 255) / 1.23 - 128)

    print(f"Y: {y}\n U: {u}\n V: {v}")

    return y,u,v

def dct(matrix):
    # Matrix in ein NumPy-Array umwandeln, damit wir bequem mit Indizes
    # und mathematischen Operationen arbeiten können.
    matrix = np.array(matrix, dtype=float)

    # n = Anzahl der Zeilen, m = Anzahl der Spalten
    # Bei deinem Beispiel ist das eine 3x3-Matrix.
    n, m = matrix.shape

    # Ergebnis-Matrix mit Nullen erzeugen.
    # Hier werden später die DCT-Koeffizienten gespeichert.
    result = np.zeros((n, m))

    # u und v sind die Frequenz-Indizes der DCT.
    # u beschreibt die vertikale Frequenz,
    # v beschreibt die horizontale Frequenz.
    for u in range(n):
        for v in range(m):

            # In sum_value wird die gewichtete Summe aller Pixelwerte
            # für den aktuellen DCT-Koeffizienten (u, v) gesammelt.
            sum_value = 0

            # x und y laufen über alle Positionen der Eingabematrix.
            # Für jeden Pixelwert wird berechnet, wie stark er zur
            # Frequenzkomponente (u, v) beiträgt.
            for x in range(n):
                for y in range(m):
                    sum_value += (
                        matrix[x, y]
                        * np.cos(((2 * x + 1) * u * np.pi) / (2 * n))
                        * np.cos(((2 * y + 1) * v * np.pi) / (2 * m))
                    )

            # Normierungsfaktor für u:
            # Für u = 0 wird anders normiert als für u > 0.
            # Das ist Teil der orthonormalen DCT-Definition.
            if u == 0:
                alpha_u = np.sqrt(1 / n)
            else:
                alpha_u = np.sqrt(2 / n)

            # Normierungsfaktor für v:
            # Auch hier gilt: v = 0 wird anders behandelt als v > 0.
            if v == 0:
                alpha_v = np.sqrt(1 / m)
            else:
                alpha_v = np.sqrt(2 / m)

            # Der endgültige DCT-Koeffizient entsteht aus:
            # Normierung in u-Richtung *
            # Normierung in v-Richtung *
            # berechneter gewichteter Summe.
            result[u, v] = alpha_u * alpha_v * sum_value

    # Die fertige Matrix mit den DCT-Koeffizienten zurückgeben.
    return result

def quantize(matrix, matrixQ, q):
    matrix1 = np.array(matrix, dtype=float)
    qmatrix = np.array(matrixQ, dtype=float)

    result = np.zeros_like(matrix)

    for u in range(matrix.shape[0]):
        for v in range(matrix.shape[1]):
            result[u, v] = np.round(matrix1[u, v] / (q * qmatrix[u, v]))

    return result




def dequantize(matrix, matrixQ, q):
    matrix1 = np.array(matrix, dtype=float)
    qmatrix = np.array(matrixQ, dtype=float)

    result = np.zeros_like(matrix)
    for u in range(matrix.shape[0]):
        for v in range(matrix.shape[1]):
            result[u, v] = matrix1[u, v] * q * qmatrix[u, v]
    return result

def idct(matrix):
    matrix = np.array(matrix, dtype=float)
    n, m = matrix.shape
    result = np.zeros((n, m))

    # x, y = Pixelposition (Ausgabe), u, v = Frequenz-Indizes (Eingabe)
    for x in range(n):
        for y in range(m):
            totalValue = 0
            for u in range(n):
                for v in range(m):
                    alpha_u = np.sqrt(1 / n) if u == 0 else np.sqrt(2 / n)
                    alpha_v = np.sqrt(1 / m) if v == 0 else np.sqrt(2 / m)

                    totalValue += (
                        alpha_u
                        * alpha_v
                        * matrix[u, v]
                        * np.cos(((2 * x + 1) * u * np.pi) / (2 * n))
                        * np.cos(((2 * y + 1) * v * np.pi) / (2 * m))
                    )

            # nicht runden, sonst gehen die .5-Werte verloren
            result[x, y] = totalValue

    return result

# Pixel (Zeile, Spalte):
# Rot,     Grün,  Blau
# Gelb,    Cyan,  Magenta
# Schwarz, Grau,  Weiß
r = [
    [0.5, 0.34],
    [0.78, 0.54]
]

g = [
    [0.8, 0.0],
    [0.23, 0.76]
]

b = [
    [0.99, 0.12],
    [0.12, 1.0]
]

qMatrix = [
    [16, 11],
    [12, 12]
    ]

q = 0.5

y, u, v = prepare(r, g, b)

print("Prepared Y:")
print(y)
print("Prepared U:")
print(u)
print("Prepared V:")
print(v)

y = dct(y)
print("DCT(Y):")
print(y)

u = dct(u)
print("DCT(U):")
print(u)

v = dct(v)
print("DCT(V):")
print(v)

yq = quantize(y, qMatrix, q)
print("Quantisierung(Y):")
print(yq)

uq = quantize(u, qMatrix, q)
print("Quantisierung(U):")
print(uq)

vq = quantize(v, qMatrix, q)
print("Quantisierung(V):")
print(vq)

rqy = dequantize(yq, qMatrix, q)
print("Dequantisierung(Y):")
print(rqy)

rqu = dequantize(uq, qMatrix, q)
print("Dequantisierung(U):")
print(rqu)

rqv = dequantize(vq, qMatrix, q)
print("Dequantisierung(V):")
print(rqv)

decoded_y = idct(rqy)
print("IDCT(Y):")
print(decoded_y)

decoded_u = idct(rqu)
print("IDCT(U):")
print(decoded_u)

decoded_v = idct(rqv)
print("IDCT(V):")
print(decoded_v)
