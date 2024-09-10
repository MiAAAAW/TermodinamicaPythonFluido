# import numpy as np
# from scipy.ndimage import map_coordinates, spline_filter
# from scipy.sparse.linalg import factorized
# from scipy.sparse import csgraph
# from functools import reduce
# from itertools import cycle
# from math import factorial
# import scipy.sparse as sp

# '''
# -------------------------------------------------------
# Código basado en: https://github.com/GregTJ/stable-fluids
# Modificado para agregar paredes
# '''
# def diferencia(derivada, precision=1):
#     derivada += 1
#     radio = precision + derivada // 2 - 1
#     puntos = range(-radio, radio + 1)
#     coeficientes = np.linalg.inv(np.vander(puntos))
#     return coeficientes[-derivada] * factorial(derivada - 1), puntos

# def operador(shape, *diferencias):
#     diferencias = zip(shape, cycle(diferencias))
#     factores = (sp.diags(*diff, shape=(dim,) * 2) for dim, diff in diferencias)
#     return reduce(lambda a, f: sp.kronsum(f, a, format='csc'), factores)

# class Fluido:
#     def __init__(self, shape, *cantidades, orden_presion=1, orden_advect=3):
#         self.shape = shape
#         self.dimension = len(shape)

#         # Se crean dinámicamente las cantidades advectadas según sea necesario.
#         self.cantidades = cantidades
#         for q in cantidades:
#             setattr(self, q, np.zeros(shape))

#         self.indices = np.indices(shape)
#         self.velocidad = np.zeros((self.dimension, *shape))

#         self.laplaciano = operador(shape, diferencia(2, orden_presion))
#         self.solver_presion = factorized(self.laplaciano)

#         self.orden_advect = orden_advect

#     def paso(self, boundary, paredes=True):
#         # La advección se calcula hacia atrás en el tiempo según lo descrito en Stable Fluids.
#         mapa_adveccion = self.indices - self.velocidad

#         def advect(campo, epsilon_filtro=10e-2, modo='constant'):
#             filtrado = spline_filter(campo, order=self.orden_advect, mode=modo)
#             campo = filtrado * (1 - epsilon_filtro) + campo * epsilon_filtro
#             return map_coordinates(campo, mapa_adveccion, prefilter=False, order=self.orden_advect, mode=modo)

#         for d in range(self.dimension):
#             self.velocidad[d] = advect(self.velocidad[d])
#             if paredes:  # Podemos detener el fluido o hacer que rebote, aquí lo detenemos
#                 if d == 0:
#                     self.velocidad[d][:, 0] = 0  # -self.velocidad[d][:, 1]
#                     self.velocidad[d][:, -1] = 0  # -self.velocidad[d][:, -2]
#                 else:
#                     self.velocidad[d][0, :] = 0  # -self.velocidad[d][1, :]
#                     self.velocidad[d][-1, :] = 0  # -self.velocidad[d][-2, :]

#         for q in self.cantidades:
#             setattr(self, q, advect(getattr(self, q)))

#         # Calcular el jacobiano en cada punto del campo de velocidad
#         forma_jacobiana = (self.dimension,) * 2
#         parciales = tuple(np.gradient(d) for d in self.velocidad)
#         jacobiano = np.stack(parciales).reshape(*forma_jacobiana, *self.shape)

#         divergencia = jacobiano.trace()

#         # Para 3D, el valor del eje y debe negarse.
#         mascara_remolino = np.triu(np.ones(forma_jacobiana, dtype=bool), k=1)
#         remolino = (jacobiano[mascara_remolino] - jacobiano[mascara_remolino.T]).squeeze()

#         # Aplicar la corrección de presión al campo de velocidad
#         presion = self.solver_presion(divergencia.flatten()).reshape(self.shape)
#         self.velocidad -= np.gradient(presion)

#         return divergencia, remolino, presion


# class Fluido2:
#     def __init__(self, shape, *cantidades):
#         self.shape = shape
#         self.dimension = len(shape)

#         self.dye = np.zeros(shape)
#         self.velocidad = np.zeros((2, shape[0], shape[1]))

#         self.difusion = 0.001
#         self.viscosidad = 0
#         self.time_step = 1

#         self.indices = np.indices(shape)

#         self.prev_dye = np.zeros(shape)
#         self.prev_velocidad = np.zeros((2, shape[0], shape[1]))

