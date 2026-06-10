# Face Recognition Door Lock Simulator

## About the Project

This project is a Face Recognition Door Lock Simulator developed using Python. It uses facial recognition to identify authorized users and simulates a smart door lock system by displaying access granted or access denied messages. The application provides a simple graphical interface for registering users and performing real-time authentication through a webcam.

## Features

* Face recognition using uploaded images
* Real-time face detection and recognition through webcam
* Register new users by storing facial encodings
* Local JSON database for user information
* Simulated door lock with access granted and denied responses
* Simple and easy-to-use graphical interface

## Technologies Used

* Python
* OpenCV
* face_recognition
* NumPy
* PySimpleGUI
* JSON

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Face-Recognition-Door-Lock.git
```

### 2. Open the project folder

```bash
cd Face-Recognition-Door-Lock
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

## How the Project Works

1. Add a new user by selecting an image or capturing one using the webcam.
2. The application extracts the facial features and stores them in the local database.
3. During recognition, the webcam scans the face and compares it with the stored data.
4. If a match is found, the system displays **Access Granted** and simulates unlocking the door.
5. If no match is found, it displays **Access Denied** and keeps the door locked.

## Future Enhancements

* Database integration using MySQL or SQLite
* Liveness detection to prevent spoofing
* Hardware integration with Arduino or Raspberry Pi
* Attendance or access log generation
* Email or SMS notifications for unauthorized access

## Screenshots

Add screenshots of the main interface, user registration, real-time recognition, access granted, and access denied screens.

## Requirements

* Python 3.9 or above
* Webcam
* Required Python libraries listed in `requirements.txt`

## Author

**Aishwaray Bhagwat**

## License

This project was developed for educational purposes and can be used or modified for learning and academic projects.
