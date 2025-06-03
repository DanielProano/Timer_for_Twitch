import customtkinter as ctk
import time
import threading

class CTKTimer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CHALLENGE TIMER")
        self.geometry("300x150")
        self.overrideredirect(True)
        self.bind("<B1-Motion>", self.drag)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.output_file = "timer.txt"
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.timer_id = None

        self.start_button = ctk.CTkButton(self, text="Start", command=self.start_timer, width=35, height=35)
        self.start_button.place(x=80, y=100)

        self.pause_button = ctk.CTkButton(self, text="Pause", command=self.pause_timer, width=35, height=35)
        self.pause_button.place(x=130, y=100)

        self.reset_button = ctk.CTkButton(self, text="Reset", command=self.reset_timer, width=35, height=35)
        self.reset_button.place(x=190, y=100)

        self.textbox = ctk.CTkTextbox(self, fg_color="transparent", width=250, height=90, font=ctk.CTkFont(size=55, weight="bold"))
        self.textbox.place(x=25, y=5)
        #self.textbox.bind("<KeyRelease>", self.manual_time_update)
        self.textbox.insert("1.0", "00:00:00")
        self.textbox.tag_config("center", justify="center")
        self.textbox.tag_add("center", "1.0", "end")

    def parse(self, text):
        try:
            parts = list(map(int, text.strip().split(":")))
            if len(parts) == 3:
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:
                return parts[0] * 60 + parts[1]
            elif len(parts) == 1:
                return parts[0]
        except ValueError:
            return None

    def format_time(self, total_seconds):
        h = total_seconds // 3600
        m = (total_seconds % 3600) // 60
        s = total_seconds % 60
        if h > 0:
            return f"{h:02}:{m:02}:{s:02}"
        else:
            return f"{h:02}:{m:02}:{s:02}"

    def update_display(self, event=None):
        time_str = self.format_time(self.remaining_seconds)
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", time_str)
        with open(self.output_file, "w") as f:
            f.write(time_str)

    def manual_time_update(self, event=None):
        if self.running: return  # Don't allow edits while running
        text = self.textbox.get("1.0", "end-1c")
        seconds = self.parse(text)
        if seconds is not None:
            self.remaining_seconds = seconds
            self.update_display()

    def countdown(self):
        if self.running and not self.paused and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()
            self.timer_id = self.after(1000, self.countdown)
        elif self.remaining_seconds == 0:
            self.running = False
            self.update_display()

    def start_timer(self):
        if not self.running:
            text = self.textbox.get("1.0", "end-1c")
            seconds = self.parse(text)
            if seconds is not None:
                self.remaining_seconds = seconds
                self.update_display()
                self.running = True
                self.paused = False
                self.countdown()
        elif self.paused:
            self.paused = False
            self.countdown()

    def pause_timer(self):
        if self.running:
            self.paused = True

    def reset_timer(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        self.running = False
        self.paused = False
        self.remaining_seconds = 0
        self.update_display()

    def drag(self, event):
        self.geometry(f"+{event.x_root}+{event.y_root}")



if __name__ == "__main__":
    app = CTKTimer()
    app.mainloop()
