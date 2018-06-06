from django.conf.urls import url
from . import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^$', views.index, name='index'),
    url(r'^correrClasificador/$', views.ajax_parametros_clasificador, name='ajax_clasificador'),
    url(r'^guardarArchivo/$', views.ajax_upload_file, name='ajax_guardarArchivo'),
    url(r'^correrEntrenamiento/$', views.ajax_correr_entrenamiento, name='ajax_correrEntrenamiento')

]