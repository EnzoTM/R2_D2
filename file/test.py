from classes.language import language
import os

ai = language(training=True, arquivo=os.path.join(os.getcwd(), "file", "arquivos", "padrao.json"), file_words=os.path.join(os.getcwd(), "file", "arquivos", "words.txt"), file_classes=os.path.join(os.getcwd(), "file", "arquivos", "classes.txt"), file_model=os.path.join(os.getcwd(), "file", "arquivos", "models", "model"))

ai.load()

input_, output = ai.load_training()

ai.create_model(input_, output)