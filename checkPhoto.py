from PIL import Image
import random, cv2, os

path = os.getcwd() + '\\'
# path = os.path.dirname(os.path.realpath(__file__)) + '\\'
filesInData = os.listdir(path)

for k in filesInData:
    if k.find('.') == -1:
        dirPath = path + k + '\\'
        filesInDir = os.listdir(dirPath)
        imgPaths = [dirPath + e for e in filesInDir if not (e.endswith('.ini')) and not (e.endswith('.py')) and not (e.endswith('.xml'))]

        cascPath = path + "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)

        for (i, el)  in enumerate(imgPaths):
            img = Image.open(el)
            width, height = img.size
            if width > height:
                img = img.resize((640, 480))
                img = img.rotate(-90, expand=True)
            else:
                img = img.resize((480, 640))
            img.save(el)
            image = cv2.imread(el)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )

            print(f'Ho trovato {len(faces)} facce!')
            ext = '.' + el.split('.')[1]
            if len(faces) == 1:
                stringa = 'tieni_'
            else:
                stringa = 'butta_'
            new = dirPath + stringa + str(hex(random.randrange(0, 32768))) + ext
            while True:
                try:
                    os.rename(el, new)
                    break
                except:
                    new = dirPath + stringa + str(hex(random.randrange(0, 32768))) + ext
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Faces found", image)
            cv2.waitKey(0)
