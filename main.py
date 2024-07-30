import tkinter as tk
from tkinter import filedialog, messagebox
from yt_dlp import YoutubeDL
import os
import threading
import ttkbootstrap as ttkb
from ttkbootstrap.constants import X, LEFT, RIGHT, BOTH, TOP

# フォントの設定
FONT_TYPE = ("游ゴシック", 10)

class Application(ttkb.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10, 20, 40))

        master.geometry("600x400")
        master.title("動画ダウンローダー")

        self.create_widgets(master)
        self.master.protocol("WM_DELETE_WINDOW", self.closeApp)

    def create_widgets(self, master):
        self.create_folder_button(master)
        self.create_folder_label(master)
        self.create_url_entry(master)
        self.create_radio_buttons(master)
        self.create_download_button(master)

    def create_folder_button(self, master):
        button = tk.Button(
            master,
            text="フォルダダイアログを開く",
            font=("", 14),
            width=24,
            height=1,
            bg="#999999",
            activebackground="#aaaaaa",
        )
        button.bind("<ButtonPress>", self.folder_dialog)
        button.pack(pady=10)

    def create_folder_label(self, master):
        self.folder = tk.StringVar()
        self.folder.set("未選択です")
        label = tk.Label(textvariable=self.folder, font=("", 12), wraplength=500)
        label.pack(pady=10)

    def create_url_entry(self, master):
        frame = tk.Frame(master)
        frame.pack(pady=10)
        
        label = tk.Label(frame, text="ビデオURLを入力:", font=("", 12))
        label.pack(side=LEFT)
        
        self.intxt = tk.Entry(frame, width=40, font=("", 12))
        self.intxt.pack(side=LEFT, padx=5)

    def create_radio_buttons(self, master):
        radio_frame = tk.Frame(master)
        radio_frame.pack(pady=20)

        self.radio_var = tk.IntVar()
        self.radio_text = ["音楽", "動画"]

        for i, text in enumerate(self.radio_text):
            radio = tk.Radiobutton(
                radio_frame, value=i, variable=self.radio_var, text=text, font=("", 14)
            )
            radio.pack(side=LEFT, padx=20)

    def create_download_button(self, master):
        sendbtn = tk.Button(
            master, text="ビデオをダウンロード", font=("", 14), width=24, height=1
        )
        sendbtn.bind("<ButtonPress>", self.start_dl_thread)
        sendbtn.pack(pady=20)

    def folder_dialog(self, event):
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.folder_name = tk.filedialog.askdirectory(initialdir=iDir)
        if len(self.folder_name) == 0:
            self.folder.set("選択をキャンセルしました")
        else:
            self.folder.set(self.folder_name)

    def start_dl_thread(self, event):
        threading.Thread(target=self.dl).start()

    def dl(self):
        num = self.radio_var.get()
        mode = self.radio_text[num]
        url = self.intxt.get()
        self.intxt.delete(0, tk.END)

        path = "E:/ffmpeg-master-latest-win64-gpl-shared/bin"
        os.environ["PATH"] += "" if path in os.environ["PATH"] else ";" + path

        options = {
            "outtmpl": f"{self.folder_name}/%(title)s.%(ext)s",
            "format": "bestaudio/best" if mode == "音楽" else "bestvideo+bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {"key": "FFmpegMetadata"},
            ] if mode == "音楽" else [],
            "http_headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            },
        }

        ydl = YoutubeDL(options)

        try:
            ydl.extract_info(url, download=True)
            messagebox.showinfo("成功", "ビデオのダウンロードが完了しました")
        except Exception as e:
            messagebox.showerror("エラー", f"ビデオのダウンロードに失敗しました: {str(e)}")

    def closeApp(self):
        if (
            messagebox.askquestion(
                title="確認", message="アプリを終了してよろしいですか?"
            )
            == "yes"
        ):
            self.master.destroy()

def main():
    winMain = ttkb.Window(
        title="動画ダウンローダー", themename="superhero", resizable=(False, False)
    )
    Application(winMain)
    winMain.mainloop()

if __name__ == "__main__":
    main()
