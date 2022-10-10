from telegram.ext import Updater, Filters, CommandHandler, MessageHandler
from telegram import Bot, Chat
import cv2
import moviepy.editor as mp
from insightface.app import FaceAnalysis
# from insightface import model_zoo
import os, glob

bot = Bot("5618721223:AAELylaAk2XjZfgB5jKtbVDkVYEcSVvnXn4")


app = FaceAnalysis(name='buffalo_sc', root='./', providers=['CUDAExecutionProvider'], allowed_modules=['detection',])
# app = model_zoo.retinaface.RetinaFace(model_file='models/retina/', providers=['CUDAExecutionProvider'],)
app.prepare(ctx_id=-10, det_thresh=0.2, det_size=(640, 640))


def delete_temp():
    files = glob.glob('temp/*')
    for f in files:
        os.remove(f)

def start(updater, context): 
    updater.message.reply_text("با این بات میتونید عکسای اعتراضات رو غیر قابل شناسایی کنید")
  

def help_(updater, context): 
    updater.message.reply_text("عکس رو ارسال کنید")


def message(updater, context):
    msg = updater.message.text
    print(msg)
    updater.message.reply_text(msg)


def image(updater, context):
    photo = updater.message.photo[-1].get_file()
    photo.download("temp/img.jpg")
    img = cv2.imread("temp/img.jpg")
    faces = app.get(img)
    bboxes = [face['bbox'] for face in faces]

    for e in bboxes:
        img[int(e[1]):int(e[3]), int(e[0]):int(e[2])] = cv2.blur(img[int(e[1]):int(e[3]), int(e[0]):int(e[2])], (50,50))



    cv2.imwrite('temp/new.jpg', img)
    chat_id = updater.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=open('temp/new.jpg', 'rb'))
    delete_temp()

    
def video(updater, context):
    photo = updater.message.video.get_file()
    try:
        photo.download("temp/vid.mp4")
    except:
        updater.message.reply_text("ویدیو باید کمتر از ۲۰ مگابایت باشد یا می‌توانید از طریق لینک گیت از برناهمه استقاده کنید")
        return
    
    cap = cv2.VideoCapture("temp/vid.mp4")

    if (cap.isOpened() == False): 
        print("Error reading video file")

    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # print(fps)
    size = (frame_width, frame_height)

    result = cv2.VideoWriter('temp/out.avi', 
                         cv2.VideoWriter_fourcc('H','2','6','4'),
                         fps, size)

    while True:
        try:
            flag, img = cap.read()
            if flag == True:

                # img = cv2.imread("img.jpg")
                # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                faces = app.get(img)
                bboxes = [face['bbox'] for face in faces]
                # print(len(bboxes), end=", ")
                for e in bboxes:
                    img[int(e[1]):int(e[3]), int(e[0]):int(e[2])] = cv2.blur(img[int(e[1]):int(e[3]), int(e[0]):int(e[2])], (50,50),)

                result.write(img)

              # Break the loop
            else:
                break
        except:
            pass

    cap.release()
    result.release()
    videoclip = mp.VideoFileClip("temp/out.avi")
    audioclip = mp.VideoFileClip("temp/vid.mp4").audio
    videoclip = videoclip.set_audio(audioclip)

    videoclip.write_videofile("temp/out.mp4")
        
    chat_id = updater.message.chat_id

    bot.send_document(chat_id=chat_id, document=open('temp/out.mp4', 'rb'), filename="out.mp4")
    # Bot.send_video(chat_id=chat_id, video=open('out.mp4', 'rb'))
       
    # except Exception as e:
    #     print(e)
    delete_temp()


updater = Updater("5618721223:AAELylaAk2XjZfgB5jKtbVDkVYEcSVvnXn4")
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_))

dispatcher.add_handler(MessageHandler(Filters.text, message))

dispatcher.add_handler(MessageHandler(Filters.photo, image))
dispatcher.add_handler(MessageHandler(Filters.video, video))


updater.start_polling()
updater.idle()