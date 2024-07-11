# donde-ta-la-bolsa
DondeTaLaBolsa: Basic tool to report bags not available from BrainHi pdf report.

## Build

Built for win11 but can work for other systems (just rebuild for that target). 

1. Install dependencies using pip:

```
pip install -r requirements.txt
```

2. Build using `pyinstaller`

```
pyinstaller --onefile --hidden-import=fitz --hidden-import=pymupdf --hidden-import=tabulate --hidden-import=argparse --hidden-import=os main.py
```

3. Run from command prompt

```
 main.exe [-h] [-p PATH] [-d] [-n NUMBER_TOTAL]
```
