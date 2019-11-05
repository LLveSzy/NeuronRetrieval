# coding:utf-8
from home.models import Neuron
import xadmin
from xadmin import views


class MainDashBoard(object):
    widgets = [
        [
            {'type': 'html', 'title': u'Paper 后台管理', 'content': '<h3>欢迎来到<strong>Neuron</strong>后台管理系统</h3>'
                                                                '<p>开发团队：Neuron team</p><p>联系方式：13032863009</p>'
                                                                '<p>联系人：×××</p>'},
        ],
    ]


class BaseSetting(object):
    enable_themes = False
    enable_bootswatch = False


class GlobalSetting(object):
    apps_label_title = {
        'auth': u'权限',
        'home': u'信息管理',
    }
    # site_title = u'NeuronClass'
    # site_footer = u'NeuronClass'
    menu_style = 'default'


xadmin.site.register(Neuron)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.website.IndexView, MainDashBoard)
