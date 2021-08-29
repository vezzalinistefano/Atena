from django.urls import path

from shop.views import CourseDetail, CourseList, CourseCreate, CourseUpdate, CourseDelete, CoursePurchase, SearchView

app_name = 'shop'

urlpatterns = [
    path('course/create', CourseCreate.as_view(), name='course-create'),
    path('course/<int:pk>/<int:teacher_id>/update', CourseUpdate.as_view(), name='course-update'),
    path('course/<int:pk>/<int:teacher_id>/delete', CourseDelete.as_view(), name='course-delete'),
    path('course/<int:pk>/detail', CourseDetail.as_view(), name='course-detail'),
    path('course/list', CourseList.as_view(), name='course-list'),
    path('course/<int:pk>/purchase', CoursePurchase.as_view(), name='course-purchase'),
    path('results/', SearchView.as_view(), name='search-results'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
