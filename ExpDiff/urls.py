from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('processing.views',
    url(r'^$', 'home', name='home'),
    url(r'^bowtie/$', 'bowtie_form'),
    url(r'^bwa/$', 'bwa_form'),
    url(r'^diffexp/$', 'diffexp_form'),
    url(r'^register/$', 'register_user'),
    url(r'^login/$', 'log_in'),
    url(r'^login/auth/$', 'auth_view'),
    url(r'^logout/$', 'log_out'),
    url(r'^files/$', 'show_files'),
    url(r'^files/upload/$', 'show_fileupload', name='file_upload'),
    url(r'^files/submit/$', 'filesubmit'),
    url(r'^files/success/$', 'upload_success', name='upload_success'),
    url(r'^files/delete/(\d+)/$', 'delete_file'),
    url(r'^files/edit/(\d+)/$', 'show_edit_file', name='show_edit_file'),
    # Examples:
    # url(r'^$', 'ExpDiff.views.home', name='home'),
    # url(r'^ExpDiff/', include('ExpDiff.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
