# The script of the game goes in this file.

label start:
    narrator "Hello!"
    $ mcname = renpy.input("What is your name ?")
    $ rlname = ""
    $ mcname = mcname.strip()
    $ social = 0
    $ study = 0
    $ sleep = 0
    $ tiredness = 0

    if mcname == "":
        narrator "Really? "
        narrator "You don't wanna name yourself?"
        narrator "How about we try again"
        $ mcname = renpy.input("What is your name ?")
        if mcname == "":
            $ mcname = "Yuki"
            "You're hopeless"
            "I'll just name you myself I guess"
        else:
            narrator "Good job!"
            narrator "Moving on..."

    else:
        narrator "No No, I apologise for the communication gap"
        narrator "I meant your name, you"
        narrator "The player behind the laptop screen"
        $ rlname = renpy.input("So?")
        narrator "[rlname], hmm... your parents made some questionable decisions"
        narrator "Anyways"
        narrator "I was just messing with you"
        narrator "Let's continue, [mcname]"

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

    scene classroom with fade

    narrator "You somehow reach the classroom"
    narrator "15 minutes late that is (tsk tsk tsk)"
    narrator "And you take a seat"

    show friend smile at right with moveinright
    friend "Yoo dude you look so dead"
    show mc void at left with moveinleft
    mc "I know man i havent been sleeping well"
    show friend normal at right 
    friend "Same man, this assignment has been draining all my energy but phew finally submitted it today."
    show mc normal at left 
    mc "uhh... "
    show mc void at left
    mc "..."
    mc "What assignment...?"
    hide mc normal with moveoutleft
    hide friend normal with moveoutright
    show prof with moveinright
    prof "Submit your assignment at my desk!"
    prof "It accounts for a quarter of your grade!!"


    scene hall with fade
    show mc sad with moveinleft
    mc "Ugh"
    mc "I can't anymore "
    mc "I'm going home."


    show dream with pixellate

    narrator "What is your life?"
    narrator "Look at you"
    narrator "College is all you do and you're messing that up as well. "
    narrator "College - Eat - Sleep"
    narrator "It's like you're stuck in this sort of... "
    narrator "How should I put it..."
    narrator "...an endless..."
    narrator "L   O   O   P"

    jump day2


label day2:


    scene dorm with pixellate

    show mc void at center with moveinbottom
    mc "Time for..."
    mc "...coffeeeeeeeeee"

    narrator "What are you even energizing yourself for…"

    scene classroom with fade

    show friend smile at right with moveinright
    friend "I hope you did the assignment this time..."
    show mc void at left with moveinleft
    mc "hmm"
    mc "nope"
    show friend normal at right 
    narrator "future einstein in the making"
    show friend laugh at right

    hide mc normal with moveoutleft
    hide friend normal with moveoutright

    scene hall with fade

    show mc void at center

    narrator "Another day wasted beautifully!"

    mc "Sleep timee"

    scene dorm with fade

    show mc void with dissolve
    mc "*yaaawwwwnn*"
    narrator "And sleep he did..."

    jump dream_sequence




label dream_sequence:

    scene dream with pixellate 
    #play dream_music  # Play dream-like music

    narrator "Another day has passed"
    narrator "and what have you achieved?"
    narrator "Absolutely nothing!"
    narrator "What is the goal of any of this?"
    narrator "Are you"
    narrator "Willing to break"
    narrator "Freeeeeeeeee"

    show mc normal with dissolve
    mc "Where am I???"

    hide mc normal with dissolve

    # More dream sequence content here

    #stop dream_music


    scene black
    pause 1.0
    jump lockpick


