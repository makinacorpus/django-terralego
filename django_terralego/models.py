import json
import logging

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djgeojson.fields import GeometryField
from requests import HTTPError, RequestException

from terralego import geodirectory
from django_terralego import conf
from django_terralego.utils import convert_geodirectory_entry_to_model_instance

logger = logging.getLogger(__name__)


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

    # Save/update handling

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
        tags = self._update_tags_with_model(tags)
        self.terralego_tags = json.dumps(tags)  # Save tags in case of error before the update_from_terralego_data
        if self.terralego_id is None:
            data = geodirectory.create_entry(self.terralego_geometry, tags)
        else:
            data = geodirectory.update_entry(self.terralego_id, self.terralego_geometry, tags)
        self.update_from_terralego_data(data)

    def delete_from_terralego(self, set_id_null=True):
        """
        Delete the entry in terralego
        """
        geodirectory.delete_entry(self.terralego_id)
        if set_id_null:
            self.terralego_id = None
            self.save(terralego_commit=False)

    def delete(self, *args, **kwargs):
        if self.terralego_id:
            try:
                self.delete_from_terralego(set_id_null=False)
            except RequestException as e:
                logger.error('Error while deleting from terralego: {0}'.format(e))
        return super(GeoDirectoryMixin, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        terralego_commit = kwargs.pop('terralego_commit', True)
        if terralego_commit and self.terralego_geometry is not None and conf.TERRALEGO.get('ENABLED', True):
            try:
                self.save_to_terralego()
            except RequestException as e:
                logger.error('Error while saving to terralego: {0}'.format(e))
        return super(GeoDirectoryMixin, self).save(*args, **kwargs)

    # Geodirectory methods

    def closest(self, tags=None):
        """
        Get the closest entry of this entry.
        
        :param tags: Optional. A list of tags to filter the entries on which the request is made.
        :return: An instance of GeoDirectoryMixin if the entry is one, or a dict describing the entry.
        """
        try:
            entry = geodirectory.closest(self.terralego_id, tags)
        except RequestException as e:
            return logger.error('Error while getting closest: {0}'.format(e))
        return convert_geodirectory_entry_to_model_instance(entry)
