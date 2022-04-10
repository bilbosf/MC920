import sys
from skimage import io
import numpy as np
from matplotlib import pyplot as plt

if(len(sys.argv) != 3):
    print('Modo de uso: $python codificar.py imagem_entrada.png texto_entrada.txt')
    exit()

img_path, text_path = sys.argv[1:3]

img = io.imread(img_path)
pbits_before = [((img & (1 << i)) >> i) * 255 for i in range(8)]

# Limpeza dos bits que serão usados na esteganografia
img[:,:,0] &= 0b11111000
img[:,:,1] &= 0b11111000
img[:,:,2] &= 0b11111100

pixel_amount = img.size // 3

# https://www.lionking.org/scripts/Script.txt
data = np.fromfile(text_path, dtype=np.uint8)
data = np.append(data, ord('%')).astype(np.uint8) # Caractere de determinação de fim de arquivo

r_mask = (data & (0b111 << 5)) >> 5
g_mask = (data & (0b111 << 2)) >> 2
b_mask = data & 0b11

dimensions = img.shape[:2]

r_mask.resize(pixel_amount)
g_mask.resize(pixel_amount)
b_mask.resize(pixel_amount)

# Adição da mensagem na imagem
img[:,:,0] |= r_mask.reshape(dimensions)
img[:,:,1] |= g_mask.reshape(dimensions)
img[:,:,2] |= b_mask.reshape(dimensions)

io.imsave(img_path[:-4] + '_hidden.png', img)

pbits_after = [((img & (1 << i)) >> i) * 255 for i in range(8)]

io.imshow_collection(pbits_before, 'matplotlib')
plt.show()

io.imshow_collection(pbits_after, 'matplotlib')
plt.show()
 