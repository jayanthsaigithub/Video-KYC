import sqlite3
import hashlib
import secrets
import cv2
import face_recognition


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)


def hash_passphrase(passphrase, salt):
    return hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, 100000)


def create_tables():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, salt TEXT, passphrase TEXT, passphrase_salt TEXT, face_encoding TEXT)''')

    conn.commit()
    conn.close()


def create_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    username = input("Enter a username: ")
    password = input("Enter a password: ")
    passphrase = input("Enter a passphrase: ")

    salt = secrets.token_bytes(16)
    hashed_password = hash_password(password, salt)
    passphrase_salt = secrets.token_bytes(16)
    hashed_passphrase = hash_passphrase(passphrase, passphrase_salt)

    # Create the face encoding for the user
    face_encoding = create_face_encoding()

    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)",
              (username, hashed_password, salt, hashed_passphrase, passphrase_salt, face_encoding))

    conn.commit()
    conn.close()

    print("User created successfully!")


def create_face_encoding():
    # Initialize OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Capture a single frame from the camera
    ret, frame = cap.read()

    # Find the face in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Release the video capture
    cap.release()

    # If no face is found, return None
    if len(face_encodings) == 0:
        return None

    # Convert the face encoding to a string for storage in the database
    face_encoding_str = ','.join(str(x) for x in face_encodings[0])

    return face_encoding_str


def login():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    c.execute("SELECT * FROM users WHERE username = ?", (username,))

    user = c.fetchone()

    if user:
        salt = user[2]
        hashed_password = hash_password(password, salt)

        if hashed_password == user[1]:
            passphrase = input("Enter your passphrase: ")
            passphrase_salt = user[4]
            hashed_passphrase = hash_passphrase(passphrase, passphrase_salt)

            if hashed_passphrase == user[3]:
                # Load the user's face encoding from the database
                face_encoding_str = user[5]
                if face_encoding_str:
                    face_encoding = [float(x) for x in face_encoding_str.split(',')]
                    if check_face_encoding(face_encoding):
                        print("Authentication successful!")
                    else:
                        print("Face recognition failed.")
                else:
                    print("No face encoding found for user.")
            else:
                print("Passphrase incorrect.")
        else:
            print("Password incorrect.")
    else:
        print("User not found.")


def check_face_encoding(face_encoding):
    # Initialize OpenCV video capture
    cap = cv2.VideoCapture(0)

    # Check if the camera was opened successfully
    if not cap.isOpened():
        print("Failed to open camera")
        return False

    # Capture a single frame from the camera
    ret, frame = cap.read()

    # Find the face in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Release the video capture
    cap.release()

    # If no face is found, return False
    if len(face_encodings) == 0:
        return False

    # Compare the face encodings
    match = face_recognition.compare_faces([face_encoding], face_encodings[0], tolerance=0.5)

    return match[0]


create_tables()

while True:
    print("1. Sign up")
    print("2. Login")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        create_user()
    elif choice == '2':
        login()
    else:
        print("Invalid choice, try again")
