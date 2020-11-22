from . import views
from django.urls import path

app_name = "users"

urlpatterns = [
    # 書籍
    # path('login/', views.book_list, name='book_list'),   # 一覧
    # path('logout/', views.book_edit, name='book_add'),  # 登録
    # path('register/', views.book_edit, name='book_mod'),  # 修正
    path('getSmaregiAccessToken/', views.getSmaregiAccessToken, name='get_smaregi_access_token'),
    path('login/', views.Login.as_view(), name='login'), # ログイン
    path('authorize/', views.Authorize.as_view(), name='auth'), # smaregi developer への認証
    # path('sign_up/smaregi/', views.SignUp.as_view(), name='sign_up_smaregi'), # スマレジからの購入通知用
    path('sign_up/smaregi/', views.sign_up, name='sign_up_smaregi'), # スマレジからの購入通知用
]
