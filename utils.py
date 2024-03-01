import cv2

def detect_and_recognise(model, reader, image):
    result = model.predict(image)

    for x1,y1,x2,y2 in result[0].boxes.xyxy:
        cv2.rectangle(image,(int(x1), int(y1)), (int(x2), int(y2)), color = (0,255,0), thickness = 5)
        ocr = reader.readtext(image[int(y1):int(y2), int(x1):int(x2)])
        text=""
        for i in ocr:
            if i:
                if i[2]>0.1:
                    text +=i[1]
        cv2.putText(image, text.upper(), (int(x1), int(y1)-30), 2,1,(0,255,0), 4, cv2.LINE_AA)
    image = cv2.resize(image, (960,540))

    return image
    


