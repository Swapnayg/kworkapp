import base64
import json
import secrets
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from .models import User
from .models import Message, Conversation,Order_Message, CustomNotifications,Order_Conversation,User_orders,ChatWords,SpamDetection
from django.db.models import Q
import itertools


class Order_ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"order_chat_{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        message, sender, receiver, time, attachment , order_no= (
            text_data_json["message"],
            text_data_json["sender"],
            text_data_json["recepient"],
            datetime.utcfromtimestamp(text_data_json["time"] / 1000.0),
            text_data_json.get("attachment"),
            text_data_json["order_no"],
        )
        #conversation = Order_Conversation.objects.get(id=int(self.room_name))
        sender = User.objects.get(username=sender)
        sender_prof = sender.avatar
        receiver = User.objects.get(username=receiver)
        receiver_prof =  receiver.avatar
        conversation = Order_Conversation.objects.get(Q(initiator=sender,receiver=receiver) | Q(initiator=receiver,receiver=sender))
        order_details = User_orders.objects.get(order_no = order_no )
        chat_words = list(ChatWords.objects.order_by().values_list('name').distinct())
        chat_list_words = []
        for chat in chat_words:
            chat_list_words.append(''.join(chat))
        if any((match := substring) in message for substring in chat_list_words):
            res = [ele for ele in chat_list_words if(ele in message)]
            spam_detection = SpamDetection(user_id=sender,detected_word=str(res))
            spam_detection.save()
        _message = Order_Message.objects.create(
            sender=sender,
            receiver=receiver,
            text = message,
            attachment = attachment,
            conversation_id=conversation,
            order_no = order_details,
            message_type = 'chat',
            is_read=False,
            mail_sent=False,
        )
        noti_create = CustomNotifications(sender = sender, recipient=receiver, verb='order_chat',description=message,order_no =order_details )
        noti_create.save()   
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username,
                "receiver": receiver.username,
                "attachment": _message.attachment,
                "time": str(_message.timestamp),
                "sender_img":str(sender_prof),
                "receiver_img": str(receiver_prof), 
                "conv_id": str(conversation.id),
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "sender": event["sender"],
                    "receiver":event["receiver"],
                    "time": event["time"],
                    "attachment": event["attachment"],
                    "sender_img":event["sender_img"],
                    "receiver_img":event["receiver_img"], 
                    "room_no": event["conv_id"], 
                }
            )
        )
