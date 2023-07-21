import os

import subprocess


def clear_console():
    # Limpia la consola dependiendo del sistema operativo
    os.system("cls" if os.name == "nt" else "clear")


def input_file_or_sheet_names(file_or_sheet_name):
    confirmation = False
    while confirmation == False:
        print(
            f'Por favor, inserte el nombre {file_or_sheet_name} {"(sin .xlsx)" if file_or_sheet_name == "del archivo" else ""}'
        )

        name = input()
        print(
            f'Has introducido: "{name}". ¿Es correcto? (presione "s" para confirmar o cualquier otra tecla para volver a introducir el nombre.)'
        )
        confirm = input().lower()
        if confirm == "s":
            confirmation = True
    return name


def execute_node():
    subprocess.run(["node", "./src/automatizedMail.js"])
    # os.system("node ./automatizedMail.js")
