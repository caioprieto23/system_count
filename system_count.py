# opencv-python
import cv2
import numpy as np

# Coordenadas das Vagas
vaga1 = [1, 89, 108, 213]
vaga2 = [115, 87, 152, 211]
vaga3 = [289, 89, 138, 212]
vaga4 = [439, 87, 135, 212]
vaga5 = [591, 90, 132, 206]
vaga6 = [738, 93, 139, 204]
vaga7 = [881, 93, 138, 201]
vaga8 = [1027, 94, 147, 202]

vagas = [vaga1,vaga2,vaga3,vaga4,vaga5,vaga6,vaga7,vaga8]

video = cv2.VideoCapture('video.mp4')

while True:
  check, img = video.read()

  # Preto e Branco
  imgPretoBranco = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  # Preto e Branco e Borrada
  imgTh = cv2.adaptiveThreshold(imgPretoBranco,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
  imgBorrada = cv2.medianBlur(imgTh,5)
  kernel = np.ones((3,3),np.int8)
  imgDilatalada = cv2.dilate(imgBorrada,kernel)

  qtdDeVagasLivres = 8

  # Cria o retângulo em volta do estacionamento e o número de pixeis brancos
  for x,y,w,h in vagas:
    recorte = imgDilatalada[y:y+h,x:x+w]
    qtdPixelBranco = cv2.countNonZero(recorte)

    ficarVerde = (0,255,0)
    ficarVermelho = (0,0,255)

    # Imagem correta
    if qtdPixelBranco > 3000:
      cv2.rectangle(img,(x,y),(x+w,y+h),ficarVermelho,3)
      qtdDeVagasLivres -= 1
    else:
      cv2.rectangle(img,(x,y),(x+w,y+h),ficarVerde,3)

    cv2.putText(img,str(qtdPixelBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

    # Imagem teste
    cv2.rectangle(imgBorrada,(x,y),(x+w,y+h),ficarVermelho,3)
    cv2.putText(imgBorrada,str(qtdPixelBranco),(x,y+h-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)

  print(qtdDeVagasLivres)
  cv2.putText(img,f'LIVRE: {qtdDeVagasLivres} / 8',(95,55),cv2.FONT_ITALIC,1,(0,0,0),3)

  # Mostra o Video da Tela colorido / Preto e branco com delay de 10 segundo
  cv2.imshow('video',img)
  cv2.imshow('video-teste',imgDilatalada)
  cv2.waitKey(10)

