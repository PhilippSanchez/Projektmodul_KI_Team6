from deepface import DeepFace
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_analysis(frame):
    results = DeepFace.analyze(frame, actions=['age', 'gender', 'race', 'emotion'], enforce_detection=False)
    if not isinstance(results, list):
        results = [results]
    if len(results) > 0: return results[0]
    return None

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fehler beim Lesen des Frames von der Webcam.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_frame = frame[y:y+h, x:x+w]

        analysis = get_analysis(face_frame)

        if analysis:
            apparance = ''
            emotion = analysis['dominant_emotion']
            age = analysis['age']
            gender = analysis['gender']
            if gender['Woman'] < 0.5:
                apparance = 'Male'
            elif gender['Man'] > 0.5:
                apparance = 'Female'
            else:
                apparance = 'Unknown'

            race = analysis['dominant_race']


            text_color = (83, 245, 126)  
            rect_color = (0, 0, 0)  

            cv2.rectangle(frame, (x, y), (x+w, y+h), text_color, 2)

            overlay = frame.copy()
            alpha = 0.6  
            rect_width = 400  
            rect_height = 150  
            rect_x = x + w + 10  
            rect_y = y  

            cv2.rectangle(overlay, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), rect_color, cv2.FILLED)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            line_height = 30
            text_x = rect_x + 5  

    
            cv2.putText(frame, f'Emotion: {emotion}', (text_x, rect_y + line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)
            cv2.putText(frame, f'Age: {age}', (text_x, rect_y + 2 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)
            cv2.putText(frame, f'Gender: {apparance}', (text_x, rect_y + 3 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)
            cv2.putText(frame, f'Appearance: {race}', (text_x, rect_y + 4 * line_height), cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)

    cv2.imshow('Live Emotion Classifier', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()