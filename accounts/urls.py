from . import views
from django.urls import path

app_name = "users"

urlpatterns = [
    # 書籍
    # path('login/', views.book_list, name='book_list'),   # 一覧
    # path('logout/', views.book_edit, name='book_add'),  # 登録
    # path('register/', views.book_edit, name='book_mod'),  # 修正
    path('getSmaregiAccessToken/', views.getSmaregiAccessToken, name='get_smaregi_access_token'),   # 削除
    path('loginBata/', views.LoginBata.as_view(), name='login_bata'),   # ログインβ
    path('login/', views.login, name='login'),
]
