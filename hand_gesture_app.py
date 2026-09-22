'''by "winac2-NSDK" - ndkhoi234@gmail.com'''

from lang.lang_mana import tr, set_lang
import cv2 #4.10.0.84
import mediapipe as mp #0.10.18
import numpy as np #1.26.4
import tkinter as tk #8.6.13
from tkinter import Label, Button, Frame
from PIL import Image, ImageTk #12.0.0
import pickle 
import time
import pyttsx3 #2.91



MODEL_PATH = './models/hand_gesture_model.pkl'
model = pickle.load(open(MODEL_PATH, 'rb'))


LABELS = {
    
    0: 'drink',
    1: 'hello',
    2: 'hot',
    3: 'iced',
    4: 'thanks'
    } 


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=2)


BG = "#e7e7e7"
CARD = "#E4E4E4"
ACCENT = "#000000"
TEXT = "#000000"
BTN_GREEN = "#22c55e"
BTN_RED = "#ef4444"

HOLD_TIME = 0.75  # seconds
threshold = 0.8

class HandGestureApp:
    def __init__(self, root):
        self.root = root
        self.root.title(tr("title"))
        self.root.geometry("1000x720")
        self.root.configure(bg=BG)
        self.root.iconbitmap("./assets/logo.ico")
        
        self.width = 640
        self.height = 480

        # ---------- HEADER ----------
        Label(
            root,
            text="SignMachine",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)
        

        # ---------- MAIN ----------
        main = Frame(root, bg=BG)
        main.pack(fill="both", expand=True, padx=20)

        camera_card = Frame(main, bg=CARD)
        camera_card.pack(side="left", padx=10)

        self.video_label = Label(camera_card, bg=CARD)
        self.video_label.pack(padx=10, pady=10)

        control = Frame(main, bg=CARD, width=260)
        control.pack(side="right", fill="y", padx=10)

        self.control_label=Label(control, text=tr("controls"), bg=CARD, fg=ACCENT,
              font=("Segoe UI", 16, "bold"))
        self.control_label.pack(pady=20)

        self.control_btn=Button(
            control, 
            text=tr("start_camera"), 
            bg=BTN_GREEN, 
            fg="white",
            font=("Segoe UI", 14, "bold"),
            bd=0,
            command=self.start_camera)
        self.control_btn.pack(pady=15, ipadx=20, ipady=10)

        self.stop_btn=Button(control, text=tr("stop_camera"), bg=BTN_RED, fg="white",
               font=("Segoe UI", 14, "bold"), bd=0,
               command=self.stop_camera)
        self.stop_btn.pack(pady=10, ipadx=22, ipady=10)
        
        self.speak_btn=Button(control, text=tr("speak"), bg="#3b82f6", fg="white",
               font=("Segoe UI", 14, "bold"), bd=0,
               command=self.speech_out)
        self.speak_btn.pack(pady=10, ipadx=22, ipady=10)
        
        #languages 
        self.lang_btn=Button(control, text="EN/VI", bg="#3b82f6", fg="white",
               font=("Segoe UI", 12, "bold"), bd=0,
               command=self.switch_lang)
        self.lang_btn.pack(pady=10, ipadx=22, ipady=10)

        
        self.prediction_label = Label(
            root, text="GESTURE: NONE",
            bg=BG, fg=TEXT,
            font=("Segoe UI", 22, "bold")
        )
        self.prediction_label.pack(pady=10)

        
        self.message_label = Label(
            root,
            text=tr("message"),
            bg=BG,
            fg="#031618",
            wraplength=900,
            justify="left",
            font=("Segoe UI", 18, "bold")
        )
        self.message_label.pack(pady=10)
        
        
    

        
        self.cap = None
        self.running = False

        self.current_gesture = None
        self.gesture_start_time = None
        self.message_words = []
        self.gesture_committed = False

        
        root.bind("p", self.delete_last_word)
        root.bind("P", self.delete_last_word)
        
        self.show_black_screen()

    
    def start_camera(self):
        if not self.running:
            self.cap = cv2.VideoCapture(0)
            
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            

            # frame = cv2.resize(self.cap, (self.width, self.height))
            actual_w = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            actual_h = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            print(f"[Camera Resolution] {actual_w}x{actual_h}")
            
            self.running = True
            self.process_frame()
            
            

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image="")
        self.prediction_label.config(text="GESTURE: NONE")
        
        self.show_black_screen()

   
    def delete_last_word(self, event=None):
        if self.message_words:
            self.message_words.pop()
            self.update_message()
            
    def speech_out(self):
        if self.message_words:
            engine = pyttsx3.init()
            engine.say(" ".join(self.message_words))
            engine.runAndWait()
            
    def show_black_screen(self):
        black_frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        img = Image.fromarray(black_frame)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.config(image=imgtk)

    def update_message(self):
        translated_words = [tr(word) for word in self.message_words]
        self.message_label.config(
            text=tr("message") + " " + " ".join(translated_words)
        )

    def switch_lang(self):
        from lang.lang_mana import current_lang
        # print(current_lang)
        if current_lang == "en":
                set_lang("vi")
        else:
            set_lang("en")
        #change
        self.refresh_ui()
            
    def refresh_ui(self):

        self.root.title(tr("title"))
        
        self.control_label.config(text=tr("controls"))

        self.prediction_label.config(text=tr("gesture_none"))

        self.update_message()
        
        self.control_btn.config(text=tr("start_camera"))
        self.stop_btn.config(text=tr("stop_camera"))
        self.speak_btn.config(text=tr("speak"))

    
    def process_frame(self):
        if not self.running or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            prediction = None

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    x_, y_ = [], []
                    for lm in hand_landmarks.landmark:
                        x_.append(lm.x)
                        y_.append(lm.y)
                    
                    x_min, x_max = min(x_), max(x_)
                    y_min, y_max = min(y_), max(y_)
                    
                    h, w, _ = frame.shape
                    x_min, x_max = int(x_min * w), int(x_max * w)
                    y_min, y_max = int(y_min * h), int(y_max * h)
                    
                    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)

                    data_aux = []
                    for lm in hand_landmarks.landmark:
                        data_aux.extend([lm.x - min(x_), lm.y - min(y_)])

                    try:
                        prob = model.predict_proba(np.array(data_aux).reshape(1, -1))
                        if max(prob[0]) > threshold:
                            prediction = LABELS[np.argmax(prob)]
                    except:
                        prediction = None

            # ---------- HOLD LOGIC ----------
            now = time.time()
            
            if prediction is None:
                self.current_gesture = None
                self.gesture_start_time = None
                self.gesture_committed = False

            elif prediction == self.current_gesture:
                if self.gesture_start_time and not self.gesture_committed:
                    if now - self.gesture_start_time >= HOLD_TIME:
            # chỉ append khi prediction chắc chắn là string
                        self.message_words.append(prediction) #self.message_words.append(prediction.upper())
                        # print(f"Added '{prediction.upper()}' to {self.message_words},")#1
                        # print(self.message_words)
                        self.update_message()
                        self.gesture_committed = True
            else:
                self.current_gesture = prediction
                self.gesture_start_time = now
                self.gesture_committed = False

            display_text = prediction.upper() if prediction else "NONE"
            self.prediction_label.config(text=f"GESTURE: {display_text}")
            # print(display_text)

            img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video_label.imgtk = img
            self.video_label.configure(image=img)

        self.root.after(10, self.process_frame)



if __name__ == "__main__":
    root = tk.Tk()
    HandGestureApp(root)
    root.mainloop()
