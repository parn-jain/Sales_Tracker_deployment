from django.db import models

class CallingAgentProxy(models.Model):
    class Meta:
        managed = False
        db_table = 'CallingAgent'
