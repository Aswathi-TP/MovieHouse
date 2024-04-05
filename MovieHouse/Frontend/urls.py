from django.urls import path
from Frontend import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('homepage/',views.homepage,name="homepage"),
    path('single_movie/<int:m_id>/',views.single_movie,name="single_movie"),
    path('save_review/<int:m_id>/',views.save_review,name="save_review"),


    path('user_logout/',views.user_logout,name="user_logout"),
    path('movie_details/',views.movie_details,name="movie_details"),
    path('filter_data/',views.filter_data,name="filter_data"),
    path('filter_movies/',views.filter_movies,name="filter_movies"),
    path('contact_page/',views.contact_page,name="contact_page"),
    path('save_contact/',views.save_contact,name="save_contact"),
    path('get_movie_details/<int:movie_id>/',views.get_movie_details,name="get_movie_details"),
    path('user_login/',views.user_login,name="user_login"),


    path('home/',views.home,name="home"),
    path('login_signup/',views.login_signup,name="login_signup"),
    path('register/',views.register,name="register"),
    path('UserLogin/',views.UserLogin,name="UserLogin"),
    path('otp_verification/',views.otp_verification,name="otp_verification"),

    path('seat_select/<int:theatre_id>/<int:movie_id>/',views.seat_select,name="seat_select"),
    path('screen_list/',views.screen_list,name="screen_list"),
    path('profile_update/',views.profile_update,name="profile_update"),
    path('movie_checkout/',views.movie_checkout,name="movie_checkout"),
    path('about_page/',views.about_page,name="about_page"),
    path('save_slot/',views.save_slot,name="save_slot"),

    path('save_booking/',views.save_booking,name="save_booking"),
    path('booking_history/',views.booking_history,name="booking_history"),
    path('download_booking_details/<int:booking_id>/download/',views.download_booking_details,name="download_booking_details"),
    path('delete_history/<int:booking_id>/',views.delete_history,name="delete_history"),

    path('search_view/', views.search_view, name="search_view"),

    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="password_reset"),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),name="password_reset_confirm"),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),name="password_reset_complete")





]