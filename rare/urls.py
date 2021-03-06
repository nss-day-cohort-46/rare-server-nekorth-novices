"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rareapi.views import CategoryViewSet, CommentViewSet, TagViewSet, ReactionViewSet, PostReactionViewSet
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from rareapi.views import register_user, login_user, check_active, PostViewSet, RareUserViewSet, change_active, change_rank
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', PostViewSet, 'post')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'comments', CommentViewSet, 'comment')
router.register(r'tags', TagViewSet, 'tag')
router.register(r'reactions', ReactionViewSet, 'reaction')
router.register(r'postreactions', PostReactionViewSet, 'postreaction')
router.register(r'users', RareUserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('check-active', check_active),
    path('change-active', change_active),
    path('change-rank', change_rank),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
