import base64
import json
import secrets
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from notifications.signals import notify
from .models import User
from .models import Message, Conversation
from django.db.models import Q

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        # parse the json data into dictionary object
        text_data_json = json.loads(text_data)

        # unpack the dictionary into the necessary parts
        message, sender, receiver, time, attachment = (
            text_data_json["message"],
            text_data_json["sender"],
            text_data_json["recepient"],
            datetime.utcfromtimestamp(text_data_json["time"] / 1000.0),
            text_data_json.get("attachment"),
        )
        #conversation = Conversation.objects.get(id=int(self.room_name))
        sender = User.objects.get(username=sender)
        #sender_prof = UserProfileDetails.objects.get(user_id=sender)
        receiver = User.objects.get(username=receiver)
        #receiver_prof = UserProfileDetails.objects.get(user_id=sender)
        conversation = Conversation.objects.get(Q(initiator=sender,receiver=receiver) | Q(initiator=receiver,receiver=sender))

        # Attachment
        if attachment:
            file_str, file_ext = attachment["data"], attachment["format"]

            # make i no lie, i don't know what happens here. later things
            file_data = ContentFile(
                base64.b64decode(file_str), name=f"{secrets.token_hex(8)}.{file_ext}"
            )
            _message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                #timestamp=time,
                attachment=file_data,
                text=message,
                conversation_id=conversation,
            )
            notify.send(sender, recipient=receiver, verb='chat',description=message)
        else:
            _message = Message.objects.create(
                sender=sender,
                receiver=receiver,
                #timestamp=time,
                text=message,
                conversation_id=conversation,
            )
            notify.send(sender, recipient=receiver, verb='chat',description=message)
        # Send message to room group
        if _message.attachment:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender.username,
                    "receiver": receiver.username,
                    "attachment": _message.attachment.url,
                    "time": str(_message.timestamp),
                    #"sender_img":str(sender_prof.profile_img),
                    #"receiver_img": str(receiver_prof.profile_img), 
                    "conv_id": str(conversation.id),
                },
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "sender": sender.username,
                    "receiver": receiver.username,
                    "time": str(_message.timestamp),
                    #"sender_img":str(sender_prof.profile_img),
                    #"receiver_img": str(receiver_prof.profile_img), 
                    "conv_id": str(conversation.id),
                },
            )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        if event.get("attachment"):
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
        else:
            self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "sender": event["sender"],
                        "receiver":event["receiver"],
                        "time": event["time"],
                        "room_no": event["conv_id"],
                        "sender_img":event["sender_img"],
                        "receiver_img":event["receiver_img"], 
                    }
                )
            )
