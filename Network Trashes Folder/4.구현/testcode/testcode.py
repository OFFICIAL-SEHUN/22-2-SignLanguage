import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
import moviepy.editor as mp
import time

cred = credentials.Certificate("signlanguage-51654-firebase-adminsdk-9e2vh-8f2a05112a.json")
firebase_admin.initialize_app(cred,{'databaseURL':'https://signlanguage-51654-default-rtdb.firebaseio.com/'})

config={
    "apiKey": "AIzaSyDLA2C32BLXMZJX8ZAkOhE1asVov0FxD1A",
    "authDomain": "signlanguage-51654.firebaseapp.com",
    "databaseURL": "https://signlanguage-51654-default-rtdb.firebaseio.com",
    "projectId": "signlanguage-51654",
    "storageBucket": "signlanguage-51654.appspot.com",
    "messagingSenderId": "466135386348",
    "appId": "1:466135386348:web:1cd5e74ae320631acabdc9",
    "measurementId": "G-JS1GR4JTQY"
}
firebase=pyrebase.initialize_app(config)
storage = firebase.storage()
################################################################################################################
def storage_down(dl_name,sv_name):
    storage.child(dl_name).download(sv_name+".mp4")

def speech_to_Text(wav_name):
    AUDIO_FILE = 'C:/firebase_python/testcode/'+wav_name+'.wav'
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)
        a="의:"+str(r.recognize_google(audio, language='ko'))
        return a

def stt_udate(num,text):
    ref = db.reference('MAUI')
    ref.update({str(num):text})

def flag_get(vv):
    ref = db.reference(vv+'/flag')
    return ref.get()

def flag_update(a):
    ref = db.reference('voice')
    ref.update({a:0})

def change_file(fl_name):
    clip = mp.VideoFileClip('C:/firebase_python/testcode/'+fl_name+'.mp4')
    clip.audio.write_audiofile(fl_name+".wav")

def title_get():
    ref = db.reference('title')
    return ref.get()

def num_get():
    ref = db.reference('num')
    return ref.get()
    
def num_pp():
    ref = db.reference()
    ref.update({'num':num_get()+1})

################################################################################################################


save_title="test"+str(num_get())

while(True):
    if flag_get("voice")==1:
        title= "Doctor/"+title_get()
        storage_down(title,save_title)
        change_file(save_title)
        stt_udate(num_get(),speech_to_Text(save_title))
        flag_update("voice")
        num_pp()
        save_title="test"+str(num_get())
    if flag_get("video")==1:
        title= "Patient/"+title_get()
        #환자 번역코드가 필요함
        flag_update("video")
        num_pp()
        save_title="test"+str(num_get())  
    time.sleep(1)
    




