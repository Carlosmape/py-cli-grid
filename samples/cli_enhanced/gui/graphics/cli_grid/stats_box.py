import re
from typing import List
from engine.characters.PlayerCharacter import PlayerCharacter
from engine.defines.defines import BodyParts
from engine.items.interactives.WearableItem import WearableItem
from engine.items.interactives.containeritem import container_item
from engine.stats.AlteredState import AlteredState
from engine.stats.character_stats import character_stats
from samples.cli_enhanced.gui.graphics.cli_grid.command_line_box import CommandLineBox
from samples.cli_enhanced.gui.graphics.render.colors import style


class PjStatsBox(CommandLineBox):
    empty_str = "-"
    full_str = "█"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.content = []
        # Margin spaces to fill entire area with elements (and margins)
        self.width_margin = self.width
        self.height_margin = self.height

    def _get_equipment_stats(self, pj: PlayerCharacter, body_part):
        if pj.items[body_part]:
            item: WearableItem = pj.items[body_part]
            eq_string = str(item)
            sts = item.stats()
            if sts.max_health() > 0:
                eq_string += " " + style.CITALIC + style.CRED + \
                    str(sts.max_health()) + style.CEND
            if sts.agility() > 0:
                eq_string += " " + style.CITALIC + \
                    style.CYELLOW + str(sts.agility()) + style.CEND
            if sts.strength() > 0:
                eq_string += " " + style.CITALIC + \
                    style.CGREEN + str(sts.strength()) + style.CEND
            if sts.movement_speed() > 0:
                eq_string += " " + style.CITALIC + style.CBLUE2 + \
                    str(sts.movement_speed()) + style.CEND
            if isinstance(item, container_item):
                eq_string += " "+style.CITALIC + \
                    str(item.load)+"/"+str(item.capacity)+" Kg" + style.CEND
            return eq_string
        else:
            return BodyParts.str(body_part)

    def _render_equipment(self, pj: PlayerCharacter):
        # Player equipment
        pj_str = str()
        # Prepare each part text
        strHead = self._get_equipment_stats(pj, BodyParts.head)
        strShoulder = self._get_equipment_stats(pj, BodyParts.shoulder)
        strChest = self._get_equipment_stats(pj, BodyParts.chest)
        strBack = self._get_equipment_stats(pj, BodyParts.back)
        strArms = self._get_equipment_stats(pj, BodyParts.arms)
        strHands = self._get_equipment_stats(pj, BodyParts.hands)
        strCore = self._get_equipment_stats(pj, BodyParts.core)
        strLegs = self._get_equipment_stats(pj, BodyParts.legs)
        strFeets = self._get_equipment_stats(pj, BodyParts.feets)
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

        max_space = max(sizeHead, sizeShoulder, sizeChest, sizeBack,
                        sizeArms, sizeHands, sizeCore, sizeLegs, sizeFeets)
        strHead = " " * (max_space - sizeHead) + strHead
        strChest = " " * (max_space - sizeChest) + strChest
        strCore = " " * (max_space - sizeCore) + strCore
        strArms = " " * (max_space - sizeArms) + strArms
        strEmpty = " " * (max_space)
        strFeets = " " * (max_space - sizeFeets) + strFeets
        # Compose body model with equipment
        pj_str += strHead + style.CVIOLET+"    O    "+style.CEND+strShoulder
        pj_str += "\n"+strChest+style.CVIOLET+"  ó(w)ò  "+style.CEND+strBack
        pj_str += "\n"+strArms + style.CVIOLET+"_/ | | \_"+style.CEND+strHands
        pj_str += "\n"+strCore + style.CVIOLET+"  .|_|.  "+style.CEND
        pj_str += "\n"+strEmpty+style.CVIOLET+"   v v   "+style.CEND+strLegs
        pj_str += "\n"+strFeets+style.CVIOLET+"  _l l_  "+style.CEND+"\n"
        return pj_str

    def _render_pj_info(self, pj: PlayerCharacter):
        str_stats = str()
        sts = pj.stats()
        # Player info
        str_stats += style.CBOLD + " " + pj.name.capitalize() + style.CEND
        str_stats += " Level:" + str(sts.level()) + style.CEND + " \n"
        # Faction
        str_stats += " Faction: " + (pj.faction.name if pj.faction else "None") + "\n"
        # XP bar
        strXP = self.full_str * sts.experience()
        strXP += self.empty_str * sts.remain_experience()
        str_stats += style.CVIOLET + style.CBOLD + \
            " XP(%s/%s) " % (sts.experience(), sts.experience() +
                             sts.remain_experience()) + style.CEND + " "
        str_stats += style.CVIOLET + strXP + style.CEND + "\n"
        # HP bar
        strHP = self.full_str * int(sts.health())
        strHP += self.empty_str * int(sts.max_health() - sts.health())
        str_stats += style.CRED + style.CBOLD + \
            " HP(%s/%s) " % (sts.health(), sts.max_health()) + \
            " " + style.CEND + " "
        if sts.health() <= sts.max_health()/4:
            str_stats += style.CBLINK + style.CBOLD
        str_stats += style.CRED + strHP + style.CEND + "\n"
        return str_stats

    def _render_stats(self, sts: character_stats):
        # Another stats as cols
        str_stats = str()
        # Agility
        str_stats += style.CBOLD + style.CYELLOW + \
            " Agility:" + str(sts.agility())+style.CEND + "\n"
        # Strength
        str_stats += style.CBOLD + style.CGREEN + " Strength:" + \
            str(sts.strength()) + style.CEND + "\n"
        # Movement speed
        str_stats += style.CBOLD + style.CBLUE2 + " Speed:" + \
            str(round(sts.movement_speed(), 2)) + style.CEND + "\n"
        # Altered status
        str_stats += style.CBOLD + " Status: "
        if sts.altered_states():
            str_stats += self._get_altered_states(sts)
        str_stats += style.CEND + "\n"
        return str_stats

    def _get_altered_states(self, sts: character_stats):
        states = str()
        for alt_sts in list(sts.altered_states()):
            if states:
                states += ", "
            states += type(alt_sts).__name__ 
            if alt_sts.is_temporary():
                states += "(" + str(alt_sts.remain_time()) + "s)"
        return states

    def _render_quests(self, pj: PlayerCharacter):
        if pj.quests and len(pj.quests) > 0:
            str_quests = style.CBOLD + "Quests:" + style.CEND
            for q in pj.quests:
                if not q.objective.done:
                    str_quests += "\n" + style.CGREEN + "+ " + style.CEND
                    str_quests += q.name + \
                        style.CVIOLET + style.CBOLD + style.CITALIC + " +" + \
                        str(q.reward.getXp()) + " xp"+style.CEND
                    if q.reward.hasItem():
                        str_quests += q.reward.getItem().name + " "
                    str_quests += style.CEND + "\n "
                    str_quests += style.CBEIGE + q.description + style.CEND
            return str_quests
        else:
            return ""

    def _render_log(self, msg: List[str]):
        return style.CBOLD + "Log:\n" + style.CEND + style.CITALIC + "\n".join(msg) + style.CEND

    def render(self, pj: PlayerCharacter, msg: List[str]):
        if pj is None:
            return ""

        info_col_str = self._render_pj_info(pj)
        stats_col_str = self._render_stats(pj.stats())
        equipment_col_str = self._render_equipment(pj)
        quest_col_str = self._render_quests(pj)
        log_col_str = self._render_log(msg)

        frame_str = self.render_cols([info_col_str + stats_col_str, equipment_col_str], False)
        frame_str += self.render_cols([log_col_str, quest_col_str], False)
        return super().render(frame_str)
