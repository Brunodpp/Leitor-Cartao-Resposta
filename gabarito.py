import cv2
import numpy as np
import random
videopath= "C:/Users/Bruno/Downloads/Screenshot_13.png"
#local das vagas
vaga1 = [60,60,16,15]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]

vagas = [vaga1, vaga2, vaga3, vaga4, vaga5, vaga6, vaga7, vaga8]
frame = cv2.imread(videopath)
frame = frame[490:882, 0:629]
def PerspectivaWarp(frame):
    img = frame.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    p1 = np.array([[38, 39], [42, 383], [604, 35], [608, 379]], np.float32)
    p2 = np.array([[0, 0], [0, 400], [600, 0], [600, 400]], np.float32)
    T = cv2.getPerspectiveTransform(p1, p2)
    imgWarp = cv2.warpPerspective(img, T, (600, 400))
    return imgWarp

imgCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
imgThresh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
imgBlur = cv2.medianBlur(imgThresh, 5)
#imgW = PerspectivaWarp(frame)

rCorretas = 0
gabarito = [random.randint(0, 4) for _ in range(20)]
for j in range (1,21):
    x, y, w, h = vaga1  
    y+= (j-1)*16
    qtdMarcada =0
    for i in range(1,6):
        x=vaga1[0]
        x+= (i-1)*16
        
        recorte = imgBlur[y:y+h, x:x+w]
        qtdPxBranco = cv2.countNonZero(recorte)
        
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #cv2.putText(frame, str(qtdPxBranco), (x+(20*i), y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        if qtdPxBranco > 70:
            if gabarito[j-1] == (i-1):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rCorretas += 1
            else:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(frame, (vaga1[0]+(gabarito[j-1]*16), y), (vaga1[0]+(gabarito[j-1]*16) + w, y + h), (255, 0, 0), 2)
            qtdMarcada += 1
cv2.rectangle(frame, (0, 0), (400, 40), (31, 125, 33), -1)
cv2.putText(frame, f"Respostas certas: {rCorretas}/20", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
print(gabarito)
cv2.imshow("Imagem", imgCinza)
cv2.imshow("Imagem Threshold", imgThresh)
cv2.imshow("Imagem Blur", imgBlur)
#cv2.imshow("Imagem Warp", imgW)

cv2.imshow("Video", frame)

cv2.waitKey(0)




cv2.destroyAllWindows()