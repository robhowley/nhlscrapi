
from nhlscrapi._tools import to_int
from nhlscrapi._tools import exclude_from as ex_junk

from nhlscrapi.scrapr.reportloader import ReportLoader
from nhlscrapi.games.events import EventType as ET


class TOIRepBase(ReportLoader):
    """
    Scrapes TOI reports. (home/away are same format).
    """
  
    def __init__(self, game_key, rep_type):
        super(TOIRepBase, self).__init__(game_key, rep_type)
    
        self.by_player = { }
        """
        By player dictionary of shift summaries. The only events recorded per shift are :py:class:`.EventType.Goal`
        or :py:class:`.EventType.Penalty`. For ``period = 0``, the game totals are returned. Format is
        
        .. code:: python
        
            {
                player_num: {
                    'player_name': { 'first': '', 'last': '' },
                    'shifts': [
                        {
                            'shift_num': shift_num,
                            'period': period_num,
                            'start': start_time (elapsed)
                            'end': end_time (elapsed)
                            'dur': length_of_shift,
                            'event': event_enum_goal_or_penalty
                        }
                    ],
                    'by_period': {
                        'period': period_num,
                        'shifts': shift_count,
                        'avg': { 'min': min, 'sec': sec },
                        'toi': { 'min': min, 'sec': sec },
                        'ev_toi': { 'min': min, 'sec': sec },
                        'pp_toi': { 'min': min, 'sec': sec },
                        'sh_toi': { 'min': min, 'sec': sec }
                    }
                }
            }
        """

    def __player_shifts(self, shift):
        parsed_shifts = []
    
        while True:
            sh_arr = ex_junk(shift.xpath('.//text()'), ['\r','\n'], [''])
            parsed_shifts.append(self.__build_shift(sh_arr))

            # get next row
            shift = shift.xpath('following-sibling::tr')[0]
            cl = shift.get('class')
            if cl is None or cl.strip() not in ['oddColor', 'evenColor']:
                break
      
        return parsed_shifts, shift
  
    def __get_time(self, time_str):
        if time_str and ':' in time_str:
            mins, secs = time_str.split(':')
            return { 'min': to_int(mins), 'sec': to_int(secs) }
        else:
            return { 'min': 0, 'sec': 0 }
    
    def __build_shift(self, shift):
        shift = [s.strip() for s in shift]
    
        ev = None
        if shift[-1] == 'G':
            ev = ET.Goal
        elif shift[-1] == 'P':
            ev = ET.Penalty
    
        return {
            'shift_num': to_int(shift[0]),
            'period': 4 if shift[1] == 'OT' else to_int(shift[1]),
            'start': self.__get_time(shift[2].split(' / ')[0]),
            'end': self.__get_time(shift[3].split(' / ')[0]),
            'dur': self.__get_time(shift[4]),
            'event': ev
        }
    
    def __get_by_per_summ(self, per_summ):
        summ = { }
        while True:
            cl = per_summ.get('class')
            if cl is not None and cl.strip() in ['oddColor', 'evenColor']:
                txt = ex_junk(per_summ.xpath('.//text()'), ['\r', '\n'], [''])
                if txt:
                    per = to_int(txt[0])
                    per = per if per > 0 else 4 if txt[0] == 'OT' else 0
                    ps = {
                        'shifts': to_int(txt[1]),
                        'avg': self.__get_time(txt[2]),
                        'toi': self.__get_time(txt[3]),
                        'ev_toi': self.__get_time(txt[4]),
                        'pp_toi': self.__get_time(txt[5]),
                        'sh_toi': self.__get_time(txt[6])
                    }
              
                summ[per] = ps
        
            per_summ = per_summ.xpath('following-sibling::tr')
            if per_summ:
                per_summ = per_summ[0]
            else:
                break
      
        return summ, per_summ

    def parse(self):
        """
        Parse full TOI document.
        
        :returns: ``self`` if successful else ``None``
        """
        
        try:
            return super(TOIRepBase, self).parse().self.parse_shifts()
        except:
            return None

    def parse_shifts(self):
        """
        Parse shifts from TOI report
        
        :returns: self if successfule else None
        """
        
        lx_doc = self.html_doc()
        pl_heads = lx_doc.xpath('//td[contains(@class, "playerHeading")]')
        for pl in pl_heads:
            sh_sum = { }
              
            pl_text = pl.xpath('text()')[0]
            num_name = pl_text.replace(',','').split(' ')
            sh_sum['player_num'] = int(num_name[0]) if num_name[0].isdigit() else -1
            sh_sum['player_name'] = { 'first': num_name[2], 'last': num_name[1] }
              
            first_shift = pl.xpath('../following-sibling::tr')[1]
            sh_sum['shifts'], last_shift = self.__player_shifts(first_shift)
              
            while ('Per' not in last_shift.xpath('.//text()')):
                last_shift = last_shift.xpath('following-sibling::tr')[0]
                
            per_summ = last_shift.xpath('.//tr')[0]
            sh_sum['by_period'], last_sum = self.__get_by_per_summ(per_summ)
            
            
            self.by_player[sh_sum['player_num']] = sh_sum
        
        return self if self.by_player else None
      

class HomeTOIRep(TOIRepBase):
    """Scrapes the home team TOI report"""
  
    def __init__(self, game_key):
        super(HomeTOIRep, self).__init__(game_key, "home_toi")
    

class AwayTOIRep(TOIRepBase):
    """Scrapes the home team TOI report"""
  
    def __init__(self, game_key):
        super(AwayTOIRep, self).__init__(game_key, "away_toi")
    
  

