# action decorator to define custom actions for viewsets
from rest_framework.decorators import action
# to return a custom response
from rest_framework.response import Response
# mixin to extract only list view from viewsets
from rest_framework import viewsets, mixins, status
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
        assigned_only = bool(
            # get('assigned_only', 0): 0 overwrites default value of 'None'
            int(self.request.query_params.get('assigned_only', 0))  # 0 or 1
        )  # T/F
        queryset = self.queryset
        if assigned_only:
            # will return recipes that are assigned to the object
            queryset = queryset.filter(recipe__isnull=False)
        # return self.queryset.filter(user=self.request.user).order_by('-name')
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()  # distinct to return unique items only

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

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        # '1,2,3' ---> ['1', '2', '3'], int converts str to int ---> [1, 2, 3]
        return [int(str_id) for str_id in qs.split(',')]

    # default actions - overwritten
    # default queryset returns all recipes - overwrite
    def get_queryset(self):
        """Retrieve the recipes for the authenticated user"""
        # checking for filters
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset
        if tags:
            tag_ids = self._params_to_ints(tags)
            # __ is used when filtering with foreign key of tags
            queryset = queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        # return self.queryset.filter(user=self.request.user)
        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        # for retrieve action: return Detail serializer
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer
        # for all other actions, return default serializer
        return self.serializer_class

    # ModelViewSet takes care of Recipe creation already. We just need to
    # assign it to a user
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)

    # custom action, method: post, detail True for specific recipe
    # path: recipe/{recipe-id}/upload-image
    @action(methods=['POST'], detail=True, url_path='upload-image')
    # pk: recipe id
    def upload_image(self, request, pk=None):
        """Upload an image to a recipe"""
        # get the current recipe object based on id in url
        recipe = self.get_object()
        serializer = self.get_serializer(
            recipe,
            data=request.data
        )

        # check if serializer is valid
        if serializer.is_valid():
            # save recipe serializer
            serializer.save()
            # custom response
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,  # default DRF errors
            status=status.HTTP_400_BAD_REQUEST
        )
