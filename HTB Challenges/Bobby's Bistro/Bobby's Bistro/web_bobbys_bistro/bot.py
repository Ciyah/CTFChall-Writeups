import requests
from dotenv import load_dotenv
import os
from time import sleep
import random

ENV_FILE = "/shared/.env"

# Wait until .env is created
while not os.path.exists(ENV_FILE):
    sleep(0.5)

print("[+] Bot started")
load_dotenv(dotenv_path=ENV_FILE)

# Base setup
HOST = "localhost"
PORT = 3000
BASE_URL = f"http://{HOST}:{PORT}"

# URLs
login_url = BASE_URL + "/login"
chat_url = BASE_URL + "/api/chat-messages"
announcements_url = BASE_URL + "/api/announcements"

# Admin credentials
admin_username = os.getenv("ADMIN_USERNAME")
admin_password = os.getenv("ADMIN_PASSWORD")

# Announcements
announcement_1 = """
# Heyyyy

Welcome to Bobby's Bistro. All we do here is chat around 🙃
So feel free to hang out and have fun, I know you will 😀

> Please don't try and break stuff, I just built this damn thing

ggs
"""

announcement_2 = """
# Vacations

Since 2026 is right around the corner, I am taking a quick break
So, while I am gone, q-bit will take over admin duties, if you don't know who q-bit is, he's my admin bot
He will be using my account to take care of all this

Enjoy :)

> Since we're new on the block, I know you guys are gonna be upto some crazy monkey business, so I added a safety net 😈, try anything funny and it's gonna be a lockout for you until I am back 😂

ggs
"""

# Session & Login
session = requests.session()
login = session.post(
    login_url,
    data={"username": admin_username, "password": admin_password},
    allow_redirects=True,
)

if "Something went wrong" in login.text or "Wrong Credentials" in login.text:
    print("Login Failed")
    exit()
else:
    print("[+] Login Successful")
    print(session.cookies)

# Post Announcements
for title, announcement in [("Welcome", announcement_1), ("Vacations", announcement_2)]:
    resp = session.post(
        announcements_url, data={"title": title, "announcement": announcement}
    )
    if resp.status_code == 200:
        print(f"[+] Made announcement '{title}' successfully")
    else:
        print(f"[-] Failed to make announcement '{title}'")

# q-bit
last_seen_timestamp = None

greeting_replies = [
    "Hey there 👋",
    "Yo! q-bit checking in",
    "Hello hello!",
    "What’s up, folks?",
    "Heyyy everyone",
    "Hi! Hope you’re all doing well",
    "Sup 😄",
    "Greetings from q-bit 🤖",
    "Hey! Just popping in",
    "Howdy! 👋",
    "Hi there! Hope you’re having a good day",
    "Yo yo yo!",
    "Hello! How’s everyone doing?",
    "Hey! How’s it going?",
    "Hi hi hi!",
    "Hey friends!",
    "Yo, what’s good?",
    "Hi all! 👋",
    "Hello everyone!",
    "Hey peeps!",
    "Hi folks!",
    "Hey squad!",
    "Yo! How’s life?",
    "Hello world! 🌎",
    "Hey hey hey!",
    "Hiya! 😄",
    "Hey team!",
    "Greetings, friends!",
    "Yo friends! 👋",
    "Hi there everyone!",
    "Hey gang!",
]

other_replies = [
    "brb grabbing water",
    "wait what just happened?",
    "lol that caught me off guard",
    "give me a second",
    "okay yeah that makes sense",
    "not gonna lie, that was kinda funny",
    "hmm I’ll think about it",
    "oh wow, didn’t expect that",
    "ah okay, got it",
    "sure, why not",
    "I might be overthinking this…",
    "fair enough",
    "gotcha gotcha",
    "that’s valid",
    "true true",
    "no worries at all",
    "mmm maybe",
    "could be",
    "alright then",
    "makes sense now",
    "huh, interesting",
    "wait really?",
    "oh dang",
    "lol yeah",
    "right right",
    "honestly yeah",
    "I’m following",
    "lowkey agree",
    "that explains a lot actually",
    "oop",
    "hold on, checking something",
    "yeah I’m good with that",
    "welp",
    "okay but hear me out",
    "so basically yeah",
    "not wrong",
    "yeah that checks out",
    "interesting point",
    "hmm fair",
    "ohhh okay",
    "I see what you mean",
    "makes sense now",
    "yeah I noticed that too",
    "dang that’s unexpected",
    "haha that’s a good one",
    "I feel that",
    "ahhh gotcha",
    "yep that tracks",
    "oh wow, didn’t see that coming",
    "huh, nice observation",
    "lol totally",
    "wait hold on",
    "okay I see",
    "that’s kinda funny",
    "ohhh I get it now",
    "sounds about right",
    "ohhh interesting",
    "got it got it",
    "fair enough I guess",
    "alright I’m on board",
    "hmm makes sense",
    "ohhhh that adds up",
    "ah yes, now it’s clear",
    "I didn’t think about that",
    "ohhh good point",
    "yep yep",
    "okay okay",
    "interesting perspective",
    "lol I agree",
    "true that",
    "ohhh I see",
    "gotcha that makes sense",
    "aha that explains it",
    "I mean… yeah",
    "hmm I get you",
    "oh okay then",
    "right right right",
    "lowkey yes",
    "haha fair enough",
    "ahhh makes sense",
    "yep that works",
    "interesting indeed",
]


while True:
    try:
        response = session.get(chat_url)
        if response.status_code != 200:
            print("[-] Failed to fetch messages")
            sleep(2)
            continue

        chat_data = response.json()["messages"]
        if not chat_data:
            sleep(2)
            continue

        latest_message = chat_data[-1]
        timestamp, content, sender, attachments = latest_message

        if timestamp == last_seen_timestamp or sender == admin_username:
            sleep(2)
            continue

        last_seen_timestamp = timestamp

        content_lower = content.lower()
        words = content_lower.split()
        if any(greet in words for greet in ["hey", "hi", "hello"]):
            reply = random.choice(greeting_replies)
        else:
            reply = random.choice(other_replies)

        files = {"attachment": ("", b"")}
        session.post(chat_url, data={"message": reply}, files=files)
        print(f"[+] Replied to '{sender}': {reply} (with blank attachment)")

        sleep(2)

    except Exception as e:
        print("Error:", e)
        sleep(2)
