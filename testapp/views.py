from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from testapp.models import student 


from linebot import LineBotApi , WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage , TextSendMessage, AudioSendMessage, VideoSendMessage, TemplateSendMessage, ButtonsTemplate, MessageTemplateAction, URITemplateAction, PostbackTemplateAction, PostbackEvent, PostbackTemplateAction,ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply, QuickReplyButton, MessageAction, ConfirmTemplate, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, URIAction, BubbleContainer
from linebot.models import ImageComponent, BoxComponent, TextComponent, IconComponent, ButtonComponent, SeparatorComponent, FlexSendMessage

from urllib.parse import parse_qsl 
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
                    if mtext == '@傳送文字':
                        sendText(event)

                    elif mtext == '@傳送圖片':
                        sendImage(event)    

                    elif mtext == '@傳送貼圖':
                        sendStick(event) 

                    elif mtext == '@多項傳送':
                        sendMulti(event) 
                    
                    elif mtext == '@傳送位置':
                        sendPosition(event) 


                    
                    elif mtext == '@快速選單':
                        sendQuickreply(event) 

                    elif mtext == '@你推薦的食譜':
                        sendQuickreply(event) 

                        

                    elif mtext == '@傳送聲音':
                        sendVoice(event)

                    elif mtext == '@傳送影片':
                        sendVideo(event)

                        

                    elif mtext == '@按鈕樣板':
                        sendButton(event)

                    elif mtext == '@今日推薦':          #今日推薦
                        sendButton(event)

                    elif mtext == '@今天推薦':          #今天推薦
                        sendButton(event)



                    elif mtext == '@購買披薩':
                        sendPizza(event)

                    elif mtext == '@確認樣板':
                        sendConfirm(event)

                    elif mtext == '@yes':
                        sendYes(event)

                    elif mtext == '@no':
                        sendNo(event)




                    elif mtext == '@轉盤樣板':
                        sendCarousel(event)

                    elif mtext == '@各種口味推薦菜':
                        sendCarousel(event)
                        

                    elif mtext == '@圖片轉盤':
                        sendImgCarousel(event)  

                    elif mtext == '@彈性':
                        sendFlex(event)

                    else:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))      
        
            if isinstance(event, PostbackEvent): 
                backdata = dict(parse_qsl(event.postback.data))
                if backdata.get('action') == 'buy':
                    sendBack_buy(event, backdata)
            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