init python:
    import pygame
    import math

    renpy.music.register_channel("Lock_Move", mixer= "sfx", loop=True)
    renpy.music.register_channel("Lock_Click", mixer= "sfx", loop=False, tight=True)

    class Lock(renpy.Displayable):

        #The lock class constructor
        def __init__(self, difficulty, resize=1920, **kwargs):
            super(Lock, self).__init__(**kwargs)

            # Set Up images and resize
            self._width = resize
            self._lock_plate_image = Transform("images/lock_plate.png", size = (resize, resize))
            self._lock_cylinder_image = Transform("images/lock_cylinder.png", size = (resize, resize))
            self._lock_tension_image = Transform("images/lock_tension.png", size = (resize, resize))
            self._lock_pick_image = Transform("images/lock_pick.png", size = (resize, resize))
            self._offset = (resize*2**0.5-resize)/2

            # Variables
            self._cylinder_min = 0 # The minimum angle allowed for the cylinder
            self._cylinder_max = 90 # The maximum angle allowed for the cylinder
            self._cylinder_rotate = 0 # The current angle of cylinder
            self._cylinder_try_rotate = False # If the cylinder is attempting to rotate (which mean the left mouse button is held down)
            self._pick_rotate = 90 # The current angle of the pick
            self._pick_can_rotate = True # If the pick can rotate
            self._pick_broke = False # If the pick just broke
            self._correct_pos = renpy.random.randint(0,180) # A point between 0 and 180 determined randomly when the lock is created
            self._difficulty = difficulty # A number between 1 and 29 - the lower the number, the more difficult the lock
            self._break_time = difficulty/10 +0.75 # A number based on difficulty, the amount of time before the lock pick breaks

        # Checking for events
        def event(self, ev, x, y, st):
            
            LEFT = 1
            RIGHT = 3

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == LEFT:
                # If holding left mouse button
                self._cylinder_try_rotate = True # the cylinder will try to rotate
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == LEFT:
                # If release left mouse button
                renpy.sound.stop(channel="Lock_Move")
                self._cylinder_try_rotate = False
                self._pick_can_rotate = True
                self._pick_broke = False

        # Function that continuously updates the graphics of the lock
        def render(self, width, height, st, at):

            if self._pick_can_rotate: 
                # Calculating the pick rotate angle based on mouse position 
                # This is more accurate than the formular on renpy cookbook             
                mouse_pos = renpy.get_mouse_pos() # Current mouse postion
                mouse_on_ox = (mouse_pos[0], 1080/2) # Perpendicular of mouse pos on coordinate x axis
                root = (1920/2, 1080/2) # Origin of the coordinate (but in vietnam we call it root)

                len_mouse_to_ox = calculate_length(mouse_pos, mouse_on_ox) # Calculate the distance from mouse pos to its perpendicular on coordinate x axis
                len_mouse_to_root = calculate_length(mouse_pos, root) # Calculate the distance from mouse pos to the origin
                
                if len_mouse_to_root != 0: # To prevent the weird situation when the player try to put there mouse in the exact middle of the screen, if we just calculate the angle without the condition and that weird situation happen, an error "divide by zero" will raise
                    the_angle = calculate_angle(len_mouse_to_ox, len_mouse_to_root)
                else:
                    the_angle = 0 # Just set it to 0

                if mouse_pos[0] > 1920/2: # If mouse is on the right half of the screen
                    if mouse_pos[1] >= 1080/2: # If mouse if on the lower part of the screen
                        self._pick_rotate = 180 # Pick can't rotate further than 180 degree
                    else: # If mouse is on the upper part of the screen (and is on the right half)
                        self._pick_rotate = 180 - the_angle # Draw the angle on a coordinate system, you will understand why it's 180 - the_angle
                elif mouse_pos[0] < 1920/2: # If mouse is on the left part of the screen 
                    if mouse_pos[1] >= 1080/2: # If mouse is on the lower part of the screen
                        self._pick_rotate = 0 # Pick can't rotate smaller than 0
                    else: # If the mouse is on the upper part of the screen (and is on the left half)
                        self._pick_rotate = the_angle


                # If the position of the pick is close to the correct spot, the cylinder can rotate
                # if self._pick_rotate in range((self._correct_pos-(self._difficulty)/2), (self._correct_pos+((self._difficulty)/2)+1)):
                # The comment above doesn't works but i like to leave it here
                if abs(self._pick_rotate - self._correct_pos) < self._difficulty/2:
                    # If it's "close enough" as determined by the difficulty
                    self._cylinder_max = 90 # Allow winning
                else:
                    self._cylinder_max = 90 - abs(self._pick_rotate - self._correct_pos)*(30/self._difficulty)
                    # If it's not close enough, it can still rotate a bit, based on how far away it is
                    if self._cylinder_max <= 0: # Just in case
                        self._cylinder_max = 0
                
            
            # Move the pick (set up the image rotation)
            if self._pick_broke:
                pick = Transform(child=None)
            else:
                pick = Transform(child=self._lock_pick_image, rotate=self._pick_rotate, subpixel=True)    

            #The following is all the render information for Lock and parts
            # Create transform to rotate the moving parts
            if self._cylinder_try_rotate: # If the button is down, which mean the player is trying to rotate
                
                self._cylinder_rotate += (2*st)/(at+1) # Start increasing the angle
                # Start to rotate the tension and cylinder image, which i think is more easier if they are 1 image only in the very beginning, but i can't draw and i don't own the image so who am i to say right :D
                cylinder = Transform(child=self._lock_cylinder_image, rotate=self._cylinder_rotate, subpixel=True)
                tension = Transform(child=self._lock_tension_image, rotate=self._cylinder_rotate, subpixel=True)

                # It can only rotate up to self.cylinder_max (this prevent line 103 from turning the cylinder to a fidget spinner)
                if self._cylinder_rotate > self._cylinder_max:
                    self._cylinder_rotate = self._cylinder_max

                # If cylinder_rotate gets to 90, you win
                if self._cylinder_rotate == 90:
                    # Play the sound and display notify of victory
                    renpy.sound.stop(channel="Lock_Move") # stop every sound before it
                    renpy.sound.play("audio/lock_unlock.mp3", channel="Lock_Click")
                    renpy.notify("You unlocked the chest!")

                    global timers
                    timers = 0
                    global set_timers
                    set_timers = False

                    self._cylinder_try_rotate = False

                    global current_chest

                    renpy.hide_screen("lock_picking")
                    renpy.show_screen("loot", False, current_chest)

                elif self._cylinder_rotate == self._cylinder_max:
                    # Jiggle jiggle jiggle when it gets to self.cylinder_max (this is checked only if it's not 90 so don't worry that it gonna jiggle for your winning)
                    if not renpy.sound.is_playing: # If not already playing the lock moving sound
                        renpy.sound.play("audio/lock_moving.mp3", channel="Lock_Move")
                    
                    # Setting up image jiggling
                    jiggle_cylinder = self._cylinder_rotate + renpy.random.randint(-2,2)
                    jiggle_tension = self._cylinder_rotate + renpy.random.randint(-3,3)
                    cylinder = Transform(child=self._lock_cylinder_image, subpixel=True, rotate=jiggle_cylinder)
                    tension = Transform(child=self._lock_tension_image, subpixel=True, rotate=jiggle_tension)

                    self.pick_can_rotate = False

                    global lockpicks
                    # If a timer here exceeds self._break_time, break a lock pick (play a sound and hide the image momentarily), reset its position, decrease number of lockpicks
                    global set_timers
                    global timers
                    if not set_timers:
                        timers = at
                        set_timers = True

                    if set_timers:
                        if at > timers+self._break_time:
                            # Play the sound of failure
                            renpy.sound.stop(channel="Lock_Move")
                            renpy.sound.play("audio/lock_pick_break.mp3", channel="Lock_Click")
                            renpy.notify("Broke a lock pick!")

                            mispick = renpy.random.randint(-30, 30)
                            pick = Transform(child=self._lock_pick_image, rotate=self._pick_rotate+(2*mispick), subpixel=True)

                            self._pick_broke = True
                            self._cylinder_try_rotate = False

                            lockpicks -= 1
                            timers = 0
                            set_timers = False
                            pygame.mouse.set_pos([self._width/2, self._width/4])

            else: # Release, slowly rotate back to the starting position
                if self._cylinder_rotate > 15:
                    renpy.sound.play("audio/lock_moving_back.mp3", channel="Lock_Click")
                self._pick_can_rotate = True
                self._cylinder_rotate -= (5*st)/(at+1)

                if self._cylinder_rotate < self._cylinder_min:
                    self._cylinder_rotate = self._cylinder_min
                    renpy.sound.stop(channel="Lock_Click")

                cylinder = Transform(child=self._lock_cylinder_image, rotate=self._cylinder_rotate, subpixel=True)
                tension = Transform(child=self._lock_tension_image, rotate=self._cylinder_rotate, subpixel=True)

            # Create a render for the children.
            lock_plate_render = renpy.render(self._lock_plate_image, width, height, st, at)
            lock_cylinder_render = renpy.render(cylinder, width, height, st, at)
            lock_tension_render = renpy.render(tension, width, height, st, at)
            lock_pick_render = renpy.render(pick, width, height, st, at)

            # Create the render we will return.
            render = renpy.Render(self._width, self._width)

            # Blit (draw) the child's render to our render.
            render.blit(lock_plate_render, (0, 0))
            render.blit(lock_cylinder_render, (-self._offset, -self._offset))
            render.blit(lock_tension_render, (-self._offset, -self._offset))
            render.blit(lock_pick_render, (-self._offset, -self._offset))

            #This makes sure our object redraws itself after it makes changes
            renpy.redraw(self, 0)

            # Return the render.
            return render

    class Chest():
        def __init__(self, name, status = "closed", keys = None, lock = None, reward = None):
            self._name = name # Name can be used to compare if you have the right keys for the right chest
            self._status = status # "closed" or "opened", for image display and tell if you can try to open it again
            self._keys = keys # If you got the keys of the chest, then you can open it without picking
            self._lock = lock # What lock you're using (so that it have different difficulty and random correct_pos)
            self._reward = [] # A list of reward
        @property 
        def name(self):
            return self._name 
        
        @property 
        def status(self):
            return self._status 
        
        @status.setter 
        def status(self, status):
            self._status = status 
        
        @property
        def keys(self):
            return self._keys
        
        @keys.setter 
        def keys(self, keys):
            self._keys = keys
        
        @property
        def lock(self):
            return self._lock 
        
        @property 
        def reward(self):
            return self._reward
        
        @reward.setter 
        def reward(self, reward):
            self._reward = reward

    class Item(): # Well i wanted to make an Item so that i can use Inventory in my project, you can have whatever you want
        def __init__(self, name, info):
            self._name = name 
            self._info = info 

        @property
        def name(self):
            return self._name 
        
        @property
        def info(self):
            return self._info
    
    class Key(): # This make me thinking a lot whether should i make it or not, a class just for the name is too much but strings is not the proper way tho
    # In fact you can create an Object named key that contain a number that match with the chest number by using Item class
        def __init__(self, name):
            self._name = name 
        
        @property
        def name(self):
            return self._name

    def calculate_length(coordinate1, coordinate2):
        # len of a line is square root of (x1-x2)**2 + (y1-y2)**2
        x = float(coordinate1[0]) - float(coordinate2[0])
        y = float(coordinate1[1]) - float(coordinate2[1])
        return math.sqrt(x**2 + y**2)

    def calculate_angle(a, b):
        # sin is the best solution because it can calculate the angle without errors on 90 degree and it's really hard to have b value to 0
        sin_value = float(a)/float(b)
        return math.degrees(math.asin(sin_value))
    
    def pickup(item):
        inventory.append(item)
    
    def remove_item(container, item):
        container.remove(item)