#     def paso(self, boundary, paredes=True):
#         self.prev_velocidad, self.velocidad = self.velocidad.copy(), self.prev_velocidad.copy()
#         self.difundir(1, self.prev_velocidad[:, :, 0], self.velocidad[:, :, 0], self.viscosidad, self.time_step)
#         self.difundir(2, self.prev_velocidad[:, :, 1], self.velocidad[:, :, 1], self.viscosidad, self.time_step)
#         self.proyectar(self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1], self.velocidad[:, :, 0], self.velocidad[:, :, 1])
#         self.advectar(1, self.velocidad[:, :, 0], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1], self.time_step)
#         self.advectar(2, self.velocidad[:, :, 1], self.prev_velocidad[:, :, 1], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1], self.time_step)
#         self.proyectar(self.velocidad[:, :, 0], self.velocidad[:, :, 1], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1])
#         self.difundir(0, self.prev_dye, self.dye, self.difusion, self.time_step)
#         self.advectar(0, self.prev_dye, self.dye, self.velocidad[:, :, 0], self.velocidad[:, :, 1], self.time_step)

#         return None, self.dye, self.velocidad

#     def advectar(self, b, d, d0, velocX, velocY, dt):
#         dtx = dt * (self.dimension - 2)
#         dty = dt * (self.dimension - 2)

#         for i in range(1, self.dimension - 1):
#             for j in range(1, self.dimension - 1):
#                 tmp1 = dtx * velocX[i, j]
#                 tmp2 = dty * velocY[i, j]
#                 x = i - tmp1
#                 y = j - tmp2

#                 if x < 1.5:
#                     x = 1.5
#                 if x > self.dimension - 1.5:
#                     x = self.dimension - 1.5

#                 i0 = int(x)
#                 i1 = i0 + 1

#                 if y < 1.5:
#                     y = 1.5
#                 if y > self.dimension - 1.5:
#                     y = self.dimension - 1.5

#                 j0 = int(y)
#                 j1 = j0 + 1

#                 s1 = x - i0
#                 s0 = 1 - s1
#                 t1 = y - j0
#                 t0 = 1 - t1

#                 d[i, j] = s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) + s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1])

#         self.set_boundary(b, d)

#     def proyectar(self, velocX, velocY, p, div):
#         for i in range(1, self.dimension - 1):
#             for j in range(1, self.dimension - 1):
#                 div[i, j] = -0.5 * (velocX[i + 1, j] - velocX[i - 1, j] + velocY[i, j + 1] - velocY[i, j - 1]) / self.dimension
#                 p[i, j] = 0
#         self.set_boundary(0, div)
#         self.set_boundary(0, p)
#         self.lin_solve(0, p, div, 1, 6)
#         for i in range(1, self.dimension - 1):
#             for j in range(1, self.dimension - 1):
#                 velocX[i, j] -= 0.5 * (p[i + 1, j] - p[i - 1, j]) * self.dimension
#                 velocY[i, j] -= 0.5 * (p[i, j + 1] - p[i, j - 1]) * self.dimension
#         self.set_boundary(1, velocX)
#         self.set_boundary(2, velocY)

#     def difundir(self, b, x, x0, difusion, dt):
#         a = dt * difusion * (self.dimension - 2) * (self.dimension - 2)
#         self.lin_solve(b, x, x0, a, 1 + 4 * a)

#     def lin_solve(self, b, x, x0, a, c):
#         cRecip = 1.0 / c
#         for i in range(1, self.dimension - 1):
#             for j in range(1, self.dimension - 1):
#                 x[i, j] = (x0[i, j] + a * (x[i - 1, j] + x[i + 1, j] + x[i, j - 1] + x[i, j + 1])) * cRecip
#         self.set_boundary(b, x)

#     def set_boundary(self, b, x):
#         for i in range(1, self.dimension - 1):
#             x[i, 0] = -x[i, 1] if b == 2 else x[i, 1]
#             x[i, self.dimension - 1] = -x[i, self.dimension - 2] if b == 2 else x[i, self.dimension - 2]
#         for j in range(1, self.dimension - 1):
#             x[0, j] = -x[1, j] if b == 1 else x[1, j]
#             x[self.dimension - 1, j] = -x[self.dimension - 2, j] if b == 1 else x[self.dimension - 2, j]

#         x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
#         x[0, self.dimension - 1] = 0.5 * (x[1, self.dimension - 1] + x[0, self.dimension - 2])
#         x[self.dimension - 1, 0] = 0.5 * (x[self.dimension - 2, 0] + x[self.dimension - 1, 1])
#         x[self.dimension - 1, self.dimension - 1] = 0.5 * (x[self.dimension - 2, self.dimension - 1] + x[self.dimension - 1, self.dimension - 2])

