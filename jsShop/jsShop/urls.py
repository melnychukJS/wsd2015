"""jsShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from webshop import views
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^developer', views.developer),
    url(r'^home',views.home),
    url(r'^user',views.user),
    url(r'^add-game',views.add_game),
	url(r'', include('webshop.urls')),
	url(r'^game/(?P<id>[0-9])/$',views.game),
	url(r'^play/(?P<id>[0-9])',views.play),
	url(r'^del-game/(?P<id>[0-9])/$',views.remove_game),
	url(r'^edit-game/(?P<id>[0-9])/$',views.edit_game),
	url(r'^edit-profile',views.edit_user_profile),
	#url(r'^gamesales/(?P<id>[0-9])/$', views.gameSales),
	url(r'^games/sales/$', views.gameSales),
	url(r'^pay/(?P<id>[0-9])/$', views.pay),
	url(r'^pay/(?P<id>[0-9])/success' , views.handle_pay),
	url(r'^pay/(?P<id>[0-9])/cancel', views.cancel_pay),
	url(r'^savedState/(?P<id>[0-9])', views.savedState),
]
