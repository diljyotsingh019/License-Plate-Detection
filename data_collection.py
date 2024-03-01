import pyautogui
import numpy as np
import cv2
import time

i=0
while True:
    i=i+1
    time.sleep(2)
    image = np.array(pyautogui.screenshot())
    cv2.imshow("Test", image)
    cv2.imwrite(f"images/Train-{i}.jpg", image)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cv2.destroyAllWindows()