import numpy as np
from scipy.ndimage import map_coordinates, spline_filter
from scipy.sparse.linalg import factorized
import scipy.sparse as sp
from functools import reduce
from itertools import cycle
from math import factorial

'''
-------------------------------------------------------
Código basado en: https://github.com/GregTJ/stable-fluids
Modificado para agregar paredes
'''

def diferencia(derivada, precision=1):
    derivada += 1
    radio = precision + derivada // 2 - 1
    puntos = range(-radio, radio + 1)
    coeficientes = np.linalg.inv(np.vander(puntos))
    return coeficientes[-derivada] * factorial(derivada - 1), puntos

def operador(shape, *diferencias):
    diferencias = zip(shape, cycle(diferencias))
    factores = (sp.diags(*diff, shape=(dim,) * 2) for dim, diff in diferencias)
    return reduce(lambda a, f: sp.kronsum(f, a, format='csc'), factores)

class Fluido:
    def __init__(self, shape, *cantidades, orden_presion=1, orden_advect=3):
        self.shape = shape
        self.n_dim = len(shape)  # Cambiado de self.dimension a self.n_dim

        # Se crean dinámicamente las cantidades advectadas según sea necesario.
        self.cantidades = cantidades
        for q in cantidades:
            setattr(self, q, np.zeros(shape))

        self.indices = np.indices(shape)
        self.velocidad = np.zeros((self.n_dim, *shape))

        self.laplaciano = operador(shape, diferencia(2, orden_presion))
        self.solver_presion = factorized(self.laplaciano)

        self.orden_advect = orden_advect

    def paso(self, boundary, paredes=True):
        # La advección se calcula hacia atrás en el tiempo según lo descrito en Stable Fluids.
        mapa_adveccion = self.indices - self.velocidad

        def advect(campo, epsilon_filtro=10e-2, modo='constant'):
            filtrado = spline_filter(campo, order=self.orden_advect, mode=modo)
            campo = filtrado * (1 - epsilon_filtro) + campo * epsilon_filtro
            return map_coordinates(campo, mapa_adveccion, prefilter=False, order=self.orden_advect, mode=modo)

        for d in range(self.n_dim):
            self.velocidad[d] = advect(self.velocidad[d])
            if paredes:  # Podemos detener el fluido o hacer que rebote, aquí lo detenemos
                if d == 0:
                    self.velocidad[d][:, 0] = 0  # Detiene el fluido en los bordes
                    self.velocidad[d][:, -1] = 0  
                else:
                    self.velocidad[d][0, :] = 0  
                    self.velocidad[d][-1, :] = 0  

        for q in self.cantidades:
            setattr(self, q, advect(getattr(self, q)))

        # Calcular el jacobiano en cada punto del campo de velocidad
        forma_jacobiana = (self.n_dim,) * 2
        parciales = tuple(np.gradient(d) for d in self.velocidad)
        jacobiano = np.stack(parciales).reshape(*forma_jacobiana, *self.shape)

        divergencia = jacobiano.trace()

        # Para 3D, el valor del eje y debe negarse.
        mascara_remolino = np.triu(np.ones(forma_jacobiana, dtype=bool), k=1)
        remolino = (jacobiano[mascara_remolino] - jacobiano[mascara_remolino.T]).squeeze()

        # Aplicar la corrección de presión al campo de velocidad
        presion = self.solver_presion(divergencia.flatten()).reshape(self.shape)
        self.velocidad -= np.gradient(presion)

        return divergencia, remolino, presion