screen chest_display(chests):
    hbox:
        yalign 0.5
        for chest in chests:
            frame:
                xsize 200
                ysize 200
                vbox:
                    text chest.name 
                    text "Status: {}".format(chest.status)
                    python:
                        if chest.lock._difficulty in range(1, 5):
                            difficulty_display = "hard" # Actually insanely hard but whatever
                        elif chest.lock._difficulty in range(5, 10):
                            difficulty_display = "medium"
                        elif chest.lock._difficulty in range(10, 20):
                            difficulty_display = "easy"
                        elif chest.lock._difficulty in range(20, 30):
                            difficulty_display = "for babies"
                        else:
                            difficulty_display = "You can click anywhere with this" # Which i don't think you want it, it's here so that i can demonstrate what gonna happen if you don't listen to me and have difficulty value out of the ramge(1, 30) 
                    text "Difficulty: {}".format(difficulty_display)
                        
                    textbutton "Open" action If(
                        chest.status == "closed",
                        true = If(
                            chest.keys, # Just Saying if it's not None but in a fancy way
                            true = [Hide("chest_display"), Show("loot", True, chest)],
                            false = [SetVariable("current_chest", chest), Hide("chest_display"), ShowMenu("lock_picking", chest.lock)]),
                        false = Notify("Chest is opened"))

