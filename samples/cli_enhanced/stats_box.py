import re
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts
from engine.items.interactives.CollectibleItem import CollectibleItem
from engine.items.interactives.containeritem import container_item
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

    def _get_equipment_stats(self,pj: PlayerCharacter, body_part):
        if pj.items[body_part]:
            item: CollectibleItem = pj.items[body_part]
            eq_string = str(item) 
            if item.health > 0:
                eq_string += " " +style.CITALIC + style.CRED + str(item.health) + style.CEND
            if item.agility > 0:
                eq_string += " " +style.CITALIC + style.CYELLOW + str(item.agility) + style.CEND
            if item.streng > 0:
                eq_string += " " +style.CITALIC + style.CGREEN + str(item.streng) + style.CEND
            if item.speed > 0:
                eq_string += " " +style.CITALIC + style.CBLUE2 + str(item.speed) + style.CEND
            if isinstance(item, container_item):
                eq_string += " "+style.CITALIC + str(item.load)+"/"+str(item.capacity)+" Kg" + style.CEND
            return eq_string
        else:
            return BodyParts.str(body_part)

    def _render_equipment(self, pj: PlayerCharacter):
        # Player equipment
        pj_str = str()
        # Prepare each part text
        strHead =       self._get_equipment_stats(pj,BodyParts.head)
        strShoulder =   self._get_equipment_stats(pj,BodyParts.shoulder)
        strChest =      self._get_equipment_stats(pj,BodyParts.chest)
        strBack =       self._get_equipment_stats(pj,BodyParts.back)
        strArms =       self._get_equipment_stats(pj,BodyParts.arms)
        strHands =      self._get_equipment_stats(pj,BodyParts.hands)
        strCore =       self._get_equipment_stats(pj,BodyParts.core)
        strLegs =       self._get_equipment_stats(pj,BodyParts.legs)
        strFeets =      self._get_equipment_stats(pj,BodyParts.feets)
        strEmpty = " "
        # Calculate the properly position for each part at the left side
        sizeHead = len(strHead) - self._non_printable_len(strHead)
        sizeShoulder = len(strShoulder) - self._non_printable_len(strShoulder)
        sizeChest = len(strChest) - self._non_printable_len(strChest)
        sizeBack = len(strBack) - self._non_printable_len(strBack)
        sizeArms = len(strArms) - self._non_printable_len(strArms)
        sizeHands = len(strHands) - self._non_printable_len(strHands)
        sizeCore = len(strCore) - self._non_printable_len(strCore)
        sizeLegs = len(strLegs) - self._non_printable_len(strLegs)
        sizeFeets = len(strFeets) - self._non_printable_len(strFeets)

        max_space = max(sizeHead, sizeShoulder, sizeChest, sizeBack, sizeArms, sizeHands, sizeCore, sizeLegs, sizeFeets)
        strHead = " " * (max_space  - sizeHead) + strHead
        strChest = " " * (max_space - sizeChest) + strChest
        strCore = " " * (max_space  - sizeCore) + strCore
        strArms = " " * (max_space  - sizeArms) + strArms
        strEmpty = " " * (max_space)
        strFeets = " " * (max_space - sizeFeets) + strFeets
        # Compose body model with equipment
        pj_str +=      strHead +style.CVIOLET+"    O    "+style.CEND+strShoulder
        pj_str += "\n"+strChest+style.CVIOLET+"  ó(w)ò  "+style.CEND+strBack
        pj_str += "\n"+strArms +style.CVIOLET+"_/ | | \_"+style.CEND+strHands
        pj_str += "\n"+strCore +style.CVIOLET+"  .|_|.  "+style.CEND
        pj_str += "\n"+strEmpty+style.CVIOLET+"   v v   "+style.CEND+strLegs
        pj_str += "\n"+strFeets+style.CVIOLET+"  _l l_  "+style.CEND+"\n"
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

    def render(self, pj: PlayerCharacter):
        if pj is None:
            return ""
        stats_col_str  = self._render_stats(pj)
        equipment_col_str = self._render_equipment(pj)
        
        frame_str = self.render_cols([stats_col_str, equipment_col_str], False)
        frame_str += self._render_quests(pj)
        return self._fill_box(frame_str)

