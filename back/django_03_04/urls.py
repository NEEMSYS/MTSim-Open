from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from user.views import RegisterViewSet, UserinfoViewSet, UpdatePwdApi
from scenarios.views import ScenariosViewSet, FilterScenariosViewSet
from game.views import CompetitionViewSet,ParticipantViewSet, SubmitWorksViewSet,userSubmitWorksViewSet,GradesViewset,MyWorksViewset,UserCustomWorksViewset
from game.views import run_container,userrun_container
from django.views.generic import TemplateView
from django.urls import path
from game.views import GenerateScenarioView
router = DefaultRouter()
router.register(r'register', RegisterViewSet)
router.register(r'userinfo', UserinfoViewSet)
router.register(r'scenarios',ScenariosViewSet,basename="scenarios")
router.register(r'filterScenarios',FilterScenariosViewSet, basename="filterScenarios")
router.register(r'submitWorks', SubmitWorksViewSet,basename="submitWorks")
router.register(r'usersubmitWorks', userSubmitWorksViewSet,basename="submitWorks")
router.register(r'grades',GradesViewset,basename="grades")
router.register(r'myWorks',MyWorksViewset)
router.register(r'userWorks', UserCustomWorksViewset)
router.register(r'competition', CompetitionViewSet)
router.register(r'participant', ParticipantViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("user.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('update-pwd/', UpdatePwdApi.as_view()),
    path('jwt-auth/', obtain_jwt_token),
    path("run/",run_container),
    path("userrun/", userrun_container),
    path('generate_scenario/', GenerateScenarioView.as_view(), name='generate_scenario'),
    #path('download_scenario/', DownloadScenarioView.as_view(), name='download_scenario'),
    #测试自定义场景

    re_path('^', include(router.urls))
]
# 上传文件配置
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)