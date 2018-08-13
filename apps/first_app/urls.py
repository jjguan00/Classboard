from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^signup$', views.signup),
	url(r'^signups$', views.signups),
	url(r'^logins$', views.logins),
	url(r'^main$', views.main),
	url(r'^logout$', views.logout),
	url(r'^create_class$', views.create_class),
	url(r'^create_classes$', views.create_classes),
	url(r'^signup_class/(?P<number>\d+)$', views.signup_class),
	url(r'^signup_classes/(?P<number>\d+)$', views.signup_classes),
	url(r'^class/(?P<number>\d+)$', views.classroom),
	url(r'^class/(?P<number>\d+)/post$', views.post),
	url(r'^class/(?P<classnumber>\d+)/(?P<postnumber>\d+)/reply$', views.reply),
	url(r'^dismiss/(?P<classnumber>\d+)/(?P<studentnumber>\d+)$', views.dismiss)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)