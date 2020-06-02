from django.urls import path, include
# DefaultRouter automatically creates all urls for a viewset
from rest_framework.routers import DefaultRouter

from recipe import views

# create default router
router = DefaultRouter()
# register viewset
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('recipes', views.RecipeViewSet)

# app name for look up by reverse
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
