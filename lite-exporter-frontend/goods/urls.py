from django.urls import path

from goods import views

app_name = "goods"
urlpatterns = [
    path("", views.Goods.as_view(), name="goods"),
    path("add/", views.AddGood.as_view(), name="add"),
    path("<uuid:pk>/edit/", views.EditGood.as_view(), name="edit"),
    path("<uuid:pk>/delete/", views.DeleteGood.as_view(), name="delete"),
    path("<uuid:pk>/add-document/", views.CheckDocumentGrading.as_view(), name="add_document"),
    path("<uuid:pk>/documents/<uuid:file_pk>/", views.Document.as_view(), name="document"),
    path("<uuid:pk>/documents/<uuid:file_pk>/delete/", views.DeleteDocument.as_view(), name="delete_document"),
    path("<uuid:pk>/attach/", views.AttachDocuments.as_view(), name="attach_documents"),
    path("<uuid:pk>/raise-good-query/", views.RaiseGoodsQuery.as_view(), name="raise_goods_query"),
    path("<uuid:pk>", views.GoodsDetailEmpty.as_view(), name="good"),
    path("<uuid:pk>/<str:type>/", views.GoodsDetail.as_view(), name="good_detail"),
    path("<uuid:pk>/ecju-queries/<uuid:query_pk>/", views.RespondToQuery.as_view(), name="respond_to_query"),
]
