import sys
from skimage import io
import numpy as np
from matplotlib import pyplot as plt

if(len(sys.argv) != 4):
    print('Modo de uso: $python codificar.py imagem_entrada.png texto_entrada.txt imagem_saida.png')
    exit()

img_path, text_path, output_path = sys.argv[1:4]

img = io.imread(img_path)
pbits_before_r = [((img[:,:,0] & (1 << i)) >> i) * 255 for i in [7, 2, 1, 0]]
pbits_before_g = [((img[:,:,1] & (1 << i)) >> i) * 255 for i in [7, 2, 1, 0]]
pbits_before_b = [((img[:,:,2] & (1 << i)) >> i) * 255 for i in [7, 2, 1, 0]]

# https://www.lionking.org/scripts/Script.txt
data = np.fromfile(text_path, dtype=np.uint8)
data = np.append(data, ord('%')).astype(np.uint8) # Caractere de determinação de fim de arquivo

byte_amount = len(data)
pixel_amount = img.size // 3

if byte_amount > pixel_amount:
    print(f'Mensagem grande demais. Essa imagem suporta no máximo {pixel_amount} bytes.')
    exit()

img_r_flat = img[:,:,0].flatten()
img_g_flat = img[:,:,1].flatten()
img_b_flat = img[:,:,2].flatten()

# Limpeza dos bits que serão usados na esteganografia
img_r_flat[:byte_amount] &= 0b11111000
img_g_flat[:byte_amount] &= 0b11111000
img_b_flat[:byte_amount] &= 0b11111100

# Criação das máscaras
r_mask = (data & (0b111 << 5)) >> 5
g_mask = (data & (0b111 << 2)) >> 2
b_mask = data & 0b11

dimensions = img.shape [:2]

r_mask.resize(pixel_amount)
g_mask.resize(pixel_amount)
b_mask.resize(pixel_amount)

# Adição da mensagem na imagem
img[:,:,0] = (img_r_flat | r_mask).reshape(dimensions)
img[:,:,1] = (img_g_flat | g_mask).reshape(dimensions)
img[:,:,2] = (img_b_flat | b_mask).reshape(dimensions)

io.imsave(output_path, img)

pbits_after_r = [((img[:,:,0] & (1 << i)) >> i) * 255 for i in [7, 2, 1, 0]]
pbits_after_g = [((img[:,:,1] & (1 << i)) >> i) * 255 for i in [7, 2, 1, 0]]
pbits_after_b = [((img[:,:,2] & (1 << i)) >> i) * 255 for i in [7, 2, 1, 0]]

io.imshow_collection(pbits_before_r + pbits_before_g + pbits_before_b, 'matplotlib', cmap='gray')
plt.tight_layout()
plt.savefig('pbits_before.png', dpi=1000)

io.imshow_collection(pbits_after_r + pbits_after_g + pbits_after_b, 'matplotlib', cmap='gray')
plt.tight_layout()
plt.savefig('pbits_after.png', dpi=1000)
#plt.show()
 