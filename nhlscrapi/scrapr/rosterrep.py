
from nhlscrapi._tools import exclude_from as ex_junk

from nhlscrapi.scrapr.officialsparser import official_parser_mapper as opm
from nhlscrapi.scrapr.reportloader import ReportLoader


class RosterRep(ReportLoader):
    """Retrieve and load roster report from nhl.com. This is a base class and not intended to be used directly."""
    
    def __init__(self, game_key):
        super(RosterRep, self).__init__(game_key, 'game_roster')
        
        self.rosters = { }
        """
        Rosters for both home and away.
        Data: ``{ 'home/away': { num: { 'pos': '', 'name': '' } } }``
        """
        
        self.scratches = { }
        """Dictionary of healthy scratches keyed home/away loaded"""
        
        self.coaches = { }
        """Dictionary of coaches keyed home/away loaded"""
        
        self.officials = { 'refs': { }, 'linesman': { } }
        """Game officials: ``{ 'refs': { }, 'linesman': { } }``"""
        
        self.__blocks = {}
        
        
    def __pl_blocks(self, doc):
        bls = doc.xpath('//td[text()="#"]')
        
        # roster page layout
        # AWAY ROSTER  | HOME ROSTER
        # AWAY SCRATCH | HOME SCRATCH
        bl_k = { 1: 'away', 2: 'home', 3: 'aw_scr', 4: 'h_scr' }
        
        # clean blocks
        for i, bl in enumerate(bls):
            table = bl.xpath('../..')[0]
            self.__blocks[bl_k[i+1]] = table
            
            
    def __clean_pl_block(self, bl):
        def no_letter(s):
            s = s.strip()
            return '(C)' not in s and '(A)' not in s
            
        r = { }
        
        for p in bl:
            txt = p.xpath('.//text()')
            if len(txt) and '#' not in txt[0]:
                txt = ex_junk(txt, ['\r','\n'])
                txt[2] = ' '.join(s.strip() for s in txt[2].split(' ') if no_letter(s))
                
            # need some unique key
            num = int(txt[0]) if txt[0].isdigit() else max(r.keys())+1
            r[num] = { 'position': txt[1], 'name': txt[2] }
            
        return r
        
        
    def parse(self):
        """
        Retreive and parse Play by Play data for the given :py:class:`nhlscrapi.games.game.GameKey``
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        
        try:
            return super(RosterRep, self).parse() \
                .parse_rosters() \
                .parse_scratches() \
                .parse_coaches() \
                .parse_officials()
        except:
            return None
            
            
    def parse_rosters(self):
        """
        Parse the home and away game rosters
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        lx_doc = self.html_doc()
        
        if not self.__blocks:
            self.__pl_blocks(lx_doc)
            
        for t in ['home', 'away']:
            self.rosters[t] = self.__clean_pl_block(self.__blocks[t])
            
        return self if self.rosters else None
        
        
    def parse_scratches(self):
        """
        Parse the home and away healthy scratches
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        lx_doc = self.html_doc()
        if not self.__blocks:
            self.__pl_blocks(lx_doc)
            
        for t in ['aw_scr', 'h_scr']:
            ix = 'away' if t == 'aw_scr' else 'home'
            self.scratches[ix] = self.__clean_pl_block(self.__blocks[t])
            
        return self if self.scratches else None
        
        
    def parse_coaches(self):
        """
        Parse the home and away coaches
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        lx_doc = self.html_doc()
        tr = lx_doc.xpath('//tr[@id="HeadCoaches"]')[0]
        
        for i, td in enumerate(tr):
            txt = td.xpath('.//text()')
            txt = ex_junk(txt, ['\n','\r'])
            team = 'away' if i == 0 else 'home'
            self.coaches[team] = txt[0]
            
        return self if self.coaches else None
        
        
    def parse_officials(self):
        """
        Parse the officials
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        # begin proper body of method
        lx_doc = self.html_doc()
        off_parser = opm(self.game_key.season)
        self.officials = off_parser(lx_doc)
        
        return self if self.officials else None