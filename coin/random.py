import random

def shuffle_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

worklist = {
    "covid19": "It's quarantine, guess the word: `C _ _ _ _ _ _`",
    "mucski": f"The loser that created this game: `{shuffle_word('mucski')}`",
    "walt disney": "Mickey Mouse was conceived by?",
    "thanos": "He is destiny. Dread it, run from it, he still arrives.",
    "captain marvel": f"A female, strong enough to defeat Thanos himself. `{shuffle_word('captain marvel')}`",
    "subscribe": f"Every YOUTUBER says it sooner or later: `{shuffle_word('subscribe')}`",
    "hit the bell icon": f"Another thing every YOUTUBER says: `{shuffle_word('hit the bell icon')}`",
    "jacksepticeye": f"Green Irish Potato: `{shuffle_word('jacksepticeye')}`",
    "subnautica": f"What game was named 'Minecraft Underwater' by its fans? Hint: `S _ _ _ _ _ _ _ _ _`",
    "no man's sky": f"What game was named 'Minecraft in Space' by its fans? Hint: `N_ _ _ _ _ _ _ _`",
    "lab": f"Dog breed that has a scientific name, 3 letters",
    "paris": f"Tour Eifel is located here .....",
    "black widow": f"Do you know the name of a marvel character that bears the name of a spider?",
}

searchlist = {
    "hospital": "Found `{}` coins under a covid-19 patients bed",
    "manhole": "You met with those famous mutated turtles. They gave you `{}` coins to buy a pizza.",
    "sewer": "You will float .. you will float ... you will float!! Georgie gave you `{}` coins.",
    "under the bed": "Hmmm, what's this, a dildo, a switch, a monster, ah there they are. You found `{}` coins",
    "forest": "It's dangerous to venture into the forest on your own. You found `{}` coins laying around in a tree bark.",
    "garage": "Found `{}` coins laying around in a pile of old dusty boxes in your garage. Lucky you.",
    "locker": "Lucky the school bully wasn't around this time. Found `{}` coins in a half open locker that wasn't even yours.",
    "cellar": "You went into the cellar looking for a fine wine, got scared by a rat and found `{}` coins instead.",
    "moon": "A giant leap to man kind, Armstrong left some `{}` coins here though.",
    "fridge": "Nothing beats frozen coins, Right? Wrong.",
    "dog": "Why would you do that.. that's animal abuse.",
    "toilet": "Why would you search a toilet... That's disgusting and so are you. ", 
    "box": "You rummaged through a box of forgotten items, found `{}` coins. Lucky you. ", 
    "drawer": "After going through many panties, a dildo, and a hand gun, you found `{}` coins wrapped in socks", 
    "story book": "You were looking for Little Red Riding Hood, instead you found `{}` coins hidden in a tree bark. ", 
    "set": "You are the next star for Ironing Man. While equipping his armor you found `{}` coins in one of the hidden compartments. ",
    "school": "You went looking for coins in your school locker, got a wedgy out of it instead. Bullies.",
    "trash": "Found nothing. Must've picked the wrong trash.",
    'club': 'You barged into a club, found `{}` coins laying around on the dance floor',
    'bank': 'They though you gonna rob them. You got arrested',
    'beach': 'You went to the beach, found `{}` coins in a sand castle.',
}

bad_loc = ['dog', 'trash', 'fridge', 'bank', 'toilet', 'school']

petlist = {
    "rock": {
        "description": "Your very own pet rock.",
        "price": 500,
        "emoji": ":moyai:",
    },
    "turtle": {
        "description": "Throwing it in a sewer is not advised.",
        "price": 1000,
        "emoji": ":turtle:",
    },
    "dog": {
        "description": "Loyal, friendly, and full of fleas",
        "price": 2000,
        "emoji": ":dog:",
    },
    "cat": {
        "description": "Lazy and fat, but cute nonetheless.",
        "price": 2000,
        "emoji": ":cat:",
    },
}
