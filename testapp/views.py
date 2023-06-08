from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from testapp.models import student 

from linebot import LineBotApi , WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage ,TextMessage
# Create your views here.

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError :
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '姓名':
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='周迎希'))

                    elif mtext == '性別':
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='男'))

                    elif mtext == '學號':
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='10827271'))

                    elif mtext == '科系':
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='資管四甲'))

                    elif mtext == '興趣':
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='學做聊天機械人'))
                    
                    elif mtext == '@好友名單':
                        all=''
                        allstudents = student.objects.all()
                        for student in allstudents:
                            all += student.sName + student.sPhone+'\n'

                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=all))

                    else :
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
               
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

