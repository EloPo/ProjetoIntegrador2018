import numpy as np
import json as json
import cv2 as cv
import json
import os 

cap = cv.VideoCapture(0)

print (cap.isOpened())
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Display the resulting frame
    cv.imshow('frame',gray)
    cv.imshow('frame',frame)
    cv.imwrite('fruta.png', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture

cap.release()
cv.destroyAllWindows()

os.system('cp fruta.png ./data')
print('Copiado')
os.system('rm predicao.txt')

os.system('rm ./data/Comida.png')
print('Removido')
os.system('mv ./data/fruta.png ./data/Comida.png')
os.system('./darknet detect ./cfg/yolov3.cfg yolov3.weights ./data/Comida.png > predicao.txt')

file = open("predicao.txt","r")

dataJson = []
data = []
ignorouPrimeira = False
for line in file:
	if ignorouPrimeira == False:
		ignorouPrimeira = True
	else:
		countLetter = 0
		item = ""
		while line[countLetter] != ':':
			item = item + line[countLetter]
			countLetter = countLetter+1
		elemento = {"nome":item}
		if(item != "person" and item != "diningtable"):
                    data.append(item)
                    dataJson.append(elemento)

dataJson = json.dumps(dataJson)
print(dataJson)
file.close()

os.system('rm predicao.txt')
file= open("predicao.txt","w+")
file.write(dataJson)
file.close()

os.system("rm index.html")

file= open("index.html","w+")
file.write("<html><head><title>Lista de ingredientes</title></head><body>")
file.write("<table style=\"border: 1px solid rgb(0, 0, 0); width:100%\"><h1 style=\"text-align: center;\">Lista de ingredientes</h1>")
if data == []:
    file.write("<tr style=\"text-align: center; font-size: 30px;\"> Lista Vazia</tr>")
else:
    for nome in data:
        file.write("<tr style=\"text-align: center; font-size: 30px;\"><td>"+ nome + "</td></tr>")
file.write("</table>")
file.write("</body></html>")
file.close()

os.system("open index.html")




