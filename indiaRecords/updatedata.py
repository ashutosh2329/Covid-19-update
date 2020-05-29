import requests
from .models import IndiaTimeSeries, State, ImpParam, District,GovernmentHelpline,TestCenters,ConfirmedTimeSeriesState,RecoveredTimeSeriesState,DeathsTimeSeriesState
import json
import difflib

url_national_and_state = 'https://api.covid19india.org/data.json'
url_district_wise = 'https://api.covid19india.org/v2/state_district_wise.json'
url_resource = 'https://api.covid19india.org/resources/resources.json'
url_state_timeseries = 'https://api.covid19india.org/states_daily.json'
#
# stateinfo ={}
# with open('stateinfo.json') as f:
#   stateinfo = json.load(f)



def read_url(url):
    res = {}
    try:
        response = requests.get(url)
        print(response.status_code)
        res = response.json()
        # prints the int of the status code. Find more at httpstatusrappers.com :)
    except requests.ConnectionError:
        print("failed to connect")
        res = {"error":404}
    return res;

def data1():
    url = url_national_and_state
    json_data = read_url(url)

    if('error' in json_data):
        print("unable to connect")

    else:
        indiatimeseries = json_data['cases_time_series']
        statewisedata = json_data['statewise']
        testdata = json_data['tested']
        saveindiatimeseries(indiatimeseries)
        savestatewisedata(statewisedata)
        savetestrecord(testdata)

def saveindiatimeseries(datas):
    for data in datas:
        date = data['date']
        dailyconfirmed = data['dailyconfirmed']
        dailydeceased = data['dailydeceased']
        dailyrecovered = data['dailyrecovered']
        totalconfirmed = data['totalconfirmed']
        totaldeceased = data['totaldeceased']
        totalrecovered = data['totalrecovered']


        day = IndiaTimeSeries(date = date,
                              dailyconfirmed=dailyconfirmed,
                              dailyrecovered=dailyrecovered,
                              dailydeaths=dailydeceased,
                              totalconfirmed=totalconfirmed,
                              totaldeaths=totaldeceased,
                              totalrecovered=totalrecovered
                              )
        day.save()

def savestatewisedata(datas):
    for data in datas:
        active = data['active']
        confirmed = data['confirmed']
        deaths = data['deaths']
        recovered = data['recovered']
        deltaconfirmed = data['deltaconfirmed']
        deltarecovered = data['deltarecovered']
        deltadeaths = data['deltadeaths']
        state = data['state']
        statecode = data['statecode']
        lastupdatedtime = data['lastupdatedtime']

        print(state)

        if(state == "Total"):
            indactive = ImpParam(key='indactive',value=active);
            indconfirmed = ImpParam(key='indconfirmed',value=confirmed)
            inddeaths = ImpParam(key='inddeaths',value=deaths);
            indrecovered= ImpParam(key='indrecovered',value=recovered)
            inddeltaconfirmed = ImpParam(key='inddeltaconfirmed',value=deltaconfirmed);
            inddeltadeaths = ImpParam(key='inddeltadeaths',value=deltadeaths)
            inddeltarecovered = ImpParam(key='inddeltarecovered',value=deltarecovered);
            indlastupdatetime = ImpParam(key='indlastupdatetime',value=lastupdatedtime)

            indactive.save()
            indconfirmed.save()
            inddeaths.save()
            indrecovered.save()
            inddeltadeaths.save()
            inddeltaconfirmed.save()
            inddeltarecovered.save()
            indlastupdatetime.save()

        else:
            statecode = stateinfo['statecode'][state]

            st = State(name=state,
                       statecode=statecode,
                       active=active,
                       confirmed=confirmed,
                       deaths=deaths,
                       recovered=recovered,
                       deltadeaths=deltadeaths,
                       deltaconfirmed=deltaconfirmed,
                       deltarecovered=deltarecovered,
                       lastupdatetime=lastupdatedtime)
            st.save()

def savetestrecord(datas):
    persontested = 0
    sampletested = 0
    for data in datas:
        totalindividualtested = data['totalindividualstested']
        totalsampletested = data['totalsamplestested']

        if(totalindividualtested!="" and persontested<int(totalindividualtested)):
            persontested = int(totalindividualtested)
        if(totalsampletested!="" and sampletested<int(totalsampletested)):
            sampletested = int(totalsampletested)


    t1 = ImpParam(key='totalindividualtested',value=persontested)
    t2 = ImpParam(key='totalsampletested',value=sampletested)

    t1.save()
    t2.save()

