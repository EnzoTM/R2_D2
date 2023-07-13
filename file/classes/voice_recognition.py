import speech_recognition as sr


#é o código para saber os microfones disponíveis
"""for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))"""


class voice_recognition:
    def __init__(self) -> None:
        self.audio = None
        

    def vr(self, voice_index):
        """
        retorna oq a pessoa disse
        """
        microfone = sr.Recognizer()
        
        try:
            #devide_index=1 é o microfone que está sendo usado para receber o áudio
            with sr.Microphone(device_index=voice_index) as source:
                print("Diga algo:")
                #para ajustar o áudio com o ambinete, coloquei duração de 0.2, pois foi a melhor q eu achei
                microfone.adjust_for_ambient_noise(source, duration=0.2)

                #pegar o áudio em forma de ondas
                audio = microfone.listen(source)

                #usar a iA da google para passar essas ondas em textos que nós possamos entender
                self.audio = microfone.recognize_google(audio, language="pt-br")

                #retornar True, pois não deu nenhum erro
                return self.audio

        except sr.UnknownValueError:
            #retornar False, pois deu algum erro
            self.vr(voice_index)