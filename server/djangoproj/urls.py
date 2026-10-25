from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

spa = TemplateView.as_view(template_name='index.html')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('about', TemplateView.as_view(template_name='About.html')),
    path('contact', TemplateView.as_view(template_name='Contact.html')),
    path('login', spa),
    path('register', spa),
    path('dealers', spa),
    path('dealer/<int:dealer_id>', spa),
    path('postreview/<int:dealer_id>', spa),
    path('', spa),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
