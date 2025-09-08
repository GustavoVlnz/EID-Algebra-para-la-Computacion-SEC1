import sys
from analisis_funciones import calcular_dominio, calcular_intersecciones, evaluar_punto
from visualizacion_graficos import generar_grafico

def main():
    print("--- Analizador de Funciones ---")
    
    # campo para ingresar la funcion
    funcion_str = input("Ingrese una función (ej. 2*x**2 + 2*x): ")
    if not funcion_str:
        print("Debe ingresar una función. Saliendo...")
        sys.exit()

    # campo opcional para ingresar un valor a evaluar
    valor_x_str = input("Ingrese un valor para evaluar (opcional): ")

    try:
        # calcular y mostrar el dominio y las intersecciones
        dominio = calcular_dominio(funcion_str)
        y_int, x_int = calcular_intersecciones(funcion_str)
        
        print("\n--- Resultados del Análisis Matemático ---")
        print(f"Dominio: {dominio}")
        print(f"Intersección con el Eje Y: {y_int}")
        print(f"Intersección con el Eje X: {x_int}")

        punto_resultante = None
        # evaluar el punto si se ingreso un valor
        if valor_x_str:
            paso_a_paso, punto = evaluar_punto(funcion_str, valor_x_str)
            print("\n--- Evaluación del Punto ---")
            print(paso_a_paso)
            if punto:
                punto_resultante = punto
        
        # funcion importada para generar el grafico
        generar_grafico(funcion_str, punto_evaluado=punto_resultante)

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()