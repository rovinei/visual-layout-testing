from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^forms/$', views.add_images_with_concepts, name='add_images_with_concepts'),
    url(r'^api/v.1/model/create', views.create_model_train, name='ajax_create_model'),
    url(r'^api/v.1/model/concepts/get', views.get_model_concepts, name='ajax_get_model_concepts'),
    url(r'^api/v.1/model/train', views.add_concepts_to_model_train, name='ajax_add_model_concepts'),
    url(r'^api/v.1/prediction', views.make_prediction, name='ajax_make_prediction'),
    url(r'^streaming_content/$', views.streaming_content, name='streaming_content')

]

