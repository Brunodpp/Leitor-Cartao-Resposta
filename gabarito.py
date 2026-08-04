import cv2
import numpy as np
import random
from PIL import Image
path= "Screenshot_13.png"
#local das vagas
vaga1 = [24,26,15,18]

frame = cv2.imread(path)
frame = frame[490:882, 0:629]
def PerspectivaWarp(frame):
    img = frame.copy()
    
    p1 = np.array([[39, 39], [42, 383], [604, 35], [607, 378]], np.float32)
    p2 = np.array([[0, 0], [0, 400], [600, 0], [600, 400]], np.float32)
    T = cv2.getPerspectiveTransform(p1, p2)
    imgWarp = cv2.warpPerspective(img, T, (600, 400))
    return imgWarp
imgW = PerspectivaWarp(frame)

imgCinza = cv2.cvtColor(imgW, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
imgBlur = cv2.medianBlur(imgThresh, 5)


rCorretas = 0
gabarito = [random.randint(0, 4) for _ in range(20)]
for j in range (1,21):
    x, y, w, h = vaga1  
    y+= (j-1)*18
    if j> 11:
        y+= 8
    qtdMarcada =0
    for i in range(1,6):
        x=vaga1[0]
        x+= (i-1)*17
        
        recorte = imgBlur[y:y+h, x:x+w]
        qtdPxBranco = cv2.countNonZero(recorte)
        
        #cv2.rectangle(imgW, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #cv2.putText(frame, str(qtdPxBranco), (x+(20*i), y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        if qtdPxBranco > 70:
            if gabarito[j-1] == (i-1):
                cv2.rectangle(imgW, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rCorretas += 1
            else:
                cv2.rectangle(imgW, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(imgW, (vaga1[0]+(gabarito[j-1]*16), y), (vaga1[0]+(gabarito[j-1]*16) + w, y + h), (255, 0, 0), 2)
            qtdMarcada += 1
cv2.rectangle(imgW, (450, 0), (600, 40), (31, 125, 33), -1)
cv2.putText(imgW, f"{rCorretas}/20", (450, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
print(gabarito)
cv2.imshow("Imagem", imgCinza)
cv2.imshow("Imagem Threshold", imgThresh)
cv2.imshow("Imagem Blur", imgBlur)
cv2.imshow("Imagem Warp", imgW)

#cv2.imshow("Video", frame)

cv2.waitKey(0)




cv2.destroyAllWindows()