def data2():
    url = url_district_wise
    json_data = read_url(url)

    if('error' in json_data):
        print("unable to connect")
    else:
        savestatedistrictdata(json_data)

def savestatedistrictdata(datas):
    for data in datas:
        state = data['state']
        districtdata = data['districtData']
        for district in districtdata:
            name = district['district']
            confirmed = district['confirmed']
            deltaconfirmed = district['delta']['confirmed']

            st12 = State.objects.get(name=state)
            Dist = District(name=name,
                            confirmed=confirmed,
                            deltaconfirmed=deltaconfirmed,
                            state=st12)
            Dist.save()

def data3():
    url = url_resource
    json_data = read_url(url)

    if('error' in json_data):
        print("unable to connect")
    else:
        saveresourcedata(json_data['resources'])

def saveresourcedata(datas):
    lststatenames = []
    for obj in State.objects.all():
        lststatenames.append(obj.name);
    for data in datas:
        state1 = data['state']
        state1 = state1.replace('&','and')
        state = difflib.get_close_matches(state1, lststatenames)[0]
        print(state1,state)
        if(data['category'] == "CoVID-19 Testing Lab"):
            st12 = State.objects.get(name=state)

            tstlab = TestCenters( name= data['category'],
                                  city= data['city'],
                                  contact = data['contact'],
                                  description = data['descriptionandorserviceprovided'],
                                  nameoforganization = data['nameoftheorganisation'],
                                  phonenumber= data['phonenumber'],
                                  state=st12)
            tstlab.save()

        elif(data['category'] == "Government Helpline"):
            st12 = State.objects.get(name=state)
            hlp = GovernmentHelpline( name= data['category'],
                                  city= data['city'],
                                  contact = data['contact'],
                                  description = data['descriptionandorserviceprovided'],
                                  nameoforganization = data['nameoftheorganisation'],
                                  phonenumber= data['phonenumber'],
                                  state=st12)
            hlp.save()

def data4():
    url = url_state_timeseries
    json_data = read_url(url)

    if('error' in json_data):
        print("unable to connect")
    else:
        savetimeseriesforstates(json_data['states_daily'])

