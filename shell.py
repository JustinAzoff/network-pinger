import readline
import rlcompleter

readline.parse_and_bind('tab: complete')

import sys
from networkpinger.model import configure
configure(sys.argv[1])

from networkpinger import model
