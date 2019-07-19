from django.urls import path

from cases import views

app_name = 'cases'
urlpatterns = [
    # ex: /cases/
    path('', views.Cases.as_view(), name='cases'),
    # ex: /cases/<uuid:pk>/
    path('<uuid:pk>/', views.ViewCase.as_view(), name='case'),
    # ex: /cases/<uuid:pk>/manage
    path('<uuid:pk>/manage/', views.ManageCase.as_view(), name='manage'),
    # ex: /cases/<uuid:pk>/decide
    path('<uuid:pk>/decide/', views.DecideCase.as_view(), name='decide'),
    # ex: /cases/<uuid:pk>/deny/
    path('<uuid:pk>/deny/', views.DenyCase.as_view(), name='deny'),
    # ex: /cases/<uuid:pk>/move/
    path('<uuid:pk>/move/', views.MoveCase.as_view(), name='move'),
    # ex: /<uuid:pk>/documents/
    path('<uuid:pk>/documents/', views.Documents.as_view(), name='documents'),
    # ex: /<uuid:pk>/documents/attach/
    path('<uuid:pk>/attach/', views.AttachDocuments.as_view(), name='attach_documents'),
    # ex: /<uuid:pk>/documents/<str:file_id>/
    path('<uuid:pk>/documents/<str:file_pk>/', views.Document.as_view(), name='document'),
]
