import os

from classes.language import language

model = language(arquivo=os.path.join(os.getcwd(), "arquivos", "padrao.json"), file_words=os.path.join(os.getcwd(), "arquivos", "words.txt"), file_classes=os.path.join(os.getcwd(), "arquivos", "classes.txt"), file_model=os.path.join(os.getcwd(), "arquivos", "models", "model"))

model.load_files()

classe = model.get_classe("perdi meu teclado")

print(classe)