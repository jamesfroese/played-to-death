import os
import sys
import requests
import math
import operator
import time as t
from datetime import datetime, date, time
import tzlocal

wURL = "https://socast-public.s3.amazonaws.com/player/lp_2066_1909.js"
HEADERS = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
TIMER = 15 #minutes
SIX_AM = t.mktime((datetime.combine(date.today(), time(hour=6, minute=0))).timetuple())


def print_song_count(count):
    sorted_count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    local_timezone = tzlocal.get_localzone()
    local_time = (datetime.fromtimestamp(first_song, local_timezone))

    total = 0
    for key in count.keys():
        total += count[key]
    print("\nTotal Songs Played: {}".format(total))

    i = 0
    while i < 20:
        song = sorted_count[i][0].split("_")[0]
        artist = sorted_count[i][0].split("_")[1]
        count = sorted_count[i][1]
        print("COUNT: {} -{} by {} since {}".format(count, song, artist, local_time.strftime("%m-%d %H:%M:%S")))
        i += 1

def call_station(previous_call_last_song, most_recent_song, first_song):
    previous_call_last_song = previous_call_last_song
    most_recent_song = most_recent_song
    first_song = first_song

    try:
        r = requests.get(wURL, headers=HEADERS, timeout=10)
        songs = r.json()
        if r.status_code == 200:
            for s in songs:
                if s["last_played"] > previous_call_last_song:
                    print("{} added".format(s["song_name"]))
                    if "{}_{}".format(s["song_name"], s["artist_name"]) not in count.keys():
                        count["{}_{}".format(s["song_name"], s["artist_name"])] = 1
                    else:
                        count["{}_{}".format(s["song_name"], s["artist_name"])] += 1
                    if s["last_played"] > most_recent_song:
                        most_recent_song = s["last_played"]
                else:
                    previous_call_last_song = most_recent_song
                    break

            if first_song == None:
                first_song = s["last_played"]
            previous_call_last_song = most_recent_song
            return previous_call_last_song, most_recent_song, first_song
        else:
            return None, None
    except Exception as e:
        print("Response Failed")
        print(e)
        print("Try again next cycle")
        return previous_call_last_song, most_recent_song, 1

if __name__ == "__main__":
    count = {}
    previous_call_last_song = 0 
    most_recent_song = 0
    first_song = None

    if "--workday" in sys.argv:
        previous_call_last_song = SIX_AM #6 am local time
        most_recent_song= SIX_AM

    try:
        while True:
            print("Try for \'new\' music")
            p, m, e = call_station(previous_call_last_song, most_recent_song, first_song)
            print("waiting...\n")

            if first_song == None:
                first_song = e
            if p != None:
                previous_call_last_song = p
                most_recent_song = m
                t.sleep(60 * TIMER)
            else:
                t.sleep(60)
    except KeyboardInterrupt as e:
        call_station(previous_call_last_song, most_recent_song, first_song)
    except Exception as e:
        print(e)
    finally:
        print_song_count(count)
