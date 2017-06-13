import datetime
import sqlite3
import sys
import pickle
 
from django.template.loader import get_template
from django.template import Context
 
from django.http import HttpResponse
b=None
try:
    with open('/home/pi/Desktop/IOT/sensor.pickle', 'rb') as handle:
        b = pickle.load(handle)
        print (b)
except EOFError:
    pass
 
def home(request):
    global b
    
    html = '''
<html>
<body>
<h1><Center>Irrigation System Check</Center></h1>
<hr>
Sensor1 value %s
<hr>
Time Flow %s
<hr>
</body>
</html>''' %(b['a'],b['b'])
    return HttpResponse(html)




