define s = Character("God", image="sylvie", color="#c88fc8")

screen space_invaders:
    default game = SpaceInvaders()

    add game


label riddim:

    s "Let's watch you do this"
    call screen space_invaders

    $ is_win, stats = _return
    $ score = stats["score"]
    $ time = stats["time"]
    $ wave = stats["wave"]

    if is_win:
        s "Nice you won. You destroyed all of them in [time] seconds."
    else:
        s "You destroyed [score] ships. Made it to wave [wave]. You survived [time] seconds, Although you're kinda trash not gonna lie."
    jump day4

    