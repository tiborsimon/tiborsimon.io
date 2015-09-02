import requests
import pickle
import json
import time
import datetime

from tspr.tspr import Store

print('runnning tspr-sync')

Store.sync()

