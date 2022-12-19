def every_minute():
    all_users = []
    all_users = User.objects.filter(is_admin=False,profile_status="active")
    for us in all_users:
        userDetails = User.objects.get(username = us.username)
        average_delivery_str = 'Within 24 hours'
        total_earnng = User_Earnings.objects.filter(user_id=userDetails)
        if(UserAvailable.objects.filter(user_id=userDetails).exists() == True):
            user_avail_details = UserAvailable.objects.get(user_id=userDetails)
            try:
                availableto_date = datetime.strptime(str(user_avail_details.available_to),"%Y-%m-%d").date()
            except:
	            availableto_date = datetime.strptime(str(user_avail_details.available_to),"%Y-%m-%d").date()
            if(int(todays_date.month) == int(availableto_date.month) and int(todays_date.day) == int(availableto_date.day) and int(todays_date.year) == int(availableto_date.year) ):
                UserAvailable.objects.filter(user_id=userDetails).delete()
        todays_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
        for earn in total_earnng:
            if(earn.clearence_date != None or earn.clearence_status == "pending" ):
                try:
                    clearence_date = datetime.strptime(str(earn.clearence_date),"%Y-%m-%d %H:%M:%S")
                except:
	                clearence_date = datetime.strptime(str(earn.clearence_date),"%Y-%m-%d %H:%M:%S.%f")
                if(int(todays_date.month) == int(clearence_date.month) and int(todays_date.day) == int(clearence_date.day) and int(todays_date.year) == int(clearence_date.year) and int(todays_date.hour) == int(clearence_date.hour)):
                    earn.aval_with = earn.earning_amount
                    earn.clearence_status = "cleared"
                    earn.cleared_on = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                    earn.save()
                    order_details = User_orders.objects.get(order_no= earn.order_no)
                    order_by = User.objects.get(username = order_details.order_by.username)
                    order_to = User.objects.get(username = order_details.order_to.username)
                    
                    try:
                        earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S").date()
                    except:
                        earned_date = datetime.strptime(str(earn.earning_date),"%Y-%m-%d %H:%M:%S.%f").date()
                    
                    re_withdrwal_val = 0
                    re_withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days") )
                    for ext in re_withdrawal_ext:
                        if(ext.parameter_name == "withdrawal_clearence_days"):
                            re_withdrwal_val = ext.no_of_days
                    re_today_date = datetime.today()
                    re_clearencedate = re_today_date + timedelta(days=int(re_withdrwal_val))   
                    buyer_refferal = None
                    try:
                        buyer_refferal = Referral_Users.objects.get(refferal_user = order_by)
                    except:
                        buyer_refferal = None
                    if(buyer_refferal != None):
                        affiliate_amount = 0
                        if(buyer_refferal.buyer_affi_done == False):
                            if(float(order_details.order_amount) > 40):
                                affiliate_amount = 5
                                refferal_user = User.objects.get(pk =buyer_refferal.user_id.pk)
                                earnings_details = User_Earnings(order_amount=affiliate_amount,earning_amount=affiliate_amount,platform_fees=0,aval_with="",order_no= order_details,clearence_date=re_clearencedate,clearence_status="pending",cleared_on=None,user_id=refferal_user,earning_type="affiliate",affiliate_user=buyer_refferal)
                                earnings_details.save()
                                order_ativity = User_Order_Activity(order_message = "×1 Affiliate Commission" ,activity_type="affiliate",activity_by=buyer_refferal,activity_to=refferal_user)
                                order_ativity.save()
                                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earned_val ,activity_type="pending",activity_by=buyer_refferal,activity_to=refferal_user)
                                order_ativity1.save()
                                buyer_refferal.buyer_affi_amount = affiliate_amount
                                buyer_refferal.buyer_affi_done = True
                                buyer_refferal.save()
                    seller_refferal = None
                    try:
                        seller_refferal = Referral_Users.objects.get(refferal_user = order_to)
                    except:
                        seller_refferal = None
                    if(seller_refferal != None):
                        s_affiliate_amount = 0
                        if(seller_refferal.seller_affi_done == False):
                            if(float(order_details.order_amount) > 40):
                                affiliate_amount = 5
                                refferal_user = User.objects.get(pk =buyer_refferal.user_id.pk)
                                earnings_details = User_Earnings(order_amount=affiliate_amount,earning_amount=affiliate_amount,platform_fees=0,aval_with="",order_no= order_details,clearence_date=re_clearencedate,clearence_status="pending",cleared_on=None,user_id=refferal_user,earning_type="affiliate",affiliate_user=seller_refferal)
                                earnings_details.save()
                                order_ativity = User_Order_Activity(order_message = "×1 Affiliate Commission" ,activity_type="affiliate",activity_by=seller_refferal,activity_to=refferal_user)
                                order_ativity.save()
                                order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earned_val ,activity_type="pending",activity_by=seller_refferal,activity_to=refferal_user)
                                order_ativity1.save()
                                seller_refferal.seller_affi_amount = affiliate_amount
                                seller_refferal.seller_affi_done = True
                                seller_refferal.save()
                    order_activity = User_Order_Activity.objects.filter(order_no=order_details,activity_type="pending",activity_by=order_by,activity_to=order_to,activity_date__year=earned_date.year,activity_date__month=earned_date.month, activity_date__day=earned_date.day)
                    for order_ac in order_activity:
                        order_ac.activity_type = "cleared"
                        order_ac.save()
        orders_count = User_orders.objects.filter(order_to=userDetails,order_status="active" ).count()
        user_orders = User_orders.objects.filter(order_to=userDetails)
        orders_deliv_lists = []
        for u_order in user_orders:
            try:
                order_date = datetime.strptime(str(u_order.order_date),"%Y-%m-%d %H:%M:%S").date()
            except:
                order_date = datetime.strptime(str(u_order.order_date),"%Y-%m-%d %H:%M:%S.%f").date()
            delivery_details =  Order_Delivery.objects.filter(delivered_by=userDetails, order_no=u_order ).last()
            if(delivery_details != None):
                if(delivery_details.delivery_date != None):
                    try:
                        delivery_date = datetime.strptime(str(delivery_details.delivery_date),"%Y-%m-%d %H:%M:%S").date()
                    except:
                        delivery_date = datetime.strptime(str(delivery_details.delivery_date),"%Y-%m-%d %H:%M:%S.%f").date()
                    diff = relativedelta.relativedelta(order_date, delivery_date)
                    orders_deliv_lists.append(diff.days)
                    try:
                        average_days = int(sum(orders_deliv_lists)/len(orders_deliv_lists))
                    except:
                        average_days = 0
                    if(average_days <= 1):
                        average_delivery_str = "Within 24 hours"
                    elif(average_days <= 2):
                        average_delivery_str = "Within 2 days"
                    elif(average_days <= 3):
                        average_delivery_str = "Within 3 days"
                    elif(average_days <= 5):
                        average_delivery_str = "Within 5 days"
                    elif(average_days >= 5):
                        average_delivery_str = "Within 10 days"
        pay_pal_api_key = ''
        pay_pal_secreat_key = ''
        api_details = Api_keys.objects.filter(Q(api_name="paypal"))
        for api in api_details:
            if(api.api_name == "paypal"):
                pay_pal_api_key = api.private_key
                pay_pal_secreat_key = api.secrete_key
        user_transaction =  User_Transactions.objects.filter(paid_by= userDetails ) 
        for pay in user_transaction:
            if(pay.payment_type == "paypal"):
                paypalrestsdk.configure({
                    "mode": "sandbox", # sandbox or live
                    "client_id": pay_pal_api_key,
                    "client_secret": pay_pal_secreat_key 
                })               
                sale = Sale.find(str(pay.transaction_id))
                pay_status = sale['state']
                if(pay_status== "refunded"):
                    pay.transaction_status= 'rufunded'
                    pay.save()
                    order_details = User_orders.objects.get(order_no = pay.order_no)
                    if(User_Refund.objects.filter(order_no= order_details,transaction=pay).exists() == False):
                        order_details.order_status = 'cancel'
                        order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        order_details.save()
                        order_by_user = User.objects.get(username= order_details.order_by.username)
                        order_to_user = User.objects.get(username= order_details.order_to.username)
                        transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                        transaction.transaction_status = "cancelled"
                        transaction.save()
                        refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res_details,order_no=order_details,transaction=transaction ,user_id=order_by_user)
                        refund_details.save()
                        try:    
                            cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                        except:
                            cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)   
                        order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "cancelled",conversation_id=cover_detls,order_no=order_details,message_type="chat",is_read=True)
                        order_message.save()
                        order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                        order_ativity.save()
                        earning_val = 0
                        if(int(order_details.order_amount) <40):
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        else:
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        earning_val = float(earning_val) + (round(float(round(float(order_details.order_amount),2) - service_fees_price),2))
                        order_ativity1 = User_Order_Activity(order_message = "Cancelled Payment Refunded to Buyer",order_amount = earning_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                        order_ativity1.save()
                        order_by =  User.objects.get(username= order_details.order_by.username)   
                        order_to =  User.objects.get(username= order_details.order_to.username)
                        service_fees_price = 0
                        if(int(order_details.order_amount) < 40):
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        else:
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                        refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=None,clearence_status="cancelled",cleared_on=None,user_id=order_to,earning_type="cancelled",affiliate_user=None)
                        refund_details.save()
                        notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                        if(notification_cancel.is_active == True):
                            noti_create = CustomNotifications(sender = order_by, recipient=order_to, verb='order' ,order_no = order_details,description= str(order_by.username).title() + " marked as cancelled.")
                            noti_create.save()
                        if(order_by.mail_order == True):
                            mail_content = MailTemplates.order_cancelled_buyer(str(order_by.username).title(),str("#"+order_details.order_no))
                            SendEmailAct(str(order_by.email),mail_content,"Your order has been cancelled.")
                        if(order_to.mail_order == True):
                            mail_content = MailTemplates.order_cancelled_seller(str(order_to.username).title(),str(order_by.username).title(),str("#"+order_details.order_no))
                            SendEmailAct(str(order_to.email),mail_content,"Your order has been cancelled.")
                        update_all_balancevalues(order_by_user)
                        update_all_balancevalues(order_to_user)
                    else:
                        order_by_user = User.objects.get(username= order_details.order_by.username)
                        order_to_user = User.objects.get(username= order_details.order_to.username)
                        refund_details = User_Refund.objects.get(order_no= order_details,transaction=pay)
                        refund_details.refund_status='refunded'
                        refund_details.save()
                        update_all_balancevalues(order_by_user)
                        update_all_balancevalues(order_to_user)
            if(pay.payment_type == "flutterwave"):
               if(pay.transaction_status == "rufunded"):
                    order_details = User_orders.objects.get(order_no = pay.order_no)
                    if(User_Refund.objects.filter(order_no= order_details,transaction=pay).exists() == False):
                        order_details.order_status = 'cancel'
                        order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        order_details.save()
                        order_by_user = User.objects.get(username= order_details.order_by.username)
                        order_to_user = User.objects.get(username= order_details.order_to.username)
                        transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                        transaction.transaction_status = "cancelled"
                        transaction.save()
                        refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res_details,order_no=order_details,transaction=transaction ,user_id=order_by_user)
                        refund_details.save()
                        try:
                            cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                        except:
                            cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)   
                        order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "cancelled",conversation_id=cover_detls,order_no=order_details,message_type="chat",is_read= True)
                        order_message.save()
                        order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                        order_ativity.save()
                        earning_val = 0
                        if(int(order_details.order_amount) < 40):
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        else:
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        earning_val = float(earning_val) + (round(float(round(float(order_details.order_amount),2) - service_fees_price),2))
                        order_ativity1 = User_Order_Activity(order_message = "Cancelled Payment Refunded to Buyer",order_amount = earning_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                        order_ativity1.save()
                        order_by =  User.objects.get(username= order_details.order_by.username)   
                        order_to =  User.objects.get(username= order_details.order_to.username)
                        service_fees_price = 0
                        if(int(order_details.order_amount) < 40):
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        else:
                            payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                            for p in payment_parameters:
                                serv_fees_val = p.service_fees
                                serv_fees_type = p.fees_type
                                if(serv_fees_type == "flat"):
                                    service_fees_price =  int(serv_fees_val)
                                else:
                                    perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                    service_fees_price = round(perceof_budg,2)
                        earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                        refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=None,clearence_status="cancelled",cleared_on=None,user_id=order_to,earning_type="cancelled",affiliate_user=None)
                        refund_details.save()
                        notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                        if(notification_cancel.is_active == True):
                            noti_create = CustomNotifications(sender = order_by, recipient=order_to, verb='order' ,order_no = order_details,description= str(order_by.username).title() + " marked as cancelled.")
                            noti_create.save()
                        if(order_by.mail_order == True):
                            mail_content = MailTemplates.order_cancelled_buyer(str(order_by.username).title(),str("#"+order_details.order_no))
                            SendEmailAct(str(order_by.email),mail_content,"Your order has been cancelled.")
                        if(order_to.mail_order == True):
                            mail_content = MailTemplates.order_cancelled_seller(str(order_to.username).title(),str(order_by.username).title(),str("#"+order_details.order_no))
                            SendEmailAct(str(order_to.email),mail_content,"Your order has been cancelled.")
                        update_all_balancevalues(order_by_user)
                        update_all_balancevalues(order_to_user)
                    else:
                        order_by_user = User.objects.get(username= order_details.order_by.username)
                        order_to_user = User.objects.get(username= order_details.order_to.username)
                        refund_details = User_Refund.objects.get(order_no= order_details,transaction=pay)
                        refund_details.refund_status='refunded'
                        refund_details.save()
                        update_all_balancevalues(order_by_user)
                        update_all_balancevalues(order_to_user)
        reolution_details = User_Order_Resolution.objects.filter( Q(resolution_status="pending") | Q(raised_to= userDetails))
        for res in reolution_details:
            if(res.resolution_last_date != None):
                try:
                    resolution_last_date = datetime.strptime(str(res.resolution_last_date ),"%Y-%m-%d %H:%M:%S")
                except:
                    resolution_last_date = datetime.strptime(str(res.resolution_last_date ),"%Y-%m-%d %H:%M:%S.%f")
                if(int(todays_date.month) == int(resolution_last_date.month) and int(todays_date.day) == int(resolution_last_date.day) and int(todays_date.year) == int(resolution_last_date.year) and int(todays_date.hour) == int(resolution_last_date.hour)):
                    if(res.resolution_type=="cancel"):
                        res.resolution_status = 'accepted'
                        res.save()
                        order_details = User_orders.objects.get(order_no = res_details.order_no)
                        if(order_details.order_status != "completed"):  
                            order_details.order_status = 'cancel'
                            order_details.incoming_request = 'site'
                            order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            order_details.save()
                            order_by_user = User.objects.get(username= order_details.order_by.username)
                            order_to_user = User.objects.get(username= order_details.order_to.username)
                            transaction = User_Transactions.objects.get(order_no=order_details,paid_for='order')
                            transaction.transaction_status = "cancelled"
                            transaction.save()
                            raised_by = User.objects.get(username = res.raised_by.username)
                            raised_to = User.objects.get(username = res.raised_to.username)
                            notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                            if(notification_cancel.is_active == True):
                                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order',order_no = order_details,description= "Your order Automatically Cancelled.")
                                noti_create.save()
                            refund_details = User_Refund(refund_amount=order_details.order_amount,resolution=res_details,order_no=order_details,transaction=transaction ,user_id=order_by_user)
                            refund_details.save()
                            try:    
                                cover_detls = Order_Conversation.objects.get(initiator=order_by_user,receiver = order_to_user)
                            except:
                                cover_detls = Order_Conversation.objects.get(initiator=order_to_user,receiver = order_by_user)   
                            order_message = Order_Message(sender=order_by_user,receiver=order_to_user,text = "cancelled",conversation_id=cover_detls,order_no=order_details,message_type="chat",is_read= True)
                            order_message.save()
                            order_ativity = User_Order_Activity(order_message = "×1 Order Cancelled" , order_no=order_details,activity_type="cancel",activity_by=order_by_user,activity_to=order_to_user)
                            order_ativity.save()
                            earning_val = 0
                            if(int(order_details.order_amount) < 40):
                                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                                for p in payment_parameters:
                                    serv_fees_val = p.service_fees
                                    serv_fees_type = p.fees_type
                                    if(serv_fees_type == "flat"):
                                        service_fees_price =  int(serv_fees_val)
                                    else:
                                        perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                        service_fees_price = round(perceof_budg,2)
                            else:
                                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                                for p in payment_parameters:
                                    serv_fees_val = p.service_fees
                                    serv_fees_type = p.fees_type
                                    if(serv_fees_type == "flat"):
                                        service_fees_price =  int(serv_fees_val)
                                    else:
                                        perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                        service_fees_price = round(perceof_budg,2)
                            earning_val = float(earning_val) + (round(float(round(float(order_details.order_amount),2) - service_fees_price),2))
                            order_ativity1 = User_Order_Activity(order_message = "Cancelled Payment Refunded to Buyer",order_amount = earning_val , order_no=order_details,activity_type="e_cancel",activity_by=order_by_user,activity_to=order_to_user)
                            order_ativity1.save()
                            order_by =  User.objects.get(username= order_details.order_by.username)   
                            order_to =  User.objects.get(username= order_details.order_to.username)
                            User_Order_Resolution.objects.filter(raised_by = order_by, raised_to= order_to,resolution_status="pending").update(resolution_status="rejected")
                            User_Order_Resolution.objects.filter(raised_by = order_to, raised_to= order_by,resolution_status="pending").update(resolution_status="rejected")
                            raised_by = User.objects.get(username = res.raised_by.username)
                            raised_to = User.objects.get(username = res.raised_to.username)
                            notification_cancel = Notification_commands.objects.get(slug = "order_cancelled")
                            if(notification_cancel.is_active == True):
                                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details,description= str(raised_to.username).title() + " cancelled the Order.")
                                noti_create.save()
                            if(order_by.mail_order == True):
                                mail_content = MailTemplates.order_cancelled_buyer(str(order_by.username).title(),str("#"+order_details.order_no))
                                SendEmailAct(str(order_by.email),mail_content,"Your order has been cancelled.")
                            if(order_to.mail_order == True):
                                mail_content = MailTemplates.order_cancelled_seller(str(order_to.username).title(),str(order_by.username).title(),str("#"+order_details.order_no))
                                SendEmailAct(str(order_to.email),mail_content,"Your order has been cancelled.")
                            service_fees_price = 0
                            if(int(order_details.order_amount) < 40):
                                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                                for p in payment_parameters:
                                    serv_fees_val = p.service_fees
                                    serv_fees_type = p.fees_type
                                    if(serv_fees_type == "flat"):
                                        service_fees_price =  int(serv_fees_val)
                                    else:
                                        perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                        service_fees_price = round(perceof_budg,2)
                            else:
                                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                                for p in payment_parameters:
                                    serv_fees_val = p.service_fees
                                    serv_fees_type = p.fees_type
                                    if(serv_fees_type == "flat"):
                                        service_fees_price =  int(serv_fees_val)
                                    else:
                                        perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                        service_fees_price = round(perceof_budg,2)
                                    earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                                    refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=None,clearence_status="cancelled",cleared_on=None,user_id=order_to,earning_type="cancelled",affiliate_user=None)
                                    refund_details.save()
                    elif(res.resolution_type=="extention"):
                        if(order_details.order_status != "completed"):  
                            res.resolution_status = 'accepted'
                            res.save()
                            raised_by = User.objects.get(username = res.raised_by.username)
                            raised_to = User.objects.get(username = res.raised_to.username)
                            order_details = User_orders.objects.get(order_no = res_details.order_no)
                            order_details.due_date = next_date
                            order_details.save()   
                            order_ativity = User_Order_Activity(order_message = "×1 Extended Delivery Time" , order_no=order_details,activity_type="extension",activity_by=raised_by,activity_to=raised_to)
                            order_ativity.save()
                            notification_extension = Notification_commands.objects.get(slug = "order_extended")
                            if(notification_extension.is_active == True):
                                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order',order_no = order_details,description=  "Your order Due Date Automatically Extended.")
                                noti_create.save()
                            if(raised_by.mail_order == True):
                                mail_content = MailTemplates.order_extension_accepted(str(raised_by.username).title(),str(raised_to.username).title(),str("#"+order_details.order_no))
                                SendEmailAct(str(raised_by.email),mail_content,"Order Extension has been Approved by " + str(raised_to.username).title() + ".")
                    elif(res.resolution_type=="delivered"):
                        if(order_details.order_status != "completed"):
                            res.resolution_status = 'accepted'
                            res.save()
                            raised_by = User.objects.get(username = res.raised_by.username)
                            raised_to = User.objects.get(username = res.raised_to.username)
                            User_Order_Resolution.objects.filter(raised_by = raised_by, raised_to= raised_to,resolution_status="pending").update(resolution_status="rejected", resolution_cancel_mssg = "Order Completed.")
                            User_Order_Resolution.objects.filter(raised_by = raised_to, raised_to= raised_by,resolution_status="pending").update(resolution_status="rejected", resolution_cancel_mssg = "Order Completed.")
                            notification_delivery = Notification_commands.objects.get(slug = "order_completed")
                            order_details = User_orders.objects.get(order_no = res_details.order_no)
                            if(notification_delivery.is_active == True):
                                noti_create = CustomNotifications(sender = raised_to, recipient=raised_by, verb='order' ,order_no = order_details,description= "Your order Automatically Marked as completed.")
                                noti_create.save()
                            service_fees_price = 0
                            if(int(order_details.order_amount) < 40):
                                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="40"))
                                for p in payment_parameters:
                                    serv_fees_val = p.service_fees
                                    serv_fees_type = p.fees_type
                                    if(serv_fees_type == "flat"):
                                        service_fees_price =  int(serv_fees_val)
                                    else:
                                        perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                        service_fees_price = round(perceof_budg,2)
                            else:
                                payment_parameters = Payment_Parameters.objects.filter(Q(parameter_name="Seller Order Fees", service_amount="41"))
                                for p in payment_parameters:
                                    serv_fees_val = p.service_fees
                                    serv_fees_type = p.fees_type
                                    if(serv_fees_type == "flat"):
                                        service_fees_price =  int(serv_fees_val)
                                    else:
                                        perceof_budg = float((int(order_details.order_amount)* int(serv_fees_val))/100)
                                        service_fees_price = round(perceof_budg,2)
                            earned_val = round(float(round(float(order_details.order_amount),2) - service_fees_price),2)
                            withdrwal_val = 0
                            withdrawal_ext = Addon_Parameters.objects.filter(Q(parameter_name="withdrawal_clearence_days") )
                            for ext in withdrawal_ext:
                                if(ext.parameter_name == "withdrawal_clearence_days"):
                                    withdrwal_val = ext.no_of_days
                            today_date = datetime.today()
                            clearencedate = today_date + timedelta(days=int(withdrwal_val))                
                            order_details.order_status = 'completed'
                            order_details.completed_date = datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            order_details.save()
                            order_by =  User.objects.get(username= order_details.order_by.username)   
                            order_to =  User.objects.get(username= order_details.order_to.username) 
                            order_to.u_last_delivery= datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                            order_to.save()
                            update_all_balancevalues(order_by)
                            update_all_balancevalues(order_to)
                            try:    
                                cover_detls = Order_Conversation.objects.get(initiator=order_by,receiver = order_to)
                            except:
                                cover_detls = Order_Conversation.objects.get(initiator=order_to,receiver = order_by)   
                            refund_details = User_Earnings(order_amount=order_details.order_amount,earning_amount=earned_val,platform_fees=service_fees_price,aval_with="",resolution=res_details,order_no= order_details,clearence_date=clearencedate,clearence_status="pending",cleared_on=None,user_id=order_to,earning_type="order",affiliate_user=None)
                            refund_details.save()
                            order_message = Order_Message(sender=order_by,receiver=order_to,text = "completed",conversation_id=cover_detls,order_no=order_details,message_type="activity",is_read=True)
                            order_message.save()
                            get_message =  Order_Message.objects.get(pk = order_message.pk)
                            resolution= User_Order_Resolution(resolution_type="completed",resolution_text = "Completed",resolution_message="Completed",resolution_desc="successfuly completed",resolution_status="accepted",order_no=order_details,raised_by=order_by,raised_to=order_to,message=get_message)
                            resolution.save()
                            order_ativity = User_Order_Activity(order_message = "×1 Order Completed" , order_no=order_details,activity_type="completed",activity_by=order_by,activity_to=order_to)
                            order_ativity.save()
                            order_ativity1 = User_Order_Activity(order_message = "Pending for Clearence",order_amount = earned_val , order_no=order_details,activity_type="pending",activity_by=order_by,activity_to=order_to)
                            order_ativity1.save()
        userDetails.ordersin_progress = orders_count
        userDetails.avg_delivery_time = average_delivery_str
        userDetails.save()