screen lock_picking(lock):
    modal True
    add lock:
        xalign 0.5
        yalign 0.5
    text "Lockpicks: [lockpicks]"

screen loot(used_keys, chest):
    if used_keys:
        $ renpy.notify("You used keys")
        $ inventory.remove(chest.keys)
    $ chest.status = "opened"
    $ loots = chest.reward

    vbox:
        align (0.5, 0.5)
        if loots is not None:
            for loot in loots:
                textbutton loot.name action [Function(pickup, loot), Function(remove_item, loots, loot)]
            textbutton "Close" action [Hide("loot"), Jump("postds")] # So this make things more realistic, you look at a chest and get to choose what to take out instead of take all of them and then throw away later on
        else:
            text "This chest is empty"
            timer 3.0 action [Hide("loot"), Jump("postds")]

screen inventory_icon():
    textbutton "Inventory" action [ShowMenu("inventory"), Hide("chest_display"), Hide("inventory_icon")]
# I got really clumsy with displaying this because it got overlay situation all the time
# But i do this just to display that the reward will go to your inventory so you can add your own

screen inventory():
    vbox:
        for item in inventory:
            text item.name
        textbutton "Return" action [Hide("inventory"), Jump("postds")]


default lockpicks = 25
default timers = 0
default set_timers = 0

