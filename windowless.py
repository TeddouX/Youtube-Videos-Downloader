from yt_dlp import YoutubeDL
from os import path, environ
from argparse import ArgumentParser
from sys import argv

PATH = path.join(path.join(environ['USERPROFILE']), 'Videos') + "/Downloaded"

argument_parser = ArgumentParser(prog="Youtube Downloader", description="Downloads youtube videos")
argument_parser.add_argument('filename')
argument_parser.add_argument('-u', '--url', help='The url of the program that you want downloaded', nargs='*', required=True)

def download(url: str):
    ydl_opts = {
        'format': 'best/bestvideo+bestaudio',
        'outtmpl': '{0}/%(title)s.%(ext)s'.format(PATH),
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    args = argument_parser.parse_args(argv)

    for i in args.url:
        download(i)