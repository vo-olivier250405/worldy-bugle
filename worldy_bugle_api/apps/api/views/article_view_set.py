from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.api.filters import ArticleFilter
from apps.api.permissions import ReadOnly
from apps.api.serializers import ArticleLiteSerializer, ArticleSerializer
from apps.api.views.pagination_view_set import BaseViewSetPagination
from apps.articles.models import Article


class ArticleViewSet(ReadOnlyModelViewSet):
    pagination_class = BaseViewSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [ReadOnly]
    filterset_class = ArticleFilter

    def get_serializer_class(self):
        serializers_by_actions = {
            "list": ArticleLiteSerializer,
            "retrieve": ArticleSerializer,
        }

        return serializers_by_actions.get(self.action, ArticleSerializer)

    def get_queryset(self):
        queryset = (
            Article.objects.filter(url__isnull=False)
            .order_by("-published_at")
            .distinct()
        )
        return queryset