define apple = Item("Choice", "Power of Choice")
define ramen = Item("Ramen", "Naruto's favourite food")

default chest_1 = Chest("Chest 1", lock = Lock(15))
# Should only go from 1 to 29, if it's above 29 then you can click anywhere to unlock, which i don't know why
default current_chest = None

default inventory = []

label lockpick:
    $ chest_1.reward = [apple]
    $ chest_list = [chest_1]
    show screen inventory_icon
    call screen chest_display(chest_list)
    jump postds


label postds:

    show dream with fade
    show mc normal at left with moveinleft
    mc "Huh..."
    mc "What's this?"
    show mc normal at center with moveinleft
    mc "Interesting..."
    
    
    narrator "(This kid does not understand that he now holds the power to break the loop.)"
    hide mc normal with dissolve
    pause 1.0
    jump day3



label day3:

    scene dorm with pixellate

    narrator " And the loop restarts..."
    narrator "you wake up, \"dink\" coffee yada yada"
    narrator "We know the whole story by now."
    narrator "I'm sure you're bored of all this"
    narrator "Aren't you [rlname]"
    narrator "Lets just skip to"
    narrator "Uhhh"
    narrator "Yeah"

    narrator "*after school*"

    scene hall with fade

    show mc normal at right

    show partyguy at left with moveinleft
    pause 1.0

    partyguy "[mcname] MY G"
    partyguy "IM GOING TO THIS DOPE ASS PARTY TONIGHT!"
    partyguy "WANNA HANG??"

menu:
    "SURE DUDE LESGOOO":
        $ social = social + 1
        $ tiredness = tiredness + 2
        jump partytime

    "Sorry, I have some work to do":
        $ study = study +1
        $ tiredness = tiredness +1
        jump studytime

    "Nah, I'm gonna sleep":
        $ sleep = sleep +1
        $ tiredness = 0
        partyguy "OKAYY CATCH THEM ZZZZsss"
        partyguy "SEE YOU LATER ALLIGATOR "
        jump day3_home


label partytime:
    scene party with fade

    show mc fond front at right with moveinright
    show partyguy at left with moveinleft

    mc "THIS IS SO FUN"

    partyguy "TOLD YA !!"

    hide partyguy with moveoutleft
    pause 1.0
    mc "WOOO HOOO"

    narrator "After dancing your feet away, you reach back to your dorm"
    jump day3_home

