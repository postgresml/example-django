from django.shortcuts import render
from django.db.models.expressions import RawSQL
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from todo.models import TodoItem, TodoItemSerializer


class TodoItemViewSet(viewsets.ModelViewSet):
    """TODO items controller."""

    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer

    @action(detail=False, methods=["get"])
    def search(self, request):
        """
        Search the TODO list by embedding similarity.
        """
        query = request.query_params.get("q")
        completed = request.query_params.get("completed")
        limit = request.query_params.get("limit")

        if limit:
            limit = int(limit)

        if completed:
            completed = completed.lower() == "true"
        else:
            completed = False

        if query:
            results = TodoItem.objects.annotate(
                # Use cosine similarty to find closest matches by their linguistic meaning
                similarity=RawSQL(
                    "pgml.embed('intfloat/e5-small', %s)::vector(384) <=> embedding",
                    [query],
                )
            ).order_by("similarity")

            if completed:
                results = results.filter(completed=completed)

            if limit:
                results = results[:limit]

            # If you want to see the query that is executed, uncomment the following line.
            # print(results.query)

            serializer = TodoItemSerializer(results, many=True)
            return Response(serializer.data)
        else:
            return Response([])
