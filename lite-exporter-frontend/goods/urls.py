from django.urls import path

from goods import views

app_name = "goods"
urlpatterns = [
    # ex: /goods/
    path("", views.Goods.as_view(), name="goods"),
    # ex: /goods/add/
    path("add/", views.AddGood.as_view(), name="add"),
    # ex: /goods/edit/<uuid:pk>/ - Edit a specific good
    path("edit/<uuid:pk>/", views.EditGood.as_view(), name="edit"),
    # ex: /goods/delete/<uuid:pk>/ - Delete a specific good
    path("delete/<uuid:pk>/", views.DeleteGood.as_view(), name="delete"),
    # ex: /goods/<uuid:pk>/documents/<uuid:file_pk>/ - Get specific document
    path("<uuid:pk>/documents/<uuid:file_pk>/", views.Document.as_view(), name="document"),
    # ex: /goods/<uuid:pk>/documents/<uuid:file_pk>/delete/ - Delete a document
    path("<uuid:pk>/documents/<uuid:file_pk>/delete/", views.DeleteDocument.as_view(), name="delete_document"),
    # ex: /goods/<uuid:pk>/attach/ - Attach a document to a good
    path("<uuid:pk>/attach/", views.AttachDocuments.as_view(), name="attach_documents"),
    # ex: /goods/<uuid:pk>/raise-clc-query/ - Raise a clc query
    path("<uuid:pk>/raise-clc-query/", views.RaiseCLCQuery.as_view(), name="raise_clc_query"),
    # ex: /goods/43a88949-5db9-4334-b0cc-044e91827451
    path("<uuid:pk>", views.GoodsDetailEmpty.as_view(), name="good"),
    # ex: /goods/43a88949-5db9-4334-b0cc-044e91827451/case-notes/
    path("<uuid:pk>/<str:type>/", views.GoodsDetail.as_view(), name="good_detail"),
    # ex: /goods/43a88949-5db9-4334-b0cc-044e91827451/ecju-queries/43a88949-5db9-4334-b0cc-044e91827451
    path("<uuid:pk>/ecju-queries/<uuid:query_pk>/", views.RespondToQuery.as_view(), name="respond_to_query"),
]
