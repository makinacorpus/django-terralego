from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from terralego import geodirectory


class GeoDirectoryMixin(models.Model):
    terralego_id = models.UUIDField(verbose_name=_('Terralego id'), editable=False)

    class Meta:
        abstract = True

    _terralego_update_required = False

    def _get_cache_key(self):
        return 'terralego-geodirectory-{entry_id}'.format(entry_id=self.terralego_id)

    def _get_terralego_entry(self):
        key = self._get_cache_key()
        data = cache.get(key)
        if data is None:
            data = geodirectory.get_entry(self.terralego_id)
            # FIXME Handle HttpError
            cache.set(key, data, 3600)
        return data

    _geometry = None

    @property
    def geometry(self):
        if self._geometry is None:
            self._geometry = self._get_terralego_entry()['geometry']
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry
        self._terralego_update_required = True

    _tags = None

    @property
    def tags(self):
        if self._tags is None:
            self._tags = self._get_terralego_entry()['properties']['tags']
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags
        self._terralego_update_required = True

    def save(self, *args, **kwargs):
        if self._terralego_update_required:
            if self.terralego_id is None:
                data = geodirectory.create_entry(self.geometry, self.tags)
                self.terralego_id = data['id']
                cache.set(self._get_cache_key(), data, 3600)
            else:
                geodirectory.update_entry(self.terralego_id, self.geometry, self.tags)
            self._terralego_update_required = False
        return super(GeoDirectoryMixin, self).save(*args, **kwargs)
