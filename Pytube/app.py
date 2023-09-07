from tkinter import *
from pytube import YouTube

root = Tk()
root.title("Youtube Video Downloader")
root.geometry('768x500')

def ask_quit():
    label = Label(root, text="Your video has been downloaded...Please Check")
    label.pack()
    btn = Button(root, text="Quit", command=exit)
    btn.pack()

def download_video_low():
    my_video = YouTube(url.get())
    my_video = my_video.streams.get_lowest_resolution()
    my_video.download()
    ask_quit()

def download_video_high():
    my_video = YouTube(url.get())
    my_video = my_video.streams.get_highest_resolution()
    my_video.download()
    ask_quit()


url = StringVar()

label = Label(root, text="Enter the url here")
label.pack()

input_url = Entry(root, textvariable=url)
input_url.pack()

btn = Button(root, text="Download with lowest resolution", command=download_video_low)
btn.pack()

btn = Button(root, text="Download for highest resolution", command=download_video_high)
btn.pack()


# url = 'https://www.youtube.com/watch?v=tPEE9ZwTmy0'
# my_video = YouTube(url)

# my_video = my_video.streams.get_lowest_resolution()
# my_video.download()

root.mainloop()