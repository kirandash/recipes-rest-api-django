# mixin to extract only list view from viewsets
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Ingredient, Recipe

from recipe import serializers


class BaseRecipeViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # default queryset returns all objects - overwrite
    def get_queryset(self):
        """Return objects for current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    # overwrite the default create method to assign object to a user
    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


# mixins.ListModelMixin is to make sure that only list view is created
# class TagViewSet(viewsets.GenericViewSet,
#                 mixins.ListModelMixin,
#                 mixins.CreateModelMixin):

class TagViewSet(BaseRecipeViewSet):
    """Manage tags in the database"""
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # default queryset returns all tags - overwrite
    # def get_queryset(self):
    #     """Return objects for current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')
    #
    # # overwrite the default create method to assign tag to a user
    # def perform_create(self, serializer):
    #     """Create a new tag"""
    #     serializer.save(user=self.request.user)


# class IngredientViewSet(viewsets.GenericViewSet,
#                         mixins.ListModelMixin,
#                         mixins.CreateModelMixin):
class IngredientViewSet(BaseRecipeViewSet):
    """Manage ingredients in the database"""
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer

    # default queryset returns all ingredients - overwrite
    # def get_queryset(self):
    #     """Return objects for current authenticated user only"""
    #     return self.queryset.filter(user=self.request.user).order_by('-name')
    #
    # # overwrite the default create method to assign tag to a user
    # def perform_create(self, serializer):
    #     """Create a new ingredient"""
    #     serializer.save(user=self.request.user)


# ModelViewSet: creates all endpoints: CRUD
class RecipeViewSet(viewsets.ModelViewSet):
    """Manage Recipes in the DB"""
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # default queryset returns all recipes - overwrite
    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # for retrieve action: return Detail serializer
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        # for all other actions, return default serializer
        return self.serializer_class