label studytime:
    partyguy "Bummer, but no hard feelings man"

    hide partyguy with moveoutleft

    mc "That was strange"
    mc "Anyways..."
    mc "...I'll head out to the library"

    scene library with fade

    show mc normal at center

    narrator "And so he studied in the peace of the library"
    narrator "and then he headed home"
    narrator "with the power of knowledge by his side"
    narrator "(thats not an actual power I'm being dramatic)"

label day3_home:

    scene dorm with fade

    show mc normal at left
    pause 1.5

    show roommate sad at right with moveinright

    roommate "Hey [mcname]! How was your day?"

    if social == 1:
        mc "AMAZING! I WENT TO THE COOLEST PARTY EVER!"
    elif study == 1:
        mc "Productive! Covered a lot of syllabus today at the library"
    else:
        mc "Boooring as always"

    pause 1.5
    roommate "Oh..."
    roommate "..."

    mc "Is everything okay with you?"

    roommate "Yeah..."
    roommate "I guess I'm feeling under the weather"
    roommate "..."

menu :
    "It's time for a GAMING SESHH!!" if tiredness<2 :
        $ social = social +1
        $ tiredness = tiredness +2
        mc "Don't be sad roomie when you have your homie! ;) "
        mc "Let's play some VALORANT!"
        show roommate happy at right
        roommate "That sounds like exactly what I need !!"

        narrator "And the two dudes game into the night"
        narrator "So wholesome, oh I'm tearing up"
        narrator "*sniff*"
        hide roommate happy with moveoutright
        hide mc normal with moveoutleft
        narrator "slumber time"
        jump day3_dream

    "Let's study together then?" if tiredness<2 :
        narrator "Oh right I forgot to tell you, If there are any choices you can't select, you're probably too tired to participate in them. Try Sleeping :)"

        $ tiredness = tiredness +1
        $ study = study + 1

        mc "Allow me to tutor you to success"
        roommate "Uhh okay, I guess that would distract me"

        hide roommate happy with moveoutright
        hide mc normal with moveoutleft

        narrator "After a rigorous study session, both the boys are drained."

        show roommate happy at right with dissolve
        roommate "Thanks [mcname], that makes stuff for me so much easier"
        roommate "I don't need to worry about the finals anymore!"
        roommate "I'm drained, Good Night!"

        jump day3_dream
    
    "I'm too tired to do anything":
        narrator "Oh right I forgot to tell you, If there are any choices you can't select, you're probably too tired to participate in them. Try Sleeping :)"
        mc "Oh, uh I'm too tired..."
        roommate "Oh no worries! Good Night..."
        jump day3_dream


label day3_dream:

    scene dream with pixellate

    narrator "Don't you think... life's just like a game..."
    narrator " And we're all trying to find our good ending..."
    narrator "..."
    narrator "Chuck it who cares. Let's make [rlname] play space invaders haha"

    jump riddim 

label day4:
    scene dorm with pixellate

    show mc normal at left with dissolve

    narrator "We're not doing this again"

    hide mc normal with moveoutright

    narrator "After college..."

    scene hall with fade

    show chick normal at right with moveinleft

    narrator "Hmm she's kinda cute, what do you think [rlname]?"

menu:
    "Talk to her !!!!!!":
        narrator "Huh never thought you would have the guts"
        jump chick_intro
    "ARE YOU CRAZY ?? NO":
        narrator "HAH knew it! But I was a step ahead"
        narrator "I've already set you up for success"
        narrator "Looks like you have no choice but to talk to her"
        jump chick_intro

label chick_intro:
    show mc fond front at left with moveinleft

    mc "Hey- uh Hi!"
    show mc fond side
    pause 0.5
    show mc fond front

    chick "Hi [mcname]!"

    mc "Hello, ...."
    pause 1.5
    show mc fond side
    pause 0.5
    show mc fond front
    mc "...sup?"
    show mc fond side
    pause 0.5
    show mc fond front
    chick "Ha ha..."
    show chick blush
    chick "Uhh nothing, you wanna do something...?"

