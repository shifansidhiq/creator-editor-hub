"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_creator_details_view', views.admin_creator_details_view, name='admin_creator_details_view'),
    path('admin_user_details_view', views.admin_user_details_view, name='admin_user_details_view'),
    
    path('admin_user_report_view', views.admin_user_report_view, name='admin_user_report_view'),
    path('admin_user_report_block', views.admin_user_report_block, name='admin_user_report_block'),

    path('creator_login', views.creator_login_check, name='creator_login'),
    path('creator_logout', views.creator_logout, name='creator_logout'),
    path('creator_home', views.creator_home, name='creator_home'),
    path('creator_details_add', views.creator_details_add, name='creator_details_add'),
    path('creator_changepassword', views.creator_changepassword, name='creator_changepassword'),

    path('creator_portfolio_details_add', views.creator_portfolio_details_add, name='creator_portfolio_details_add'),
    path('creator_portfolio_details_view', views.creator_portfolio_details_view, name='creator_portfolio_details_view'),
    path('creator_portfolio_details_delete', views.creator_portfolio_details_delete, name='creator_portfolio_details_delete'),

    path('creator_portfolio_allratings_view', views.creator_portfolio_allratings_view, name='creator_portfolio_allratings_view'),


    path('creator_transaction_view', views.creator_transaction_view, name='creator_transaction_view'),

    path('creator_user_proposal_view', views.creator_user_proposal_view, name='creator_user_proposal_view'),
    path('creator_user_proposal_reply', views.creator_user_proposal_reply, name='creator_user_proposal_reply'),



    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_portfolio_details_view', views.user_portfolio_details_view, name='user_portfolio_details_view'),
    path('user_portfolio_details_search', views.user_portfolio_details_search, name='user_portfolio_details_search'),

    path('user_creator_details_search', views.user_creator_details_search, name='user_creator_details_search'),
    # path('user_creator_details_view', views.user_creator_details_view, name='user_creator_details_view'),

    path('user_portfolio_rating_add', views.user_portfolio_rating_add, name='user_portfolio_rating_add'),
    path('user_portfolio_allratings_view', views.user_portfolio_allratings_view, name='user_portfolio_allratings_view'),

    path('user_payments_add', views.user_payments_add, name='user_payments_add'),
    path('user_transaction_view', views.user_transaction_view, name='user_transaction_view'),
    path('user_purchased_portfolio_details_view', views.user_purchased_portfolio_details_view, name='user_purchased_portfolio_details_view'),

    path('user_creator_proposal_add', views.user_creator_proposal_add, name='user_creator_proposal_add'),
    path('user_creator_proposal_view', views.user_creator_proposal_view, name='user_creator_proposal_view'),

    path('user_payments_add2', views.user_payments_add2, name='user_payments_add2'),
    path('user_creator_profile_view', views.user_creator_profile_view, name='user_creator_profile_view'),    

    path('user_report_view', views.user_report_view, name='user_report_view'),
    path('user_report_add', views.user_report_add, name='user_report_add'),


]
