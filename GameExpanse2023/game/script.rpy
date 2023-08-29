# The script of the game goes in this file.

label start:

    $ mcname = renpy.input("What is your name pookie?")
    $ mcname = mcname.strip()

    if mcname == "":
        narrator "Mehh, ima just call ye Yukki."
    else:
        narrator "[mcname], that's a dope af name."

    scene dorm

    narrator "You wake up at 6."
    narrator "and it's another day..."
    narrator "the same ol'..."
    narrator "anyway, chop chop, get ready for college"

    show mc void at left with moveinleft 

    mc "*yawwwwwwnnnnsssss*"
    mc "man why do we have to wake up..."
    show mc sad with dissolve
    mc "I need a coffee :///"
    show mc fond side at center with moveinright
    mc "*sips*"
    mc "it feels good"
    show mc sad with dissolve
    mc "time to go to college, i guess :/"

    show black screen

    narrator "you walk to school"
    narrator "slowly..."
    narrator "as the lazy sloth you are."

    show classroom

    # This ends the game.

    return
