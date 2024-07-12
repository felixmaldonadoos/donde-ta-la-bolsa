# donde-ta-la-bolsa
DondeTaLaBolsa: Basic tool to report bags not available from BrainHi pdf report.

## Usage

### Help menu 

Print help menu and example usge using the following command: 

```main.exe -h``` 

Output: 

```

++ DondeTaLaBolsa v1.0 | Ultima actualización: 2024-07-10 | Escrito por: Alexander M. ++
Para ver como usar el programa, usa el argumento -h o --help.
usage: main.py [-h] [-p PATH] [-d] [-n NUMBER_TOTAL] [-s] [-sp PATH_SAVE]

Verifica e imprime lista de numeros no disponibles en reporte (.pdf) de bolsas empezando en 100 hasta numero pasado con -n (default 700) .

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Setea la ubicación del archivo de archivo. (default: bolsa.pdf)
  -d, --display_found   Imprime cuales bolsas hay disponibles y su cantidad.
  -n NUMBER_TOTAL, --number_total NUMBER_TOTAL
                        Setea numero total de archivos para comparar (default: 700)
  -s, --guardar_lista   Guarda la lista de bolsas no encontradas en pdf a un archivo
                        "resultado.csv".
  -sp PATH_SAVE, --path_save PATH_SAVE
                        Setea la ubicación del archivo de salida. Si no pasas "-s" como argumento,
                        no se va a guardar el archivo. (default: resultado.csv)

Ejemplo de uso:
1) main.exe -p bolsa.pdf
2) main.exe -n 1000 -d -s -sp resultado.csv

```

### Use default pdf file 

```main.exe```

### Use default pdf file and save results to pdf 

Use default filename of `bolsa.pdf` by simply running 

```main.exe -s```. 

### Define specific filepath and save results as csv to working directory 

```main.exe -s -p <path/to/document.pdf>```


## Build from source 

Built for win11 but can work for other systems (just rebuild for that target). 

1. Install dependencies using pip:

```
pip install -r requirements.txt
```

2. Build for windows using `.bat`

```
.\build.bat
```

3. Run from command prompt

```
main.exe [-h] [-p PATH] [-d] [-n NUMBER_TOTAL] [-s] [-sp PATH_SAVE]
```
