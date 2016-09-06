from haystack import indexes


from . import models


class FlatIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='message')

    def get_model(self):
        return models.Flat

    def index_queryset(self, using=None):
        return self.get_model().objects.all()