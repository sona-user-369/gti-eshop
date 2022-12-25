from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from home.models import Produit
# from elasticsearch_dsl import connections

# connections.create_connection(hosts=['localhost'], timeout=20)


@registry.register_document
class DocumentProduit(Document):
    class Index:
        name = 'produit'

        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Produit

        fields = [
            'nom',
        ]
