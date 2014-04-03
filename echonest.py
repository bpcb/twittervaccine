from pyechonest import config, artist

config.ECHO_NEST_API_KEY = 'OT96HEX0YVCGJEMZK'

washed_out = artist.Artist('classixx')
print washed_out.style

chillwave = artist.search(style='chillwave')
print chillwave