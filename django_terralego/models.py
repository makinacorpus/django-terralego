from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from terralego import geodirectory


class GeoDirectoryMixin(models.Model):
    terralego_id = models.UUIDField(verbose_name=_('Terralego id'), editable=False, null=True)

    class Meta:
        abstract = True

    _terralego_update_required = False

    def _get_cache_key(self):
        return 'terralego-geodirectory-{entry_id}'.format(entry_id=self.terralego_id)

    def _get_terralego_entry(self):
        """
        Get the terralego entry related to self.terralego_id and update the instance tags and geometry.

        :return: The geojson representing the entry.
        """
        key = self._get_cache_key()
        data = cache.get(key)
        if data is None:
            data = geodirectory.get_entry(self.terralego_id)
            self._update_from_terralego_data(data)
        return data

    def _update_from_terralego_data(self, data):
        """
        Set self.geometry and self.tags with the values in data and cache it.

        :param data: the geojson representing the entry
        """
        self.terralego_id = data['id']
        self._geometry = data['geometry']
        self._tags = data['properties']['tags']
        cache.set(self._get_cache_key(), data, 3600)

    def _save_to_terralego(self):
        """
        Create or update the entry in terralego, adding the model_path to the tags if needed.
        """
        model_path = '{0}.{1}'.format(self._meta.app_label, self._meta.object_name)
        if self.tags is None:
            self.tags = []
        if model_path not in self.tags:
            # Add the model_path to the tags
            tags = self.tags
            tags.insert(0, model_path)
            self.tags = tags
        elif self.tags[0] != model_path:
            # The model_path is already there but not in first place
            tags = self.tags
            tags.remove(model_path)
            tags.insert(0, model_path)
            self.tags = tags
        if self.terralego_id is None:
            data = geodirectory.create_entry(self.geometry, self.tags)
        else:
            data = geodirectory.update_entry(self.terralego_id, self.geometry, self.tags)
        self._update_from_terralego_data(data)
        self._terralego_update_required = False

    _geometry = None

    @property
    def geometry(self):
        if self._geometry is None and self.terralego_id is not None:
            self._get_terralego_entry()
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        self._geometry = geometry
        self._terralego_update_required = True

    _tags = None

    @property
    def tags(self):
        if self._tags is None and self.terralego_id is not None:
            self._get_terralego_entry()
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags
        self._terralego_update_required = True

    def save(self, *args, **kwargs):
        if self._terralego_update_required:
            self._save_to_terralego()
        return super(GeoDirectoryMixin, self).save(*args, **kwargs)
