from django.shortcuts import render
from django.views.generic import View
from .updatedata import write, dataupdate
import random
from .models import IndiaTimeSeries, State, ImpParam, District,GovernmentHelpline,TestCenters,ConfirmedTimeSeriesState,RecoveredTimeSeriesState,DeathsTimeSeriesState
from django.http import JsonResponse
import time
import difflib
import json
import os
# Create your views here.
THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class Sitemap(View):
    mytemplate = 'sitemap.xml'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {
            'message':"Success",
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class Bingsitemap(View):
    mytemplate = 'BingSiteAuth.xml'
    unsupported = 'Unsupported operation'
    def get(self, request):

        context = {
            'message':"Success",
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)






class India(View):
    mytemplate = 'india_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request):
        indconfirmed = ImpParam.objects.get(key="indconfirmed").value
        indactive = ImpParam.objects.get(key="indactive").value
        inddeaths = ImpParam.objects.get(key="inddeaths").value
        indrecovered = ImpParam.objects.get(key="indrecovered").value
        inddeltadeaths = ImpParam.objects.get(key="inddeltadeaths").value
        inddeltaconfirmed = ImpParam.objects.get(key="inddeltaconfirmed").value
        inddeltarecovered = ImpParam.objects.get(key="inddeltarecovered").value
        totalindividualtested = ImpParam.objects.get(key="totalindividualtested").value
        totalsampletested = ImpParam.objects.get(key="totalsampletested").value
        lastupdated = ImpParam.objects.get(key="indlastupdatetime").value

        statedata = State.objects.all().filter(confirmed__gte=1).order_by('-confirmed')

        indiatimeseries = IndiaTimeSeries.objects.all()
        last24hr = indiatimeseries[len(indiatimeseries)-1].dailyconfirmed
        indiatimeserieslabel = []
        indiatimeseriesdailydata = []
        inditimeseriescummdata = []
        barcolorlist = []
        statenameslabel = []
        statecasedata=[]
        barcolorlistforstate = []
        for tcs in indiatimeseries:
            indiatimeserieslabel.append(tcs.date)
            indiatimeseriesdailydata.append(tcs.dailyconfirmed)
            # clr = "rgba("+str(int(tcs.dailyconfirmed/255)*10+100)+", 30, 30, 0.2)"
            barcolorlist.append('rgba(255, 99, 132, 8)',)
            inditimeseriescummdata.append(tcs.totalconfirmed)


        mapdatalist = [['State', 'Count']]
        for st in statedata:
            statenameslabel.append(st.name)
            statecasedata.append(st.confirmed)
            mapdatalist.append([st.name,st.confirmed])
            clr = 'rgba('+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+'8';
            barcolorlistforstate.append(clr)


        top5namelabel = []
        top5data = []
        topstate = statedata[0:5]
        top5 = {}
        for tpss in topstate:
            distr = District.objects.all().filter(state=tpss).order_by('-confirmed')
            top5.update({tpss:distr})
            top5namelabel.append(tpss.name)
            top5data.append(tpss.confirmed)

        # for inn in indiatimeseries:
        #     print(inn.date)

        context = {
            'indconfirmed':indconfirmed,
            'indactive':indactive,
            'inddeaths':inddeaths,
            'indrecovered':indrecovered,
            'totalindividualtested':totalindividualtested,
            'totalsampletested':totalsampletested,
            'indiatimeserieslabel':indiatimeserieslabel[-20:],
            'indiatimeseriesdailydata':indiatimeseriesdailydata[-20:],
            'barcolorlist':barcolorlist,
            'inditimeseriescummdata':inditimeseriescummdata[-20:],
            'statenameslabel':statenameslabel,
            'statecasedata':statecasedata,
            'statedata':statedata,
            'top5':top5,
            'mapdatalist':mapdatalist,
            'top5data':top5data,
            'top5namelabel':top5namelabel,
            'barcolorlistforstate':barcolorlistforstate,
            'lastupdated':lastupdated,
            'refresh_message':"No new update",
            'last24hr':last24hr,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)



class StateView(View):
    mytemplate = 'state_status.html'
    unsupported = 'Unsupported operation'
    def get(self, request, statecode):
        lastupdated = ImpParam.objects.get(key="indlastupdatetime").value

        state = State.objects.get(statecode=statecode)
        districts = District.objects.all().filter(state=state).order_by('-confirmed')

        confirmseries = ConfirmedTimeSeriesState.objects.all()
        datelabel = []
        datacumm = []
        datadaily = []
        barcolorlist=[]
        i=0
        callf = (statecode[-2]+statecode[-1]).lower()+"i"
        for cnf in confirmseries:
            datelabel.append(cnf.date)
            datadaily.append(getattr(cnf, callf))
            if(i==0):
                datacumm.append(getattr(cnf, callf))
            else:
                datacumm.append((datacumm[i-1]+getattr(cnf, callf)))
            clr = 'rgba('+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+str(random.randint(1, 10)*25)+','+'0.4';
            barcolorlist.append(clr)
            i = i+1


        context = {
            'state':state,
            'datacumm':datacumm,
            'datadaily':datadaily,
            'datelabel':datelabel,
            'districts':districts,
            'barcolorlist':barcolorlist,
            'lastupdated':lastupdated,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class StateTable(View):

    mytemplate = 'states_table.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        states = State.objects.all().filter(confirmed__gte=1).order_by('-confirmed')
        statedata = {}

        for sta in states:
            distr = District.objects.all().filter(state=sta).order_by('-confirmed')
            statedata.update({sta:distr})
        context = {
            'statedata':statedata,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)


class Helpline(View):
    mytemplate = 'helpline.html'
    unsupported = 'Unsupported operation'
    def get(self, request):

        testcenters = TestCenters.objects.all()
        helplines = GovernmentHelpline.objects.all()

        context = {
            'testcenters':testcenters,
            'helplines':helplines,
        }
        return render(request,self.mytemplate,context)

    def post(self, request):
        return HttpResponse(self.unsupported)





def Update(request):
    my_file = os.path.join(THIS_FOLDER, 'lastupdate.json')
    with open(my_file, 'r') as openfile:
        timefile = json.load(openfile)

    last_update = timefile['lasttime']
    if((last_update+600) > time.time()):
        msg = "Data Fetched less than 10 mins ago."
    else:
        try:
            dataupdate()
            with open('lastupdate.json', 'w') as json_file:
                json.dump({"lasttime": time.time()}, json_file)
            msg = "Data Updated now"
        except Exception as e:
            print(e)
            msg = "Scraping sources..."
    data = {
        "message":msg,
    }
    return JsonResponse(data)



def GetdistrictResult(request):
    exactflag = False
    foundflag = False
    suggestflag = False
    dist_name = ''
    dist_conf = ''
    dist_state = ''
    dist_state_count = ''

    dstnme = request.GET.get('district_name', None)
    dstlist = []
    districts = District.objects.all()
    for dd in districts:
        dstlist.append(dd.name)

    closematches = difflib.get_close_matches(dstnme, dstlist);
    if(len(closematches)>0):
        foundflag = True
        obj = District.objects.all().filter(name=closematches[0])[0]
        dist_name = obj.name
        dist_conf = obj.confirmed
        dist_state = obj.state.name
        dist_state_count = obj.state.confirmed
        if(closematches[0].lower()==dstnme.lower()):
            exactflag = True
        else:
            exactflag = False

    else:
        foundflag = False


    data = {
    'foundflag':foundflag,
    'exactflag':exactflag,
    'dist_name':dist_name,
    'dist_conf':dist_conf,
    'dist_state':dist_state,
    'dist_state_count':dist_state_count
    }
    return JsonResponse(data)
