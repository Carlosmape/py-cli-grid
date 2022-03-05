
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
        strHead = " Head(" + str(pj.items[BodyParts.head] or '-') + ") "
        strShoulder = " Shoulders(" + str(pj.items[BodyParts.shoulder] or '-') + ") "
        strChest = " Chest(" + str(pj.items[BodyParts.chest] or '-') + ") "
        strBack = " Back(" + str(pj.items[BodyParts.back] or '-') + ") "
        strArms = " Arms(" + str(pj.items[BodyParts.arms] or '-') + ") "
        strHands = " Hands(" + str(pj.items[BodyParts.hands] or '-') + ") "
        strCore = " Core(" + str(pj.items[BodyParts.core] or '-') + ") "
        strLegs = " Legs(" + str(pj.items[BodyParts.legs] or '-') + ") "
        strFeets = " Feets(" + str(pj.items[BodyParts.feets] or '-') + ") "
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
        pj_str += "\n"+style.CITALIC+strHead +style.CEND+style.CVIOLET+"    O    "+style.CEND+strShoulder
        pj_str += "\n"+style.CITALIC+strChest+style.CEND+style.CVIOLET+"  ó(w)ò  "+style.CEND+strBack
        pj_str += "\n"+style.CITALIC+strArms +style.CEND+style.CVIOLET+"_/ | | \_"+style.CEND+strHands
        pj_str += "\n"+style.CITALIC+strCore +style.CEND+style.CVIOLET+"  .|_|.  "+style.CEND
        pj_str += "\n"+style.CITALIC+strEmpty+style.CEND+style.CVIOLET+"   v v   "+style.CEND+strLegs
        pj_str += "\n"+style.CITALIC+strFeets+style.CEND+style.CVIOLET+"  _l l_  "+style.CEND+"\n"
        return pj_str

    def _render_stats(self, pj: PlayerCharacter):
        str_stats = str()
        # Player status
        str_stats += style.CBOLD + "\n Level:" + str(pj.get_level())

        # XP bar 
        strXP = self.full_str * pj.stats.experience()
        strXP += self.empty_str * pj.stats.remain_experience()
        str_stats += style.CVIOLET + style.CBOLD+ " XP(%s/%s)\t" %(pj.stats.experience(), pj.stats.experience()+pj.stats.remain_experience()) + style.CEND
        str_stats += style.CVIOLET + strXP +style.CEND

        # HP bar
        strHP = self.full_str * pj.get_health()
        strHP += self.empty_str * (pj.get_max_health() - pj.get_health()) 
        str_stats += style.CRED + style.CBOLD + "\n\t HP(%s/%s)\t" %(pj.get_health(), pj.get_max_health()) + style.CEND
        str_stats += style.CRED + strHP + style.CEND

        # Another stats
        str_stats += style.CBOLD + style.CYELLOW + "\n Agility:" + str(pj.get_agility())
        str_stats += style.CGREEN + " Strength:" + str(pj.get_strength())
        str_stats += style.CBLUE2 + " Speed:" + str(round(pj.get_speed(),2)) + style.CEND+"\n"
        return str_stats

    def _render_quests(self, pj: PlayerCharacter):
        if pj.quests and len(pj.quests) > 0:
            str_quests = style.CBOLD + " Quests:" + style.CEND
            for q in pj.quests:
                if not q.objective.done:
                    str_quests += "\n" + style.CGREEN + " + " + style.CEND
                    str_quests += q.name + style.CITALIC + " +" + str(q.reward.getXp()) + " xp"+style.CEND
                    if q.reward.hasItem():
                        str_quests += q.reward.getItem().name + " "
                    str_quests += style.CEND + "\n\t"
                    str_quests += style.CBEIGE + q.description + style.CEND
            return str_quests
        else:
            return ""

    def render(self, pj: PlayerCharacter):
        if pj is None:
            return ""
        str_frame  = self._render_stats(pj)
        str_frame += self._render_equipment(pj)
        str_frame += self._render_quests(pj)
        return self._fill_box(str_frame)

