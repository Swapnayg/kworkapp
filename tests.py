def post_seller_review_view(request):
    if request.method == 'GET':
        order_no = request.GET['order_no']
        s_comm = request.GET['s_comm']
        s_serv = request.GET['s_serv']
        s_recomm = request.GET['s_recomm']
        s_review_txt = request.GET['s_review_txt']
        data = []
        try:
            ord_details = User_orders.objects.get(order_no = order_no)
            orderedby_user = User.objects.get(username = ord_details.order_by.username)
            orderedto_user = User.objects.get(username = ord_details.order_to.username)
            gig_details = UserGigs.objects.get(gig_title = ord_details.package_gig_name.gig_title)  
            average_val =  round(float(int(int(s_comm) + int(s_serv)+ int(s_recomm)) / 3),2)
            if(Seller_Reviews.objects.filter(order_no=ord_details,s_review_from=orderedby_user,s_review_to=orderedto_user,package_gig_name= gig_details).exists() == False):
                seller_reviews = Seller_Reviews(communication=s_comm,recommendation=s_recomm,service=s_serv,average_val=average_val,seller_response="",review_message=s_review_txt,order_no=ord_details,package_gig_name= gig_details,s_review_from=orderedby_user,s_review_to=orderedto_user,buyer_resp_date=None)
                seller_reviews.save()
                notification_seller = Notification_commands.objects.get(slug = "order_seller_reviews")
                if(notification_seller.is_active == True):
                    noti_create = CustomNotifications(sender = orderedby_user, recipient=orderedto_user,order_no= ord_details, verb='reviews',description= str(orderedby_user.username).title() + " left a " + str(round(average_val)) + " star review.")  
                    noti_create.save()
            data.append({"sucess" : str("sucess")})
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(data,safe=False)