def savetimeseriesforstates(datas):

    for data in datas:
        date = data['date']

        if(data['status'] == "Confirmed"):
            for d in data:
                if(data[d]==""):
                    data[d]="0";
            cnftime = ConfirmedTimeSeriesState( date = data['date'],
                                                ani = int(data['an']),
                                                api = int(data['ap']),
                                                ari = int(data['ar']),
                                                asi = int(data['as']),
                                                bri = int(data['br']),
                                                chi = int(data['ch']),
                                                cti = int(data['ct']),
                                                ddi = int(data['dd']),
                                                dli = int(data['dl']),
                                                dni = int(data['dn']),
                                                gai = int(data['ga']),
                                                gji = int(data['gj']),
                                                hpi = int(data['hp']),
                                                hri = int(data['hr']),
                                                jhi = int(data['jh']),
                                                jki = int(data['jk']),
                                                kai = int(data['ka']),
                                                kli = int(data['kl']),
                                                lai = int(data['la']),
                                                ldi = int(data['ld']),
                                                mhi = int(data['mh']),
                                                mli = int(data['ml']),
                                                mni = int(data['mn']),
                                                mpi = int(data['mp']),
                                                mzi = int(data['mz']),
                                                nli = int(data['nl']),
                                                ori = int(data['or']),
                                                pbi = int(data['pb']),
                                                pyi = int(data['py']),
                                                rji = int(data['rj']),
                                                ski = int(data['sk']),
                                                tgi = int(data['tg']),
                                                tni = int(data['tn']),
                                                tri = int(data['tr']),
                                                tti = int(data['tt']),
                                                upi = int(data['up']),
                                                uti = int(data['ut']),
                                                wbi = int(data['wb']))
            cnftime.save()
        elif(data['status'] == "Recovered"):
            rectm = RecoveredTimeSeriesState( date = data['date'],
                                                ani = int(data['an']),
                                                api = int(data['ap']),
                                                ari = int(data['ar']),
                                                asi = int(data['as']),
                                                bri = int(data['br']),
                                                chi = int(data['ch']),
                                                cti = int(data['ct']),
                                                ddi = int(data['dd']),
                                                dli = int(data['dl']),
                                                dni = int(data['dn']),
                                                gai = int(data['ga']),
                                                gji = int(data['gj']),
                                                hpi = int(data['hp']),
                                                hri = int(data['hr']),
                                                jhi = int(data['jh']),
                                                jki = int(data['jk']),
                                                kai = int(data['ka']),
                                                kli = int(data['kl']),
                                                lai = int(data['la']),
                                                ldi = int(data['ld']),
                                                mhi = int(data['mh']),
                                                mli = int(data['ml']),
                                                mni = int(data['mn']),
                                                mpi = int(data['mp']),
                                                mzi = int(data['mz']),
                                                nli = int(data['nl']),
                                                ori = int(data['or']),
                                                pbi = int(data['pb']),
                                                pyi = int(data['py']),
                                                rji = int(data['rj']),
                                                ski = int(data['sk']),
                                                tgi = int(data['tg']),
                                                tni = int(data['tn']),
                                                tri = int(data['tr']),
                                                tti = int(data['tt']),
                                                upi = int(data['up']),
                                                uti = int(data['ut']),
                                                wbi = int(data['wb']))
            rectm.save()
        elif(data['status'] == "Deceased"):
            dctim = DeathsTimeSeriesState(  date = data['date'],
                                            ani = int(data['an']),
                                            api = int(data['ap']),
                                            ari = int(data['ar']),
                                            asi = int(data['as']),
                                            bri = int(data['br']),
                                            chi = int(data['ch']),
                                            cti = int(data['ct']),
                                            ddi = int(data['dd']),
                                            dli = int(data['dl']),
                                            dni = int(data['dn']),
                                            gai = int(data['ga']),
                                            gji = int(data['gj']),
                                            hpi = int(data['hp']),
                                            hri = int(data['hr']),
                                            jhi = int(data['jh']),
                                            jki = int(data['jk']),
                                            kai = int(data['ka']),
                                            kli = int(data['kl']),
                                            lai = int(data['la']),
                                            ldi = int(data['ld']),
                                            mhi = int(data['mh']),
                                            mli = int(data['ml']),
                                            mni = int(data['mn']),
                                            mpi = int(data['mp']),
                                            mzi = int(data['mz']),
                                            nli = int(data['nl']),
                                            ori = int(data['or']),
                                            pbi = int(data['pb']),
                                            pyi = int(data['py']),
                                            rji = int(data['rj']),
                                            ski = int(data['sk']),
                                            tgi = int(data['tg']),
                                            tni = int(data['tn']),
                                            tri = int(data['tr']),
                                            tti = int(data['tt']),
                                            upi = int(data['up']),
                                            uti = int(data['ut']),
                                            wbi = int(data['wb']))
            dctim.save()


def write():
    data1()
    data2()
    data3()
    data4()

def updatedistrictdata(datas):
    print("entering district data update")
    for data in datas:
        st = data['state']
        state = State.objects.get(name=st)
        distdata = data['districtData']
        for dist in distdata:
            try:
                d = District.objects.get(name=dist['district'],state=state)
                d.confirmed = dist['confirmed']
                d.deltaconfirmed = dist['delta']['confirmed']
                d.save()
            except Exception as e:
                d = District(name=dist['district'],state=state,confirmed=dist['confirmed'],deltaconfirmed=dist['delta']['confirmed'])
                d.save()
    print("exiting district data update")

