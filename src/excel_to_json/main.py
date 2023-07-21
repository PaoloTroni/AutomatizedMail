# importamos las librerías necesarias
import os
import pandas as pd  # pandas, en ese caso sirve para leer los datos desde excel
import json  # json es una librería para manejar datos json en python.
import time  # La biblioteca time proporciona funciones para trabajar con el tiempo y la medición del tiempo en un programa.

# funciones de la aplicación
from utilities import clear_console, input_file_or_sheet_names, execute_node

clear_console()
print(
    "\n--- Bienvenido a la aplicación para envíos de email personalizados y automatizados ---\n"
)

time.sleep(1)

print(
    "La aplicación está desarrollada para funcionar con datos de archivos excel con extensión .xlsx\n"
)
time.sleep(1)

# pedimos al usuario el nombre del archivo excel

file_name = input_file_or_sheet_names("del archivo")
# Obtenemos la ruta del directorio dos niveles arriba del directorio actual
two_levels_up = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Construimos la ruta completa al archivo Excel en el directorio dos niveles arriba
path_excel_file = os.path.join(two_levels_up, file_name + ".xlsx")
print("Archivo ubicado en:", path_excel_file)

print("Seguimos adelante...")
time.sleep(3)
clear_console()

# pedimos al usuario el nombre de la hoja donde están ubicados los datos que nos interesa.
time.sleep(1)
print(
    '\nLa aplicación enviará emails con los siguientes datos personalizados: "nombre de la empresa", "nombre del responsable de la empresa", "dirección de email de la empresa".'
)
time.sleep(1)

print(
    '\nPor definición, estos datos deben estar respectivamente en las columnas "B", "C" y "D" y a partir de la fila "2" del archivo de excel.'
)
time.sleep(1)
print(
    '\nSi los datos no están en este formato te rogamos que presiones "CTRL + C" para cerrar la aplicación y vuelvas cuando los datos estén formateados correctamente.\n'
)
time.sleep(1)


sheet_name = input_file_or_sheet_names("de la hoja")
print("Nombre de la hoja:", sheet_name)

file = None  # declaramos la variable "file" para que después se gestione correctamente el bloque "finally"

# Con Pandas podemos acceder a los datos del excel, según los parámetros que pasamos. Se creará un DataFrame con los datos
try:
    excel_destinatarios = pd.read_excel(
        path_excel_file,  # ubicación del excel
        sheet_name,  # nombre de la hoja
        header=0,  # fila que será el encabezado, accederemos a los datos a partir de la siguiente fila
        usecols="B:D",  # rango de columnas
        names=[
            "nombreEmpresa",
            "nombreResponsable",
            "email",
        ],  # nombre de las columnas resultantes
        nrows=50,  # número de filas que deseamos incluir
        dtype=str,  # tipo de datos
    )
    # Pasamos el dataframe resultante a un archivo JSON con el método .to_json de Pandas
    destinatarios_json = excel_destinatarios.to_json(
        orient="records", force_ascii=False
    )

    # Al especificar orient="records" y force_ascii=False, estamos solicitando que se genere un JSON donde cada registro (fila) del DataFrame se convierta en un objeto JSON separado y que los caracteres no ASCII se mantengan sin cambios en la salida JSON.

    # Generamos el archivo json con los datos:

    filename = (
        "./src/destinatarios.json"  # Guardamos el nombre del archivo en una variable
    )

    # Se utiliza la función open() para abrir el archivo en modo de escritura. El primer argumento es el nombre del archivo y el segundo argumento, "w", indica que se abrirá en modo de escritura.
    file = open(filename, "w")

    # Se crea un objeto "file" que representa el archivo abierto. Este objeto se utilizará para realizar operaciones de escritura en el archivo.
    file.write(destinatarios_json)

    print(f"Archivo {filename} creado (o actualizado) satisfactoriamente")
    print("\nProcesando...")
    file.close()  # HAY QUE CERRAR EL ARCHIVO, EN CASO CONTRARIO, PYTHON TIENE EL ARCHIVO ABIERTO Y NO DEJA QUE NODE LO LEA
    # AUNQUE QUE QUIZAS NO SEA NECESARIO, DEJAMOS ALGO DE TIEMPO ANTES DE LLAMAR A LA FUNCION QUE EJECUTA NODE
    time.sleep(5)

    execute_node()  # llamamos a la función que "hace la magia" ESA FUNCION TIENE QUE LLAMARSE AQUI Y NO DESPUES DE FINALLY, PORQUE EN CASO DE ERROR, PUEDE QUE MANDE LOS EMAILS A DATOS QUE NO SON ACTUALIZADOS O INCORRECTOS

except Exception as e:
    print("\nOcurrió un error:", str(e), "\n")


finally:
    # El código dentro de este bloque se ejecutará siempre, independientemente de si ocurre un error o no.
    # Cerramos el archivo para asegurar que los recursos del sistema se liberen adecuadamente.
    if file is not None:
        file.close()
    time.sleep(5)
    print(
        '\nLa operación se ha finalizado. Presione "1" para finalizar o espere 60 segundos y la consola se despejará sola.'
    )
    final = input()
    if final == "1":
        clear_console()
    else:
        time.sleep(60)
        clear_console()
