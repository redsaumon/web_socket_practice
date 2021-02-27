import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name 
        # 사용자가 지정한 방 이름으로 채팅 구성할 경우. 문자 숫자 하이픈 및 마침표만 포함함 수정 필요

        # 그룹 참여
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept() # connect 메서드 내에서 얘를 호출하지 않으면 연결 거부되고 닫힘

    async def disconnect(self, close_code):
        # 그룹 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 메세지 받기
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 채팅방 그룹에 메세지 보내기
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # 채팅방 그룹에서 메세지 받기
    async def chat_message(self, event):
        message = event['message']

        # 메세지 보내기
        await self.send(text_data=json.dumps({
            'message': message
        }))
