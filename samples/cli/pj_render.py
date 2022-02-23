import random


class render():
    heads_iddle =  ["ó","ü","ô", "ö", "a", "e"]
    heads_iddle2 = ["ò","û","ö", "o", "â", "ë"]
    arms =   ["i","î","i"]
    hands_iddle =  [",",".","·"]
    sword_iddle =  ["|","!","|"]
    hands_action = ["+","*","-"]
    torsos = ["#","@","X", "T", "H", "Y"]
    legs_iddle  =  ["/║ "," ║ ","/T\\","/n\\","/Y\\","/║\\"]
    legs_run_e  =  ["/\\ "," \\ ","/\\\\","/\\\\","/\\\\","/\\\\"]
    legs_run_e2  =  ["// "," / ","//\\","//\\","//\\","//\\"]
    FRAME_SIZE = 7
    MAX_STEPS = 2

    _head = 0
    _arms = 0
    _hands = 0
    _torso = 0
    _legs = 0

    _iddle_step = 0
    _run_step = 0

    @staticmethod
    def initialize():
        render._head = random.randint(0, len(render.heads_iddle)-1)
        render._torso = random.randint(0, len(render.torsos)-1)
        render._legs = random.randint(0, len(render.legs_iddle)-1)

    @staticmethod
    def render(w_sword = True):
        #In this string array will compose the character
        composed_str = []
        #Needed parts to compose whole character body
        head=''
        l_arm=''
        r_arm=''
        l_hand=''
        r_hand=''
        torso=''
        sword=''

        #Check if MAX_STEPS reached (to reinitialize animation)
        if render._iddle_step > render.MAX_STEPS:
            render._iddle_step = 0

        #Used to generate iddle animation
        if(render._iddle_step % render.MAX_STEPS == 0):
            head = render.heads_iddle[render._head]
            torso = render.torsos[render._torso]
            l_arm = render.arms[render._iddle_step]
            r_arm = render.arms[render._iddle_step]
            l_hand = render.hands_iddle[render._iddle_step]
            r_hand = render.hands_iddle[render._iddle_step]
            if w_sword:
                r_hand = render.hands_action[render._iddle_step]
                sword = render.sword_iddle[render._iddle_step]
        else:
            head = render.heads_iddle2[render._head]
            torso = render.torsos[render._torso]
            l_arm = render.arms[render._iddle_step]
            r_arm = render.arms[render._iddle_step]
            l_hand = render.hands_iddle[render.MAX_STEPS - render._iddle_step]
            r_hand = render.hands_iddle[render.MAX_STEPS - render._iddle_step]
            if w_sword:
                r_hand = render.hands_action[render.MAX_STEPS - render._iddle_step]
                sword = render.sword_iddle[render._iddle_step]

        composed_str.append(render.__fill_frame("  "+head+" "+sword))
        composed_str.append(render.__fill_frame(l_hand+l_arm+torso+r_arm+r_hand))
        composed_str.append(render.__fill_frame(render.legs_iddle[render._legs]))

        render._iddle_step += 1

        return composed_str

    @staticmethod
    def render_run(to_east = True, w_sword = True):
        #In this string array will compose the character
        composed_str = []
        #Needed parts to compose whole character body
        head=''
        l_arm=''
        r_arm=''
        l_hand=''
        r_hand=''
        torso=''
        legs=''

        #Check if MAX_STEPS reached (to reinitialize animation)
        if render._run_step > render.MAX_STEPS:
            render._run_step = 0

        #Used to generate iddle animation
        if(render._run_step % render.MAX_STEPS == 0):
            head = render.heads_iddle[render._head]
            torso = render.torsos[render._torso]
            l_arm = render.arms[render._run_step]
            r_arm = render.arms[render._run_step]
            sword = render.sword_iddle[render._run_step]
            l_hand = render.hands_iddle[render._run_step]
            r_hand = render.hands_iddle[render._run_step]
            if to_east:
                legs=render.legs_run_e[render._legs]
            else:
                legs=render.legs_run_e2[render._legs]
        else:
            head = render.heads_iddle2[render._head]
            torso = render.torsos[render._torso]
            l_arm = render.arms[render._run_step]
            r_arm = render.arms[render._run_step]
            sword = render.sword_iddle[render._run_step]
            if to_east:
                legs = render.legs_run_e2[render._legs]
                r_hand = render.hands_action[render.MAX_STEPS - render._run_step]
                l_hand = render.hands_iddle[render.MAX_STEPS - render._run_step]
            else:
                legs = render.legs_run_e[render._legs]
                l_hand = render.hands_action[render.MAX_STEPS - render._run_step]
                r_hand = render.hands_iddle[render.MAX_STEPS - render._run_step]

        if render._run_step == render.MAX_STEPS:
            legs = render.legs_iddle[render._legs]
        
        if w_sword:
            if to_east:
                composed_str.append(render.__fill_frame("  "+head+" "+sword))
            else:
                composed_str.append(render.__fill_frame(sword+" "+head+" "))
        else:
            composed_str.append(render.__fill_frame(head))

        composed_str.append(render.__fill_frame(l_hand+l_arm+torso+r_arm+r_hand))
        composed_str.append(render.__fill_frame(legs))

        render._run_step += 1

        return composed_str

    @staticmethod
    def __fill_frame(part:str):
        part_size = len(part)
        return " "*int((render.FRAME_SIZE - part_size)/2) + part + " "*int(render.FRAME_SIZE/2)
