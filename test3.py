def post_credit_transaction_view(request):
    if request.method == 'GET':
        u_offer_id = request.GET['offer_id']
        u_base_price = request.GET['base_price']
        u_total_price =  round(float(request.GET['total_price']),2)
        u_service_fees = request.GET['fees']
        u_extra_gigs = request.GET['extra_gigs']
        u_user_id = request.GET['pay_user']
        u_pay_by = request.GET['pay_by']
        u_credit_used = round(float(request.GET['used_credits']),2)
        pay_by_user = User.objects.get(username = u_pay_by)
        offers_sent = Request_Offers.objects.get(pk= u_offer_id)
        pay_to_user = User.objects.get(pk = offers_sent.user_id.id)
        gig_details = UserGigs.objects.get(gig_title = offers_sent.gig_name.gig_title)
        already_submitted = 0
        data = []
        try:
            current_val = u_credit_used
            if(User_Transactions.objects.filter(gig_name= gig_details,offer_id=offers_sent,paid_by=pay_by_user,paid_to=pay_to_user,paid_for='order').exists() == False):
                if(float(u_credit_used) != 0.0):
                    refund_earning = User_Refund.objects.filter(user_id=pay_by_user,refund_status="cancelled")
                    for r_earn in refund_earning:
                        previous_credit = 0.0
                        if(r_earn.refund_amount != None):
                            if(len(r_earn.refund_amount) != 0):
                                prev_credit = float(r_earn.credit_used)
                                actual_available = float(r_earn.refund_amount) - float(prev_credit)
                                if(float(current_val) <= float(r_earn.refund_amount)):
                                    previous_credit = round(float(current_val),2) + float(r_earn.credit_used)
                                    current_val =  float(actual_available) - float(current_val)
                                    r_earn.credit_used = str(round(float(previous_credit),2))
                                    r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                    r_earn.save()
                                elif(float(u_credit_used) > float(r_earn.refund_amount)):
                                    if(float(current_val) != 0.0):
                                        current_val1 =  float(actual_available) - float(current_val)
                                        previous_credit = round(float(actual_available),2) + float(prev_credit)
                                        r_earn.credit_used = str(round(float(previous_credit),2))
                                        r_earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        r_earn.save()
                                        current_val = round(float(current_val) - float(current_val1),2)
                    if(float(current_val) != 0.0):
                        total_earnng = User_Earnings.objects.filter(user_id=pay_by_user, )
                        for earn in total_earnng:
                            if(earn.aval_with != None):
                                if(len(earn.aval_with) != 0):
                                    prev_credit = float(earn.credit_used)
                                    actual_available = float(earn.aval_with) - float(prev_credit)
                                    if(float(current_val) <= float(earn.aval_with)): 
                                        previous_credit = round(float(current_val),2) + float(earn.credit_used)
                                        current_val =  float(actual_available) - float(current_val)
                                        earn.credit_used = str(round(float(previous_credit),2))
                                        earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                        earn.save()
                                    elif(float(current_val) > float(earn.aval_with)):
                                        if(float(current_val) != 0.0):
                                            current_val1 =  float(actual_available) - float(current_val)
                                            previous_credit = round(float(actual_available),2) + float(prev_credit)
                                            earn.credit_used = str(round(float(previous_credit),2))
                                            earn.used_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                                            earn.save()
                                            current_val = round(float(current_val) - float(current_val1),2)
                u_trans_status = "successful"
                s = shortuuid.ShortUUID(alphabet="0123456789")
                u_trans_id = s.random(length=8)
                no_of_days = int(offers_sent.offer_time)
                Begindatestring = datetime.today()
                due_date = Begindatestring + timedelta(days=no_of_days)
                order_details = User_orders(order_status="active",package_gig_name=gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user,order_amount=u_base_price,due_date=due_date,completed_date=None)
                order_details.save()
                order_details_get = User_orders.objects.get(pk = order_details.pk)
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details_get).count()
                else:
                    already_submitted = 2
                try:    
                    cover_detls = Order_Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        cover_detls = Order_Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        cover_detls = Order_Conversation(initiator=pay_by_user,receiver=pay_to_user,order_no=order_details_get)
                        cover_detls.save()
                try:    
                    message_cover_detls = Conversation.objects.get(initiator=pay_by_user,receiver = pay_to_user)
                except:
                    try:
                        message_cover_detls = Conversation.objects.get(initiator=pay_to_user,receiver = pay_by_user)
                    except:
                        message_cover_detls = Conversation(initiator=pay_to_user,receiver = pay_by_user,convers_type="active")
                        message_cover_detls.save()   
                cover_detls =  Order_Conversation.objects.get(pk = cover_detls.pk)
                order_activity = User_Order_Activity(order_message="×1"+ str(gig_details.gig_title),order_amount=u_base_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                order_activity.save()
                user_trans = User_Transactions(gig_name= gig_details,offer_id=offers_sent,payment_type='credit',transaction_id=u_trans_id,payment_status=u_trans_status,payment_currency="USD",offer_amount=u_base_price,total_amount=u_total_price,processing_fees= u_service_fees,paid_by=pay_by_user,paid_to=pay_to_user,order_no=order_details_get,paid_for='order')
                user_trans.save()
                meta_data_list = u_extra_gigs.split(",")
                for meta in meta_data_list:
                    if(meta != "None"):
                        try:
                            extra_gig = UserExtra_gigs.objects.get(pk = int(meta))
                            user_extra_gig = User_orders_Extra_Gigs(order_no=order_details_get,package_gig_name=gig_details,gig_extra_package= extra_gig)
                            user_extra_gig.save()
                            order_activity = User_Order_Activity(order_message="×1"+ str(extra_gig.extra_gig_title),order_amount=extra_gig.extra_gig_price,order_no = order_details_get,activity_type="active",activity_by=pay_by_user,activity_to=pay_to_user)
                            order_activity.save()
                        except:
                            pass
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
            else:
                order_details = User_orders.objects.get(package_gig_name= gig_details,offer_id=offers_sent,order_by=pay_by_user,order_to=pay_to_user)
                if(offers_sent.ask_requirements == True):
                    already_submitted = Buyer_Requirements.objects.filter(user_id=pay_by_user,gig_name=gig_details,order_no=order_details).count()
                else:
                    already_submitted = 2
                data.append({"order_no":str(order_details.order_no),"ordered_by":pay_by_user.username,"ordered_to":pay_to_user.username,"submitted":already_submitted})
            notification_order = Notification_commands.objects.get(slug = "order_received")
            if(notification_order.is_active == True):
                noti_create = CustomNotifications(sender = pay_by_user, recipient=pay_to_user, verb='order' ,order_no = order_details,description="Congrates! Your Order with " + str(pay_by_user.username).title() + " is started.")   
                noti_create.save()
            if(pay_by_user.mail_order == True):
                mail_content = MailTemplates.order_mail_receipt_buyer(str(pay_by_user.username).title(),str(pay_to_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                SendEmailAct(str(pay_by_user.email),mail_content,"Here's your receipt of order.")
            if(pay_to_user.mail_order == True):
                mail_content = MailTemplates.order_mail_seller(str(pay_to_user.username).title(),str(pay_by_user.username).title(),"1",int(offers_sent.offer_time),str(user_trans.total_amount),str("#"+order_details.order_no),str(gig_details.gig_title).title())
                SendEmailAct(str(pay_to_user.email),mail_content," Great news: Your offer has been accepted.")                 
        except Exception as e:
            data.append({"error" : str(type(e)) + str(e)})
        return JsonResponse(json.dumps(data),safe=False)
