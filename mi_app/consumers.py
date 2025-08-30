import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def get_usuario_from_session(self):
        session = self.scope.get('session')
        if not session:
            return None
        
        usuario_id = session.get('usuario_id')
        if not usuario_id:
            return None
        
        try:
            from mi_app.models import usuarios
            return usuarios.objects.get(id=usuario_id)
        except usuarios.DoesNotExist:
            return None

    def connect(self):
        self.id = self.scope['url_route']['kwargs']['sala_id']
        self.room_group_name = 'sala_chat_%s' % self.id
        self.usuario = self.get_usuario_from_session()

        if not self.usuario:
            self.close()
            return
        
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()
        print(f'Usuario conectado: {self.usuario.usuario}')

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)
        print ('Se ha desconectado')

    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            
            # Enviar el mensaje al grupo de la sala
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, 
                {
                    'type': 'chat_message',
                    'message': message,
                    'usuario': self.usuario.usuario
                }
            )
            print("Mensaje recibido y enviado al grupo.")

        except json.JSONDecodeError as e:
            print('Hubo un error al decodificar el JSON:', e)
        except KeyError as e:
            print('El JSON no contiene la propiedad esperada:', e)
        except Exception as e:
            print('Error desconocido:', e)

    def chat_message(self, event):
        message = event['message']
        usuario = event['usuario']
        
        # Enviar el mensaje de vuelta al cliente
        self.send(text_data=json.dumps({
            'message': message,
            'usuario': usuario,
        }))
        print("Mensaje retransmitido al cliente.")