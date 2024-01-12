from customtkinter import *
from selenium import webdriver
import threading
import time
import random


class BrowserBot:
    def __init__(self):
        self.drivers = {}
        self.running = False
        self.selected_option = 1
        self.all_urls = [
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
        self.refresh_interval = 300

        self.app = self.create_gui()

    def create_gui(self):
        app = CTk()
        app.title("By:TRON")
        app.geometry("400x400")
        set_appearance_mode("dark")
        deactivate_automatic_dpi_awareness()

        # button
        button_start = CTkButton(
            app,
            fg_color="transparent",
            text="Start",
            command=self.button_start_event,
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
            command=self.button_stop_event,
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

        # dropdown for the number of URLs
        option_dropdown = CTkComboBox(
            option_frame,
            values=[str(i) for i in range(1, 11)],
            font=("Helvetica", 13),
            command=self.on_option_select,
            corner_radius=32,
            border_color="#9502de",
        )
        option_dropdown.set(str(self.selected_option))
        option_dropdown.grid(row=1, column=1, pady=(0, 10))

        app.protocol("WM_DELETE_WINDOW", self.on_closing)
        return app

    def run_bot(self, urls):
        chromedriver_path = "C:/ChromeDriver/chromedriver.exe"

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)",
            "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
            "Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1",
            "Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; MAR-LX1A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; moto g stylus 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36v",
            "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-A515U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
        ]

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-insecure-localhost')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])

        try:
            for url in urls:
                service = webdriver.chrome.service.Service(chromedriver_path)
                driver = webdriver.Chrome(
                    service=service, options=chrome_options)
                self.drivers[url] = driver

            while self.running:
                time.sleep(self.refresh_interval)
                for url, driver in self.drivers.items():
                    # Set user agent for each request
                    user_agent = random.choice(user_agents)
                    driver.execute_cdp_cmd(
                        "Network.setUserAgentOverride", {
                            "userAgent": user_agent}
                    )
                    driver.get(url)
                    if not self.check_browser_status(driver):
                        print("Browser telah ditutup oleh user")
                        self.stop_bot()
                        break
        finally:
            for driver in self.drivers.values():
                driver.quit()

    def start_bot(self):
        if not self.running:
            self.running = True
            selected_urls = self.all_urls[:int(self.selected_option)]
            threading.Thread(target=self.run_bot,
                             args=(selected_urls,)).start()

    def check_browser_status(self, driver):
        try:
            driver.title
            return True
        except Exception:
            return False

    def stop_bot(self):
        self.running = False

    def on_option_select(self, selection):
        self.selected_option = selection

    def button_start_event(self):
        self.start_bot()

    def button_stop_event(self):
        self.stop_bot()

    def on_closing(self):
        self.stop_bot()
        self.app.destroy()


if __name__ == "__main__":
    bot = BrowserBot()
    bot.app.mainloop()
