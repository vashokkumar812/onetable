import os
from .base import *

if os.getenv('environment') is not None:
    if os.environ['environment'] == 'production':
       from .production import *
else:
   from .dev import *
