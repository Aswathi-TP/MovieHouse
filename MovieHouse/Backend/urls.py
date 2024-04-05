from django.urls import path
from Backend import views

urlpatterns = [
    path('index_page/',views.index_page,name="index_page"),
    path('add_theatre/',views.add_theatre,name="add_theatre"),
    path('save_theatre/',views.save_theatre,name="save_theatre"),
    path('display_theatre/',views.display_theatre,name="display_theatre"),
    path('edit_theatre/<int:t_id>/',views.edit_theatre,name="edit_theatre"),
    path('update_theatre/<int:t_id>/',views.update_theatre,name="update_theatre"),
    path('delete_theatre/<int:t_id>/',views.delete_theatre,name="delete_theatre"),

    path('add_screen/',views.add_screen,name="add_screen"),
    path('save_screen/',views.save_screen,name="save_screen"),
    path('display_screen/',views.display_screen,name="display_screen"),
    path('edit_screen/<int:s_id>/',views.edit_screen,name="edit_screen"),
    path('update_screen/<int:s_id>/',views.update_screen,name="update_screen"),
    path('delete_screen/<int:s_id>/',views.delete_screen,name="delete_screen"),

    path('add_movies/',views.add_movies,name="add_movies"),
    path('save_movie/',views.save_movie,name="save_movie"),
    path('display_movies/',views.display_movies,name="display_movies"),
    path('edit_movie/<int:m_id>/',views.edit_movie,name="edit_movie"),
    path('update_movie/<int:m_id>/',views.update_movie,name="update_movie"),
    path('delete_movie/<int:m_id>/',views.delete_movie,name="delete_movie"),

    path('add_cast/',views.add_cast,name="add_cast"),
    path('save_cast_crew/',views.save_cast_crew,name="save_cast_crew"),
    path('display_cast_crew/',views.display_cast_crew,name="display_cast_crew"),
    path('edit_cast_crew/<int:c_id>/',views.edit_cast_crew,name="edit_cast_crew"),
    path('update_cast_crew/<int:c_id>/',views.update_cast_crew,name="update_cast_crew"),
    path('delete_cast_crew/<int:c_id>/',views.delete_cast_crew,name="delete_cast_crew"),

    path('add_show/',views.add_show,name="add_show"),
    path('save_show/',views.save_show,name="save_show"),
    path('display_show/',views.display_show,name="display_show"),
    path('edit_show/<int:s_id>/',views.edit_show,name="edit_show"),
    path('update_show/<int:s_id>/',views.update_show,name="update_show"),
    path('delete_show/<int:s_id>/',views.delete_show,name="delete_show"),
    path('add_seat/',views.add_seat,name="add_seat"),
    path('save_seat/',views.save_seat,name="save_seat"),
    path('display_seat/',views.display_seat,name="display_seat"),
    path('edit_seat/<int:s_id>/',views.edit_seat,name="edit_seat"),
    path('update_seat/<int:s_id>/',views.update_seat,name="update_seat"),
    path('delete_seat/<int:s_id>/',views.delete_seat,name="delete_seat"),

    path('admin_login_page/',views.admin_login_page,name="admin_login_page"),
    path('adminlogin/',views.adminlogin,name="adminlogin"),
    path('adminlogout/',views.adminlogout,name="adminlogout"),
    path('display_contact/',views.display_contact,name="display_contact"),
    path('delete_contact/<int:c_id>/',views.delete_contact,name="delete_contact"),
    path('display_user/',views.display_user,name="display_user"),
    path('display_booking/',views.display_booking,name="display_booking"),

]