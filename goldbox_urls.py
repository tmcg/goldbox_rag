

__all__ = ('get_urls')

_urls_poolrad = [
        # GameBanshee Pool of Radiance Walkthrough
        "https://www.gamebanshee.com/poolofradiance/armor.php",
        "https://www.gamebanshee.com/poolofradiance/meleeweapons.php",
        "https://www.gamebanshee.com/poolofradiance/rangedweapons.php",
        "https://www.gamebanshee.com/poolofradiance/miscellaneous.php",
        "https://www.gamebanshee.com/poolofradiance/companions.php",
        "https://www.gamebanshee.com/poolofradiance/bestiary/0-c.php",
        "https://www.gamebanshee.com/poolofradiance/bestiary/d-i.php",
        "https://www.gamebanshee.com/poolofradiance/bestiary/j-s.php",
        "https://www.gamebanshee.com/poolofradiance/bestiary/t-z.php",
        "https://www.gamebanshee.com/poolofradiance/spells/clericlevelone.php",
        "https://www.gamebanshee.com/poolofradiance/spells/clericleveltwo.php",
        "https://www.gamebanshee.com/poolofradiance/spells/clericlevelthree.php",
        "https://www.gamebanshee.com/poolofradiance/spells/magelevelone.php",
        "https://www.gamebanshee.com/poolofradiance/spells/mageleveltwo.php",
        "https://www.gamebanshee.com/poolofradiance/spells/magelevelthree.php",        
        "https://www.gamebanshee.com/poolofradiance/classes.php",
        "https://www.gamebanshee.com/poolofradiance/races.php",
        "https://www.gamebanshee.com/poolofradiance/attributes.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/gameplaytips.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/troubleshooting.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/charactercreation.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/civilizeddistrict.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/theslums.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/sokalkeep.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/kutoswell.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/podalplaza.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/textilehouse.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/mendorslibrary.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/kovelmansion.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/wealthydistrict.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/templeofbane.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/valhingengraveyard.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/stojanowgate.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/overview.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/buccaneerbase.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/koboldcave.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/nomadcamp.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/pyramid.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/ruinedcastle.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/zhentilkeep.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/southwesternquadrant.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/southeasternquadrant.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/northwesternquadrant.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/northeasternquadrant.php",
        "https://www.gamebanshee.com/poolofradiance/walkthrough/upperandlowerlevels.php",
]

_urls_curse = [
        # GameBanshee Curse of the Azure Bonds Walkthrough
        "https://www.gamebanshee.com/curseoftheazurebonds/armor.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/weapons.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/miscellaneous.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/companions.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/bestiary/humanoids-al.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/bestiary/humanoids-mz.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/bestiary/monsters-al.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/bestiary/monsters-mz.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/bestiary/bosses.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/clericlevelone.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/clericleveltwo.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/clericlevelthree.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/clericlevelfour.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/clericlevelfive.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/mulevelone.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/muleveltwo.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/mulevelthree.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/mulevelfour.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/mulevelfive.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/spells/druidlevelone.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/classes.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/races.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/attributes.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/partycreation.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/wilderness.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/tilverton.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/tilvertonsewers.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/firekniveshideout.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/hap.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/wizardstower.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/yulash.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/pitofmoander.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/zhentilkeep.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/beholdercave.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/burialglen.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/ruinsofmythdrannor.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/grandruinedtemple.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/hillsfarruins.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/oxamstower.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/phlanruins.php",
        "https://www.gamebanshee.com/curseoftheazurebonds/walkthrough/teshwaveruins.php"
]

_urls_pooldark = [
        # GameBanshee Pools of Darkness Walkthrough
        "https://www.gamebanshee.com/poolsofdarkness/equipment-stats.php",
        "https://www.gamebanshee.com/poolsofdarkness/equipment-locs.php",
        "https://www.gamebanshee.com/poolsofdarkness/bestiary/bosses.php",
        "https://www.gamebanshee.com/poolsofdarkness/bestiary/humanoids.php",
        "https://www.gamebanshee.com/poolsofdarkness/bestiary/giants.php",
        "https://www.gamebanshee.com/poolsofdarkness/bestiary/monsters-ag.php",
        "https://www.gamebanshee.com/poolsofdarkness/bestiary/monsters-hz.php",
        "https://www.gamebanshee.com/poolsofdarkness/bestiary/undead.php",
        "https://www.gamebanshee.com/poolsofdarkness/abilityscores.php",
      
        # TODO: Remaining pages
]

def get_urls():
    return _urls_poolrad + _urls_curse + _urls_pooldark

def get_urls_for_game(game: str):
    if game == 'poolrad':
        return _urls_poolrad
    if game == 'curse':
        return _urls_curse
    if game == 'pooldark':
        return _urls_pooldark
    return []
