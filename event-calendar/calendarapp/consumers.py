import logging

from asgiref.sync import sync_to_async
# calendarapp/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from calendarapp.models.event import Event


# Dicționar global pentru a asocia utilizatorii cu channel_name-urile lor.
CHANNEL_MAP = {}
logger = logging.getLogger(__name__)
class RoleBasedNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # # Acceptă conexiunea WebSocket
        # await self.accept()
        # # Obține utilizatorul din contextul conexiunii
        # user = self.scope['user']
        # # Salvează channel_name-ul utilizatorului în dicționar
        # CHANNEL_MAP[user.id] = self.channel_name
        # print(f"User {user.id} connected with channel {self.channel_name}")
        user = self.scope['user']
        if user.is_anonymous:
            await self.close()
            return
        self.group_name = 'notificare_grup'
        logger.debug(f"CONNECT: adaug canalul {self.channel_name} la grupul {self.group_name}")
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self.personal_group = f"user_{user.id}"
        await self.channel_layer.group_add(self.personal_group, self.channel_name)
        await self.accept()
        logger.debug("CONNECT: conexiune acceptată")
    async def disconnect(self, close_code):
        # La deconectare, elimină utilizatorul din dicționar
        logger.debug(f"DISCONNECT: elimin canalul {self.channel_name} din grupul {self.group_name} (code={close_code})")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        logger.debug(f"RECEIVE: primit text_data={text_data!r}")
        if not text_data:
            return

        data = json.loads(text_data)
        msg_type = data.get('type') # cel mai important câmp
        logger.debug(msg_type)
        if msg_type == "notificare":
            # -- primul tip de mesaj --
            sender = data.get("sender", "Necunoscut")
            message = f"Utilizatorul {sender} a apăsat butonul!"
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "notificare_message",
                    "message": message,
                    "sender": sender,
                }
            )
        elif msg_type == "addEvent":
            # -- al doilea tip de mesaj --
            sender = data.get("sender")
            event_id = data.get("title")
            message = f"Evenimentul {event_id} a fost adăugat de {sender}"
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "addEvent",
                    "message": message,
                    "sender": sender,
                }
            )

        elif msg_type == "delete_event":
            # -- al doilea tip de mesaj --
            sender = data.get("sender")
            ev_id = data.get("eventId")
            message = f"Evenimentul {ev_id} a fost șters de {sender}"
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "notificare_message",
                    "message": message,
                    "sender": sender,
                }
            )

        elif msg_type == "custom_type":
            # -- alt tip de mesaj, poate trimitem alt event --
            payload = data.get("payload", {})
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "custom_message",
                    "payload": payload,
                }
            )
        elif msg_type == "event_approved":
            owner_id = data["ownerId"]  # îl bagi în payload din JS
            target_group = f"user_{owner_id}"
            message = f"Evenimentul {data['event_id']} a fost aprobat de {data['sender']}"
            await self.channel_layer.group_send(
                target_group,
                {
                    "type": "approve_message",
                    "message": message,
                    "sender": data["sender"],
                }
            )
        elif msg_type == "event_denied":
            owner_id = data["ownerId"]  # îl bagi în payload din JS
            target_group = f"user_{owner_id}"
            message = f"Evenimentul {data['event_id']} a fost denided de {data['sender']}"
            await self.channel_layer.group_send(
                target_group,
                {
                    "type": "denied_message",
                    "message": message,
                    "sender": data["sender"],
                }
            )

        # try:
            #     event = await sync_to_async(Event.objects.get)(id=event_id)
            #     logger.debug("Event găsit: %s", event)
            # except Event.DoesNotExist:
            #     logger.error(f"Event {event_id} nu există")
            #     return

            # notificăm creatorul evenimentului

            # channel = CHANNEL_MAP.get(ownerId)
            # logger.debug(f"Canal pentru ownerId {ownerId}: {channel}")
            # if channel:
            #     message = f"Evenimentul “{event_id}” a fost {verb} de {sender}"
            #     await self.channel_layer.send(
            #         channel,
            #         {
            #             "type": "notificare_message",
            #             "message": message,
            #             "sender": sender,
            #         }
            #     )
            # else:
            #     logger.debug(f"No channel pentru user {ownerId}, notificare sărită")
        else:
            logger.warning(f"RECEIVE: tip necunoscut: {msg_type}")

    async def notificare_message(self, event):
        logger.debug(f"NOTIFICARE_MESSAGE: event={event!r}, trimitem către client canal {self.channel_name}")
        logger.debug(f"NOTIFICARE_MESSAGE: event={event!r}, trimitem către client canal {self.channel_name}")
        payload = {
            'message': event.get('message'),
            'sender': event.get('sender'),
        }
        await self.send(text_data=json.dumps(payload))
        logger.debug(f"NOTIFICARE_MESSAGE: mesaj trimis payload={payload!r}")
    async  def addEvent(self,event):
        logger.debug(f"ADDEVENT: event={event!r}, trimitem către client canal {self.channel_name}")
        payload = {
            'type': 'addEvent',
            'message': event.get('message'),
            'sender': event.get('sender'),
            'url': '/calendar/'
        }
        await self.send(text_data=json.dumps(payload))
        logger.debug(f"ADDEVENT: mesaj trimis payload={payload!r}")
    async  def approve_message(self,event):
        logger.debug(f"APPROVE_MESSAGE: event={event!r}, trimitem către client canal {self.channel_name}")
        payload = {
            'message': event.get('message'),
            'sender': event.get('sender'),
        }
        await self.send(text_data=json.dumps(payload))
        logger.debug(f"APPROVE_MESSAGE: mesaj trimis payload={payload!r}")
    async  def denied_message(self,event):
        logger.debug(f"DENIED_MESSAGE: event={event!r}, trimitem către client canal {self.channel_name}")
        payload = {
            'message': event.get('message'),
            'sender': event.get('sender'),
        }
        await self.send(text_data=json.dumps(payload))
        logger.debug(f"DENIED_MESSAGE: mesaj trimis payload={payload!r}")



