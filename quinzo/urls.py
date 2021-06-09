from quiz import views as quiz_views
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt import views as jwt_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


router = routers.DefaultRouter()
router.register('question', quiz_views.QuestionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('question/by_subject/<int:id>', quiz_views.ByQuestion.as_view(), name='by-question'),
    path('subjects', quiz_views.SubjectViews.as_view(), name='subjects'),
    path('papers', quiz_views.PaperViews.as_view(), name='papers'),
    path('subject/by_paper/<int:paper_id>', quiz_views.SubjectByPaper.as_view(), name='subject-by-papers'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('login', quiz_views.LoginView.as_view(), name='login'),
    # path('logout', quiz_views.LogoutView.as_view(), name='logout'),
    path('signup', quiz_views.CreateUserView.as_view(), name='signup'),
    path('test/<int:test_id>', quiz_views.QuizView.as_view(), name='view-test'),
    path('time', quiz_views.TimeView.as_view(), name='time'),
    path('result', quiz_views.QuizResultView.as_view(), name='quiz-result'),
]

# Url's configuration for static, media, and router url's
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]