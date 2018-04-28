#!/usr/bin/env python3

### 
# If you use 'geoclue' in redshift and run vpn, it's getting pretty confused (as it should!).
# But timezone information is available on ubuntu anyway, so this script uses it and reruns redshift in case something changed.
# requirements: geopy, tzlocal
###

import signal
import time
import os
from subprocess import check_output, Popen

from geopy.geocoders import Nominatim

def get_tz_city():
    from tzlocal import get_localzone
    city = get_localzone().zone.split('/')[-1]
    return city

class RedshiftDaemon:
    def __init__(self, check_every_s):
        self.city = None
        self.redshift = None
        self.geolocator = Nominatim()
        self.check_every_s = check_every_s

    def restart_redshift(self, location):
        if self.redshift is not None:
            os.killpg(os.getpgid(redshift.pid), signal.SIGTERM)
            self.redshift = None
        cmd = f'redshift-gtk -l {location.latitude}:{location.longitude}'.split()
        print("Running " + str(cmd))
        self.redshift = Popen(cmd, preexec_fn=os.setsid)

    def run(self):
        while True:
            new_city = get_tz_city()
            print(f"Detected city: {new_city}")
            if new_city != self.city:
                self.city = new_city
                print(f"Detected change in city {self.city} -> {new_city}, rerunning...")
                geo = self.geolocator.geocode(new_city)
                print(f"Current location: {geo}")
                self.restart_redshift(geo)
        
            print(f"Sleeping for {self.check_every_s} seconds")
            time.sleep(self.check_every_s)

if __name__ == '__main__':
    RedshiftDaemon(5).run()
