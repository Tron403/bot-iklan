from customtkinter import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
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

        with open('user_agents.txt', 'r') as file:
            self.user_agents = [line.strip() for line in file]

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
                threads = []
                for url, driver in self.drivers.items():
                    thread = threading.Thread(
                        target=self.process_url, args=(driver, url))
                    threads.append(thread)
                    thread.start()

                # Join all threads to wait for them to finish
                for thread in threads:
                    thread.join()

        finally:
            for driver in self.drivers.values():
                driver.quit()

    def process_url(self, driver, url):
        try:
            # Cek jumlah tab saat ini
            if len(driver.window_handles) > 1:
                # Tutup tab tambahan jika ada lebih dari satu tab
                for handle in driver.window_handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()
                    # Kembalikan fokus ke tab pertama
                driver.switch_to.window(driver.window_handles[0])

            user_agent = random.choice(self.user_agents)
            driver.execute_cdp_cmd(
                "Network.setUserAgentOverride", {"userAgent": user_agent}
            )
            driver.get(url)

            # Atur header HTTP untuk mengatasi deteksi proxy
            driver.execute_cdp_cmd("Network.clearBrowserCookies", {})
            driver.execute_cdp_cmd("Network.clearBrowserCache", {})
            driver.execute_cdp_cmd(
                "Network.setExtraHTTPHeaders",
                {"headers": {"Proxy-Control": "no-cache"}}
            )

            driver.refresh()
            time.sleep(self.refresh_interval)

            if not self.check_browser_status(driver):
                print("Browser telah ditutup oleh user")
                self.stop_bot()
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    def start_bot(self):
        if not self.running:
            self.running = True
            selected_urls = self.all_urls[:int(self.selected_option)]
            threading.Thread(target=self.run_bot,
                             args=(selected_urls,)).start()

    def check_browser_status(self, driver):
        try:
            # Check if the window handle is still valid
            current_window_handle = driver.current_window_handle
            driver.switch_to.window(current_window_handle)
            return True
        except NoSuchWindowException:
            # Handle the case where the window is already closed
            return False
        except Exception as e:
            # Handle other exceptions if necessary
            print(f"Error checking browser status: {e}")
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
