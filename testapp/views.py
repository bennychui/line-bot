from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, AudioSendMessage, VideoSendMessage, PostbackEvent, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, URITemplateAction, PostbackTemplateAction, ConfirmTemplate, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn

from testapp.models import student
from urllib.parse import parse_qsl


# Create your views here.
line_bot_api=LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser=WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method=='POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')
        try:
            events=parser.parse(body,signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event,MessageEvent):
                if isinstance(event.message,TextMessage):
                    mtext=event.message.text
                    if mtext =='@傳送文字':
                        sendText(event)

                    elif mtext =='@傳送圖片':
                        sendImage(event)

                    elif mtext =='@傳送貼圖':
                        sendStick(event)

                    elif mtext =='@多項傳送':
                        sendMulti(event)

                    elif mtext =='@傳送位置':
                        sendPosition(event)

                    elif mtext =='@快速選單':
                        sendQuickreply(event)

                    elif mtext =='@傳送聲音':
                        sendVoice(event)

                    elif mtext =='@傳送影片':
                        sendVideo(event)

                    elif mtext =='@按鈕樣板':
                        sendButton(event)

                    elif mtext =='@購買披薩':
                        sendPizza(event)

                    elif mtext =='@確認樣板':
                        sendConfirm(event)

                    elif mtext =='@yes':
                        sendYes(event)

                    elif mtext =='@no':
                        sendNo(event)

                    elif mtext =='@轉盤樣板':
                        sendCarousel(event)

                    elif mtext =='@圖片轉盤':
                        sendImgCarousel(event)
                                
                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

        if isinstance(event, PostbackEvent): #PostbackTemplateAction觸發事件
            backdata = dict(parse_qsl(event.postback.data)) #取得Postback資料
            if backdata.get('action')=='buy':
                sendBack_buy(event,backdata)

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# def listone(request):
#     try:
#         unit=student.objects.get(sName=" hihi ")
#     except:
#         errormessage="讀取錯誤"
#     return render (request,"listone.html",locals())

# def listall(request):
#     allstudents = student.objects.all().order_by('id')
#     return render (request,"listall.html",locals())

def sendVoice(event): #發出聲音
    try:
        message = AudioSendMessage(
            original_content_url='https://b028-140-135-112-180.ngrok.io/static/mario.m4a',
            duration=20000
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendVideo(event): #傳送影片
    try:
        message = VideoSendMessage(
            original_content_url='https://b028-140-135-112-180.ngrok.io/static/robot.mp4',
            preview_image_url='https://b028-140-135-112-180.ngrok.io/static/robot.jpg'
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendButton(event):
    try:
        message = TemplateSendMessage(
            alt_text='按鈕樣板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://b028-140-135-112-180.ngrok.io/static/pizza.jpg',
                title='按鈕樣板示範',#主標題
                text='請選擇:',#副標題
                actions=[
                    MessageTemplateAction(
                        label='文字訊息',
                        text='@購買披薩'
                    ),
                    URITemplateAction(
                        label='連結網頁',
                        uri='https://www.pizzahut.com.tw/menu/?parent_id=262&ppid=3857'
                    ),
                    PostbackTemplateAction(
                        label='回傳訊息',
                        data='action=buy'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendPizza(event):
    try:
        message = TextSendMessage(
            text = '感謝你購買披薩，我們將儘快爲您製作。'
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TemplateSendMessage(text='發生錯誤！'))

def sendBack_buy(event, backdata):
    try:
        text1 = 'thanks,'
        text1 += '\n我們將將儘快製作。'
        message = TextSendMessage(
            text = text1
        )

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


def sendConfirm(event): #確認樣板
    try:
        message = TemplateSendMessage(
            alt_text='確認樣板',
            template=ConfirmTemplate(
                text='你確定要購買這項商品嗎？',
                actions=[
                    MessageTemplateAction(  #按鈕選項
                        label='是',
                        text='@yes'
                    ),
                    MessageTemplateAction(
                        label='否',
                        text='@no'
                    )
                ]
            )
        )

        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TemplateSendMessage(text='發生錯誤！'))


def sendYes(event):
    try:
        message=TextSendMessage(
            text='感謝你的購買，\n我們將會儘快送出',
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


def sendNo(event):
    try:
        message=TextSendMessage(
            text='沒關係，\n請你重新操作',
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


def sendCarousel(event): #轉盤樣板
    try:
        message = TemplateSendMessage(
            alt_text='轉盤樣板',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://image.pizzahut.com.tw/dynamic/content/041aa5a249f31baad4177a8a6a64e746.jpg',
                        title='pizza',
                        text='pizza pizza',
                        actions=[
                            URITemplateAction(
                                label='煙燻黃金總匯',
                                uri='https://www.pizzahut.com.tw/menu/?parent_id=822&ppid=1784'
                            ),
                            URITemplateAction(
                                label='法式卡菲海陸比薩',
                                uri='https://www.pizzahut.com.tw/menu/?parent_id=263&ppid=3798'
                            ),
                            URITemplateAction(
                                label='煙燻培根手撕豬比薩',
                                uri='https://www.pizzahut.com.tw/menu/?parent_id=263&ppid=3660'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://image.pizzahut.com.tw/dynamic/content/b6b774891e8f40d799a5bd2e6800b3a9.jpg',
                        title='pizza現時',
                        text='pizza 優惠優惠',
                        actions=[
                            URITemplateAction(
                                label='煙燻黃金總匯',
                                uri='https://www.pizzahut.com.tw/menu/?parent_id=822&ppid=1784'
                            ),
                            URITemplateAction(
                                label='法式卡菲海陸比薩',
                                uri='https://www.pizzahut.com.tw/menu/?parent_id=263&ppid=3798'
                            ),
                            URITemplateAction(
                                label='煙燻培根手撕豬比薩',
                                uri='https://www.pizzahut.com.tw/menu/?parent_id=263&ppid=3660'
                            )
                        ]
                    )
                ] 
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendImgCarousel(event): #圖片轉盤
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://image.pizzahut.com.tw/dynamic/content/3965f1a62482bd8e3a7e726e26f6956e.jpg',
                        action=MessageTemplateAction(
                            label='歡迎訂購',
                            text='訂購披薩'
                        )
                    ),
                   ImageCarouselColumn(
                        image_url='https://image.pizzahut.com.tw/dynamic/content/99beff110efbe9c6c56e9b9d96e47b67.jpg',
                        action=MessageTemplateAction(
                          label='歡迎訂購',
                          text='訂購飲料'
                        )
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))