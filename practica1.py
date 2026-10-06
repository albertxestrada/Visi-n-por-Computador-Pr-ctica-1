import cv2

ROJO = (0, 0, 255)

puntos = []  # clics

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        puntos.append((x, y))

video = cv2.VideoCapture('MyInputVid.avi')
fps = video.get(cv2.CAP_PROP_FPS)

cv2.namedWindow('Video')
cv2.setMouseCallback('Video', onMouse)

pausado = False
tecla = -1
success, frame = video.read()

while success and tecla != ord('q'):

    # dibujo un circulo
    for punto in puntos:
        cv2.circle(frame, punto, 5, ROJO, -1)

    cv2.imshow('Video', frame)
    tecla = cv2.waitKey(int(1000 / fps))

    if tecla == ord(' '):
        pausado = not pausado

    if not pausado:
        success, frame = video.read()

cv2.destroyWindow('Video')
video.release()

print(puntos)  