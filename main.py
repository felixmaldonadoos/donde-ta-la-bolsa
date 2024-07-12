import fitz  # PyMuPDF
from tabulate import tabulate
import argparse 
import os 
import pandas as pd

def read_pdf_line_by_line(pdf_path:str=None)->list:
    
    if not pdf_path.lower().endswith('.pdf'): 
        print(f"-Error! Documento no es .pdf ({pdf_path})")

    pdf_document = fitz.open(pdf_path)
    num_list = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text("text")

        lines = text.splitlines()

        for line in lines:
            try: 
                num_list.append(int(line))
            except ValueError:
                pass

    return num_list

def vals_missing_from_list(number_list:list=None, N:int=None)->list:
    if number_list is None:
        print("number_list=None, returning None")
        return None
    if N is None: 
        print('N is None, returning')
        return None

    number_list = list(set(number_list)) # remove dupes 

    full_set = set(range(100, N + 1))
    given_set = set(number_list)
    l = list(full_set-given_set)
    l.sort()

    return l 

def check_and_ask_overwrite(filepath):
    if os.path.exists(filepath):
        response = input(f"WARNING: Documento '{filepath}' ya existe. Presiona 'y' para reemplazar y cualquier otro para abortar: ").strip().lower()
        if response != 'y':
            return False
    return True

def print_dict_as_table(occurrence_dict: dict):
    table = [(k, v) for k, v in occurrence_dict.items()]
    print(tabulate(table, headers=["Bolsa", "Cantidad"], tablefmt="grid"))

def count_occurrences(number_list: list) -> dict:
    occurrence_dict = {}

    for number in number_list:
        str_number = str(number)
        if str_number in occurrence_dict:
            occurrence_dict[str_number] += 1
        else:
            occurrence_dict[str_number] = 1

    return occurrence_dict

def _intro_():
    print("\n++ DondeTaLaBolsa v1.0 | Ultima actualización: 2024-07-10 | Escrito por: Alexander M. ++\nPara ver como usar el programa, usa el argumento -h o --help.")

def set_args():

    path_def = 'bolsa.pdf'
    N_def = 700
    path_save_def = 'resultado.csv'

    parser = argparse.ArgumentParser(description="Verifica e imprime lista de numeros no disponibles en reporte (.pdf) de bolsas empezando en 100 hasta numero pasado con -n (default 700) .",
                                        epilog=f"Ejemplo de uso: \n1) main.exe -p {path_def}\n2) main.exe -n 1000 -d -s -sp {path_save_def}",
                                            formatter_class=argparse.RawDescriptionHelpFormatter)
    # Define flags
    parser.add_argument('-p',  '--path', type=str, default=path_def,help=f'Setea la ubicación del archivo de archivo. (default: {path_def})')
    parser.add_argument('-d',  '--display_found',          action='store_true', help=f'Imprime cuales bolsas hay disponibles y su cantidad.')
    parser.add_argument('-n',  '--number_total',           type=int, default=N_def, help=f'Setea numero total de archivos para comparar (default: {N_def})')
    parser.add_argument('-s',  '--guardar_lista',          action='store_true', help=f'Guarda la lista de bolsas no encontradas en pdf a un archivo "{path_save_def}".')
    parser.add_argument('-sp', '--path_save',              type=str, default=path_save_def, help=f'Setea la ubicación del archivo de salida. Si no pasas "-s" como argumento, no se va a guardar el archivo. (default: {path_save_def})')
    # Parse arguments
    args = parser.parse_args()
    print(f"\nArgumentos: Documento: {args.path} | Cantidad bolsas: {args.number_total} | Imprime disponibles: {args.display_found} | Guarda resultados: {args.guardar_lista}")
    return args 

def main():
    _intro_()
    args = set_args()
    if args is None: print("ERROR! Argumentos no son validos (main()). Cerrando el programa."); return
    if args.number_total is None: args.number_total = 700
    if not os.path.isfile(args.path): print(f"\nError! File not found! {args.path}"); return

    # get list of numbers found and dict w/ occurrences 
    num_list = read_pdf_line_by_line(args.path)
    occurrences_dict = count_occurrences(num_list) 
    
    # print occurrence table if flag is passed 
    if args.display_found: print_dict_as_table(occurrences_dict)

    vals_missing = vals_missing_from_list(num_list, args.number_total) # unique vals not found in full list 
    if vals_missing is None: print("vals_missing is None"); return

    print(f'\nBolsas no disponibles ({len(vals_missing)}/{args.number_total}):\n {vals_missing}')
    
    if args.guardar_lista and len(vals_missing) > 0:
        print(f"\nGuardando lista de bolsas no encontradas en pdf a {args.path_save}")
        df_vals_missing = pd.DataFrame(vals_missing, columns=['bolsa_no_existe'])
        if check_and_ask_overwrite(args.path_save):
            try:
                df_vals_missing.to_csv(args.path_save, index=False)
            except PermissionError:
                print("ERROR! No tienes permiso para guardar el archivo. Intenta correr con administrador (Right-Click al .exe y presiona 'Run as administrator').")
            print("Documento guardado bien :)")
        else:
            print("Documento no guardado :( ")
    print("Fin del programa.")

if __name__ == '__main__':
    main()