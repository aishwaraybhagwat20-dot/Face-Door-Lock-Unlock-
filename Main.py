
import PySimpleGUI as sg
import face_recognition
import json
import cv2
import numpy as np

try:
    with open("database.json", "r") as file:
        database = json.load(file)
except FileNotFoundError:
    database = {}

def load_and_encode(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        raise ValueError("No face found in the image!")

    return encodings

def real_time_camera_recognition():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        sg.popup_error("Camera Error", "Cannot access camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_frame,
            face_locations
        )

        for (top, right, bottom, left), face_encoding in zip(
            face_locations,
            face_encodings
        ):

            label = "Access Denied"
            color = (0, 0, 255)

            for name, data in database.items():

                stored_encoding = np.array(data["encoding"])

                match = face_recognition.compare_faces(
                    [stored_encoding],
                    face_encoding,
                    tolerance=0.45
                )[0]

                if match:
                    label = f"Access Granted - {name}"
                    color = (0, 255, 0)
                    break

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                color,
                2
            )

            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                color,
                2
            )

        cv2.imshow("Face Recognition Door Lock", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

def add_person(values):

    image_path = values["-IMAGE_PATH-"].strip()
    name = values["-NAME-"].strip()
    instagram = values["-INSTA_HANDLE-"].strip()

    if name == "":
        sg.popup_error("Please enter a name.")
        return

    try:

        if image_path == "":

            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                sg.popup_error("Camera Error")
                return

            for i in range(10):
                ret, frame = cap.read()

            cap.release()

            if not ret:
                sg.popup_error("Failed to capture image.")
                return

            image_path = "camera_capture.jpg"
            cv2.imwrite(image_path, frame)

        encoding = load_and_encode(image_path)[0]

        database[name] = {
            "encoding": encoding.tolist(),
            "info": {
                "instagram": instagram,
                "link": f"https://www.instagram.com/{instagram}/"
            }
        }

        with open("database.json", "w") as file:
            json.dump(database, file, indent=4)

        sg.popup("Success", f"{name} added successfully.")

    except Exception as e:
        sg.popup_error(str(e))

def recognize_face(values, window):

    image_path = values["-IMAGE_PATH-"].strip()

    if image_path == "":
        sg.popup_error("Please select an image.")
        return

    try:

        unknown_encodings = load_and_encode(image_path)

        result = ""

        for unknown_encoding in unknown_encodings:

            found = False

            for name, data in database.items():

                stored_encoding = np.array(data["encoding"])

                match = face_recognition.compare_faces(
                    [stored_encoding],
                    unknown_encoding,
                    tolerance=0.45
                )[0]

                if match:
                    result += (
                        f"Access Granted\n"
                        f"Welcome {name}\n"
                        f"Door Unlocked\n\n"
                    )
                    found = True
                    break

            if not found:
                result += (
                    "Access Denied\n"
                    "Door Locked\n\n"
                )

        window["-RESULTS-"].update(result)

    except Exception as e:
        sg.popup_error(str(e))

layout = [
    [
        sg.Text("Image Path"),
        sg.Input(key="-IMAGE_PATH-", size=(40, 1)),
        sg.FileBrowse()
    ],

    [
        sg.Button("Recognize", key="-RECOGNIZE-"),
        sg.Button("Add Person", key="-ADD_PERSON-"),
        sg.Button("Use Camera", key="-USE_CAMERA-")
    ],

    [
        sg.Text("Name"),
        sg.Input(key="-NAME-", size=(30, 1))
    ],

    [
        sg.Text("Instagram"),
        sg.Input(key="-INSTA_HANDLE-", size=(30, 1))
    ],

    [
        sg.Text("Results")
    ],

    [
        sg.Multiline(
            "",
            key="-RESULTS-",
            size=(60, 10),
            disabled=False
        )
    ]
]

window = sg.Window(
    "Face Recognition Door Lock Simulation",
    layout
)

while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    elif event == "-ADD_PERSON-":
        add_person(values)

    elif event == "-RECOGNIZE-":
        recognize_face(values, window)

    elif event == "-USE_CAMERA-":
        real_time_camera_recognition()

window.close()
