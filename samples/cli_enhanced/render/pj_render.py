import random

from samples.cli_enhanced.render.colors import style
from .base_render import base_render

class character_render(base_render):
    heads_iddle =   ["ó","ü","ô", "ö", "a", "e"]
    heads_iddle2 =  ["ò","û","ö", "o", "ä", "ë"]
    arms =          ["¡","î","i"]
    hands_iddle =   [",",".","·"]
    sword_iddle =   [" | "," ! "," | "] # This works as staff (top) aswell
    staff_iddle =   ["|","|","!"]
    sword_attack =  ["  /"," ! ","\\  "] # This works as staff (top) aswell
    staff_attack_e=  ["´","|","\\"]
    staff_attack_w=  ["/","|","`"]
    hands_action =  ["+","*","-"]
    nude_torsos =   ["T", "Y", "V"]
    armor_torsos=   ["#","@","X","H", "O", "0"]
    nude_legs =         [" ║ ", " ║ ", " ║ ", " ║ "]
    armor_legs1  =      ["!n!", "!║!", "!Y!", "!T!"]
    armor_legs2  =      ["/n\\","/║\\","/Y\\","/T\\"]
    nude_legs_run_e= " / "
    nude_legs_run_w= " \\ "
    armor_legs1_run_e=  "!/!"
    armor_legs1_run_w=  "!\\!"
    armor_legs2_run_e=  "//\\" 
    armor_legs2_run_w=  "/\\\\"

    #Define max steps
    MAX_STEPS = min(len(arms), len(hands_iddle), len(hands_action))

    def __init__(self, background, foreground):
        # Initialize base class for iddle animation
        super().__init__(7,3, background, foreground, 0.5, character_render.MAX_STEPS, True)
        # Run animation
        self._action_render = base_render(7,3, background, foreground, 0.2, character_render.MAX_STEPS, False)
        
        # Generate random parts
        self._head = random.randint(0, len(character_render.heads_iddle)-1)
        self._torso = random.randint(0, len(character_render.nude_torsos)-1)
        self._legs = random.randint(0, len(character_render.nude_legs)-1)

        # Set default state
        self._to_east = True
        self._sword = False
        self._staff = False
        self._running = False
        self._attacking = False
        self._dead = False
        self._torso_armor = False
        self._legs_armor = None

    def update_equipment(self, torso_armor = False, legs_armor_type: bool = None, weapon_type: bool = None ):
        """
        torso_armor True/False (no types allowed)
        legs_armor_type None/True/False (True:trousers, False:Skirt)
        weapon_type None/True/False (True:sword, False:staff)
        """
        self._torso_armor = torso_armor
        self._legs_armor = legs_armor_type
        if weapon_type is None:
            self._sword = False
            self._staff = False
        elif weapon_type == True:
            self._sword = True
            self._staff = False
        elif weapon_type == False:
            self._sword = True
            self._staff = True


    def update_state(self, to_east, running, attacking, dead):
        # Update state of the character, should be call just before render new frame
        self._to_east = to_east
        self._running = running
        self._attacking = attacking
        self._dead = dead

    def render(self):

        if self._dead:
            return self.composeDead()

        composed_str = []

        if self._running or self._attacking:
            curr_step = self._action_render._get_curr_step()
        else:
            curr_step = self._get_curr_step()
        self._update_step()
        self._action_render._update_step()
                
        #Compose the character
        composed_str.append(self.composeHead(curr_step))
        composed_str.append(self.composeTorso(curr_step))
        composed_str.append(self.composeLegs(curr_step))

        return composed_str

    def composeDead(self):
        composed_str = []
        composed_str.append(" "*self._frame_width)
        composed_str.append(" "*self._frame_width)
        composed_str.append(" --"+self.nude_torsos[self._torso]+self.heads_iddle[self._head])

    def composeHead(self, step):
        # We known that we have 7 chars to compose upper body
        # sword(3),head(1) + 2 extra padding withespaces depending on character direction
        sword = "   " #3 chars by default

        head = self.heads_iddle[self._head]
        if step % 2 == 0:
            head = self.heads_iddle2[self._head]

        if self._sword:
            if self._attacking:
                sword = self.sword_attack[step]
            else:
                sword = self.sword_iddle[step]

        if self._to_east:
            return self._back_color+self._fore_color+"   " + head + sword+style.CEND
        else:
            return self._back_color+self._fore_color+sword + head + "   "+style.CEND

    def composeTorso(self, step):
        # We known that we have 7 chars to compose middle body
        # hands+arms+torso = 5 chars + 1 padding char on each side
        torso = character_render.nude_torsos[self._torso]
        l_arm = character_render.arms[step]
        r_arm = character_render.arms[step]
        l_hand = character_render.hands_iddle[step]
        r_hand = character_render.hands_iddle[step]
        
        if self._torso_armor:
            torso = character_render.armor_torsos[self._torso]

        if self._to_east:
            if self._attacking or self._running:
                r_hand = character_render.hands_action[step]
        else:
            if self._attacking or self._running:
                l_hand = character_render.hands_action[step]

        return self._back_color+self._fore_color+" " + l_hand + l_arm + torso + r_arm + r_hand + " "+style.CEND

    def composeLegs(self, step):
        # We know that we have 7 chars to compose lower boddy
        # legs(3)+staff(2) + 2 padding whitespace depending on character direction
        staff = "  "
        legs = character_render.nude_legs[self._legs]
        if self._legs_armor == True:
            legs = character_render.armor_legs1[self._legs]
        elif self._legs_armor == False:
            legs = character_render.armor_legs2[self._legs]

        if self._staff:
            if self._to_east:
                staff = character_render.staff_iddle[step] + " "
                if self._attacking:
                    if step < character_render.MAX_STEPS-1:
                        staff = character_render.staff_attack_e[step] + " "
                    else:
                        staff = " " + character_render.staff_attack_e[step]
            else:
                staff = " " + character_render.staff_iddle[step]
                if self._attacking:
                    if step == 0:
                        staff = character_render.staff_attack_w[step] + " "
                    else:
                        staff = " " + character_render.staff_attack_w[step]

        if self._running and step % 2 == 0:
            if self._to_east:
                if self._legs_armor == True:
                    legs = character_render.armor_legs1_run_e
                elif self._legs_armor == False:
                    legs = character_render.armor_legs2_run_e
                else:
                    legs = character_render.nude_legs_run_e
            else:
                if self._legs_armor == True:
                    legs = character_render.armor_legs1_run_w
                elif self._legs_armor == False:
                    legs = character_render.armor_legs2_run_w
                else:
                    legs = character_render.nude_legs_run_w

        if self._to_east:
            return self._back_color+self._fore_color+"  " + legs + staff+style.CEND
        else:
            return self._back_color+self._fore_color+staff + legs + "  "+style.CEND
