#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 24 09:51:25 2025

@author: ces
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from itertools import product
import pandas as pd
import os

# Parámetros base
M_p = 1.0
k = 0.00
c = 1.0
kappa=1

# Sistema de ecuaciones
def sistema(t, y, V_0, m3, nu):
    a, adot, phi, phidot, theta, thetadot = y
    addot = kappa**2*a*(V_0*(1- phi**2/nu**2)**2+m3**3*theta)- 2*adot**2/a-2*c**2*k/a
    phiddot = 2*c**2*phi*V_0/nu**2*(1-phi**2/nu**2)-3*adot*phidot/a
    thetaddot = -2*c**2*(m3)-3*adot*thetadot/a
    return [adot, addot, phidot, phiddot, thetadot, thetaddot]

def buscar_parametros():
    ranges = {
        'a0': np.logspace(-8, -1, 5),
        'adot0': np.logspace(-4, -1, 5),
        'phi0': np.logspace(-1, 1, 3),
        'phidot0': np.logspace(-1, 1, 3),
        'theta0': np.logspace(-1, 1, 3),
        'thetadot0': np.logspace(-10, -1, 3),
        'V_0': np.logspace(-6, 0, 5),
        'm3': np.logspace(-6, 0, 5),
        'nu': np.logspace(-6, 0, 5)
    }

    results_df = pd.DataFrame(columns=list(ranges.keys()) + ['ln_a_ratio', 'success'])
    target = 60
    tolerance = 5

    for i, vals in enumerate(product(*ranges.values())):
        params = dict(zip(ranges.keys(), vals))
        y0 = [params['a0'], params['adot0'], params['phi0'], 
              params['phidot0'], params['theta0'], params['thetadot0']]
        
        sol = solve_ivp(
            lambda t, y: sistema(t, y, params['V_0'], params['m3'], params['nu']),
            t_span=(0, 1100),
            y0=y0,
            t_eval=np.linspace(0, 1100, 1000),
            method='RK45'
        )
        
        if not sol.success:
            continue
        
        a_ratio = np.log(sol.y[0][-1] / sol.y[0][0])
        
        if i % 100 == 0:
            print(f"Iteración {i}: ln(a_ratio) = {a_ratio:.2f}")
        
        if abs(a_ratio - target) <= tolerance:
            results_df.loc[len(results_df)] = {**params, 'ln_a_ratio': a_ratio, 'success': True}
            print(f"\n✅ Combinación encontrada! (Total: {len(results_df)})")
            print(f"ln(a_final/a_inicial) = {a_ratio:.2f}")

    if len(results_df) > 0:
        results_df.to_csv('resultados_exitosos.csv', index=False)
        print("\n🌟 Resumen de combinaciones exitosas:")
        print(results_df)
        return results_df
    else:
        print("No se encontraron combinaciones válidas.")
        return None

def graficar_desde_csv(filename='resultados_exitosos.csv'):
    if not os.path.exists(filename):
        print(f"Archivo {filename} no encontrado.")
        return
    
    df = pd.read_csv(filename)
    if df.empty:
        print("El DataFrame está vacío.")
        return
    
    for _, row in df.iterrows():
        graficar_solucion(row.to_dict())

def graficar_manual():
    print("\nIngrese los parámetros manualmente:")
    params = {
        'a0': float(input("a0 (ej. 1e-12): ")),
        'adot0': float(input("adot0 (ej. 1e-8): ")),
        'phi0': float(input("phi0 (ej. 1.0): ")),
        'phidot0': float(input("phidot0 (ej. 0.1): ")),
        'theta0': float(input("theta0 (ej. 1.0): ")),
        'thetadot0': float(input("thetadot0 (ej. 1e-12): ")),
        'V_0': float(input("V_0 (ej. 1e-2): ")),
        'm3': float(input("m3 (ej. 1e-12): ")),
        'nu': float(input("nu (ej. 1.0): "))
    }
    
    graficar_solucion(params)

def graficar_solucion(params):
    y0 = [params['a0'], params['adot0'], params['phi0'], 
          params['phidot0'], params['theta0'], params['thetadot0']]
    
    sol = solve_ivp(
        lambda t, y: sistema(t, y, params['V_0'], params['m3'], params['nu']),
        t_span=(0, 1100),
        y0=y0,
        t_eval=np.linspace(0, 1100, 1000),
        method='RK45'
    )
    
    if sol.success:
        a_ratio = np.log(sol.y[0][-1] / sol.y[0][0])
        print(f"\nln(a_final/a_inicial) = {a_ratio:.2f}")
        
        plt.figure(figsize=(14, 6))
        
        # Gráfica de a(t) en escala logarítmica
        plt.subplot(1, 3, 1)
        plt.plot(sol.t, sol.y[0], 'b-')
        plt.yscale('log')
        plt.xlabel('Tiempo')
        plt.ylabel('a(t) (log)')
        plt.title('Evolución de a(t)')
        plt.grid(True)
        
        # Gráfica de phi(t)
        plt.subplot(1, 3, 2)
        plt.plot(sol.t, sol.y[2], 'r-')
        plt.xlabel('Tiempo')
        plt.ylabel('φ(t)')
        plt.title('Evolución de φ(t)')
        plt.grid(True)
        
        # Gráfica de theta(t)
        plt.subplot(1, 3, 3)
        plt.plot(sol.t, sol.y[4], 'g-')
        plt.xlabel('Tiempo')
        plt.ylabel('θ(t)')
        plt.title('Evolución de θ(t)')
        plt.grid(True)
        
        plt.suptitle(f"Parámetros:\n"
                    f"a0={params['a0']:.2e}, V_0={params['V_0']:.2e}, m3={params['m3']:.2e}\n"
                    f"ln(a_final/a_inicial) = {a_ratio:.2f}")
        plt.tight_layout()
        plt.show()
    else:
        print("La solución no convergió. Intente con otros parámetros.")

def main():
    while True:
        print("\nMENU PRINCIPAL")
        print("1. Buscar nuevos parámetros automáticamente")
        print("2. Graficar desde archivo existente")
        print("3. Ingresar parámetros manualmente para graficar")
        print("4. Salir")
        
        opcion = input("Seleccione una opción (1-4): ")
        
        if opcion == '1':
            resultados = buscar_parametros()
            if resultados is not None:
                if input("¿Desea graficar los resultados? (s/n): ").lower() == 's':
                    graficar_desde_csv()
        elif opcion == '2':
            graficar_desde_csv()
        elif opcion == '3':
            graficar_manual()
        elif opcion == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()