from django.contrib import admin
from corona_app.models import region, comuna, reportes, reportexcomuna, activesCase, deathsporRegion

# Register your models here.
@admin.register(region)
class regionAdmin(admin.ModelAdmin):
    list_display = ('Codregion', 'RegionName', 'Area', 'Lat', 'Long', 'Population')

@admin.register(comuna)
class comunaAdmin(admin.ModelAdmin):
    list_display = ('CodComuna', 'Reg', 'ComunaName', 'Poblation')

@admin.register(reportes)
class reportesAdmin(admin.ModelAdmin):
    list_display = ('RDate','RComuna','RConfirmed','RActive')

@admin.register(reportexcomuna)
class repoComunaAdmin(admin.ModelAdmin):
    list_display = ('region', 'cod_region','comunaCodComuna','comuna', 'poblacion')

@admin.register(activesCase)
class activesCaseAdmin(admin.ModelAdmin):
    list_display = ('AcCod_comuna', 'AcDate','AcCantidad')


@admin.register(deathsporRegion)
class deathsporRegionAdmin(admin.ModelAdmin):
    list_display = ('DDate', 'DCodRegion','Ddeaths')


    