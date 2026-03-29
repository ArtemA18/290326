from Connections.connection import *

class Base(Model):
    class Meta:
        database = connect()