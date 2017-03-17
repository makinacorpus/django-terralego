Geodirectory
============

Django Terralego provides a mixin you can add to your models to enable the geodirectory. Each model will have
a geometry field which will be automatically updated to terralego after each save.

.. autoclass:: django_terralego.models.GeoDirectoryMixin
    :members:

You can use django-leaflet to add a map widget. For example for the admin site::

    from leaflet.admin import LeafletGeoAdmin

    class MyModelAdmin(LeafletGeoAdmin):
        fields = ('terralego_geometry')
        map_width = '500px'
