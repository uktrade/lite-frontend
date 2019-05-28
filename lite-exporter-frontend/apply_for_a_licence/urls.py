from django.urls import path

from apply_for_a_licence import views

app_name = 'apply_for_a_licence'

urlpatterns = [
    # ex: /
    path('', views.StartApplication.as_view(), name='index'),
    # ex: /start/
    path('start/', views.InitialQuestions.as_view(), name='start'),
    # ex: /<uuid:pk>/overview/
    path('<uuid:pk>/overview/', views.Overview.as_view(), name='overview'),

    # ex: /<uuid:pk>/goods/
    path('<uuid:pk>/goods/', views.DraftGoodsList.as_view(), name='goods'),
    # ex: /<uuid:pk>/goods/add_preexisting/
    path('<uuid:pk>/goods/add_preexisting/', views.GoodsList.as_view(), name='preexisting_good'),
    # ex: /<uuid:pk>/goods/add_preexisting/<uuid:pk>/add/
    path('<uuid:pk>/goods/add_preexisting/<uuid:good_pk>/add/', views.AddPreexistingGood.as_view(),
         name='add_preexisting_good'),

    # ex: /<uuid:pk>/delete/
    path('<uuid:pk>/delete/', views.DeleteApplication.as_view(), name='delete'),

    # ex: /<uuid:pk>/sites
    path('<uuid:pk>/sites', views.Sites.as_view(), name='sites'),
]
