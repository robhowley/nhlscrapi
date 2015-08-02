
import re

from nhlscrapi._tools import (
    to_int,
    re_comp_num_pos_name,
    exclude_from as ex_junk
)
from nhlscrapi.scrapr.reportloader import ReportLoader


class FaceOffRep(ReportLoader):
    """Retrieve and load face-off comparison report from nhl.com"""
    
    def __init__(self, game_key):
        super(FaceOffRep, self).__init__(game_key, 'face_offs')
        
        self.face_offs = { }
        """
        report in dictionary format
        
        .. code:: python
        
            {
                home/away: {
                    player_nums: {
                        'name': name,
                        'pos': position,
                        'off/def/neut/all': {
                            'won': won, 'total': total
                        },
                        'opps': {
                            basically same info as above.
                            name, pos, and zone info of opponents
                        }
                    }
                }
            }
        """
        
        self.__vis_doc = None
        self.__home_doc = None
    
    def __set_team_docs(self):
        if self.__vis_doc is None or self.__home_doc is None:
            lx_doc = self.html_doc()
            # report banner as reference
            header = lx_doc.xpath("//table[@id='StdHeader']/../..")[0]
            header_sibs = header.xpath('following-sibling::tr')
            self.__vis_doc = header_sibs[1]
            self.__home_doc = header_sibs[3]
    
    def parse(self):
        """
        Retreive and parse Play by Play data for the given nhlscrapi.GameKey
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        try:
            return (
                super(FaceOffRep, self).parse()
                and self.parse_home_face_offs()
                and self.parse_away_face_offs()
            )
        except:
            return None
    
    def parse_home_face_offs(self):
        """
        Parse only the home faceoffs
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        self.__set_team_docs()
        self.face_offs['home'] = FaceOffRep.__read_team_doc(self.__home_doc)
        return self
        
    def parse_away_face_offs(self):
        """
        Parse only the away faceoffs
        
        :returns: ``self`` on success, ``None`` otherwise
        """
        self.__set_team_docs()
        self.face_offs['away'] = FaceOffRep.__read_team_doc(self.__vis_doc)
        return self
    
    @staticmethod
    def __tot_pct(res):
        ct = res.split('/')[0].strip()
        won, tot = tuple(to_int(i) for i in ct.split('-'))
        return { 'won': won, 'total': tot }
    
    @staticmethod
    def __player_fo_rec(name, pos, zone_raw):
        off, defz, neut, tot = tuple(
            FaceOffRep.__tot_pct(ri) if ord(ri[0]) < 128 else { 'won': 0, 'total': 0 }
            for ri in zone_raw
        )
        return {
            'name': name,
            'pos': pos,
            'off': off,
            'def': defz,
            'neut': neut,
            'all': tot
        }
    
    @staticmethod
    def __read_team_doc(lx_doc):
        fo = { }
        re_opp = re_comp_num_pos_name()
        
        took_draw = lx_doc.xpath(".//td[contains(@class,'playerHeading')]/..")
        for cent in took_draw:
            # extract info of center taking the draw
            rec = ex_junk(cent.xpath('.//text()'), containing=['\n','\r'])
            
            num, pos, name = to_int(rec[0]), rec[1], ' '.join(ri.strip() for ri in reversed(rec[2].split(',')))
            fo[num] = FaceOffRep.__player_fo_rec(name, pos, rec[3:7])
            fo[num]['opps'] = { }
            
            for vs in cent.xpath('following-sibling::tr'):
                if vs.xpath(".//td[contains(@class,'space')]"):
                    break
                else:
                    opp_rec = ex_junk(vs.xpath('.//text()'), containing=['\n','\r'])
                    reg_res = re_opp.findall(opp_rec[2])
                    opp_num, opp_pos, opp_last, opp_first = reg_res[0] if reg_res else ('-1', '', '', '')
                    opp_name = ' '.join(oi.strip() for oi in [ opp_first, opp_last ])
                    fo[num]['opps'][to_int(opp_num)] = FaceOffRep.__player_fo_rec(opp_name, opp_pos, opp_rec[3:7])
        
        return fo