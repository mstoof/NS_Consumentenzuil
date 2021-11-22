import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

from Backend.API.send_tweet import get_tweets
from Backend.API.weather_api import weather_api
from Backend.database import Database


class Application(tk.Tk):
    "Application root window for tkinter GUI"

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('700x500')
        self.title("NS Consumenten Zuil")
        self.resizable(width=False, height=False)

        # Empty values
        self.review = ""
        self.name_entry = ""
        self.station_entry = ""
        self.send_button = ""

        # Reject message
        self.reject_message = ""
        self.reject_button = ""

        self.background_image = ImageTk.PhotoImage(Image.open("../Files/background.png"))
        self.background_image_lbl = tk.Label(self, image=self.background_image).place(x=0, y=0)
        self.ns_logo = ImageTk.PhotoImage(Image.open("../Files/ns_logo.png"))
        self.ns_logo_lbl = tk.Label(self, image=self.ns_logo, borderwidth=0).place(x=275, y=3)
        self.canvas = tk.Canvas(self, width=500, height=400, bg='white').place(x=100, y=50)

        self.header = tk.Label(self, text=f"NS Consumenten Zuil", bg='white', font=("TkDefaultFont", 16)).place(x=250,
                                                                                                                y=60)
        self.review_func()

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Review", command=self.review)
        filemenu.add_command(label="Moderator", command=self.moderator)
        filemenu.add_command(label="Screen", command=self.stationshal)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="Options", menu=filemenu)

        self.config(menu=menubar)

    def review_func(self):
        tk.Label(self, text="Name", bg='white', font=("TkDefaultFont", 12)).place(x=150, y=125)
        self.name_entry = tk.Entry(self, width=28, bg='#F5F5F5')
        self.name_entry.place(x=150, y=150)

        register = self.register(self.check_station_entry)
        tk.Label(self, text="Station", bg='white', font=("TkDefaultFont", 12)).place(x=375, y=125)
        self.station_entry = tk.Entry(self, width=28, bg='#F5F5F5', validate='key', validatecommand=(register, '%P'))
        self.station_entry.place(x=375, y=150)

        tk.Label(self, text="Message", bg='white', font=("TkDefaultFont", 12)).place(x=150, y=200)
        self.review_counter = tk.Label(self, text=0, bg='white', font=("TkDefaultFont", 12))
        self.review_counter.place(x=470, y=200)
        self.review_counter_max = tk.Label(self, text="/ 140", bg='white', font=("TkDefaultFont", 12))
        self.review_counter_max.place(x=500, y=200)
        self.review = tk.Text(self, bg='#F5F5F5', state='normal')
        self.review.bind('<KeyPress>', self.update)
        self.review.bind('<KeyRelease>', self.update)
        self.review.place(x=150, y=225, width=400, height=150)

        self.send_button = tk.Button(self, text="Send the Message", state='disabled', command=self.send_message,
                                     bg="green", fg="white")
        self.send_button.place(x=300, y=400)

    def moderator(self):

        conn = Database()
        newest_review = conn.get_review()
        try:
            id = newest_review[0]
            message = newest_review[1]
            time = newest_review[2]
            gebruiker_id = newest_review[3]

        except:
            self.canvas = tk.Canvas(self, width=500, height=400, bg='white').place(x=100, y=50)
            self.header = tk.Label(self, text=f"NS Consumenten Zuil", bg='white', font=('Tahoma', 16)).place(x=250,
                                                                                                             y=60)
            tk.Label(self, text="You're done for today! Check again tomorrow", bg='white',
                     font=("TkDefaultFont", 14)).place(x=175, y=250)

        if newest_review:
            self.canvas = tk.Canvas(self, width=500, height=400, bg='white').place(x=100, y=50)
            self.header = tk.Label(self, text=f"NS Consumenten Zuil", bg='white', font=('Tahoma', 16)).place(x=250,
                                                                                                             y=60)
            tk.Label(self, text=f"Message ID: {id}", bg='white', font=("TkDefaultFont", 12)).place(x=150, y=125)
            tk.Label(self, text=f"Gebruiker ID: {gebruiker_id}", bg='white',
                     font=("TkDefaultFont", 12)).place(x=150, y=150)
            tk.Label(self, text=f"time: {time}", bg='white', font=("TkDefaultFont", 12)).place(x=400, y=125)
            tk.Label(self, text="Mod ID: ", bg='white', font=("TkDefaultFont", 12)).place(x=400, y=150)

            mod_id = tk.Entry(self, width=8, bg='#F5F5F5')
            mod_id.place(x=475, y=153)

            tk.Label(self, text=f"Message: ", bg='white', font=("TkDefaultFont", 12)).place(x=150, y=200)
            tk.Label(self, text=f"{message}", bg='white', font=("TkDefaultFont", 10), wraplength=450).place(x=150,
                                                                                                            y=225)

            tk.Label(self, text="Reject Message:", bg='white', font=("TkDefaultFont", 12)).place(x=150, y=275)
            self.reject_message = tk.Text(self, bg='#F5F5F5')
            self.reject_message.bind('<KeyPress>', self.check_reject_entry)
            self.reject_message.bind('<KeyRelease>', self.check_reject_entry)
            self.reject_message.place(x=150, y=300, width=400, height=75)

            accept_button = tk.Button(self, text="Accept",
                                      command=lambda: self.moderate_review(id, "accept", message, time, mod_id.get(),
                                                                           gebruiker_id), bg="green", fg="white")
            accept_button.place(x=300, y=400)
            self.reject_button = tk.Button(self, text="Reject", state='disabled',
                                           command=lambda: self.moderate_review(id, "reject", message, time,
                                                                                mod_id.get(), gebruiker_id),
                                           bg="red", fg="white")
            self.reject_button.place(x=350, y=400)

    def stationshal(self, latest_tweet=False):
        self.canvas = tk.Canvas(self, width=500, height=400, bg='white').place(x=100, y=50)
        self.header = tk.Label(self, text=f"NS Consumenten Zuil", bg='white', font=('Tacoma', 16)).place(x=250, y=60)
        canvas1 = tk.Canvas(self, width=400, height=200, bg='#F5F5F5')
        canvas1.place(x=150, y=150)

        if not latest_tweet:
            latest_tweet = get_tweets()
            all_tweets = {}
            for index, single_tweet in enumerate(latest_tweet[:3]):
                all_tweets.update({index: {
                    'id': single_tweet.id,
                    'message': single_tweet.full_text,
                    'created_at': single_tweet.created_at
                }})
            current_tweet_iter = all_tweets.get(next(iter(all_tweets)))
        elif latest_tweet == -1:
            print('Weather will be shown')
            canvas1.destroy()
            canvas = tk.Canvas(self, width=400, height=200, bg='#F5F5F5').place(x=150, y=225)
            tk.Label(self, text="7 Day Weather Forecast", bg='white', font=("TkDefaultFont", 14)).place(x=145, y=90)
            self.clear_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/sunny_cloudy.png"))
            self.cloudy_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/cloudy.png"))
            self.thunder_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/thunder.png"))
            self.thunder_raining_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/thunder_raining.png"))
            self.sunny_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/sunny.png"))
            self.raining_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/raining.png"))
            self.freezing_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/freezing.png"))
            self.night_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/night.png"))
            self.cloudy_l_icon = ImageTk.PhotoImage(Image.open("../Files/weather_icons/cloudy_large.png"))

            temperatures = weather_api('Utrecht')
            index = 0
            for key, value in temperatures.items():

                today = datetime.now()
                if key == 'today':
                    today_temp = value['temperature']
                    feels_like = value['feels_like']
                    humidity = value['humidity']
                    type_of_weather = value['type_of_weather']

                    tk.Label(self, text=f"{today.day}, {today.month}, {today.year}", bg='white',
                             font=("TkDefaultFont", 14)).place(x=145, y=150)
                    tk.Label(self, text=f"{today_temp}°C", bg='white', font=("TkDefaultFont", 24)).place(x=140, y=175)
                    tk.Label(self, text=f"Feels like: {feels_like}", bg='white',
                             font=("TkDefaultFont", 12)).place(x=420, y=150)
                    tk.Label(self, text=f"Humidity: {humidity}", bg='white',
                             font=("TkDefaultFont", 12)).place(x=420, y=170)
                    tk.Label(self, text=f"Conditions: {type_of_weather}", bg='white',
                             font=("TkDefaultFont", 12)).place(x=420, y=190)

                    if type_of_weather == 'Clouds':
                        tk.Label(self, image=self.cloudy_l_icon, bg='white').place(x=300, y=150)
                    else:
                        tk.Label(self, image=self.cloudy_l_icon, bg='white').place(x=300, y=150)

                    continue

                index += 1
                temp = value['temperature_max']
                temp_min = value['temperature_min']
                type_of_weather = value['type_of_weather']
                if type_of_weather == 'Clouds':
                    tk.Label(self, image=self.cloudy_icon, bg='#F5F5F5').place(x=120 + (55 * index), y=255)

                elif type_of_weather == 'Clear':
                    tk.Label(self, image=self.clear_icon, bg='#F5F5F5').place(x=120 + (55 * index), y=255)

                elif type_of_weather == 'Rain':
                    tk.Label(self, image=self.raining_icon, bg='#F5F5F5').place(x=120 + (55 * index), y=255)

                elif type_of_weather == 'Sunny':
                    tk.Label(self, image=self.sunny_icon, bg='#F5F5F5').place(x=120 + (55 * index), y=255)

                elif type_of_weather == 'Thunder':
                    tk.Label(self, image=self.thunder_raining_icon, bg='#F5F5F5').place(x=120 + (55 * index), y=255)

                else:
                    tk.Label(self, image=self.night_icon, bg='#F5F5F5').place(x=120 + (55 * index), y=255)

                tk.Label(self, text=f"{key}", bg="#F5F5F5").place(x=120 + (55 * index), y=230)
                tk.Label(self, text=f"{type_of_weather}", wraplength=50, bg="#F5F5F5").place(x=120 + (55 * index),
                                                                                             y=300)
                tk.Label(self, text=f"{temp}", fg="red", bg="#F5F5F5").place(x=120 + (55 * index), y=325)
                tk.Label(self, text=f"{temp_min}", fg="blue", bg="#F5F5F5").place(x=120 + (55 * index), y=350)

        else:
            all_tweets = latest_tweet
            current_tweet_iter = latest_tweet.get(next(iter(latest_tweet)))

        if latest_tweet != -1:
            db = Database()
            db_information = db.get_review_by_tweet(current_tweet_iter.get('id'))
            name = db.get_name_by_id(db_information[6])[0].strip()
            tweet_date = current_tweet_iter.get('created_at')
            tk.Label(self, text="Latest Tweets", bg='white', font=("TkDefaultFont", 14)).place(x=150, y=120)
            self.user_image = ImageTk.PhotoImage(Image.open("../Files/anonymous_user.png"))
            tk.Label(self, image=self.user_image).place(x=175, y=200)
            self.username = tk.Label(self, text=name, fg='black', bg='#F5F5F5', font=("TkDefaultFont", 10, 'bold'))
            self.tweet_date = tk.Label(self, text=f"{tweet_date.day}/{tweet_date.month}", bg='#F5F5F5',
                                       font=("TkDefaultFont", 10))
            self.tweet_text = tk.Label(self, text=current_tweet_iter.get('message'), bg='#F5F5F5')
            self.tweet_date.place(x=325, y=200)
            self.username.place(x=250, y=200)
            self.tweet_text.place(x=250, y=220)

            self.after(3000, lambda: self.renew_tweet(all_tweets))

    def renew_tweet(self, tweet):
        tweet.pop(next(iter(tweet)))
        try:
            latest_tweet = tweet.get(next(iter(tweet)))
            tweet_id = latest_tweet.get('id')
            tweet_date = latest_tweet.get('created_at')
            tweet_message = latest_tweet.get('message')
            db = Database()
            db_information = db.get_review_by_tweet(tweet_id)
            try:
                name = db.get_name_by_id(db_information[6])[0].strip()

            except TypeError:
                name = 'anoniem'

            self.tweet_date.config(text=f'{tweet_date.day}/{tweet_date.month}')
            self.username.config(text=f'{name}')
            self.tweet_text.config(text=f'{tweet_message}')

            self.stationshal(tweet)
        except:
            self.stationshal(-1)

    def update(self, event):
        review = self.review.get('1.0', 'end')
        if len(review) == 140:  # The first keypress will not include a single letter
            self.validate_length()
        self.review_counter.config(text=len(review))

    def validate_length(self):
        self.review.config(state=('disabled'))

    def check_station_entry(self, input):
        self.send_button.config(state=('normal' if input else 'disabled'))

    def check_reject_entry(self, input):
        if len(self.reject_message.get('1.0', 'end')) != 0:
            self.reject_button.config(state=('normal' if input else 'disabled'))

    def moderate_review(self, id, approval, commentaar, tijd, mod_id, gebruiker_id):
        conn = Database()
        if approval == "accept":
            conn.moderate_reviews(id, 1, commentaar, tijd, mod_id, gebruiker_id)
            self.moderator()
        else:
            conn.moderate_reviews(id, 0, commentaar, tijd, mod_id, gebruiker_id)
            self.moderator()

    def send_message(self):
        naam = self.name_entry.get()
        review = self.review.get("1.0", "end")
        station = self.station_entry.get()
        naam = 'anoniem' if naam == '' else naam
        time = datetime.now()

        conn = Database()
        gebruiker_id = conn.new_user(naam, station)
        conn.new_review(gebruiker_id, review, time)

        messagebox.showinfo("Response", message="Your response has been received! \n"
                                                "And will be reviewed by our Moderators before being posted.")
        self.destroy()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
