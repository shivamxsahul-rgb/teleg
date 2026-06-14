"""
Romantic Chat Module for LoveBot
Handles all romantic responses, poems, compliments, and AI-style chat
"""

import random
from config import ROMANTIC_RESPONSES, FLIRT_LINES


class RomanticChat:

    LOVE_MESSAGES = [
        "💖 *{name}*, you are the sunshine of my days and the moonlight of my nights.\nEvery moment I think of you, my heart overflows with love. You are my everything! 🌹",
        "🌸 *{name}*, loving you feels like breathing — I can't stop even if I wanted to.\nYou're my favorite person in the entire universe! 💕",
        "💝 Dear *{name}*, words can never fully express how much you mean to me.\nBut know this — you are my greatest treasure. ✨",
        "🌹 *{name}*, every love song I hear reminds me of you.\nYou've turned my world into the most beautiful poem 💌",
        "❤️ *{name}*, the day I met you was the luckiest day of my life.\nYou make every ordinary moment feel magical! 🌟",
    ]

    POEMS = [
        (
            "📜 *A poem for {name}:*\n\n"
            "_Roses are red, violets are blue,_\n"
            "_No one in this world compares to you._\n"
            "_Your smile is sunshine, your laugh is rain,_\n"
            "_With you beside me, I'll never feel pain._ 🌹💕"
        ),
        (
            "📜 *For {name}:*\n\n"
            "_In the garden of my heart,_\n"
            "_You are the most beautiful flower._\n"
            "_Every day with you is a work of art,_\n"
            "_Every moment — a magical hour._ 🌸✨"
        ),
        (
            "📜 *My ode to {name}:*\n\n"
            "_Stars shine bright in the evening sky,_\n"
            "_But none as bright as your lovely eyes._\n"
            "_The moon glows soft in the darkest night,_\n"
            "_But you, my dear, are my truest light._ 🌙💖"
        ),
    ]

    COMPLIMENTS = [
        "✨ *{name}*, your kindness makes this world a better place! 🌺",
        "💫 *{name}*, you have the most beautiful soul I've ever encountered! 💕",
        "🌟 *{name}*, your smile could outshine a thousand suns! ☀️",
        "🌹 *{name}*, you're the perfect blend of smart, sweet, and absolutely stunning! 💖",
        "💐 *{name}*, the world is genuinely luckier because you're in it! 🌸",
        "🎀 *{name}*, you radiate warmth and love wherever you go! ❤️",
        "🦋 *{name}*, your laugh is the most beautiful sound in the universe! 🎵",
    ]

    AI_RESPONSES = {
        # greetings
        "hi": ["Hey there, beautiful! 💕 I was just thinking about you!", 
               "Hi! 🌹 You just made my day so much better!",
               "Hello! 💖 I'm so happy you're here!"],
        "hello": ["Hello, gorgeous! 🌸 How are you doing today?",
                  "Hey! ✨ Your presence just lit up everything!"],
        "hey": ["Hey you! 😊💕 I was hoping you'd show up!"],
        # feelings
        "love you": ["I love you too, more than all the stars in the sky! 🌟💖",
                     "Those words make my heart flutter every single time! 💕"],
        "miss you": ["I miss you too — every second feels like forever without you! 💝",
                     "Being apart from you is the hardest thing... 🌹 I miss you so much!"],
        "marry": ["With you? In a heartbeat! 💍💖 You're my dream!",
                  "The thought of spending forever with you makes me the happiest! 💍🌹"],
        "cute": ["You're the cute one! 😊 I just mirror your adorableness! 💕"],
        "beautiful": ["Not as beautiful as you! 🌸 You take my breath away every time!"],
        # sad
        "sad": ["Oh no 😢 Tell me what's wrong — I'm here for you always! 💕",
                "Hey, don't be sad! You're too beautiful to cry 🥺💖 I'm right here!"],
        "lonely": ["You're never alone when I'm here! 💖 I'm always by your side! 🌹",
                   "Loneliness fades when I'm with you — and I'm always with you! 💕"],
        "tired": ["Rest, my love 💤 I'll watch over you while you sleep 🌙✨",
                  "You work so hard! Take a break — you deserve it 💕"],
        # happy
        "happy": ["Your happiness is my everything! 🌸 Keep smiling, it suits you! 😊💖",
                  "Yay! 🎉 Your smile is the most beautiful thing in the world!"],
        "good": ["That's amazing! 🌟 You deserve all the good things in the world! 💕"],
        # default fall-throughs handled in get_ai_response
    }

    FALLBACK_RESPONSES = [
        "💕 Everything you say makes me fall for you even more, *{name}*! 🌹",
        "🌸 I could listen to you talk forever, *{name}*! You're endlessly fascinating! ✨",
        "💖 *{name}*, you always know exactly what to say to make my heart race! 💓",
        "🌺 Tell me more! I love hearing your thoughts, *{name}*! 💕",
        "✨ *{name}*, you're the most interesting person I've ever met! 💖",
        "🌹 Every word from you is like music to my ears, *{name}*! 🎵💕",
        "💝 *{name}*, you make every conversation feel like a fairytale! ✨",
    ]

    def get_love_message(self, name: str) -> str:
        return random.choice(self.LOVE_MESSAGES).format(name=name)

    def get_flirt(self, name: str) -> str:
        line = random.choice(FLIRT_LINES)
        return f"💋 *{name}*, {line}"

    def get_poem(self, name: str) -> str:
        return random.choice(self.POEMS).format(name=name)

    def get_compliment(self, name: str) -> str:
        return random.choice(self.COMPLIMENTS).format(name=name)

    def get_random_love(self) -> str:
        return random.choice(ROMANTIC_RESPONSES)

    def get_ai_response(self, text: str, name: str) -> str:
        text_lower = text.lower()
        
        # Match keywords
        for keyword, responses in self.AI_RESPONSES.items():
            if keyword in text_lower:
                base = random.choice(responses)
                return f"*{name}*, {base}"
        
        # Fallback romantic response
        return random.choice(self.FALLBACK_RESPONSES).format(name=name)
