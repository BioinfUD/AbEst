from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('processing.views',
	url(r'^upload_file/$', 'upload_file', name="upload_file"),
    url(r'^$', 'core.views.home', name='home'),
    url(r'^upload_success/$', 'core.views.upload_success', name='upload success'),
    url(r'^bowtie/$', 'core.views.bowtie_form'),
    url(r'^bwa/$', 'core.views.bwa_form'),
    url(r'^diffexp/$', 'core.views.diffexp_form'),
    url(r'^register/$', 'core.views.register_user'),
    url(r'^login/$', 'core.views.log_in'),
    # Examples:
    # url(r'^$', 'ExpDiff.views.home', name='home'),
    # url(r'^ExpDiff/', include('ExpDiff.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
