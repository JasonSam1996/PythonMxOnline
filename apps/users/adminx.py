import xadmin
from xadmin import views
from .models import UserProfile, EmailCode, Banner


class UserProfileAdmin(object):
    pass


class EmailCodeAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerCode(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = 'accordion'


# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailCode, EmailCodeAdmin)
xadmin.site.register(Banner, BannerCode)

# 设置主题
xadmin.site.register(views.BaseAdminView, BaseSetting)
# 设置标题和页脚
xadmin.site.register(views.CommAdminView, GlobalSettings)
