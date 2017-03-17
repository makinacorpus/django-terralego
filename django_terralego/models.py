import json

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djgeojson.fields import GeometryField

from terralego import geodirectory
from django_terralego import conf


class GeoDirectoryMixin(models.Model):
    """
    A model with a corresponding entry in Terralego.

    The entry will be updated at every save.
    You can pass `terralego_commit` at False to force not updating the entry.

    This model is designed to be one-way only. This means that it won't update from terralego automatically.
    If you update the entry from somewhere else, you will have to call `_update_from_terralego_entry` manually.
    """

    terralego_id = models.UUIDField(verbose_name=_('Terralego id'), editable=False, null=True)
    terralego_last_update = models.DateTimeField(_('Terralego last update'), editable=False, null=True)
    terralego_geometry = GeometryField(_('Terralego geometry field'), blank=True, null=True)
    terralego_tags = models.TextField(_('Terralego tags'), blank=True, null=True)  # JSON list of tags

    class Meta:
        abstract = True

    def update_from_terralego_data(self, data):
        """
        Set self.geometry and self.tags with the values in data and cache it.

        :param data: the geojson representing the entry
        """
        self.terralego_id = data['id']
        self.terralego_last_update = timezone.now()
        self.terralego_geometry = data['geometry']
        self.terralego_tags = json.dumps(data['properties']['tags'])

    def _update_tags_with_model(self, tags):
        model_path = '{0}.{1}'.format(self._meta.app_label, self._meta.object_name)
        if tags is None:
            tags = []
        if model_path not in tags:
            # Add the model_path to the tags
            tags.insert(0, model_path)
        elif tags[0] != model_path:
            # The model_path is already there but not in first place
            tags.remove(model_path)
            tags.insert(0, model_path)
        return tags

    def update_from_terralego_entry(self):
        """
        Get the terralego entry related to self.terralego_id and update the instance tags and geometry.
        """
        if self.terralego_id is not None and conf.TERRALEGO.get('ENABLED', True):
            data = geodirectory.get_entry(self.terralego_id)
            self.update_from_terralego_data(data)

    def save_to_terralego(self):
        """
        Create or update the entry in terralego, adding the model_path to the tags if needed.
        """
        tags = self.terralego_tags and json.loads(self.terralego_tags) or None
        self.terralego_tags = self._update_tags_with_model(tags)
        if self.terralego_id is None:
            data = geodirectory.create_entry(self.terralego_geometry, self.terralego_tags)
        else:
            data = geodirectory.update_entry(self.terralego_id, self.terralego_geometry, self.terralego_tags)
        self.update_from_terralego_data(data)

    def save(self, *args, **kwargs):
        terralego_commit = kwargs.pop('terralego_commit', True)
        if terralego_commit and self.terralego_geometry is not None and conf.TERRALEGO.get('ENABLED', True):
            self.save_to_terralego()
        return super(GeoDirectoryMixin, self).save(*args, **kwargs)
