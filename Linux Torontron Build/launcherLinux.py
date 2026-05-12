import py5
import subprocess
import threading
import os
import time
import datetime
from pynput import keyboard

last_input_time = time.time()
IDLE_TIMEOUT = 60  # seconds

game1="" #Insert first Game Name
game2="" #Insert second Game Name

games = [
    game1+"/"+game1+".exe",
    game2+"/"+game2+".exe"
]

banner = [
    "Assets/"+game1+"/"+game1+".png",
    "Assets/"+game2+"/"+game2+".png"
]

selected = 0
current_process = None
WINE_PATH = "/usr/bin/wine"   # adjust to your system
        
def on_key_press(key):
    global last_input_time
    last_input_time = time.time()

keyboard.Listener(on_press=on_key_press).start()
        
def launch_game(path):
    global current_process, last_input_time, loading
    if current_process is not None:
        print("A game is already running!")
        return
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    #LINUX VER
    current_process = subprocess.Popen(
        [WINE_PATH, path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    last_input_time = time.time()
    loading = True
    # Start both watchers
    threading.Thread(target=wait_for_game_exit, daemon=True).start()
    threading.Thread(target=idle_timeout_check, daemon=True).start()


def wait_for_game_exit():
    global current_process, loading
    if current_process:
        current_process.wait()
        current_process = None
        loading = False
        print("Game exited.")
        with open("stats.txt", "a") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Time Closed:{timestamp}\n\n")

def quit_game():
    global current_process, loading
    if current_process:
        current_process.terminate()
        current_process = None
        loading = False
        print("Game terminated.")
        with open("stats.txt", "a") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Time Closed:{timestamp}\n\n")
        
def idle_timeout_check():
    global current_process, last_input_time
    while current_process:
        if time.time() - last_input_time > IDLE_TIMEOUT:
            print("Idle timeout reached. Exiting game.")
            quit_game()
            break
        time.sleep(1)  # check every second


def setup():
    global banner_img, background_img, hand_select, logo, info, loading, game_info, control_images, title_font, reg_font, about_HES, selected_button, qr_img, point_select
    py5.full_screen()
    banner_img = []
    for i in range(len(banner)):
        banner_img.append(py5.load_image(banner[i]))
    background_img = py5.load_image("Assets/Torontron.png")
    hand_select = py5.load_image("Assets/hands.png")
    logo = py5.load_image("Assets/Logo.png")
    qr_img = py5.load_image("Assets/QR_code.png")
    point_select = py5.load_image("Assets/point.png")
    
    info = False
    loading = False
    about_HES = False
        
    selected_button = 0  # 0 = PLAY, 1 = BACK

    title_font = py5.create_font("Assets/Fonts/title.TTF", 64)  # Bigger size for titles
    reg_font = py5.create_font("Assets/Fonts/upheavtt.ttf", 28)  # Regular UI text

    
    game_info = []  # holds strings loaded from .txt files
    control_images = [] # holds controller scheme images from png

    for g in games:
        folder_name = os.path.basename(os.path.dirname(g))
        info_path = f"Assets/{folder_name}/info.txt"

        meta = {"title": "", "desc": "", "dev": ""}
        if os.path.exists(info_path):
            with open(info_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Title:"):
                        meta["title"] = line.replace("Title:", "").strip()
                    elif line.startswith("Description:"):
                        meta["desc"] = line.replace("Description:", "").strip().replace("\\n", "\n")
                    elif line.startswith("Developed By:"):
                        meta["dev"] = line.replace("Developed By:", "").strip()
            game_info.append(meta)
        else:
            game_info.append("No information available.")

    # Control image
        control_path = f"Assets/{folder_name}/controls.png"
        if os.path.exists(control_path):
            control_images.append(py5.load_image(control_path))
        else:
            control_images.append(None)




def draw():
    global about_HES
    
    py5.background(background_img)

    py5.no_cursor()
    # Draw title
    py5.fill(255)
    py5.text_align(py5.CENTER, py5.CENTER)  # ✅ Correct py5 usage


    # Game selector UI
    py5.rect_mode(py5.CENTER)  # ✅ Correct rect mode
    py5.no_stroke()
    

    py5.image(logo, py5.width/10, py5.height - py5.height/7, py5.width/10, py5.width/10)


    for i, g in enumerate(games):
        y = py5.height / 6 * (i+3) + (i*(py5.height/10))

        py5.image_mode(py5.CENTER)
        py5.image(banner_img[i], py5.width / 2, y, py5.width/3 * 1.2, py5.height/4.5)  # ✅ No tuple syntax here
    	
        if i == selected:
            py5.fill(100, 75)  # highlight
            py5.image(hand_select, py5.width/2, y - 7, py5.width/3 * 1.5, py5.height/3)
        else:
            py5.fill(0, 0)
    
    if selected == len(games):
        py5.image(point_select, py5.width/10, py5.height * 0.7, py5.height/10, py5.width/10)
    else:
        about_HES = False
    
    if loading:
        py5.fill(0)
        py5.rect(py5.width/2, py5.height/2, py5.width, py5.height)
        
        py5.fill(255)
        py5.text("LOADING...", py5.width/2, py5.height/2)
        
    if info or about_HES:
    # ... existing overlay drawing
        py5.fill(0, 150)
        py5.rect(py5.width/2, py5.height/2, py5.width, py5.height)

        py5.fill(56, 55, 54)
        py5.stroke(255)
        py5.stroke_weight(4)
        py5.rect(py5.width/2, py5.height/2, py5.width * 0.75, py5.height* 0.75)
        
        py5.fill(56, 55, 54)
        py5.stroke(255)
        py5.stroke_weight(4)
        py5.rect(py5.width/2, py5.height/2, py5.width * 0.75, py5.height* 0.75)
        
        py5.no_stroke()
        py5.fill(255)
        
        btn_y = py5.height * 0.85
        btn_spacing = py5.width * 0.25
        
        if not info:
            py5.fill
            py5.text_font(title_font)
            py5.text_size(64)  
            py5.text_align(py5.CENTER, py5.TOP)
            py5.text("HAND EYE SOCIETY", py5.width/2, py5.height/6)
            py5.text_font(reg_font)
            py5.text_size(28)
            py5.text("Hand Eye Society is a Toronto not-for-profit that showcases and nurtures videogames made primarily for creative expression\n\nThe Hand Eye Society’s mission is to support and showcase video games as creative expression, centring our work around artists and fostering inclusive communities through games as art. We aim to provide exhibition opportunities, education, creative support, mentorship, knowledge sharing, and inspiration to artists, enthusiasts, and the game-curious in Toronto.\n\nFounded in 2009, it is one of the first videogame arts organizations of its kind in the world.", py5.width/2, py5.height * 0.4, py5.width * 0.6, py5.height * 0.3)
            #QR CODE
            py5.text_size(45)
            py5.text("Scan for More Info", py5.width/2, py5.height * 0.47)
            py5.image_mode(py5.CENTER)
            py5.image(qr_img, py5.width/2, py5.height * 0.68, py5.width * 0.2, py5.width * 0.2)
            
            py5.stroke(255)
            py5.fill(228, 73, 94)  # highlight selected
            py5.rect(py5.width * 0.18, py5.height * 0.825, 200, 80,60)  # width=150, height=60, rounded corners
            py5.fill(253, 227, 42)
            py5.text_size(62)
            py5.text("BACK", py5.width* 0.18, py5.height * 0.814)
        
        if not about_HES:
            meta = game_info[selected]
            
            # Title
            py5.text_font(title_font)
            py5.text_size(64)  
            py5.text_align(py5.CENTER, py5.TOP)
            py5.text(meta["title"], py5.width/2, py5.height/6)
            #Description
            py5.text_font(reg_font)
            py5.text_size(28)
            py5.text(meta["desc"], py5.width/2, py5.height * 0.4, py5.width * 0.6, py5.height * 0.3)
            #Developer
            py5.text_size(32)
            py5.text(f"By: {meta['dev']}", py5.width/2, py5.height * 0.82)


            # ✅ Draw control image (bottom half)
            control_img = control_images[selected]
            if control_img:
                img_y = py5.height/3 + py5.height * 0.27  # Position image lower
                py5.text_size(45)
                py5.text("Controls", py5.width/2, img_y - py5.height * 0.2)
                py5.image_mode(py5.CENTER)
                py5.image(control_img, py5.width/2, img_y, py5.width * 0.4, py5.height * 0.4)
            
            py5.stroke(255)
            if selected_button == 0:
                py5.fill(228, 73, 94)  # highlight selected
                py5.rect(py5.width * 0.82, py5.height * 0.825, 200, 80, 80)  # width=150, height=60, rounded corners
                py5.fill(253, 227, 42)
            else:
                py5.fill(56, 55, 54)
                py5.rect(py5.width * 0.82, py5.height * 0.825, 200, 80, 80)  # width=150, height=60, rounded corners
                py5.fill(255)
            py5.text_size(62)
            py5.text("PLAY", py5.width * 0.82, py5.height * 0.814)
            if selected_button == 1:
                py5.fill(228, 73, 94)  # highlight selected
                py5.rect(py5.width * 0.18, py5.height * 0.825, 200, 80,60)  # width=150, height=60, rounded corners
                py5.fill(253, 227, 42)
            else:
                py5.fill(56, 55, 54)
                py5.rect(py5.width * 0.18, py5.height * 0.825, 200, 80, 60)  # width=150, height=60, rounded corners
                py5.fill(255)
            py5.text_size(62)
            py5.text("BACK", py5.width* 0.18, py5.height * 0.814)
    
                    
   


def key_pressed():
    global info, loading, selected, game_opened_time, about_HES, selected_button
    options = len(games) + 1
    if py5.key == py5.ESC:
        py5.intercept_escape()

    # Only handle button selection if info screen is active
    if info:
        if py5.key_code in [py5.UP, py5.DOWN, py5.LEFT, py5.RIGHT]:
            # Toggle between 0 and 1
            selected_button = 1 - selected_button
        elif py5.key_code == 10:  # Enter or Space
            if selected_button == 0:  # PLAY
                loading = True
                info = False
                launch_game(games[selected])
            # Log stats
                with open("stats.txt", "a") as f:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    game_name = os.path.basename(os.path.dirname(games[selected]))
                    f.write(f"Game: {game_name}\nTime Opened: {timestamp}\n")
            elif selected_button == 1:  # BACK
                info = False  # go back to menu
    else:
        if py5.key_code == py5.UP or py5.key in ['w', 'W']:
            selected = (selected + 1) % options
        elif py5.key_code == py5.DOWN or py5.key in ['s', 'S']:
            selected = (selected - 1 + options) % options
        elif py5.key_code == 10:  # Enter or Space
            if selected == len(games):
                if about_HES:
                    about_HES = False
                else:
                    about_HES = True
            else:
                info = True  # Open info box
    
    

if __name__ == '__main__':
    py5.run_sketch()


