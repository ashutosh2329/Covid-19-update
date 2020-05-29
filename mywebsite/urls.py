from django.contrib import admin
from django.urls import path,include
from globalRecords import views as gv
from indiaRecords import views as iv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('india/status', iv.India.as_view(),name='india_status_home'),
    path('india/<statecode>/status', iv.StateView.as_view(),name='state_status'),
    path('india/state-table', iv.StateTable.as_view(),name='states_table'),
    path('india/helpline', iv.Helpline.as_view(),name='helpline'),
    path('global/status', gv.Global.as_view(),name='global_status'),
    path('covid19', gv.Covid19.as_view(),name='covid19'),
    path('', iv.India.as_view(),name='india_status'),
    path('ajax/update-data', iv.Update,name='update_status'),
    path('ajax/get-details', iv.GetdistrictResult,name='update_status'),
    path('sitemap.xml', iv.Sitemap.as_view(),name='sitemap'),
    path('BingSiteAuth.xml', iv.Bingsitemap.as_view(),name='sitemap'),


    # path('global/', include('globalRecords.urls')),
    # path('india/', include('indiaRecords.urls'))
    # path('about-covid19', gv.Covid.as_view(),name='about_covid19'),
    # path('', iv.India.as_view(),name='HomePage')
]
