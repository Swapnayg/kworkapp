from django.urls import include, path
from . import views
from . views import indexView,aboutView,privacyView,resolution_view,blocked_view,payments_view,buyer_review_view,seller_review_view,warning_review_view,requirements_p_view,requirements_f_view,offers_view,search_gig_view,search_profile_view,manage_gigs_view,seller_manage_orders_view,earnings_view,gig_View_View,order_activities_view,buyer_request_view,buyer_manage_orders_view,seller_manage_orders_view,favourites_view,inbox_view,billing_view,post_request_view,Manage_request_view,seller_main_view,create_gig_view,menu_pageView,all_gigs_pageView,signup_view,account_settings_view,dashboard_view,buyer_dashboard_view,login_view,profile_view,partners_View,approval_process_View,buyer_protectionView,faq_View,contact_support_View,prohibited_service_View,term_serviceView,for_freelancerView,reviews_View,earn_letorkbdoneView,categoriesView,affiliate_programView
urlpatterns  = [
	path('', indexView.as_view(), name='index' ),
	path('about', aboutView.as_view(), name='about' ),
	path('privacy', privacyView.as_view(), name='privacy' ),
	path('buyer_protection', buyer_protectionView.as_view(), name='buyer_protection' ),
 	path('buyer_reviews/<str:order_no>', buyer_review_view.as_view(), name='buyer_reviews' ),
  	path('seller_reviews/<str:order_no>', seller_review_view.as_view(), name='seller_reviews' ),
    path('warning/<str:username>', warning_review_view.as_view(), name='warning' ),
    path('blocked/<str:username>', blocked_view.as_view(), name='blocked' ),
	path("user/<str:username>/seller_dashboard",seller_main_view.as_view(),name = 'seller_main'),
 	path("seller",seller_main_view.as_view(),name = 'seller'),
	path('user/<str:username>/manage_request', Manage_request_view.as_view(), name='manage_request' ),
	path('user/<str:username>/post_request', post_request_view.as_view(), name='post_request' ),
	path('gigs/<str:username>/<str:gig_title>', gig_View_View.as_view(), name='gig_view'),
	path('buyer_request', buyer_request_view.as_view(), name='buyer_request' ),
 	path('payments/<str:req_id>/<str:offer_id>', payments_view.as_view(), name='payments' ),
	path('user/<str:username>/manage_gigs', manage_gigs_view.as_view(), name='manage_gigs' ),
	path('user/<str:username>/balance', earnings_view.as_view(), name='balance'),
 	path('user/<str:username>/manage_orders/<str:orderid>/resolution', resolution_view.as_view(), name='resolution'),
	path('user/<str:username>/manage_orders/<str:orderid>/activities', order_activities_view.as_view(), name='activities'),
	path('billing', billing_view.as_view(), name='billing' ),
	path('manage_orders', buyer_manage_orders_view.as_view(), name='manage_orders' ),
	path('inbox', inbox_view.as_view(), name='inbox' ),
 	path('inbox/<str:username>/', inbox_view.as_view(), name='inbox' ),
	path('favourites', favourites_view.as_view(), name='favourites' ),
	path('term_service', term_serviceView.as_view(), name='term_service' ),
	path('for_freelancer', for_freelancerView.as_view(), name='for_freelancer' ),
	path('earn_letworkbdone', earn_letorkbdoneView.as_view(), name='earn_letworkbdone' ),
	path('categories', categoriesView.as_view(), name='categories' ),
	path('affiliate_program', affiliate_programView.as_view(), name='affiliate_program' ),
	path('reviews', reviews_View.as_view(), name='reviews' ),
	path('prohibited_service', prohibited_service_View.as_view(), name='prohibited_service' ),
	path('faq', faq_View.as_view(), name='faq' ),
	path('contact_support', contact_support_View.as_view(), name='contact_support' ),
	path('approval_process', approval_process_View.as_view(), name='approval_process' ),
	path('partners', partners_View.as_view(), name='partners' ),
	path("save_content/",views.save_content_view,name = 'save_content'),
	path("image_upload/",views.Imgupload_view,name = 'image_upload'),
	path("get_menus/",views.get_menus_view,name = 'get_menus'),
	path("get_menus_data/",views.get_menus_data_view,name = 'get_menus_data'),
	path("post_contact_support/",views.post_contact_support_view,name = 'post_contact_support'),
	path("get_articles/",views.get_articles_view,name = 'get_articles'),
	path("get_all_categories/",views.get_all_categories_view,name = 'get_all_categories'),
	path("get_sub_categories/",views.get_sub_categories_view,name = 'get_sub_categories'),
	path("subcategories_for_category/",views.subcategories_for_category_view,name = 'subcategories_for_category'),
	path("post_increase_count/",views.post_increase_count_view,name = 'post_increase_count'),
	path("register",signup_view.as_view(),name = 'register'),
 	path("ref/<str:username>",signup_view.as_view(),name = 'reference'),
	path("login",login_view.as_view(),name = 'login'),
	path("user/profile/<str:username>",profile_view.as_view(),name = 'profile'),
 	path("search/<str:keyword>",search_gig_view.as_view(),name = 'profile'),
  	path("search/user/<str:keyword>",search_profile_view.as_view(),name = 'profile'),
	path("buyer",buyer_dashboard_view.as_view(),name = 'buyer'),
 	path("requirements/paypal/<str:offer_id>/<str:pay_id>/<str:pay_email>/<str:trans_id>/<str:pay_status>/<str:base_price>/<str:total_price>/<str:service_fee>/<str:pay_to>/<str:extra_gig>",requirements_p_view.as_view(),name = 'requirements'),
  	path("requirements/flutter/<str:offer_id>/<str:base_price>/<str:total_price>/<str:service_fee>/<str:pay_to>/",requirements_f_view.as_view(),name = 'requirements'),
	path("dashboard",dashboard_view.as_view(),name = 'dashboard'),
 	path("users/<str:username>/manage_requests/<str:req_id>",offers_view.as_view(),name = 'offers_view'),
	path("account_settings",account_settings_view.as_view(),name = 'account_settings'),
	path("user/<str:username>/create_gig/<str:gigid>",create_gig_view.as_view(),name = 'create_gig'),
 	path("user/<str:username>/edit_gig/<str:gigid>",create_gig_view.as_view(),name = 'edit_gig'),
	path("manage_request",Manage_request_view.as_view(),name = 'manage_request'),
	path("categories/<str:category>",menu_pageView.as_view(),name = 'categories'),
	path("categories/<str:category>/<str:topic>/",all_gigs_pageView.as_view(),name = 'categories'),
	path("categories/<str:category>/<str:subcategry>/<str:topic>/",all_gigs_pageView.as_view(),name = 'categories'),
	path('logoutsocial', views.logout_social , name='logoutsocial'),
	path("Prof_image_upload/",views.Prof_image_upload_view,name = 'Prof_image_upload'),
	path("gig_image_upload/",views.gig_image_upload_view,name = 'gig_image_upload'),
	path("post_user_Details/",views.post_user_Details_view,name = 'post_user_Details'),
	path("post_useremail_Details/",views.post_useremail_Details_view,name = 'post_useremail_Details'),
	path("post_user_category/",views.post_user_category_view,name = 'post_user_category'),
 	path("post_user_paypal/",views.post_user_paypal_view,name = 'post_user_paypal'),
	path("post_user_languages/",views.post_user_languages_view,name = 'post_user_languages'),
	path("post_user_overview/",views.post_user_overview_view,name = 'post_user_overview'),
	path('user/<str:username>/manage_orders', seller_manage_orders_view.as_view(), name='manage_orders' ),
 	path("post_create_gig/",views.post_create_gig_view,name = 'post_create_gig'),
 	path("post_sub_category_details/",views.post_sub_category_details_view,name = 'post_sub_category_details'),
  	path("post_tags_category_details/",views.post_tags_category_details_view,name = 'post_tags_category_details'),
   	path("post_gig_save/",views.post_gig_save_view,name = 'post_gig_save'),
    path("post_packages_save/",views.post_packages_save_view,name = 'post_packages_save'),
    path("post_gig_desp_save/",views.post_gig_desp_save_view,name = 'post_gig_desp_save'),
    path("post_gig_des_faq_save/",views.post_gig_des_faq_save_view,name = 'post_gig_des_faq_save'),
    path("post_rquirements_save/",views.post_rquirements_save_view,name = 'post_rquirements_save'),
    path("post_images_save/",views.post_images_save_view,name = 'post_images_save'),
    path("post_publish_save/",views.post_publish_save_view,name = 'post_publish_save'),
    path("get_gig_details/",views.get_gig_details_view,name = 'get_gig_details'),
    path("get_gig_package_details/",views.get_gig_details_view,name = 'get_gig_details'),
    path("get_gig_extra_package_details/",views.get_gig_details_view,name = 'get_gig_details'),
    path("post_pause_gig/",views.post_pause_gig_view,name = 'post_pause_gig'),
    path("post_delete_gig/",views.post_delete_gig_view,name = 'post_delete_gig'),
    path("post_activate_gig/",views.post_activate_gig_view,name = 'post_activate_gig'),
    path("post_availability/",views.post_availability_view,name = 'post_availability'),
    path("post_avail_delete/",views.post_avail_delete_view,name = 'post_avail_delete'),
    path("post_service_request/",views.post_service_request_view,name = 'post_service_request'),
    path("get_availability/",views.get_availability_view,name = 'get_availability'),
    path("post_request_image_upload/",views.post_request_image_upload_view,name = 'post_request_image_upload'),
    path("post_make_fav/",views.post_make_fav_view,name = 'post_make_fav'),
    path("post_make_unfav/",views.post_make_unfav_view,name = 'post_make_unfav'),
    path("post_search_key/",views.post_search_key_view,name = 'post_search_key'),
    path("get_buyer_reviews/",views.get_buyer_reviews_view,name = 'get_buyer_reviews'),
    path("add_referral_link/",views.add_referral_link_view,name = 'add_referral_link'),
    path("get_filter_gigs_details/",views.get_filter_gigs_details_view,name = 'get_filter_gigs_details'),
    path("post_delete_request/",views.post_delete_request_view,name = 'post_delete_request'),
    path("post_active_request/",views.post_active_request_view,name = 'post_active_request'),
    path("post_pause_request/",views.post_pause_request_view,name = 'post_pause_request'),
    path("get_buyer_request/",views.get_buyer_request_view,name = 'get_buyer_request'),
    path("get_modal_show_request_details/",views.get_modal_show_request_details_view,name = 'get_modal_show_request_details'),
    path("get_gig_parameters/",views.get_gig_parameters_view,name = 'get_gig_parameters'),
    path("post_remove_request/",views.post_remove_request_view,name = 'post_remove_request'),
    path("post_offer_details/",views.post_offer_details_view,name = 'post_offer_details'),
    path("get_sorted_offers/",views.get_sorted_offers_view,name = 'get_sorted_offers'),
    path("get_sent_offers/",views.get_sent_offers_view,name = 'get_sent_offers'),
    path("post_remove_b_offer_req/",views.post_remove_b_offer_req_view,name = 'post_remove_b_offer_req'),
    path("post_paypal_transaction/",views.post_paypal_transaction_view,name = 'post_paypal_transaction'),
    path("post_flutterwave_transaction/",views.post_flutterwave_transaction_view,name = 'post_flutterwave_transaction'),
    path("post_mark_as_read/",views.post_mark_as_read_view,name = 'post_mark_as_read'),
    path("post_buyer_requ_save/",views.post_buyer_requ_save_view,name = 'post_buyer_requ_save'),
    path("post_req_image_upload/",views.post_req_image_upload_view,name = 'post_req_image_upload'),
    path("post_check_for_order/",views.post_check_for_order_view,name = 'post_check_for_order'),
    path("get_date_range_data/",views.get_date_range_data_view,name = 'get_date_range_data'),
    path("post_draft_object/",views.post_draft_object_view,name = 'post_draft_object'),
    path("post_delivered_object/",views.post_delivered_object_view,name = 'post_delivered_object'),
    path("post_resolutions/",views.post_resolutions_view,name = 'post_resolutions'),
    path("post_order_upload/",views.post_order_upload_view,name = 'post_order_upload'),
    path("post_delivery_order_upload/",views.post_delivery_order_upload_view,name = 'post_delivery_order_upload'),
    path("get_all_order_messages/",views.get_all_order_messages_view,name = 'get_all_order_messages'),
    path("post_accept_click/",views.post_accept_click_view,name = 'post_accept_click'),
    path("post_decline_click/",views.post_decline_click_view,name = 'post_decline_click'),
    path("post_confirm_warning/",views.post_confirm_warning_view,name = 'post_confirm_warning'),
    path("post_seller_review/",views.post_seller_review_view,name = 'post_seller_review'),
]