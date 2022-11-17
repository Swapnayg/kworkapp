import base64
import json
import secrets
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from notifications.signals import notify
from .models import User
from .models import Message, Conversation,Order_Message,Request_Offers, Order_Conversation,User_orders,ChatWords,SpamDetection
from django.db.models import Q
import itertools


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
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

        message, sender, receiver, time, attachment , message_type, offer_id= (
            text_data_json["message"],
            text_data_json["sender"],
            text_data_json["recepient"],
            datetime.utcfromtimestamp(text_data_json["time"] / 1000.0),
            text_data_json.get("attachment"),
            text_data_json["message_type"],
            text_data_json["offer_id"],
        )
        sender = User.objects.get(username=sender)
        sender_prof = sender.avatar
        receiver = User.objects.get(username=receiver)
        receiver_prof =  receiver.avatar
        conversation = Conversation.objects.get(Q(initiator=sender,receiver=receiver) | Q(initiator=receiver,receiver=sender))
        chat_words = list(ChatWords.objects.order_by().values_list('name').distinct())     
        chat_list_words = []
        for chat in chat_words:
            chat_list_words.append(''.join(chat))
        if any((match := substring) in message for substring in chat_list_words):
            res = [ele for ele in chat_list_words if(ele in message)]
            spam_detection = SpamDetection(user_id=sender,detected_word=str(res))
            spam_detection.save()
        Message.objects.filter(sender=sender,receiver=receiver).update(is_read=True)
        if(len(offer_id.strip()) == 0):
            _message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                text = message,
                attachment = attachment,
                conversation_id=conversation,
                message_type = message_type,
            )
        else:
            request_offer = Request_Offers.objects.get(pk = offer_id)
            _message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                text = message,
                attachment = attachment,
                conversation_id=conversation,
                message_type = message_type,
                request_offers_id = request_offer,
            )  
        notify.send(sender, recipient=receiver, verb='chat',description=message)
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
                "offer_id": str(offer_id),  
                "message_type": str(message_type),  
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
                    "offer_id": event["offer_id"],
                    "message_type": event["message_type"],  
                    "room_no": event["conv_id"], 
                }
            )
        )