def sendText(event): #文字
    try:
        message = TextSendMessage(
            text = "我是KingSman菜譜機械人 ，\n您好!"                         #自我介紹
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


# def sendImage(event): #圖片
#     try:
#         message = ImageSendMessage(
#             original_content_url = 'https://748c-140-135-112-179.ngrok.io/static/4QfKuz1.png',
#             preview_image_url = 'https://748c-140-135-112-179.ngrok.io/static/4QfKuz1.png'
#         ) 
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


# def sendStick(event): #貼圖
#     try:
#         message = StickerSendMessage(
#             package_id = '446',
#             sticker_id = '1988'
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

# def sendMulti(event): #多項傳送
#     try:
#         message = [  #串列
#             StickerSendMessage(  #貼圖
#                 package_id = '1',
#                 sticker_id = '2'
#             ),
#             TextSendMessage(  #文字
#                 text = "這是Pizza 圖片!"
#             ),
#             ImageSendMessage(   #圖片
#                 original_content_url = 'https://748c-140-135-112-179.ngrok.io/static/4QfKuz1.png',
#                 preview_image_url = 'https://748c-140-135-112-179.ngrok.io/static/4QfKuz1.png'
#             )
#         ]
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendPosition(event): #位置
    try: 
        message = LocationSendMessage(
            title = '中原大學',
            address = '320桃園市中壢區xxx路xx號',
            latitude = 24.957577223811143, #緯度
            longitude = 121.24079785364792 #經度
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendQuickreply(event): #快速選單
    try:
        message = TextSendMessage(
            text = '我推薦的食譜',
            quick_reply = QuickReply(
                items = [
                    QuickReplyButton(
                        action = URIAction(label="酸", uri='https://www.518.com.tw/article/1850')
                    ),
                    QuickReplyButton(
                        action = URIAction(label="甜", uri='https://icook.tw/recipes/409877')
                    ),
                    QuickReplyButton(
                        action = URIAction(label="苦", uri='https://zineblog.com.tw/blog/post/210528')
                    ),
                    QuickReplyButton(
                        action = URIAction(label="辣", uri='https://www.wecook123.com/recipe633/')
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))


# def sendVoice(event): #聲音
#     try:
#         message = AudioSendMessage(
#             original_content_url='https://748c-140-135-112-179.ngrok.io/static/mario.m4a',
#             duration=20000
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

# def sendVideo(event): #影片
#     try:
#         message = VideoSendMessage(
#             original_content_url='https://748c-140-135-112-179.ngrok.io/static/robot.mp4',
#             preview_image_url='https://748c-140-135-112-179.ngrok.io/static/robot.jpg'
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendButton(event): # 按鈕
    try:
        message = TemplateSendMessage(
            alt_text='今日推薦',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.unileverfoodsolutions.tw/dam/global-ufs/mcos/na/taiwan/calcmenu/recipes/TW-recipes/general/%E5%8E%9F%E6%B1%81%E7%B4%85%E7%87%92%E7%89%9B%E8%82%89%E9%BA%B5/main-header.jpg', # 菜式圖片的URL
                title='今日推薦的菜式', # 主標題
                text='原汁紅燒牛肉麵:', # 副標題
                actions=[
                    URITemplateAction( # 開啟網頁
                        label='查看食譜',
                        uri='https://www.unileverfoodsolutions.tw/recipe/%E5%8E%9F%E6%B1%81%E7%B4%85%E7%87%92%E7%89%9B%E8%82%89%E9%BA%B5-R0078210.html',
                    ),
                    URITemplateAction( # 開啟網頁
                        label='查看教學影片',
                        uri='https://youtu.be/0NZvuPH1D60',
                    ),
                    URITemplateAction( # 開啟網頁
                        label='購買食譜',
                        uri='https://www.books.com.tw/products/0010943417',
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


# def sendPizza(event):
#     try:
#         message = TextSendMessage(
#             text = '感謝您購買披薩，我們將盡快為您製作-'
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

# def sendBack_buy(event, backdata): #處理Poskback
#     try:
#         text1 = '感謝您購買披薩，'
#         text1 += '\n我們將盡快為您製作。'
#         message = TextSendMessage(
#             text = text1
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

# def sendConfirm(event): #確認樣板
#     try:
#         message = TemplateSendMessage(
#             alt_text = '確認樣板',
#             template = ConfirmTemplate(
#                 text = '你確定要購買這項商品嗎?',
#                 actions=[
#                     MessageTemplateAction(
#                         label='是',
#                         text='@yes'
#                     ),
#                     MessageTemplateAction(
#                         label='否',
#                         text='@no'
#                     )
#                 ]
#             )
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

# def sendYes(event):
#     try:
#         message = TextSendMessage(
#             text = '感謝你的購買，\n我們將盡快送出商品。',
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

# def sendNo(event):
#     try:
#         message = TextSendMessage(
#             text = '沒關係，\n請您重新操作。',
#         )
#         line_bot_api.reply_message(event.reply_token,message)
#     except:
#         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text = '轉盤樣板',
            template = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://images.1111.com.tw/media/share/81/81fcb807dc594abd88c62486420ba772.jpg',
                        title = '酸',
                        text = '讓你的味蕾充滿酸爽的刺激！🍋🥝🍅😋',
                        actions=[
                            URITemplateAction(
                                label='川味酸菜魚🐟',
                                uri='https://www.518.com.tw/article/1850'
                            ),
                             URITemplateAction(
                                label='泰式酸辣蝦湯🍤',
                                uri='https://icook.tw/recipes/105640'
                            ),
                             URITemplateAction(
                                label='酸豆角炒牛肉 🍖',
                                uri='https://udn.com/umedia/story/12919/4914240'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://tokyo-kitchen.icook.network/uploads/recipe/cover/375227/2f5f0e2d8f577a65.jpg',
                        title = '甜',
                        text = '🍍🍍🍍🍍🍍🍍🍍🍍🍍！',
                        actions=[
                            URITemplateAction(
                                label='左宗棠雞🐔🥡',
                                uri='https://icook.tw/recipes/409877'
                            ),
                             URITemplateAction(
                                label='蜜汁叉燒黯然銷魂飯🍚🍖😍😘🥰',
                                uri='https://icook.tw/recipes/422000'
                            ),
                             URITemplateAction(
                                label='菠蘿比薩🍍',
                                uri='https://home.meishichina.com/recipe-405923.html'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i0.wp.com/www.mrspskitchen.net/wp-content/uploads/20170427-_TDP0167.jpg',
                        title = '苦',
                        text = '挑戰你的味蕾，感受苦味的刺激！以下是一些苦味十足的菜式推薦！😖🥬🍵💥',
                        actions=[
                            URITemplateAction(
                                label='苦瓜炒蛋🤮',
                                uri='https://icook.tw/recipes/214346'
                            ),
                             URITemplateAction(
                                label='涼拌苦菊🌼',
                                uri='https://icook.tw/recipes/405341'
                            ),
                             URITemplateAction(
                                label='苦茶炒牛肉🥩',
                                uri='https://icook.tw/recipes/37318'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://d3l76hx23vw40a.cloudfront.net/recipe/whk089-107.jpg',
                        title = '辣',
                        text = '燃燒你的味蕾，品味辣味的狂熱！♪(^∇^*)!🌶️🌶️🌶️🌶️🌶️🌶️',
                        actions=[
                            URITemplateAction(
                                label='麻婆豆腐👵',
                                uri='https://icook.tw/recipes/436289'
                            ),
                             URITemplateAction(
                                label='四川麻辣水煮魚🐟',
                                uri='https://icook.tw/recipes/167947'
                            ),
                             URITemplateAction(
                                label='乾燒辣炒蝦仁🦐',
                                uri='https://tasty-note.com/ebitiri/'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendImgCarousel(event):
    try:
        message = TemplateSendMessage(
            alt_text='圖片轉盤樣板',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://cs-f.ecimg.tw/items/DJAO21A900FTSLZ/000001_1670496024.jpg',
                        action=URIAction(
                            label='戈登‧拉姆齊的快速食譜',
                            uri='https://www.books.com.tw/products/0010943417'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://cdn.kobo.com/book-images/8065b67f-4c7c-4922-9694-68bc8bb3c211/353/569/90/False/mess-tin.jpg',
                        action=URIAction(
                            label='Miss Tin✌炊料理',
                            uri='https://www.books.com.tw/products/E050127043'
                        )
                    )
                ]
            )
        )    
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))


def sendFlex(event):
    try:
        bubble = BubbleContainer(
            direction = 'ltr',
            header = BoxComponent(
                layout = 'vertical',
                background_color='#101935',
                contents =[
                    TextComponent(text = 'KS菜譜機械人', color='#F2FDFF', weight='bold', size = 'xxl',),
                ]
            ),
            hero = ImageComponent(
                url='https://ibw.bwnet.com.tw/image/pool/2015/05/c02d89979032306a89ee07d66c70f89f.jpg',   #圖片
                size = 'full',
                aspect_ratio='792:555',
                aspect_mode='cover',
            ),
            body = BoxComponent(
                layout= 'vertical',
                contents=[
                     TextComponent(text = '一個根據你的口味推薦食譜的機器人', size='md'),
                    # BoxComponent(
                    #     layout='baseline',
                    #     margin='md',
                    #     contents=[
                    #         IconComponent(size='lg', url='https://cs-f.ecimg.tw/items/DJAO21A900FTSLZ/000001_1670496024.jpg'),
                    #         TextComponent(text='25   ', size='sm', color='#999999', flex=0),
                    #         IconComponent(size='lg', url='https://cs-f.ecimg.tw/items/DJAO21A900FTSLZ/000001_1670496024.jpg'),
                    #         TextComponent(text='14   ', size='sm', color='#999999', flex=0),
                    #     ]
                    # ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        contents=[
                        SeparatorComponent(color='#0000ff'),
                            BoxComponent(
                                layout='baseline',
                                contents=[
                                    TextComponent(text='營頁時間',color='#aaaaaa', size='sm', flex=2),
                                    TextComponent(text="10:00 - 18:00",color='#666666', size='sm', flex=5),
                                ],
                            ),
                        ],   
                    ),

                    BoxComponent(
                        layout='horizontal',
                        margin='xxl',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                height='sm',
                                action=URIAction(label='電話聯絡',uri='tel:0979600347'),
                            ),
                            ButtonComponent(
                                style='secondary',
                                height='sm',
                                action=URIAction(label='查看網頁',uri="https://icook.tw/")
                            )
                        ]
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Kingsman菜譜機械人 2023',color='#888888', size='sm', align='center'),
                ]
            )
        )
        message = FlexSendMessage(alt_text="彈性",contents=bubble)
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤!'))





