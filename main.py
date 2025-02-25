import sys
import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QSpinBox, QCheckBox, QTextEdit

class BolsaChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("DondeTaLaBolsa GUI")
        self.setGeometry(100, 100, 600, 400)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("No se ha seleccionado un archivo PDF")
        layout.addWidget(self.label)
        
        self.file_button = QPushButton("Seleccionar PDF")
        self.file_button.clicked.connect(self.load_pdf)
        layout.addWidget(self.file_button)
        
        self.replace_button = QPushButton("Reemplazar PDF")
        self.replace_button.clicked.connect(self.load_pdf)
        self.replace_button.setVisible(False)
        layout.addWidget(self.replace_button)
        
        self.n_label = QLabel("Número máximo (N):")
        layout.addWidget(self.n_label)
        
        self.n_spinbox = QSpinBox()
        self.n_spinbox.setMinimum(100)
        self.n_spinbox.setMaximum(10000)
        self.n_spinbox.setValue(700)
        layout.addWidget(self.n_spinbox)
        
        self.display_check = QCheckBox("Mostrar bolsas disponibles y su cantidad")
        layout.addWidget(self.display_check)
        
        self.save_check = QCheckBox("Guardar resultados en CSV")
        layout.addWidget(self.save_check)
        
        self.run_button = QPushButton("Ejecutar")
        self.run_button.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_button)
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        self.setLayout(layout)
        self.pdf_path = ""
    
    def load_pdf(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_path:
            self.pdf_path = file_path
            self.label.setText(f"Archivo seleccionado: {os.path.relpath(file_path)}")
            self.file_button.setVisible(False)
            self.replace_button.setVisible(True)
        else:
            self.label.setText("No se ha seleccionado un archivo PDF")
            self.file_button.setVisible(True)
            self.replace_button.setVisible(False)
    
    def run_analysis(self):
        if not self.pdf_path:
            self.result_text.setText("Error: No se ha seleccionado un archivo PDF.")
            return
        
        num_list = self.read_pdf_line_by_line(self.pdf_path)
        occurrences_dict = self.count_occurrences(num_list)
        
        if self.display_check.isChecked():
            result_str = "Bolsas encontradas y sus cantidades:\n"
            result_str += "\n".join([f"Bolsa {k}: {v} veces" for k, v in occurrences_dict.items()])
        else:
            result_str = ""
        
        N = self.n_spinbox.value()
        vals_missing = self.vals_missing_from_list(num_list, N)
        result_str += f"\n\nBolsas no disponibles ({len(vals_missing)}/{N}):\n{vals_missing}"
        
        if self.save_check.isChecked():
            save_path = self.pdf_path.replace(".pdf", "_resultado.csv")
            if self.check_and_ask_overwrite(save_path):
                try:
                    with open(save_path, 'w') as f:
                        f.write("bolsa_no_existe\n")
                        f.write("\n".join(map(str, vals_missing)))
                    result_str += f"\n\nResultados guardados en: {save_path}"
                except PermissionError:
                    result_str += "\n\nERROR! No se pudo guardar el archivo."
        
        self.result_text.setText(result_str)
    
    def read_pdf_line_by_line(self, pdf_path):
        pdf_document = fitz.open(pdf_path)
        num_list = []
        for page in pdf_document:
            lines = page.get_text("text").splitlines()
            for line in lines:
                try:
                    num_list.append(int(line))
                except ValueError:
                    pass
        return num_list
    
    def vals_missing_from_list(self, number_list, N):
        number_list = list(set(number_list))  # remove duplicates
        full_set = set(range(100, N + 1))
        given_set = set(number_list)
        return sorted(full_set - given_set)
    
    def count_occurrences(self, number_list):
        occurrence_dict = {}
        for number in number_list:
            str_number = str(number)
            occurrence_dict[str_number] = occurrence_dict.get(str_number, 0) + 1
        return occurrence_dict
    
    def check_and_ask_overwrite(self, filepath):
        if os.path.exists(filepath):
            return True  # Always overwrite in GUI mode
        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BolsaChecker()
    ex.show()
    sys.exit(app.exec_())
