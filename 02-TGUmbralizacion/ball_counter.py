import numpy as np
import cv2
from pupil_apriltags import Detector
import sys
import time

WIDTH = np.uintc(360)
HEIGHT = np.uintc(500)

#Toca cuadrar bien los límites de las Máscaras
GREEN = [ [90,30,30], [150,100,100] ]
BLUE = [ [210,30,30], [270,100,100] ]
RED = [ [0,30,30], [20,100,100] ]
colors = [(0, 0, 255) , (0,255, 0), (255, 0, 0)]

kalman = [None, None, None, None, None, None]

def kalman_start(i):
    kalman[i] = cv2.KalmanFilter(4,2)
    kalman[i].measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
    kalman[i].transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
    kalman[i].processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03

def hsv_to_cv(hsv):
    return np.array([int(hsv[0]/2.0), int(255.0*hsv[1]/100.0), int(255.0*hsv[2]/100.0)])

if __name__ == '__main__':
    if len(sys.argv)!=2:
        print("Número de Argumentos no permitidos")
        print("Favor ejecute el archivo de la siguiente manera:\npython ball_counter 'file_path'")
        sys.exit()

    try:
        video_path = sys.argv[1]
        cap = cv2.VideoCapture(video_path)
    except:
        print(f"No se pudo cargar el archivo en la ruta {video_path}")
        print(f"Favor compruebe que sea un formato de video soportado por OpenCV2")
        print(f"Favor compruebe que cuente con los codecs adecuados en su SO")
        sys.exit()
    
    count_red = 0
    count_blue = 0
    count_green = 0

    #######---------Identificar Tags----------######
    aprildet = Detector()

    found = [[False,10], [False,11], [False,12], [False,13], [False,14], [False,15]]
    found_counter = 0
    #Definiciones de parámetros para la visualización de los bordes de los Tags
    box_color = (0,255,255) 
    box_tickness = 3
    box_corner_radio = 10

    id_font = cv2.FONT_HERSHEY_SIMPLEX 
    id_scale = 1.0
    id_color = (255,255,0)
    id_tickness = 3
    
    pts_ref = [((0,0),10), ((WIDTH,0),11), ((0,int(4/7*HEIGHT)),12),((WIDTH,int(4/7*HEIGHT)),13),((0,HEIGHT),14),((WIDTH,HEIGHT),15)] #Puntos de referencia a transformar
    #Solo se necesitan 4 puntos, 2 son los del medio, son por si falla la detección
    
    ######-----Filtro de Kalman con Tags----######
    while(True):
        _, frame = cap.read() #Leer Frame de Video
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pts1  = []
        pts2  = []
        for f in found:
            if f[0]: #Estimación del filtro de kalman porque no se encontró Tag
                tp = kalman[f[1]-10].predict()
                center = (int(tp[0]), int(tp[1]))
                cv2.circle(frame, center, 10, (255,0,255), 3)
                pts1.append(list(center))
                pts2.append(list(pts_ref[[i[1] for i in pts_ref].index(f[1])][0]))

        results = aprildet.detect(gray)    #Detección de los Tags

        if len(results)>0:
            for result in results:    
                f = [i[1] for i in found].index(result.tag_id)
                if not found[f][0]:
                    kalman_start(result.tag_id-10) # Reinicia el filtro kalman
                    found_counter = 0
                found[f][0] = True
                center = (int(result.center[0]), int(result.center[1]))
                corners = result.corners.astype(int)
                cv2.circle(frame, tuple(corners[0]), box_corner_radio, box_color, -1)
                cv2.line(frame, tuple(corners[0]), tuple(corners[1]), box_color, box_tickness) 
                cv2.line(frame, tuple(corners[1]), tuple(corners[2]), box_color, box_tickness) 
                cv2.line(frame, tuple(corners[2]), tuple(corners[3]), box_color, box_tickness) 
                cv2.line(frame, tuple(corners[3]), tuple(corners[0]), box_color, box_tickness) 
                cv2.putText(frame, str(result.tag_id), (center[0]-10, center[1]+10), id_font, id_scale, id_color, id_tickness, cv2.LINE_AA) 
                pts1.append(list(center))
                pts2.append(list(pts_ref[[i[1] for i in pts_ref].index(result.tag_id)][0]))
                mp1 = np.array([[np.float32(center[0])],[np.float32(center[1])]])
                kalman[result.tag_id-10].correct(mp1)
        else:
            found_counter+=1
            if found_counter>200:
                for f in found:
                    f[0] = False
    
        # Trasnformación Geométrica
        M = cv2.getPerspectiveTransform(np.float32(pts1[0:4]),np.float32(pts2[0:4]))
        dst = cv2.warpPerspective(frame,M,(WIDTH,HEIGHT), borderMode=cv2.BORDER_REPLICATE)
        hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)

        #Umbralización
        red_mask = cv2.inRange(hsv, hsv_to_cv(RED[0]), hsv_to_cv(RED[1]))
        green_mask = cv2.inRange(hsv, hsv_to_cv(GREEN[0]), hsv_to_cv(GREEN[1]))
        blue_mask = cv2.inRange(hsv, hsv_to_cv(BLUE[0]), hsv_to_cv(BLUE[1]))
        mask = [red_mask, green_mask, blue_mask]

        #Preprocesamiento Morfológico
        for i, m in enumerate(mask):
            mask[i]= cv2.erode(mask[i], None, iterations=5)
            mask[i] = cv2.dilate(mask[i], None, iterations=5)

            (_, cnts, _) = cv2.findContours(mask[i].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                center = (x, y)
                _, _, h, w = cv2.boundingRect(c)
                rat = h/w
                if radius > 7 and rat>0.7 and rat<1.3:
                    cv2.circle(dst, (int(x), int(y)), int(radius), colors[i], 2)
                    cv2.circle(dst, (int(x), int(y)), 5, colors[i], -1)

        #Conteo
        cv2.putText(dst, 'RED = '+ str(count_red), (10, 480), id_font, id_scale, colors[0], id_tickness, cv2.LINE_AA) 
        cv2.putText(dst, 'GREEN = '+ str(count_green), (10, 440), id_font, id_scale, colors[1], id_tickness, cv2.LINE_AA) 
        cv2.putText(dst, 'BLUE = '+ str(count_blue), (10, 400), id_font, id_scale, colors[2], id_tickness, cv2.LINE_AA) 

        #Gráfica
        cv2.line(dst, pts_ref[2][0], pts_ref[3][0], (255,255,255), box_tickness, lineType=0) 
        frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), interpolation = cv2.INTER_AREA)
        cv2.imshow('Tags', frame)

        cv2.imshow('Main', dst)
        
        
        cv2.imshow('Green Mask', green_mask)
        cv2.imshow('Red Mask', red_mask)
        cv2.imshow('Blue Mask', blue_mask)
        time.sleep(0.1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print('Ok')