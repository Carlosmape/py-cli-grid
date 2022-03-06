import re
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts
from engine.menu import Menu
from samples.cli_enhanced.command_line_box import CommandLineBox
from samples.cli_enhanced.render.colors import style


class PjStatsBox(CommandLineBox):
    empty_str = "░"
    full_str = "▓"

    """This class represents a box inside a terminal (TODO just vertical boxes currently)"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height
    
    def _fill_box(self, string):
        self.height_margin = int(self.height - string.count("\n"))
        return string +"\n"*self.height_margin+""

    def _render_equipment(self, pj: PlayerCharacter):
        # Player equipment
        pj_str = str()
        # Prepare each part text
        strHead =       str(pj.items[BodyParts.head] or 'Head' )
        strShoulder =   str(pj.items[BodyParts.shoulder] or 'Shoulders')
        strChest =      str(pj.items[BodyParts.chest] or 'Chest')
        strBack =       str(pj.items[BodyParts.back] or 'Back')
        strArms =       str(pj.items[BodyParts.arms] or 'Arms')
        strHands =      str(pj.items[BodyParts.hands] or 'Hand')
        strCore =       str(pj.items[BodyParts.core] or 'Core')
        strLegs =       str(pj.items[BodyParts.legs] or 'Legs')
        strFeets =      str(pj.items[BodyParts.feets] or 'Feets')
        strEmpty = " "
        # Calculate the properly position for each part at the left side
        max_space = max(len(strHead), len(strChest), len(strArms), len(strCore), len(strFeets))
        strHead = " " * (max_space - len(strHead)) + strHead
        strChest = " " * (max_space - len(strChest)) + strChest
        strCore = " " * (max_space - len(strCore)) + strCore
        strArms = " " * (max_space - len (strArms)) + strArms
        strEmpty = " " * (max_space)
        strFeets = " " * (max_space - len(strFeets)) + strFeets
        # Compose body model with equipment
        pj_str +=      style.CITALIC+strHead +style.CEND+style.CVIOLET+"    O    "+style.CEND+strShoulder
        pj_str += "\n"+style.CITALIC+strChest+style.CEND+style.CVIOLET+"  ó(w)ò  "+style.CEND+strBack
        pj_str += "\n"+style.CITALIC+strArms +style.CEND+style.CVIOLET+"_/ | | \_"+style.CEND+strHands
        pj_str += "\n"+style.CITALIC+strCore +style.CEND+style.CVIOLET+"  .|_|.  "+style.CEND
        pj_str += "\n"+style.CITALIC+strEmpty+style.CEND+style.CVIOLET+"   v v   "+style.CEND+strLegs
        pj_str += "\n"+style.CITALIC+strFeets+style.CEND+style.CVIOLET+"  _l l_  "+style.CEND+"\n"
        return pj_str

    def _render_stats(self, pj: PlayerCharacter):
        str_stats = str()
        # Player status
        str_stats += style.CBOLD + " Level:" + str(pj.get_level()) + style.CEND + " \n"
        # XP bar 
        strXP = self.full_str * pj.stats.experience()
        strXP += self.empty_str * pj.stats.remain_experience()
        str_stats += style.CVIOLET + style.CBOLD+ " XP(%s/%s) " %(pj.stats.experience(), pj.stats.experience()+pj.stats.remain_experience()) + style.CEND + " "
        str_stats += style.CVIOLET + strXP +style.CEND + "\n"
        # HP bar
        strHP = self.full_str * pj.get_health()
        strHP += self.empty_str * (pj.get_max_health() - pj.get_health()) 
        str_stats += style.CRED + style.CBOLD + " HP(%s/%s) " %(pj.get_health(), pj.get_max_health()) + " " + style.CEND + " "
        if pj.get_health() <= pj.get_max_health()/4:
            str_stats += style.CBLINK
        str_stats += style.CRED + strHP + style.CEND + "\n"
        # Another stats
        str_stats += style.CBOLD + style.CYELLOW + " Agility:" + str(pj.get_agility())+style.CEND + "\n"
        str_stats += style.CGREEN + " Strength:" + str(pj.get_strength()) +style.CEND+ "\n"
        str_stats += style.CBLUE2 + " Speed:" + str(round(pj.get_speed(),2)) + style.CEND + "\n"
        return str_stats

    def _render_quests(self, pj: PlayerCharacter):
        if pj.quests and len(pj.quests) > 0:
            str_quests = style.CBOLD + "Quests:" + style.CEND
            for q in pj.quests:
                if not q.objective.done:
                    str_quests += "\n" + style.CGREEN + "+ " + style.CEND
                    str_quests += q.name + style.CITALIC + " +" + str(q.reward.getXp()) + " xp"+style.CEND
                    if q.reward.hasItem():
                        str_quests += q.reward.getItem().name + " "
                    str_quests += style.CEND + "\n "
                    str_quests += style.CBEIGE + q.description + style.CEND
            return str_quests
        else:
            return ""

    def render_cols(self, col_list_str: list):
        n_cols = len(col_list_str)
        col_width = int(self.width/n_cols)
        col_max_height = max(l.count("\n") for l in col_list_str)

        frame_str = ""
        for line in range(col_max_height):
            line_str = ""
            line_remaining = None
            for col in col_list_str:
                col_str = ""
                lines = col.split("\n")
                if line_remaining is not None:
                    col_str += line_remaining
                elif len(lines) > line:
                    if len(lines[line])- self.count_printable(lines[line]) > col_width:
                        line_size = col_width+self.count_printable(lines[line][0:col_width])
                        col_str += lines[line][0:line_size]
                        line_remaining = lines[line][line_size:-1]
                    else:
                        col_str += lines[line]
                col_fill_size = (col_width - len(col_str) + self.count_printable(col_str))
                line_str += col_str + "x" * col_fill_size
            frame_str += line_str + "\n"
        return frame_str

    def count_printable(self, string:str):
        matches = re.findall("\x1b.[0-9]*m", string)
        size = 0
        for m in matches:
            size += len(m)
        return size

    def render(self, pj: PlayerCharacter):
        if pj is None:
            return ""
        stats_col_str  = self._render_stats(pj)
        equipment_col_str = self._render_equipment(pj)
        
        frame_str = self.render_cols([stats_col_str, equipment_col_str])
        frame_str += self._render_quests(pj)
        return self._fill_box(frame_str)

