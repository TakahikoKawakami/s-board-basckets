from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from .models import Book
from .forms import *
import base64
import requests
from urllib.parse import urlencode
import json

def book_list(request):
    """書籍の一覧"""
    # return HttpResponse('書籍の一覧')
    books = Book.objects.all().order_by('id')

    return render(request,
                  's_board_relations/book_list.html',     # 使用するテンプレート
                  {'books': books})         # テンプレートに渡すデータ


def book_edit(request, book_id=None):
    """書籍の編集"""
    # return HttpResponse('書籍の編集')
    if book_id:   # book_id が指定されている (修正時)
        book = get_object_or_404(Book, pk=book_id)
    else:         # book_id が指定されていない (追加時)
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # POST された request データからフォームを作成
        if form.is_valid():    # フォームのバリデーション
            book = form.save(commit=False)
            book.save()
            return redirect('s_board_relations:book_list')
    else:    # GET の時
        form = BookForm(instance=book)  # book インスタンスからフォームを作成

    return render(request, 's_board_relations/book_edit.html', dict(form=form, book_id=book_id))


def book_del(request, book_id):
    """書籍の削除"""
    # return HttpResponse('書籍の削除')
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect('s_board_relations:book_list')


def network(request):
    """network"""
    url = 'https://id.smaregi.dev/app/sb_skc130x6/token'
    smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
    smaregiClientSecret = getattr(settings, "SMAREGI_CLIENT_SECRET", None)
    base = base64.b64encode((smaregiClientId+":"+smaregiClientSecret).encode())
    smaregiAuth = "Basic " + str(base).split("'")[1]
    
    headers = {
        'Authorization': smaregiAuth,
        'Content-Type':	'application/x-www-form-urlencoded',        
    }
    body = {
        'grant_type':'client_credentials',
        'scope': ''
    }
    encodedBody = urlencode(body)
    r_post = requests.post(url, headers=headers, data=urlencode(body))
    r_post = r_post.json()
#    return HttpResponse(r_post["access_token"])
    return render(request, 's_board_relations/network.html')
