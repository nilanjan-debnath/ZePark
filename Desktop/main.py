import cv2
import time
import queue
import cvzone
import datetime
import threading
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk

import firebase_data

# Initialize global variables
slot_counts = [0, 0, 0]
frames = []
slots = []
statuses = []
park_buttons = []
namelbs = []
carnolbs = []
bookingtimelbs = []
parkingtimelbs = []
edit_buttons = []
spaces = []
posList = []

ui_update_queue = queue.Queue()
update_data_queue = queue.Queue()
fetch_firebase_queue = queue.Queue()
firebase_update_queue = queue.Queue()
count_update_queue = queue.Queue()

# Fetch data from Firebase
grid = firebase_data.get_grid_details()
parkings = firebase_data.get_parking_details()
provider = firebase_data.get_provider_details()

for i in range(len(grid)):
    posList.append(grid[str(i)])

states = {
    0: ("Empty", "Green"),
    1: ("Booked", "Blue"),
    2: ("Parked", "Red"),
}  

def ui_update(n: int):
    # Change the counts
    spaces[0].configure(text=f"Available Slots: {slot_counts[0]}")
    spaces[1].configure(text=f"Booked Slots: {slot_counts[1]}")
    spaces[2].configure(text=f"Parked Slots: {slot_counts[2]}")
    spaces[3].configure(text=f"Total Spaces: {slot_counts[0]+slot_counts[1]+slot_counts[2]}")
    # change slot details
    namelbs[n].configure(text=f'Name: {parkings[n]["name"]}')
    carnolbs[n].configure(text=f'Car No: {parkings[n]["car_no"]}')
    bookingtimelbs[n].configure(text=f'Booking Time: {parkings[n]["booking_time"]}')
    parkingtimelbs[n].configure(text=f'Parking Time: {parkings[n]["parking_time"]}')
    text, color = states[parkings[n]["state"]]
    park_buttons[n].configure(text=text, fg_color=color)

def update_data(n: int, i: int, data: dict = None):
    slot_counts[parkings[n]["state"]] -= 1
    slot_counts[i] += 1
    if i == 0:
        parkings[n]["name"] = ""
        parkings[n]["car_no"] = ""
        parkings[n]["booking_time"] = ""
        parkings[n]["parking_time"] = ""
        parkings[n]["state"] = i
    elif i == 1:
        parkings[n]["name"] = data["name"]
        parkings[n]["car_no"] = data["car_no"]
        parkings[n]["booking_time"] = data["booking_time"]
        parkings[n]["state"] = i
    elif i == 2:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parkings[n]["parking_time"] = str(now)
        parkings[n]["state"] = i

    # Schedule UI updates on the main thread
    ui_update_queue.put(n)
    if i != 1:
        firebase_update_queue.put((n, parkings[n]))
        count_update_queue.put(slot_counts[0])

def fetch_firebase():
    update = firebase_data.get_parking_details()
    for n in range(len(parkings)):
        if parkings[n]["state"]==0 and update[n]["state"]==1:
            print(f"booking on slot {n}")
            update_data_queue.put((n, 1, update[n]))
            print(f"booking on slot {n} complete")
        elif parkings[n]["state"]==1 and update[n]["state"]==0:
            print(f"booking cancelling on slot {n}")
            update_data_queue.put((n, 0, update[n]))
            print(f"booking cancelled on slot {n} complete")


def ui_update_worker():
    while True:
        item = ui_update_queue.get()
        ui_update(item)
        ui_update_queue.task_done()

def count_update_worker():
    while True:
        item = count_update_queue.get()
        firebase_data.update_spot_count(item)
        count_update_queue.task_done()

def firebase_update_worker():
    while True:
        item = firebase_update_queue.get()
        firebase_data.update_parking_details(*item)
        firebase_update_queue.task_done()

def update_data_worker():
    while True:
        item = update_data_queue.get()
        update_data(*item)
        update_data_queue.task_done()


