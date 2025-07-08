import customtkinter as ctk
from tkinter import filedialog
import pyshorteners
import pyperclip
import qrcode
from datetime import datetime

# Set AMOLED appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class LinkShortenerPro(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🔗 Link Shortener Pro - Y7X AMOLED Edition")
        self.geometry("580x580")
        self.configure(bg="#000000")
        self.resizable(False, False)

        self.short_history = []

        # === Title ===
        self.logo_label = ctk.CTkLabel(
            self, text="🔗 Link Shortener Pro", font=("Segoe UI Black", 24),
            text_color="#FF4B4B"
        )
        self.logo_label.pack(pady=(15, 8))

        # === Shortener Dropdown ===
        self.shortener_var = ctk.StringVar(value="TinyURL")
        self.shortener_menu = ctk.CTkOptionMenu(
            self, values=["TinyURL", "Is.gd"], variable=self.shortener_var,
            width=180, fg_color="#000000", button_color="#FF4B4B", text_color="white"
        )
        self.shortener_menu.pack(pady=5)

        # === URL Input ===
        self.url_entry = ctk.CTkEntry(
            self, placeholder_text="Paste your long URL here...",
            width=520, height=45, fg_color="#000000", text_color="white",
            border_color="#FF4B4B", border_width=2, corner_radius=20
        )
        self.url_entry.pack(pady=10)

        # === Shorten Button ===
        self.shorten_btn = ctk.CTkButton(
            self, text="✂️ Shorten", command=self.shorten_link,
            width=140, height=45, fg_color="#FF4B4B", hover_color="#FF2222",
            text_color="white", font=("Segoe UI", 15), corner_radius=15
        )
        self.shorten_btn.pack(pady=(8, 5))

        # === Save Button ===
        self.save_btn = ctk.CTkButton(
            self, text="💾 Save", command=self.save_link,
            width=140, height=45, fg_color="#000000", hover_color="#1a1a1a",
            border_color="#FF4B4B", border_width=2, text_color="#FF4B4B",
            font=("Segoe UI", 15), corner_radius=15
        )
        self.save_btn.pack(pady=(0, 10))

        # === Short URL Result Box ===
        self.result_box = ctk.CTkTextbox(
            self, height=50, width=520, fg_color="#000000", font=("Segoe UI", 14),
            text_color="#00FFAA", corner_radius=15, border_color="#FF4B4B", border_width=2
        )
        self.result_box.pack(pady=(12, 5))
        self.result_box.insert("0.0", "✅ Your short URL will appear here...")
        self.result_box.configure(state="disabled")
        self.result_box.bind("<Button-1>", self.copy_result)

        # === QR Code Button ===
        self.qr_btn = ctk.CTkButton(
            self, text="📱 Generate QR Code", command=self.generate_qr,
            fg_color="#000000", hover_color="#222222", text_color="white",
            border_color="#FF4B4B", border_width=2, width=200, corner_radius=15
        )
        self.qr_btn.pack(pady=5)

        # === History Label ===
        self.history_label = ctk.CTkLabel(
            self, text="🕓 Shortened History", font=("Segoe UI", 14),
            text_color="#888888"
        )
        self.history_label.pack(pady=(10, 0))

        # === History Box ===
        self.history_box = ctk.CTkTextbox(
            self, width=520, height=100, fg_color="#000000", text_color="#888888",
            corner_radius=15, font=("Consolas", 12), border_color="#333333", border_width=1
        )
        self.history_box.pack(pady=(5, 10))
        self.history_box.insert("0.0", "📝 Shortened links will appear here...")
        self.history_box.configure(state="disabled")

        # === Footer ===
        self.footer = ctk.CTkLabel(
            self, text="🔎 Powered by Y7X 💗", font=("Courier New", 13),
            text_color="#555555"
        )
        self.footer.pack(side="bottom", pady=6)

    def shorten_link(self):
        long_url = self.url_entry.get().strip()
        if not long_url:
            self.show_result("⚠️ Please enter a URL.", "orange")
            return

        try:
            s = pyshorteners.Shortener()
            short_url = ""
            if self.shortener_var.get() == "TinyURL":
                short_url = s.tinyurl.short(long_url)
            elif self.shortener_var.get() == "Is.gd":
                short_url = s.isgd.short(long_url)

            pyperclip.copy(short_url)
            self.show_result(f"🔗 {short_url}  📋 (Copied!)", "#00FFAA")
            self.log_history(short_url)

        except Exception as e:
            self.show_result(f"❌ Error: {e}", "red")

    def show_result(self, text, color="#00FFAA"):
        self.result_box.configure(state="normal")
        self.result_box.delete("0.0", "end")
        self.result_box.insert("0.0", text)
        self.result_box.configure(state="disabled", text_color=color)

    def log_history(self, link):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"[{timestamp}] {link}\n"
        self.history_box.configure(state="normal")
        self.history_box.insert("1.0", entry)
        self.history_box.configure(state="disabled")

    def copy_result(self, event=None):
        try:
            self.result_box.configure(state="normal")
            result_text = self.result_box.get("0.0", "end").strip()
            if "http" in result_text:
                pyperclip.copy(result_text.split()[1])
                self.show_result(f"📋 Copied to clipboard!\n{result_text.split()[1]}", "#00FFAA")
        finally:
            self.result_box.configure(state="disabled")

    def save_link(self):
        result = self.result_box.get("0.0", "end").strip()
        if "http" in result:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text Files", "*.txt")])
            if filepath:
                with open(filepath, "a") as f:
                    f.write(result.split()[1] + "\n")
                self.show_result("✅ Link saved successfully!", "#FF4B4B")
        else:
            self.show_result("⚠️ No link to save.", "orange")

    def generate_qr(self):
        result = self.result_box.get("0.0", "end").strip()
        if "http" not in result:
            self.show_result("⚠️ No link to generate QR for!", "orange")
            return
        link = result.split()[1]
        qr = qrcode.make(link)
        qr.show()


if __name__ == "__main__":
    app = LinkShortenerPro()
    app.mainloop()