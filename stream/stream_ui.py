import tkinter as tk
import sounddevice as sd
import numpy as np
from threading import Thread, Event

class StreamThread(Thread):
    def __init__(self):
        super().__init__()
        self.dispositivo_input = 1
        self.dispositivo_output = 3
        self.tamano_bloque = 5500
        self.canales = 1
        self.tipo_dato = np.int16
        self.latencia = "high"
        self.frecuencia_muestreo = 44100
    
    def callback_stream(self, indata, outdata, frames, time, status):
        global app
        app.etiqueta_valor_estado["text"] = "Grabando"
        return

    def run(self):
        try:
            self.event = Event()
            with sd.Stream(
                device = (self.dispositivo_input, self.dispositivo_output),
                blocksize = self.tamano_bloque,
                samplerate = self.frecuencia_muestreo,
                channels = self.canales,
                dtype = self.tipo_dato,
                latency = self.latencia,
                callback = self.callback_stream

            ) as self.stream: 
                self.event.wait()

        except Exception as e:
            print(str(e))

# Heredamos de Tk para hacer una ventana
class App(tk.Tk):
    def _init_(self):
        super()._init_()
        # Establecer titulo de la ventana
        self.title("Aplicación de audio")
        # Establecemos tamaño
        self.geometry("400x300")

        #Iniciar Boton
        boton_iniciar = tk.Button(self, 
            width = 20, text = "Iniciar grabación",
            command = lambda: self.click_boton_iniciar())
        #Boton Funcional
        boton_iniciar.grid(column = 0, row = 0)

        boton_detener = tk.Button(self, 
            width = 20, text = "Detener grabación",
            command = lambda: self.click_boton_detener())
        boton_detener.grid(column = 1, row = 0)

        etiqueta_estado = tk.Label(text = "Estado: ")
        etiqueta_estado.grid(column = 0, row = 1)

        self.etiqueta_valor_estado = tk.Label(text = "- ")
        self.etiqueta_valor_estado.grid(column = 1, row = 1)

        self.stream_thread = StreamThread()
    
    def click_boton_detener(self):
        if self.stream_thread.is_alive():
            self.etiqueta_valor_estado["text"] = "Grabación Detenida" 
            self.stream_thread.stream.abort()
            self.stream_thread.event.set()
            self.stream_thread.join()
            
    def click_boton_iniciar(self):
        if not self.stream_thread.is_alive():
            self.stream_thread.daemon = True
            self.stream_thread.start()
           
app = App()

def main():
    global app
    app.mainloop()

if __name__ == "__main__":
    main()
