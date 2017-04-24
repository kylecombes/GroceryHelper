import json
import math
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import urlopen

from keys import *

class Mapping:

    GMAPS_BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?"

    def encodeAddr()
