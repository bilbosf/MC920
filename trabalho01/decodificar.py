import sys
from skimage import io
import numpy as np

if(len(sys.argv) != 3):
    print('Modo de uso: $python decodificar.py imagem_entrada.png texto_saida.txt')
    exit()

img_path, output_path = sys.argv[1:3]

img = io.imread(img_path)

r_data = (img[:,:,0] & 0b00000111).flatten()
g_data = (img[:,:,1] & 0b00000111).flatten()
b_data = (img[:,:,2] & 0b00000011).flatten()

data = (r_data << 5) + (g_data << 2) + b_data
eof = np.where(data == ord('%'))[0][0] # Determinação do fim da mensagem
data = data[:eof]

with open(output_path, 'wb') as text_file:
    text_file.write(data)