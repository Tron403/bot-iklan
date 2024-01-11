from customtkinter import *
from selenium import webdriver
import threading
import time

drivers = {}
running = False
selected_option = 1

# List URL
all_urls = [
    "https://www.yahatash.com",
    "https://www.torrentsome60.com",
    "https://007y2sf4.yahatash.com",
    "https://0ag3xlgv.yahatash.com",
    "https://0d32n458.yahatash.com",
    "https://171.yahatash.com",
    "https://1c97ppf3.yahatash.com",
    "https://2gsa19f5.yahatash.com",
    "https://2t5ja6xy.yahatash.com",
    "https://32j7aq8k.yahatash.com",
]

# Waktu refresh
refresh_interval = 120


def run_bot(urls):
    global drivers
    global running
    chromedriver_path = "C:/ChromeDriver/chromedriver.exe"

    # Konfigurasi opsi Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])

    try:
        # Membuat instance WebDriver untuk setiap URL
        for url in urls:
            service = webdriver.chrome.service.Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            drivers[url] = driver

            # Navigasi ke URL
            driver.get(url)

        # Melakukan refresh setiap 4 detik
        while running:
            time.sleep(refresh_interval)
            for url, driver in drivers.items():
                driver.get(url)
                if not check_browser_status(driver):
                    print("Browser telah ditutup oleh user")
                    stop_bot()
                    break

    finally:
        # Menutup semua instance WebDriver ketika selesai
        for driver in drivers.values():
            driver.quit()


def start_bot():
    global running
    if not running:
        running = True
        global selected_urls
        selected_option_int = int(selected_option)
        selected_urls = all_urls[:selected_option_int]
        threading.Thread(target=run_bot, args=(selected_urls,)).start()


def check_browser_status(driver):
    try:
        driver.title  # memeriksa apakah browser masih aktif
        return True
    except Exception:
        return False


def stop_bot():
    global running
    running = False


def on_option_select(selection):
    global selected_option
    selected_option = selection


def button_start_event():
    start_bot()


def button_stop_event():
    stop_bot()


def create_gui():
    app = CTk()

    # Atur ukuran window
    app.title("By:TRON")
    app.geometry("400x400")
    set_appearance_mode("dark")
    deactivate_automatic_dpi_awareness()

    # button
    button_start = CTkButton(
        app,
        fg_color="transparent",
        text="Start",
        command=button_start_event,
        corner_radius=32,
        border_width=2,
        hover_color="#4f0275",
        border_color="#9502de",
        text_color="#fcfcfc",
    )
    button_start.place(relx=0.3, rely=0.5, anchor="center")

    button_stop = CTkButton(
        app,
        fg_color="transparent",
        text="Stop",
        command=button_stop_event,
        corner_radius=32,
        border_width=2,
        hover_color="#4f0275",
        border_color="#9502de",
        text_color="#fcfcfc",
    )
    button_stop.place(relx=0.7, rely=0.5, anchor="center")

    # frame
    option_frame = CTkFrame(app)
    option_frame.place(relx=0.5, rely=0.35, anchor="center")

    # label
    option_label = CTkLabel(
        option_frame, text="Select number of URLs:", font=("Helvetica", 13)
    )
    option_label.grid(row=0, column=0, pady=(0, 10))

    # dropdown for number of URLs
    option_dropdown = CTkComboBox(
        option_frame,
        values=[str(i) for i in range(1, 11)],
        font=("Helvetica", 13),
        command=on_option_select,
        corner_radius=32,
        border_color="#9502de",
    )
    option_dropdown.set(str(selected_option))
    option_dropdown.grid(row=1, column=1, pady=(0, 10))

    app.protocol("WM_DELETE_WINDOW", on_closing)
    return app


def on_closing():
    stop_bot()
    app.destroy()


app = create_gui()
app.mainloop()
