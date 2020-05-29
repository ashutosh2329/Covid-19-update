from django.contrib import admin
from .models import State, District, ImpParam, IndiaTimeSeries, DeathsTimeSeriesState, RecoveredTimeSeriesState, ConfirmedTimeSeriesState, GovernmentHelpline, TestCenters
# Register your models here.


admin.site.register(State)
admin.site.register(ImpParam)
admin.site.register(IndiaTimeSeries)
admin.site.register(District)

admin.site.register(DeathsTimeSeriesState)
admin.site.register(RecoveredTimeSeriesState)
admin.site.register(ConfirmedTimeSeriesState)
admin.site.register(GovernmentHelpline)
admin.site.register(TestCenters)
