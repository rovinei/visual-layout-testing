from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.projects_list, name='automate_index'),
    url(r'^project/(?P<project_uuid>\w+)', views.get_project, name='get_project'),
    url(r'^cross-browser/(?P<project_uuid>\w+)', views.CrossBrowserTestAPI.as_view(), name='cross_browser_test'),
    url(r'^screenshot/(?P<project_uuid>\w+)', views.ScreenshotJobAPI.as_view(), name='automate_screenshot'),

    url(r'^ajax/visual_testing', views.CrossBrowserTestAPI.as_view(), name="ajax_visual_testing"),
    url(r'^ajax/project_view', views.ProjectAjaxView.as_view(), name="ajax_choose_project"),
    # url(r'^report/(?P<report_uuid>\w+)/', views.ReportView.as_view(), name='report_detail_root'),
    url(r'^report/(?P<path>.*\..*)$', views.get_detail_report, name='report_detail'),
    # url(r'^report/(?P<report_uuid>\w+)/(?P<path>.*)$', views.serve_report_static),
    # url(r'^report/(?P<path>.*)$', serve, {'document_root': settings.GALEN_REPORT_DIR}),
]