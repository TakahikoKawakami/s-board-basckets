from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SmaregiContract

admin.site.register(User, UserAdmin)


class SmaregiContractAdmin(admin.ModelAdmin):
    list_display = ('id', )
    list_display_links = ('id',)
#    raw_id_fields = ('book',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防）


admin.site.register(SmaregiContract, SmaregiContractAdmin)