def updatestatetimeseries(datas):
    print("entering state-timeseries data update")
    for data in datas:
        try:
            tms = ConfirmedTimeSeriesState.objects.get(date=data['date'])
        except Exception as e:
            for d in data:
                if(data[d]==""):
                    data[d]="0";
            if(data['status'] == "Confirmed"):
                cnftime = ConfirmedTimeSeriesState( date = data['date'],
                                                    ani = int(data['an']),
                                                    api = int(data['ap']),
                                                    ari = int(data['ar']),
                                                    asi = int(data['as']),
                                                    bri = int(data['br']),
                                                    chi = int(data['ch']),
                                                    cti = int(data['ct']),
                                                    ddi = int(data['dd']),
                                                    dli = int(data['dl']),
                                                    dni = int(data['dn']),
                                                    gai = int(data['ga']),
                                                    gji = int(data['gj']),
                                                    hpi = int(data['hp']),
                                                    hri = int(data['hr']),
                                                    jhi = int(data['jh']),
                                                    jki = int(data['jk']),
                                                    kai = int(data['ka']),
                                                    kli = int(data['kl']),
                                                    lai = int(data['la']),
                                                    ldi = int(data['ld']),
                                                    mhi = int(data['mh']),
                                                    mli = int(data['ml']),
                                                    mni = int(data['mn']),
                                                    mpi = int(data['mp']),
                                                    mzi = int(data['mz']),
                                                    nli = int(data['nl']),
                                                    ori = int(data['or']),
                                                    pbi = int(data['pb']),
                                                    pyi = int(data['py']),
                                                    rji = int(data['rj']),
                                                    ski = int(data['sk']),
                                                    tgi = int(data['tg']),
                                                    tni = int(data['tn']),
                                                    tri = int(data['tr']),
                                                    tti = int(data['tt']),
                                                    upi = int(data['up']),
                                                    uti = int(data['ut']),
                                                    wbi = int(data['wb']))
                cnftime.save()
            elif(data['status'] == "Recovered"):
                rectm = RecoveredTimeSeriesState( date = data['date'],
                                                    ani = int(data['an']),
                                                    api = int(data['ap']),
                                                    ari = int(data['ar']),
                                                    asi = int(data['as']),
                                                    bri = int(data['br']),
                                                    chi = int(data['ch']),
                                                    cti = int(data['ct']),
                                                    ddi = int(data['dd']),
                                                    dli = int(data['dl']),
                                                    dni = int(data['dn']),
                                                    gai = int(data['ga']),
                                                    gji = int(data['gj']),
                                                    hpi = int(data['hp']),
                                                    hri = int(data['hr']),
                                                    jhi = int(data['jh']),
                                                    jki = int(data['jk']),
                                                    kai = int(data['ka']),
                                                    kli = int(data['kl']),
                                                    lai = int(data['la']),
                                                    ldi = int(data['ld']),
                                                    mhi = int(data['mh']),
                                                    mli = int(data['ml']),
                                                    mni = int(data['mn']),
                                                    mpi = int(data['mp']),
                                                    mzi = int(data['mz']),
                                                    nli = int(data['nl']),
                                                    ori = int(data['or']),
                                                    pbi = int(data['pb']),
                                                    pyi = int(data['py']),
                                                    rji = int(data['rj']),
                                                    ski = int(data['sk']),
                                                    tgi = int(data['tg']),
                                                    tni = int(data['tn']),
                                                    tri = int(data['tr']),
                                                    tti = int(data['tt']),
                                                    upi = int(data['up']),
                                                    uti = int(data['ut']),
                                                    wbi = int(data['wb']))
                rectm.save()
            elif(data['status'] == "Deceased"):
                dctim = DeathsTimeSeriesState(  date = data['date'],
                                                ani = int(data['an']),
                                                api = int(data['ap']),
                                                ari = int(data['ar']),
                                                asi = int(data['as']),
                                                bri = int(data['br']),
                                                chi = int(data['ch']),
                                                cti = int(data['ct']),
                                                ddi = int(data['dd']),
                                                dli = int(data['dl']),
                                                dni = int(data['dn']),
                                                gai = int(data['ga']),
                                                gji = int(data['gj']),
                                                hpi = int(data['hp']),
                                                hri = int(data['hr']),
                                                jhi = int(data['jh']),
                                                jki = int(data['jk']),
                                                kai = int(data['ka']),
                                                kli = int(data['kl']),
                                                lai = int(data['la']),
                                                ldi = int(data['ld']),
                                                mhi = int(data['mh']),
                                                mli = int(data['ml']),
                                                mni = int(data['mn']),
                                                mpi = int(data['mp']),
                                                mzi = int(data['mz']),
                                                nli = int(data['nl']),
                                                ori = int(data['or']),
                                                pbi = int(data['pb']),
                                                pyi = int(data['py']),
                                                rji = int(data['rj']),
                                                ski = int(data['sk']),
                                                tgi = int(data['tg']),
                                                tni = int(data['tn']),
                                                tri = int(data['tr']),
                                                tti = int(data['tt']),
                                                upi = int(data['up']),
                                                uti = int(data['ut']),
                                                wbi = int(data['wb']))
                dctim.save()
    print("exiting state-timeseries data update")

