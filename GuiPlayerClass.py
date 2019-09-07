import vlc, os, sys, time, pickle
from tkinter import filedialog
import tkinter as tk

class GuiPlayerClass(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.load_audio_from = os.getcwd()
        # set wimdow title
        self.title("...")
        # set widow geometry
        self.geometry('370x200+500+200')
        # set close button acrion
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # initialize player instance
        self.instance = vlc.Instance()
        # plying file nidex
        self.file_index = 0
        # new player object
        self.player = self.instance.media_player_new()
        # set default volume
        self.i_volume = 50

        # set play button and pleace it on window
        self.play_button = tk.Button(self, text='>', command=self.play)
        self.play_button.place(x=20, y=160)

        # set stop button and pleace it on window
        self.stop_button = tk.Button(self, text='[]', command=self.stop)
        self.stop_button.place(x=40, y=160)

        # set pause button and pleace it on window
        self.pause_button = tk.Button(self, text='II', command=self.pause)
        self.pause_button.place(x=80, y=160)

        # set play next button and pleace it on window
        self.play_next_button = tk.Button(self, text='>>I', command=self.play_next)
        self.play_next_button.place(x=100, y=160)

        # set play previous button and pleace it on window
        self.play_prev_button = tk.Button(self, text='I<<', command=self.play_prev)
        self.play_prev_button.place(x=130, y=160)

        # set volume up button and pleace it on window
        self.volume_up = tk.Button(self, text='vol up', command=self.vol_up)
        self.volume_up.place(x=200, y=160)

        # set volume down button and pleace it on window
        self.volume_down = tk.Button(self, text='vol down', command=self.vol_down)
        self.volume_down.place(x=250, y=160)

        # set save progress button and pleace it on window
        self.save_button = tk.Button(self, text='M+', command=self.save_progress)
        self.save_button.place(x=300, y=120)

        # set load progress button and pleace it on window
        self.load_button = tk.Button(self, text='M-', command=self.load_progress)
        self.load_button.place(x=300, y=85)

        # set play directory button and pleace it on window
        self.set_dir = tk.Button(self, text='Load From', command=self.set_audio_directory)
        self.set_dir.place(x=300, y=60)

        # set text box
        self.output_text = ""
        self.text = tk.Text(self, height=1, width=30)
        self.text.place(x=30, y=100)
        self.text.insert(tk.END, self.output_text)

        # set check box
        self.play_all = tk.IntVar()
        self.check_box_1 = tk.Checkbutton(self, text="Play All", variable=self.play_all)
        self.check_box_1.place(x=0, y=0)

        # set check box
        self.mute = tk.IntVar()
        self.check_box_2 = tk.Checkbutton(self, text="Mute", variable=self.mute)
        self.check_box_2.place(x=0, y=20)

        # filtered - playable files list
        self.file_list = []
        self.set_playlist()
        self.load_file()

        # periodicaly call self.test_player_state method
        self.after(1000, self.test_player_state)

    def set_audio_directory(self):
        load_audio_from = tk.filedialog.askdirectory()
        if 0 < len(load_audio_from):
            self.load_audio_from = load_audio_from
            self.set_playlist()
            self.load_file()
            print(load_audio_from)


    def test_player_state(self):
        state = self.player.get_state()
        if state == vlc.State.NothingSpecial:
            pass
        elif state == vlc.State.Opening:
            pass
        elif state == vlc.State.Buffering:
            pass
        elif state == vlc.State.Playing:
            pass
        elif state == vlc.State.Paused:
            pass
        elif state == vlc.State.Stopped:
            pass
        elif state == vlc.State.Ended and self.play_all.get():
            self.play_next()
        elif state == vlc.State.Error:
            pass

        self.after(1000, self.test_player_state)

    def load_file(self):
        if 0 < len(self.file_list):
            #Get file name from files list
            filename = self.file_list[self.file_index]
            #Save filename as self.output_text
            self.output_text = filename
            #Clear text box
            self.text.delete('1.0', tk.END)
            #Insert text into text box
            self.text.insert(tk.END, self.output_text)
            #Get absolute path
            absolute_path = os.path.join(self.load_audio_from, filename)
            #Load the media file
            self.media = self.instance.media_new(absolute_path)
            #Give media variable to player
            self.player.set_media(self.media)

    def set_playlist(self):
        files_list = os.listdir(self.load_audio_from )
        for name in files_list:
            if '.mp3' in name:
                print("loading file ", name)
                self.file_list.append(name)
            elif '.ogg' in name:
                print("loading file ", name)
                self.file_list.append(name)
            elif '.wav' in name:
                print("loading file ", name)
                self.file_list.append(name)
            elif '.mp3' in name:
                print("loading file ", name)
                self.file_list.append(name)
            elif '.mp3' in name:
                print("loading file ", name)
                self.file_list.append(name)

    def vol_up(self):
        self.i_volume += 5
        self.player.audio_set_volume(self.i_volume)
        print('current volume ', self.i_volume)

    def vol_down(self):
        self.i_volume -= 5
        self.player.audio_set_volume(self.i_volume)
        print('current volume ', self.i_volume)

    def play(self):
        print('play')
        self.player.play()

    def stop(self):
        self.player.stop()

    def pause(self):
        self.player.pause()

    def play_prev(self):
        if self.file_index > 0:
            self.file_index -= 1
            self.load_file()
            self.play()

    def play_next(self):
        if self.file_index < len(self.file_list):
            self.file_index += 1
            self.load_file()
            self.play()

    def save_progress(self):
        play_time = self.player.get_time()
        playing_file_index = self.file_index
        load_audio_from = self.load_audio_from
        progress_data = {"load_audio_from":load_audio_from,"file_index":playing_file_index, "play_time":play_time}

        print(progress_data)
        f = open("play_time_progress.bat", "wb")
        pickle.dump(progress_data, f)
        f.close()

    def load_progress(self):
        f = open("play_time_progress.bat", "rb")
        progress_data = pickle.load(f)
        f.close()

        print(progress_data)
        self.file_index = progress_data["file_index"]
        play_time = progress_data["play_time"]
        self.load_file()
        self.player.set_time(play_time)

    def on_closing(self):
        self.save_progress()
        self.player.stop()
        self.destroy()

if __name__ == "__main__":
    
    playerObject = GuiPlayerClass()
    playerObject.mainloop()
 