class Fluido2:
    def __init__(self, shape, *cantidades):
        self.shape = shape
        self.n_dim = len(shape)  # Cambiado de self.dimension a self.n_dim

        self.dye = np.zeros(shape)
        self.velocidad = np.zeros((2, shape[0], shape[1]))

        self.difusion = 0.001
        self.viscosidad = 0
        self.time_step = 1

        self.indices = np.indices(shape)

        self.prev_dye = np.zeros(shape)
        self.prev_velocidad = np.zeros((2, shape[0], shape[1]))

    def paso(self, boundary, paredes=True):
        self.prev_velocidad, self.velocidad = self.velocidad.copy(), self.prev_velocidad.copy()
        self.difundir(1, self.prev_velocidad[:, :, 0], self.velocidad[:, :, 0], self.viscosidad, self.time_step)
        self.difundir(2, self.prev_velocidad[:, :, 1], self.velocidad[:, :, 1], self.viscosidad, self.time_step)
        self.proyectar(self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1], self.velocidad[:, :, 0], self.velocidad[:, :, 1])
        self.advectar(1, self.velocidad[:, :, 0], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1], self.time_step)
        self.advectar(2, self.velocidad[:, :, 1], self.prev_velocidad[:, :, 1], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1], self.time_step)
        self.proyectar(self.velocidad[:, :, 0], self.velocidad[:, :, 1], self.prev_velocidad[:, :, 0], self.prev_velocidad[:, :, 1])
        self.difundir(0, self.prev_dye, self.dye, self.difusion, self.time_step)
        self.advectar(0, self.prev_dye, self.dye, self.velocidad[:, :, 0], self.velocidad[:, :, 1], self.time_step)

        return None, self.dye, self.velocidad

    def advectar(self, b, d, d0, velocX, velocY, dt):
        dtx = dt * (self.shape[0] - 2)
        dty = dt * (self.shape[1] - 2)

        for i in range(1, self.shape[0] - 1):
            for j in range(1, self.shape[1] - 1):
                tmp1 = dtx * velocX[i, j]
                tmp2 = dty * velocY[i, j]
                x = i - tmp1
                y = j - tmp2

                if x < 1.5:
                    x = 1.5
                if x > self.shape[0] - 1.5:
                    x = self.shape[0] - 1.5

                i0 = int(x)
                i1 = i0 + 1

                if y < 1.5:
                    y = 1.5
                if y > self.shape[1] - 1.5:
                    y = self.shape[1] - 1.5

                j0 = int(y)
                j1 = j0 + 1

                s1 = x - i0
                s0 = 1 - s1
                t1 = y - j0
                t0 = 1 - t1

                d[i, j] = s0 * (t0 * d0[i0, j0] + t1 * d0[i0, j1]) + s1 * (t0 * d0[i1, j0] + t1 * d0[i1, j1])

        self.set_boundary(b, d)

    def proyectar(self, velocX, velocY, p, div):
        for i in range(1, self.shape[0] - 1):
            for j in range(1, self.shape[1] - 1):
                div[i, j] = -0.5 * (velocX[i + 1, j] - velocX[i - 1, j] + velocY[i, j + 1] - velocY[i, j - 1]) / self.shape[0]
                p[i, j] = 0
        self.set_boundary(0, div)
        self.set_boundary(0, p)
        self.lin_solve(0, p, div, 1, 6)
        for i in range(1, self.shape[0] - 1):
            for j in range(1, self.shape[1] - 1):
                velocX[i, j] -= 0.5 * (p[i + 1, j] - p[i - 1, j]) * self.shape[0]
                velocY[i, j] -= 0.5 * (p[i, j + 1] - p[i, j - 1]) * self.shape[0]
        self.set_boundary(1, velocX)
        self.set_boundary(2, velocY)

    def difundir(self, b, x, x0, difusion, dt):
        a = dt * difusion * (self.shape[0] - 2) * (self.shape[1] - 2)
        self.lin_solve(b, x, x0, a, 1 + 4 * a)

    def lin_solve(self, b, x, x0, a, c):
        cRecip = 1.0 / c
        for i in range(1, self.shape[0] - 1):
            for j in range(1, self.shape[1] - 1):
                x[i, j] = (x0[i, j] + a * (x[i - 1, j] + x[i + 1, j] + x[i, j - 1] + x[i, j + 1])) * cRecip
        self.set_boundary(b, x)

    def set_boundary(self, b, x):
        for i in range(1, self.shape[0] - 1):
            x[i, 0] = -x[i, 1] if b == 2 else x[i, 1]
            x[i, self.shape[1] - 1] = -x[i, self.shape[1] - 2] if b == 2 else x[i, self.shape[1] - 2]
        for j in range(1, self.shape[1] - 1):
            x[0, j] = -x[1, j] if b == 1 else x[1, j]
            x[self.shape[0] - 1, j] = -x[self.shape[0] - 2, j] if b == 1 else x[self.shape[0] - 2, j]

        x[0, 0] = 0.5 * (x[1, 0] + x[0, 1])
        x[0, self.shape[1] - 1] = 0.5 * (x[1, self.shape[1] - 1] + x[0, self.shape[1] - 2])
        x[self.shape[0] - 1, 0] = 0.5 * (x[self.shape[0] - 2, 0] + x[self.shape[0] - 1, 1])
        x[self.shape[0] - 1, self.shape[1] - 1] = 0.5 * (x[self.shape[0] - 2, self.shape[1] - 1] + x[self.shape[0] - 1, self.shape[1] - 2])
