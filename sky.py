import datetime as dt
import skyfield as sky
from skyfield import almanac
from skyfield.api import N, W, wgs84, load
from skyfield.api import load
import pytz

class Skywatcher:

    current_coords = (0, 0)
    ts = None
    earth = None
    location = None
    timezone = 'US/Central'
    eph = None


    def __init__(self, location = (0,0), timezone = 'US/Central'):
        current_coords = location
        self.ts = load.timescale()
        self.eph = load('de421.bsp')
        self.earth = self.eph['earth']
        self.timezone = pytz.timezone(timezone)
        self.location = wgs84.latlon(current_coords[0] * N, current_coords[1] * W)

    """ 
    Update the location of the Skywatcher object

    Params:
        @longitude
        @latitude
    """

    def update_location(self, longitude, latitude):
        current_coords = (longitude, latitude)
        location = wgs84.latlon(current_coords[0] * N, current_coords[1] * W)




    """
    This function will output the times that it will get dark tonight at the current_coords

    Parameters:
        @twilight_type: accepts a list of the twilights that you want outputted: Options [Astronomical, Nautical, Civil, Day]
    """
    def get_dark_times(self):
        zone = self.timezone
        now = zone.localize(dt.datetime.now())
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + dt.timedelta(days=1.5)


        t0 = self.ts.from_datetime(midnight + dt.timedelta(hours=12))
        t1 = self.ts.from_datetime(next_midnight)

        f = almanac.dark_twilight_day(self.eph, self.location)
        times, events = almanac.find_discrete(t0, t1, f)

        previous_e = f(t0).item()

        outs = []
        best_viewing = []
        for t, e in zip(times, events):
            dnt = str(t.astimezone(zone))[:16].split()
            if len(outs) == 0: outs.append(f"On {self.__convert_time__(dnt[0])[0]}: ")

            if almanac.TWILIGHTS[e] == "Astronomical twilight" or almanac.TWILIGHTS[previous_e] == "Astronomical twilight": best_viewing.append(self.__convert_time__(None, dnt[1])[1])
            if previous_e < e:
                # print(tstr, ' ', almanac.TWILIGHTS[e], 'starts')
                outs.append(f"{almanac.TWILIGHTS[e]} on {self.__convert_time__(dnt[0])[0]} starts at {self.__convert_time__(None, dnt[1])[1]}")
            else:
                # print(tstr, ' ', almanac.TWILIGHTS[previous_e], 'ends')
                outs.append(f"{almanac.TWILIGHTS[previous_e]} on {self.__convert_time__(dnt[0])[0]} ends at {self.__convert_time__(None, dnt[1])[1]}")
            previous_e = e

        outs.append(f"Best viewing time: {best_viewing[0]} to {best_viewing[1]} tonight into tomorrow.")
        
        return outs

    """
    Will get the rise and set time and location (topocentric coordinates)

    Parameters:
        @object - the object that you want rise and set time and location for
    """
    def get_rise_and_set(self, object):
        pass

    """
    Get rise and set location + time for moon as well as the phase and %illumination

    Params:
        None
    """
    def get_moon_info(self):
        pass

    def get_star_id(self, star_name):
        pass

    def get_current_object_location(self, object):
        pass

    def get_planet_position_map(self, planet):
        pass

    def get_constellation_info(self, constellation):
        pass

    def __convert_time__(self, input_date_str=None, input_time_str=None):
        try:
            date_output_str, time_output_str = "", ""

            if input_date_str:
                # If a date is provided
                input_datetime = dt.datetime.strptime(input_date_str, '%Y-%m-%d')
                date_output_str = input_datetime.strftime('%B %d, %Y')
            
            if input_time_str:
                # If a time is provided
                input_time = dt.datetime.strptime(input_time_str, '%H:%M')
                time_output_str = input_time.strftime('%I:%M %p')

            return date_output_str, time_output_str
        except ValueError:
            return "Invalid input format. Please use 'YYYY-MM-DD' for date and 'HH:MM' for time."