menu:
    "Coffee? (It's a date)":
        $ social = social + 1
        jump coffee_date
    "Let's go to the library? (It's a date)":
        $ study = study + 1
        jump study_date
    "NOOO RUNNN TIREDD (It's not a date)":
        $ sleep = sleep + 1
        jump final_deam
    "IM NOT INTERESTED IN WOMEN":
        narrator "oh..."
        narrator "...oops"
        $ sleep = sleep + 1 
        jump final_deam


label coffee_date:
    scene date with fade

    show chick blush at right with moveinbottom
    show mc fond front at left with moveinbottom

    narrator "And they had a great time"

    show mc fond side
    show chick smile
    pause 0.5
    show mc fond front

    narrator "I mean just look at them"
    narrator "Let's give them some privacy"

    jump lady_scene

label study_date:
    scene library with fade
    show chick blush at right with moveinbottom
    show mc fond front at left with moveinbottom

    narrator "And they had a great time"

    show mc fond side
    show chick smile
    pause 0.5
    show mc fond front

    narrator "I mean just look at them"
    narrator "Let's give them some privacy"

    jump lady_scene

label sleep:
    show chick_annoy at right
    chick "Ugh. OK FINE!"
    show mc void at left
    pause 0.5
    hide mc void with moveoutleft

    narrator "And then he went and slept like he always does."
    jump final_deam

label lady_scene:
    $ morality = True
    scene road crossing with fade

    narrator "When coming back from his date he sees an old lady trying to cross the road"
    show obachan at center with dissolve
    obachan "Oww!!!!! My back hurts and I can't really see straight"
    narrator "She looks way too young, hmm did the devs run out of assets... "
    mc "Hmm..."

menu:
    "Help the lady out.":
        narrator "At least you have some sense of morality in you."
        jump final_deam
    "Be on your way.":
        $ morality = False
        narrator "Oh god you're beyond repair. You don't have your life together anyways and have also lost your sense of morality."
        narrator "It's just downhill from here isn't it. How do you feel about yourself? Do you feel good?"
        narrator "NO point in continuing further."
        narrator "I'm not letting you play ahead until you make good decisions in life"
        jump lady_scene

label final_deam:
    
    scene black screen with fade

    narrator "Having helped the old lady"
    narrator "You're filled with determination"
    narrator "You go home and go to sleep with a smile on your face"

    scene dream with pixellate

    narrator "How do you feel?"
    narrator "Do you think you made the right decisions?"
    narrator "I have been keeping track of you"
    pause 1.5
    narrator "So here it is the moment of truth"

    if social>sleep and social>study:
        narrator "You're a social butterfly"
        narrator "All the choices you made enhanced your social life"
        narrator "That's good, very good"
        narrator "But do not neglect your studies"
        narrator "And sleep please"
        pause 1.0
    elif sleep>social and sleep>study:
        narrator "You're a dreamy dozer !"
        narrator "All throughout the game you've prioritized your sleep"
        narrator "You're healthy, but now what?"
        narrator "Aren't social skills and your academic important as well?"
        narrator "How else will Sakura like you (wink wink)"
        pause 1.0
    elif study>sleep and study>social:
        narrator "Oooo ho ho ho"
        narrator "YOU'RE A KNOWLEDGE KNIGHT"
        narrator "ALL YOU DID WAS STUDY"
        narrator "AHAHAHAH..."
        narrator "...ha ha sorry that's a little funny to me"
        narrator "Well atleast you're rich"
        narrator "Live life man, you're in college"
        pause 1.0
    else:
        narrator "WOOOO HOOO YOU'RE AN ALL-ROUNDER"
        narrator "You just tried out all the choices, didn't you [rlname]?"
        narrator "Good job! You're well rounded"

    
    narrator "Well, I may be your narrator but I care about you"
    narrator "And I want you to be the best version of yourself"
    narrator "[mcname] is doomed, he's stuck in a game"
    narrator "but you, [rlname] can achieve big things!"
    narrator "I, being stuck in this game, can only point out your flaws"
    narrator "But you have to identify and work on them"
    narrator "I believe in you..."
    narrator "Keep going and maybe we'll meet again"
    pause 1.5

    narrator "Thank you for playing"
    narrator "With love, the devs."

    return


