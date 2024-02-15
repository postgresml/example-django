from django.db import models
from pgvector.django import VectorField, HnswIndex

from rest_framework import serializers


class EmbedSmallExpression(models.Expression):
    """
    An expression to automatically embed any text column in the same table.
    """

    output_field = VectorField(null=False, blank=True, dimensions=384)

    def __init__(self, field):
        self.embedding_field = field

    def as_sql(self, compiler, connection, template=None):
        return f"pgml.embed('intfloat/e5-small', {self.embedding_field})", None


class TodoItem(models.Model):
    """
    TODO item.
    """

    description = models.CharField(max_length=256)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    embedding = models.GeneratedField(
        expression=EmbedSmallExpression("description"),
        output_field=VectorField(null=False, blank=False, dimensions=384),
        db_persist=True,
    )

    def __str__(self):
        return self.description

    class Meta:
        indexes = [
            # Adding an HNSW index on the embedding column
            # allows approximate nearest neighbor searches on datasets
            # that are so large that the exact search would be too slow.
            #
            # The trade-off here is the results are approximate and
            # may miss some of the nearest neighbors.
            HnswIndex(
                name="todoitem_embedding_hnsw_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]


class TodoItemSerializer(serializers.ModelSerializer):
    """
    TODO item serializer used by the Django Rest Framework.
    """

    class Meta:
        model = TodoItem
        fields = ["id", "description", "due_date", "completed", "embedding"]
