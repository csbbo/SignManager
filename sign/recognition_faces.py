
import face_recognition

def face_list(known_img,unknown_img):
    strange_image = face_recognition.load_image_file(unknown_img)
    strange_image_encoding = face_recognition.face_encodings(strange_image)[0]
    face_encoding_list = []
    for img in known_img:
        known_image = face_recognition.load_image_file(img)
        known_image_encoding = face_recognition.face_encodings(known_image)[0]
        face_encoding_list.append(known_image_encoding)
    results = face_recognition.compare_faces(face_encoding_list, strange_image_encoding,tolerance=0.4)
    return results