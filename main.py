from tkinter import StringVar
from typing import Tuple
from customtkinter import CTkLabel, CTkProgressBar, CTkButton, CTkEntry, CTk
from asyncio import run
from threading import Thread
from yt_dlp import YoutubeDL
from os import path, environ, getenv, system as run_command
from subprocess import run as run_subprocess
from re import compile, VERBOSE
from argparse import ArgumentParser
from sys import argv

argument_parser = ArgumentParser(prog='Youtube Downloader', description='Downloads Youtube videos')
argument_parser.add_argument('filename') 
argument_parser.add_argument('-c', '--compile', help='Compiles the file', action='store_true')

COMPILE_COMMAND = "pyinstaller --noconfirm --onefile --windowed --icon \"C:/Users/Victor/Desktop/Programming/Python/Youtube Downloader/icon.ico\" --name \"Youtube Downloader\" --collect-all customtkinter \"C:/Users/Victor/Desktop/Programming/Python/Youtube Downloader/main.py\""

PATH = path.join(path.join(environ['USERPROFILE']), 'Videos') + "/Downloaded"
FILEBROWSER_PATH = path.join(getenv('WINDIR'), 'explorer.exe')
ANSI_ESCAPE = compile(r'''
    \x1B  # ESC
    (?:   # 7-bit C1 Fe (except CSI)
        [@-Z\\-_]|     # or [ for CSI, followed by a control sequence
        \[
        [0-?]*  # Parameter bytes
        [ -/]*  # Intermediate bytes
        [@-~]   # Final byte
    )
''', VERBOSE)


class AppWindow(CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Youtube Downloader")
        self.geometry("500x400")
        self.minsize(500, 400)

        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_columnconfigure((0), weight=1)

        self.download_txt = StringVar(master=self, value='Download status')

        url = CTkEntry(master=self, width=425, placeholder_text="Enter URL here", font=("Arial", 11))
        url.grid(column=0, row=1)
        url.grid_rowconfigure(1, weight=2)
        url.grid_columnconfigure(1, weight=2)

        download_btn = CTkButton(master=self, text='Download', command=lambda: start_download(url.get()))
        download_btn.grid(column=0, row=2)
        download_btn.grid_rowconfigure(2, weight=1)
        download_btn.grid_columnconfigure(2, weight=1)
        download_btn.configure(text='Download')

        self.download_progressbar = CTkProgressBar(master=self, width=320)
        self.download_progressbar.grid(column=0, row=3)
        self.download_progressbar.set(0)
        self.download_progressbar.grid_rowconfigure(3, weight=1)
        self.download_progressbar.grid_columnconfigure(3, weight=1)

        download_txt_label = CTkLabel(master=self, textvariable=self.download_txt)
        download_txt_label.grid(column=0, row=4)
        download_txt_label.grid_rowconfigure(4, weight=1)
        download_txt_label.grid_columnconfigure(4, weight=1)

        self.open_folder_btn = CTkButton(master=self, text='', fg_color="transparent", state="disabled", command=lambda: explore(PATH))
        self.open_folder_btn.grid(column=0, row=5)
        self.open_folder_btn.grid_rowconfigure(5, weight=1)
        self.open_folder_btn.grid_columnconfigure(5, weight=1)

    def show_file_btn(self, b: bool):
        if b:
            self.open_folder_btn.configure(text='Open file location', fg_color=("#3a7ebf", "#1f538d"), state="normal")
        else:
            self.open_folder_btn.configure(text='', fg_color="transparent", state="disabled")
            

def explore(path_):
    path_ = path.normpath(path_)

    if path.isdir(path_):
        run_subprocess([FILEBROWSER_PATH, path_])
    elif path.isfile(path_):
        run_subprocess([FILEBROWSER_PATH, '/select,', path_])

def progress_hook(data: dict[str]):
    if data['status'] == 'downloading':
        percent = ANSI_ESCAPE.sub('', data['_percent_str'].replace(' ', '').replace('%', ''))
        time_remaining = ANSI_ESCAPE.sub('', data['_eta_str'].replace(' ', ''))
        size = ANSI_ESCAPE.sub('', data['_total_bytes_str'].replace(' ', ''))
        size_remaining = ANSI_ESCAPE.sub('', data['_downloaded_bytes_str'].replace(' ', ''))
        elapsed = ANSI_ESCAPE.sub('', data['_elapsed_str'].replace(' ', ''))
        download_speed = ANSI_ESCAPE.sub('', data['_speed_str'].replace(' ', ''))

        window.download_progressbar.set(float(percent)/100)
        window.download_txt.set(f'\n{percent}% \n {size_remaining} of {size} at {download_speed} \n\n Time remaining: {time_remaining} \n Time elapsed: {elapsed}')
    if data['status'] == 'finished':
        window.show_file_btn(True)
        window.download_txt.set('Finished. Your video is in your \'Videos\' folder')

def start_download(url: str):
    thread = Thread(target=lambda: run(download(url)))
    window.show_file_btn(False)
    thread.start()

async def download(url: str):
    ydl_opts = {
        'format': 'best/bestvideo+bestaudio',
        'outtmpl': '{0}/%(title)s.%(ext)s'.format(PATH),
        'progress_hooks': [progress_hook],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    window = AppWindow()
    args = argument_parser.parse_args(argv)

    if args.compile:
        run_command(COMPILE_COMMAND)
    else:
        window.mainloop()

