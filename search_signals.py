from haystack.signals import BaseSignalProcessor
from haystack.exceptions import NotHandled
from elasticsearch import TransportError
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend, ElasticsearchSearchEngine

from .models import *



import logging

logger = logging.getLogger(__name__)


class RobustElasticSearchBackend(ElasticsearchSearchBackend):
    """A robust backend that doesn't crash when no connection is available"""

    def mute_error(f):
        def error_wrapper(self, *args, **kwargs):
            try:
                return f(self, *args, **kwargs)
            except TransportError:
                logger.error("Elastic search is not running ! index is outdated")
            except Exception as e:
                logger.error("Elastic search issue" + str(e))
        return error_wrapper

    def __init__(self, connectionalias, **options):
        super(RobustElasticSearchBackend, self).__init__(connectionalias, **options)

    @mute_error
    def update(self, indexer, iterable, commit=True):
        super(RobustElasticSearchBackend, self).update(indexer, iterable, commit)

    @mute_error
    def remove(self, obj, commit=True):
        super(RobustElasticSearchBackend, self).remove(obj, commit)

    @mute_error
    def clear(self, models=[], commit=True):
        super(RobustElasticSearchBackend, self).clear(models, commit)


class RobustElasticSearchEngine(ElasticsearchSearchEngine):
    backend = RobustElasticSearchBackend


class CustomRealtimeSignalProcessor(BaseSignalProcessor):
    """
    Allows for observing when saves/deletes fire & automatically updates the
    search engine appropriately.
    """
    def setup(self):
        # Naive (listen to all model saves).
        models.signals.post_save.connect(self.handle_save)
        models.signals.post_delete.connect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then hooking up signals only for those.

    def teardown(self):
        # Naive (listen to all model saves).
        models.signals.post_save.disconnect(self.handle_save)
        models.signals.post_delete.disconnect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then disconnecting signals only for those.

    def handle_save(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance=instance)
        delete_object = False
        if sender == Flat:
            if instance.is_deleted:
                delete_object = True


        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                if delete_object:
                    index.remove_object(instance, using=using)
                else:
                    index.update_object(instance, using=using)
            except NotHandled:
                logger.info("Elastic search issue1")
            except Exception as e:
                logger.error("Elastic search issue2" + str(e))
