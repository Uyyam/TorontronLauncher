import py5
import subprocess
import threading
import os
import time
import datetime
import sys

IDLE_TIMEOUT = 60  # seconds
current_process = None
last_input_time = time.time()

game1 = "GAME NAME 1" #Insert first Game Name
game2 = "GAME NAME 2" #Insert second Game Name

games = [
    game1 + "/" + game1 + ".exe",
    game2 + "/" + game2 + ".exe"
]

banner = [
    "Assets/" + game1 + "/" + game1 + ".png",
    "Assets/" + game2 + "/" + game2 + ".png"
]

selected = 0
loading = False
info = False
about_HES = False
selected_button = 0


def launch_game(path):
    """Launch a game and restart launcher after exit"""
    global current_process, loading, last_input_time
    if current_process is not None:
        return
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    loading = True
    last_input_time = time.time()

    def run_and_restart():
        global current_process, loading
        print("Launching game:", path)
        current_process = subprocess.Popen(
            [path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        current_process.wait()
        current_process = None
        loading = False
        print("Game exited. Restarting launcher...")
        with open("stats.txt", "a") as f:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"Time Closed:{timestamp}\n\n")
        os.execl(sys.executable, sys.executable, *sys.argv)

    threading.Thread(target=run_and_restart, daemon=True).start()


def setup():
    global banner_img, background_img, hand_select, logo, qr_img, point_select
    global title_font, reg_font, game_info, control_images
    py5.full_screen()
    banner_img = [py5.load_image(b) for b in banner]
    background_img = py5.load_image("Assets/Torontron.png")
    hand_select = py5.load_image("Assets/hands.png")
    logo = py5.load_image("Assets/Logo.png")
    qr_img = py5.load_image("Assets/QR_code.png")
    point_select = py5.load_image("Assets/point.png")

    title_font = py5.create_font("Assets/Fonts/title.TTF", 64)
    reg_font = py5.create_font("Assets/Fonts/upheavtt.ttf", 28)

    game_info = []
    control_images = []

    for g in games:
        folder = os.path.basename(os.path.dirname(g))
        info_path = f"Assets/{folder}/info.txt"
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
        else:
            meta["title"] = "Unknown Game"
        game_info.append(meta)

        control_path = f"Assets/{folder}/controls.png"
        control_images.append(py5.load_image(control_path) if os.path.exists(control_path) else None)


def draw():
    global selected
    py5.background(background_img)
    py5.no_cursor()
    py5.image(logo, py5.width/10, py5.height - py5.height/7, py5.width/10, py5.width/10)

    for i, g in enumerate(games):
        y = py5.height / 6 * (i + 3) + (i * (py5.height / 10))
        py5.image_mode(py5.CENTER)
        py5.image(banner_img[i], py5.width / 2, y, py5.width / 3 * 1.2, py5.height / 4.5)
        if i == selected:
            py5.image(hand_select, py5.width / 2, y - 7, py5.width / 3 * 1.5, py5.height / 3)

    if loading:
        py5.fill(0)
        py5.rect(py5.width / 2, py5.height / 2, py5.width, py5.height)
        py5.fill(255)
        py5.text("LOADING...", py5.width / 2, py5.height / 2)


def key_pressed():
    global selected, info, about_HES
    options = len(games)
    if py5.key == py5.ESC:
        py5.intercept_escape()
    elif py5.key_code in [py5.UP, py5.DOWN]:
        selected = (selected + (1 if py5.key_code == py5.DOWN else -1)) % options
    elif py5.key_code in [10, 32]:  # Enter or Space
        launch_game(games[selected])


if __name__ == "__main__":
    py5.run_sketch()