def updatestatewise(datas):
    print("entering state-wise data update")
    for data in datas:
        if(data['state']=="Total"):
            indactive = ImpParam.objects.get(key='indactive')
            indconfirmed = ImpParam.objects.get(key='indconfirmed')
            inddeaths = ImpParam.objects.get(key='inddeaths');
            indrecovered= ImpParam.objects.get(key='indrecovered')
            inddeltaconfirmed = ImpParam.objects.get(key='inddeltaconfirmed');
            inddeltadeaths = ImpParam.objects.get(key='inddeltadeaths')
            inddeltarecovered = ImpParam.objects.get(key='inddeltarecovered');
            indlastupdatetime = ImpParam.objects.get(key='indlastupdatetime')

            indactive.value=data['active']
            indconfirmed.value=data['confirmed']
            inddeaths.value=data['deaths']
            indrecovered.value=data['recovered']
            inddeltadeaths.value=data['deltadeaths']
            inddeltaconfirmed.value=data['deltaconfirmed']
            inddeltarecovered.value=data['deltarecovered']
            indlastupdatetime.value=data['lastupdatedtime']

            indactive.save()
            indconfirmed.save()
            inddeaths.save()
            indrecovered.save()
            inddeltadeaths.save()
            inddeltaconfirmed.save()
            inddeltarecovered.save()
            indlastupdatetime.save()
        else:
            st = State.objects.get(name=data['state'])

            st.confirmed = data['confirmed']
            st.deaths = data['deaths']
            st.recovered = data['recovered']
            st.active = data['active']
            st.deltaconfirmed= data['deltaconfirmed']
            st.deltadeaths= data['deltadeaths']
            st.deltarecovered= data['deltarecovered']
            st.lastupdatetime = data['lastupdatedtime']

            st.save()
    print("exiting state-wise data update")

def updateindtimeseries(datas):
    print("entering india timeseries data update")
    for data in datas:
        date = data['date']
        try:
            tp = IndiaTimeSeries.objects.get(date=date)
        except Exception as e:
            tps = IndiaTimeSeries(date=date,
                                  dailyconfirmed = data['dailyconfirmed'],
                                  dailyrecovered = data['dailyrecovered'],
                                  dailydeaths = data['dailydeceased'],
                                  totalconfirmed = data['totalconfirmed'],
                                  totaldeaths = data['totaldeceased'],
                                  totalrecovered = data['totalrecovered'])
            tps.save()
    print("exiting india timeseries data update")

def updatetested(datas):
    print("entering tested data update")
    persontested = int(ImpParam.objects.get(key='totalindividualtested').value)
    sampletested = int(ImpParam.objects.get(key='totalsampletested').value)
    for data in datas:
        totalindividualtested = data['totalindividualstested']
        totalsampletested = data['totalsamplestested']

        if(totalindividualtested!="" and persontested<int(totalindividualtested)):
            persontested = int(totalindividualtested)
        if(totalsampletested!="" and sampletested<int(totalsampletested)):
            sampletested = int(totalsampletested)


    t1 = ImpParam.objects.get(key='totalindividualtested')
    t2 = ImpParam.objects.get(key='totalsampletested')
    t1.value = persontested
    t2.value = sampletested

    t1.save()
    t2.save()
    print("exiting tested data update")


def edit1():
    url = url_district_wise
    json_data = read_url(url)

    if('error' in json_data):
        print("unable to connect api")
    else:
        updatedistrictdata(json_data)

def edit2():
    url = url_state_timeseries

    json_data = read_url(url)
    if('error' in json_data):
        print('unable to connect')
    else:
        updatestatetimeseries(json_data['states_daily'])

def edit3():
    url = url_national_and_state
    json_data = read_url(url)

    if('error' in json_data):
        print('unable to connect')
    else:
        updateindtimeseries(json_data['cases_time_series'])
        updatestatewise(json_data['statewise'])
        updatetested(json_data['tested'])

def dataupdate():
    edit1()
    edit2()
    edit3()

#dataupdate()
# write()