def fetch_firebase_worker():
    while True:
        item = fetch_firebase_queue.get()
        fetch_firebase()
        fetch_firebase_queue.task_done()

class ParkDetails(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.font0 = ctk.CTkFont(family='Times New Roman', size=24, weight='bold')
        self.font1 = ctk.CTkFont(family='Helvetica', size=18, weight='bold')
        self.font2 = ctk.CTkFont(family='Helvetica', size=14)

        global frames
        global slots
        global statuses
        global park_states
        global park_buttons
        global namelbs
        global carnolbs
        global bookingtimelbs
        global edit_buttons

        self.create_ui()

    def create_ui(self):
        for i in parkings:
            self.create_frame(i)
            self.create_labels(i)
            self.create_buttons(i)
            slot_counts[i["state"]] += 1

    def create_frame(self, i):
        frame = ctk.CTkFrame(
            master=self,
            width=500,
            height=50,
            fg_color="gray",
        )
        frame.grid(row=i["slot_no"], column=0, padx=5, pady=5, columnspan=7, sticky="EW")
        frames.append(frame)

    def create_labels(self, i):
        slot = ctk.CTkLabel(
            master=self,
            text=f'Slot: {i["slot_no"]}',
            bg_color="grey",
            text_color="White",
            font=self.font1,
        )
        slot.grid(row=i["slot_no"], column=0, padx=20, sticky="W")
        slots.append(slot)

        status = ctk.CTkLabel(
            master=self,
            text="Status",
            bg_color="grey",
            text_color="White",
            font=self.font1,
        )
        status.grid(row=i["slot_no"], column=1, padx=5, sticky="W")
        statuses.append(status)

        namelb = ctk.CTkLabel(
            master=self, 
            text=f'Name: {i["name"]}', 
            bg_color="grey", 
            text_color="White", 
            font=self.font2,
        )
        namelb.grid(row=i["slot_no"], column=3, padx=20, sticky="W")
        namelbs.append(namelb)

        carnolb = ctk.CTkLabel(
            master=self, 
            text=f'Car No: {i["car_no"]}', 
            bg_color="grey", 
            text_color="White", 
            font=self.font2,
        )
        carnolb.grid(row=i["slot_no"], column=4, padx=20, sticky="W")
        carnolbs.append(carnolb)

        bookingtimelb = ctk.CTkLabel(
            master=self, 
            text=f'Booking Time: {i["booking_time"]}', 
            bg_color="grey", 
            text_color="White", 
            font=self.font2,
        )
        bookingtimelb.grid(row=i["slot_no"], column=5, padx=20, sticky="W")
        bookingtimelbs.append(bookingtimelb)

        parkingtimelb = ctk.CTkLabel(
            master=self, 
            text=f'Parking Time: {i["parking_time"]}', 
            bg_color="grey", 
            text_color="White", 
            font=self.font2,
        )
        parkingtimelb.grid(row=i["slot_no"], column=6, padx=20, sticky="W")
        parkingtimelbs.append(parkingtimelb)

    def create_buttons(self, i):
        park_button = ctk.CTkButton(
            master=self,
            text=states[i["state"]][0],
            font=self.font1,
            fg_color=states[i["state"]][1],
            bg_color="grey",
            hover=None,
        )
        park_button.grid(row=i["slot_no"], column=2, padx=20, sticky="W")
        park_buttons.append(park_button)

        editbt = ctk.CTkButton(
            master=self,
            text="Edit",
            font=self.font2,
            fg_color="brown",
            bg_color="transparent",
            hover=None,
        )
        editbt.grid(row=i["slot_no"], column=7, padx=10, sticky="W")
        edit_buttons.append(editbt)

t = time.time()

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=700, width=1260, **kwargs)
        self.dashboard_tab = self.add("Dashboard")
        self.cctv_tab = self.add("CCTV")
        self.font0 = ctk.CTkFont(family='Times New Roman', size=30, weight='bold')
        self.font1 = ctk.CTkFont(family='Helvetica', size=18, weight='bold')
        self.font2 = ctk.CTkFont(family='Helvetica', size=14)
        global spaces
        self.setup_dashboard()
        self.setup_cctv()
        self.update()

    def setup_dashboard(self):
        placeName = ctk.CTkLabel(
            master=self.tab("Dashboard"), 
            text=provider["name"],
            font=self.font0
        )
        placeName.grid(row=0, column=0, padx=20, pady=10)
        
        for n in range(4):
            slotsDetails = ctk.CTkLabel(
                master=self.tab("Dashboard"), 
                text="",
                font=self.font1
            )
            slotsDetails.grid(row=1, column=n, padx=20, pady=10)
            spaces.append(slotsDetails)
        
        self.my_frame = ParkDetails(master=self.tab("Dashboard"), width=1220, height=500)
        self.my_frame.grid(row=2, column=0, columnspan=20)

    def setup_cctv(self):
        self.canvas_cctv = ctk.CTkCanvas(master=self.tab("CCTV"), width=1530, height=790)
        self.canvas_cctv.grid(row=0, column=0, padx=10, pady=10)

        # self.cap = cv2.VideoCapture("video6.mp4")  # Video
        self.cap = cv2.VideoCapture("video69.mp4")  # Video
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Unable to capture initial frame from the camera.")
            self.cap.release()

    def checking_parking_space(self, imgPro):
        # # slot 6
        # width = 200
        # height = 50
        # slot 69
        width = 106
        height = 48
        for i, pos in enumerate(posList):
            x, y = pos
            slot_number = i
            imgcrop = imgPro[y:y+height, x:x+width]
            count = cv2.countNonZero(imgcrop)
            cvzone.putTextRect(self.frame, str(count), (x, y+height-3), scale=1.1, thickness=2, offset=0)
            cvzone.putTextRect(self.frame, str(slot_number), (x, y+height-30), scale=1, thickness=2, offset=0, colorR=(255, 0, 0))
            if count > 900:
                colour = (255, 0, 0)
                thickness = 3
                if parkings[slot_number]["state"] != 2:
                    update_data_queue.put((slot_number, 2))
            else:
                colour = (0, 255, 0)
                thickness = 1
                if parkings[slot_number]["state"] != 0:
                    if parkings[slot_number]["state"] != 1:
                        update_data_queue.put((slot_number, 0))
                    else:
                        colour = (0, 0, 255)
                        thickness = 2
            cv2.rectangle(self.frame, pos, (pos[0] + width, pos[1] + height), colour, thickness)
        cvzone.putTextRect(self.frame, f'Free: {slot_counts[0]}/{len(posList)}', (100, 50), scale=2, thickness=5, offset=20)
        fetch_firebase_queue.put((True))

    def update(self):
        global t
        # by checking the current frame count with total frames count, repeating the video
        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.cap.read()
        if not ret:
            return
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_height, original_width, _ = frame.shape
        ratio = (original_width / original_height)
        # # slot 6
        # new_height = 1280
        # new_width = 720
        # # slot 69
        new_height = 1100
        new_width = 720
        self.frame = cv2.resize(self.frame, (new_height, new_width))
        imgGray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
        self.checking_parking_space(imgDilate)
        # if time.time()-t > 2:
        #     self.checking_parking_space(imgDilate)
        #     t = time.time()
        img = Image.fromarray(self.frame)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas_cctv.create_image(5, 5, image=self.photo, anchor="nw")
        self.canvas_cctv.update_idletasks()
        self.canvas_cctv.after(10, self.update)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title('ParKing')
        self.iconbitmap('parcar.ico')
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10)

app = App()

threading.Thread(target=ui_update_worker, daemon=True).start()
threading.Thread(target=update_data_worker, daemon=True).start()
threading.Thread(target=fetch_firebase_worker, daemon=True).start()
threading.Thread(target=count_update_worker, daemon=True).start()
threading.Thread(target=firebase_update_worker, daemon=True).start()

app.mainloop()