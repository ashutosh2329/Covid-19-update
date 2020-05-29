from django.db import models
from datetime import datetime

# Create your models here.



class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    statecode = models.CharField(max_length=10,unique=True)
    confirmed = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    recovered = models.IntegerField(default=0)
    active = models.IntegerField(default=0)
    deltaconfirmed= models.IntegerField(default=0)
    deltadeaths= models.IntegerField(default=0)
    deltarecovered= models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    longitude = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    lastupdatetime = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    confirmed = models.IntegerField(default=0)
    deltaconfirmed = models.IntegerField(default=0)
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TestCenters(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    nameoforganization = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class GovernmentHelpline(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    nameoforganization = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    state = models.ForeignKey(State,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ConfirmedTimeSeriesState(models.Model):
    date = models.CharField(max_length=100, unique=True)
    ani = models.IntegerField(default=0)
    api = models.IntegerField(default=0)
    ari = models.IntegerField(default=0)
    asi = models.IntegerField(default=0)
    bri = models.IntegerField(default=0)
    chi = models.IntegerField(default=0)
    cti = models.IntegerField(default=0)
    ddi = models.IntegerField(default=0)
    dli = models.IntegerField(default=0)
    dni = models.IntegerField(default=0)
    gai = models.IntegerField(default=0)
    gji = models.IntegerField(default=0)
    hpi = models.IntegerField(default=0)
    hri = models.IntegerField(default=0)
    jhi = models.IntegerField(default=0)
    jki = models.IntegerField(default=0)
    kai = models.IntegerField(default=0)
    kli = models.IntegerField(default=0)
    lai = models.IntegerField(default=0)
    ldi = models.IntegerField(default=0)
    mhi = models.IntegerField(default=0)
    mli = models.IntegerField(default=0)
    mni = models.IntegerField(default=0)
    mpi = models.IntegerField(default=0)
    mzi = models.IntegerField(default=0)
    nli = models.IntegerField(default=0)
    ori = models.IntegerField(default=0)
    pbi = models.IntegerField(default=0)
    pyi = models.IntegerField(default=0)
    rji = models.IntegerField(default=0)
    ski = models.IntegerField(default=0)
    tgi = models.IntegerField(default=0)
    tni = models.IntegerField(default=0)
    tri = models.IntegerField(default=0)
    tti = models.IntegerField(default=0)
    upi = models.IntegerField(default=0)
    uti = models.IntegerField(default=0)
    wbi = models.IntegerField(default=0)

    def __str__(self):
        res = "Confirmed "+self.date
        return res

class RecoveredTimeSeriesState(models.Model):
    date = models.CharField(max_length=100, unique=True)
    ani = models.IntegerField(default=0)
    api = models.IntegerField(default=0)
    ari = models.IntegerField(default=0)
    asi = models.IntegerField(default=0)
    bri = models.IntegerField(default=0)
    chi = models.IntegerField(default=0)
    cti = models.IntegerField(default=0)
    ddi = models.IntegerField(default=0)
    dli = models.IntegerField(default=0)
    dni = models.IntegerField(default=0)
    gai = models.IntegerField(default=0)
    gji = models.IntegerField(default=0)
    hpi = models.IntegerField(default=0)
    hri = models.IntegerField(default=0)
    jhi = models.IntegerField(default=0)
    jki = models.IntegerField(default=0)
    kai = models.IntegerField(default=0)
    kli = models.IntegerField(default=0)
    lai = models.IntegerField(default=0)
    ldi = models.IntegerField(default=0)
    mhi = models.IntegerField(default=0)
    mli = models.IntegerField(default=0)
    mni = models.IntegerField(default=0)
    mpi = models.IntegerField(default=0)
    mzi = models.IntegerField(default=0)
    nli = models.IntegerField(default=0)
    ori = models.IntegerField(default=0)
    pbi = models.IntegerField(default=0)
    pyi = models.IntegerField(default=0)
    rji = models.IntegerField(default=0)
    ski = models.IntegerField(default=0)
    tgi = models.IntegerField(default=0)
    tni = models.IntegerField(default=0)
    tri = models.IntegerField(default=0)
    tti = models.IntegerField(default=0)
    upi = models.IntegerField(default=0)
    uti = models.IntegerField(default=0)
    wbi = models.IntegerField(default=0)

    def __str__(self):
        res = "Recovered "+self.date
        return res

class DeathsTimeSeriesState(models.Model):
    date = models.CharField(max_length=100, unique=True)
    ani = models.IntegerField(default=0)
    api = models.IntegerField(default=0)
    ari = models.IntegerField(default=0)
    asi = models.IntegerField(default=0)
    bri = models.IntegerField(default=0)
    chi = models.IntegerField(default=0)
    cti = models.IntegerField(default=0)
    ddi = models.IntegerField(default=0)
    dli = models.IntegerField(default=0)
    dni = models.IntegerField(default=0)
    gai = models.IntegerField(default=0)
    gji = models.IntegerField(default=0)
    hpi = models.IntegerField(default=0)
    hri = models.IntegerField(default=0)
    jhi = models.IntegerField(default=0)
    jki = models.IntegerField(default=0)
    kai = models.IntegerField(default=0)
    kli = models.IntegerField(default=0)
    lai = models.IntegerField(default=0)
    ldi = models.IntegerField(default=0)
    mhi = models.IntegerField(default=0)
    mli = models.IntegerField(default=0)
    mni = models.IntegerField(default=0)
    mpi = models.IntegerField(default=0)
    mzi = models.IntegerField(default=0)
    nli = models.IntegerField(default=0)
    ori = models.IntegerField(default=0)
    pbi = models.IntegerField(default=0)
    pyi = models.IntegerField(default=0)
    rji = models.IntegerField(default=0)
    ski = models.IntegerField(default=0)
    tgi = models.IntegerField(default=0)
    tni = models.IntegerField(default=0)
    tri = models.IntegerField(default=0)
    tti = models.IntegerField(default=0)
    upi = models.IntegerField(default=0)
    uti = models.IntegerField(default=0)
    wbi = models.IntegerField(default=0)

    def __str__(self):
        res = "Deaths "+self.date
        return res

class IndiaTimeSeries(models.Model):
    dailyconfirmed = models.IntegerField(default=0)
    dailyrecovered = models.IntegerField(default=0)
    dailydeaths = models.IntegerField(default=0)
    totalconfirmed = models.IntegerField(default=0)
    totaldeaths = models.IntegerField(default=0)
    totalrecovered = models.IntegerField(default=0)
    date = models.CharField(max_length=100, unique=True)

    def __str__(self):
        res = "India "+self.date
        return res

class ImpParam(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.key
