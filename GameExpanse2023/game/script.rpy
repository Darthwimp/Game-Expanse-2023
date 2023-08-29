# The script of the game goes in this file.

label start:

    $ mcname = renpy.input("What is your name ?")
    $ mcname = mcname.strip()

    if mcname == "":
        narrator "Mehh, imma just call you Yuki."
    else:
        narrator "[mcname], hmm... your parents made some questionable decisions"
        narrator "Anyways"

    scene dorm

    narrator "You wake up at 6."
    narrator "And it's another day..."
    narrator "The same ol'..."
    narrator "Chop chop, get ready for college"

    show mc void at left with moveinleft 

    mc "*yawwwwwwnnnn*"
    mc "man why do we have to wake up..."
    show mc sad with dissolve
    mc "I need a coffee :("
    show mc fond side at center with moveinright
    mc "*sips*"
    show mc sad with dissolve
    mc "Time to go to college, i guess :("

    show black screen

    narrator "You walk to college"
    narrator "Slowly..."
    narrator "Like the lazy sloth you are."

    show classroom

    # This ends the game.

    return
