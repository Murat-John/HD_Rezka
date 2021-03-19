from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Genre, Movie, Comment, Like, Favorite, Rating, History
from main.parsing import pars
from main.permissions import IsAuthorPermission, IsAdminPermission
from main.serializers import GenreSerializer, MovieSerializer, CommentSerializer, LikeSerializer, FavoriteSerializer, \
    RatingSerializer, ParsSerializer, HistorySerializer
from main.utils import add_to_history


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsAuthenticated, IsAdminPermission, ]
        else:
            permissions = [AllowAny, ]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny, ]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            permissions = [IsAuthenticated, IsAdminPermission, ]
        elif self.action == 'retrieve':
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny, ]
        return [permission() for permission in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        add_to_history(object=instance, request=request)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])  # router build path post/search/?q=paris
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request, 'action': self.action})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        rating = int(self.request.query_params.get('rating', 0))
        if rating > 0:
            queryset = queryset.filter(ratings__gte=rating)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorPermission]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class LikeViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class FavoriteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class RatingViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, ]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}


class ParsOcView(APIView):
    def get(self, request):
        dict_ = pars()
        serializer = ParsSerializer(instance=dict_, many=True)
        return Response(serializer.data)


class ViewHistory(APIView):
    def get(self, request):
        user = request.user
        history = History.objects.filter(user=user).order_by('-created')
        serializer = HistorySerializer(instance=history, many=True)
        return Response(serializer.data)


class OverView(APIView):
    pass
