import math, os, re, threading, time
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
try:
    from plyer import stt, tts
except Exception:
    stt = tts = None

BG=(0,0.012,0.031,1); PRI=(0,0.831,1,1); TEXT=(0.81,0.91,0.96,1); MUTED=(0.36,0.5,0.55,1); RED=(1,0.3,0.37,1)
DEFAULT_MODEL='gemini-2.0-flash'
Window.clearcolor=BG

def ui(fn,*args): Clock.schedule_once(lambda dt: fn(*args))

class Reactor(Widget):
    def __init__(self,**kw): super().__init__(**kw); self.state='IDLE'; self.angle=0.; self.t=0.; Clock.schedule_interval(self._tick,1/30)
    def _tick(self,dt): self.angle += {'THINKING':3,'SPEAKING':1.6,'LISTENING':1}.get(self.state,.5)*dt; self.t+=dt; self.draw()
    def draw(self):
        self.canvas.clear(); cx,cy=self.center; r=min(self.width,self.height)/2-dp(6)
        if r<=0:return
        col=RED if self.state=='ERROR' else PRI; pulse=1+.05*math.sin(self.t*6) if self.state=='LISTENING' else 1
        with self.canvas:
            Color(*col); Line(circle=(cx,cy,r*pulse),width=dp(2)); Color(col[0],col[1],col[2],.5); Line(circle=(cx,cy,r*.72),width=1); Color(*col)
            for i in range(6):
                a=self.angle+i*math.pi/3; Line(points=[cx+math.cos(a)*r*.3,cy+math.sin(a)*r*.3,cx+math.cos(a)*r*.62,cy+math.sin(a)*r*.62],width=dp(2))
            Ellipse(pos=(cx-r*.13,cy-r*.13),size=(r*.26,r*.26))

class JarvisApp(App):
    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.RECORD_AUDIO,Permission.INTERNET])
        except Exception: pass
        self.store=JsonStore(os.path.join(self.user_data_dir,'jarvis.json')); d=self.store.get('cfg') if self.store.exists('cfg') else {}
        self.cfg={'name':d.get('name','JARVIS'),'key':d.get('key',''),'model':d.get('model',DEFAULT_MODEL),'voice':d.get('voice',True)}
        self.history=[]; self.lines=[]; self.listening=False; self.muted=False
        root=BoxLayout(orientation='vertical',padding=dp(8),spacing=dp(6)); head=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(6))
        self.title=Label(text=self.cfg['name'].upper(),color=TEXT,font_size=dp(20),halign='left',valign='middle'); self.title.bind(size=lambda w,s:setattr(w,'text_size',s))
        self.clock=Label(color=TEXT,font_size=dp(16),size_hint_x=None,width=dp(64)); head.add_widget(self.title); head.add_widget(self.clock); head.add_widget(Button(text='SET',size_hint_x=None,width=dp(52),on_press=lambda *_:self.open_settings())); root.add_widget(head)
        self.reactor=Reactor(size_hint_y=.42); root.add_widget(self.reactor); self.chip=Label(text='IDLE',color=PRI,size_hint_y=None,height=dp(20)); root.add_widget(self.chip)
        self.log_label=Label(text='',color=TEXT,font_size=dp(14),halign='left',valign='top',size_hint_y=None); self.log_label.bind(width=lambda w,v:setattr(w,'text_size',(v,None)),texture_size=lambda w,v:setattr(w,'height',v[1]))
        self.log_scroll=ScrollView(size_hint_y=.38,do_scroll_x=False); self.log_scroll.add_widget(self.log_label); root.add_widget(self.log_scroll)
        bar=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6)); self.input=TextInput(multiline=False,hint_text='Type or speak...'); self.input.bind(on_text_validate=self.send_text); bar.add_widget(self.input); bar.add_widget(Button(text='SEND',size_hint_x=None,width=dp(64),on_press=self.send_text)); self.mic_btn=Button(text='MIC',size_hint_x=None,width=dp(60),on_press=lambda *_:self.toggle_mic()); bar.add_widget(self.mic_btn); root.add_widget(bar)
        row=BoxLayout(size_hint_y=None,height=dp(44),spacing=dp(6)); self.mute_btn=Button(text='MUTE: OFF',on_press=lambda *_:self.toggle_mute()); row.add_widget(self.mute_btn); row.add_widget(Button(text='READ TEXT',on_press=lambda *_:self.open_read_text())); row.add_widget(Button(text='SMS',on_press=lambda *_:self.open_sms())); row.add_widget(Button(text='STOP',on_press=lambda *_:self.stop_speaking())); root.add_widget(row)
        if stt is not None:
            try: stt.bind(on_results=self._on_stt_results)
            except Exception: pass
        Clock.schedule_interval(lambda dt:self._tick_clock(),1); self._tick_clock(); self.log('SYS',f"{self.cfg['name']} online."); return root
    def set_state(self,s): self.reactor.state=s; self.chip.text=s
    def log(self,who,msg): self.lines=(self.lines+[f'{who}: {msg}'])[-200:]; self.log_label.text='\n\n'.join(self.lines); Clock.schedule_once(lambda dt:setattr(self.log_scroll,'scroll_y',0),.1)
    def _tick_clock(self): self.clock.text=time.strftime('%H:%M')
    def send_text(self,*_):
        text=self.input.text.strip()
        if text:self.input.text=''; self.ask(text)
    def ask(self,text): self.log('You',text); self.set_state('THINKING'); threading.Thread(target=self._worker,args=(text,),daemon=True).start()
    def _worker(self,text):
        try:
            if re.search(r'\b(time|waqt)\b',text.lower()): reply=f'Abhi {time.strftime("%H:%M")} hain.'
            elif not self.cfg['key']: raise RuntimeError('SET mein Gemini API key daalein.')
            else: reply=self.gemini(text)
            ui(self.on_reply,reply,True)
        except Exception as e: ui(self.on_reply,str(e) or 'Unknown error',False)
    def gemini(self,text):
        self.history.append({'role':'user','parts':[{'text':text}]})
        try:
            r=requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{self.cfg['model']}:generateContent",params={'key':self.cfg['key']},json={'systemInstruction':{'parts':[{'text':f"You are {self.cfg['name']}, a calm personal AI assistant. Be concise. Reply in the user's language; if they write Roman Urdu, reply in Roman Urdu."}]},'contents':self.history[-20:]},timeout=30)
            j=r.json()
            if not r.ok: raise RuntimeError(j.get('error',{}).get('message',f'HTTP {r.status_code}'))
            reply=''.join(p.get('text','') for p in j['candidates'][0]['content']['parts']) or '(no reply)'
        except Exception: self.history.pop(); raise
        self.history.append({'role':'model','parts':[{'text':reply}]}); del self.history[:-20]; return reply
    def on_reply(self,reply,ok):
        self.log('JARVIS' if ok else 'SYS',reply)
        if ok:self.speak(reply); self.set_state('IDLE')
        else:self.set_state('ERROR'); Clock.schedule_once(lambda dt:self.set_state('IDLE'),2)
    def speak(self,text):
        if self.cfg['voice'] and tts is not None:
            try:tts.speak(text)
            except Exception:pass
    def stop_speaking(self):
        try:tts.stop()
        except Exception:pass
        self.set_state('IDLE')
    def _stop_listening(self):
        try:stt.stop()
        except Exception:pass
        self.listening=False; self.mic_btn.text='MIC'
    def toggle_mic(self):
        if stt is None:return self.log('SYS','Voice input unavailable.')
        if self.muted:return self.log('SYS','Mic muted hai; unmute karein.')
        if self.listening:self._stop_listening(); return self.set_state('IDLE')
        try:stt.start()
        except Exception as e:return self.log('SYS',f'Mic error: {e}')
        self.listening=True; self.mic_btn.text='STOP'; self.set_state('LISTENING')
    def _on_stt_results(self,results,*_):ui(self._stt_done,results)
    def _stt_done(self,results):
        self._stop_listening(); text=results[0] if isinstance(results,(list,tuple)) and results else str(results or '')
        if text.strip():self.ask(text.strip())
        else:self.set_state('IDLE')
    def toggle_mute(self):
        self.muted=not self.muted; self.mute_btn.text='MUTE: ON' if self.muted else 'MUTE: OFF'
        if self.muted and self.listening:self._stop_listening(); self.set_state('MUTED')
        self.log('SYS','Microphone muted.' if self.muted else 'Microphone active.')
    def open_read_text(self):
        box=BoxLayout(orientation='vertical',padding=dp(8),spacing=dp(6)); ti=TextInput(hint_text='Yahan screen se copy kiya hua text paste karein...',multiline=True); box.add_widget(ti)
        row=BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(6)); pop=Popup(title='READ TEXT ALOUD',content=box,size_hint=(.92,.75))
        def read(*_):
            text=ti.text.strip(); pop.dismiss()
            if text:self.log('TEXT',text); self.speak(text)
            else:self.log('SYS','Pehle text paste karein.')
        row.add_widget(Button(text='READ / SPEAK',on_press=read)); row.add_widget(Button(text='CLOSE',on_press=lambda *_:pop.dismiss())); box.add_widget(row); pop.open()
    def open_sms(self):
        box=BoxLayout(orientation='vertical',padding=dp(8),spacing=dp(6)); number=TextInput(hint_text='Phone number',multiline=False); message=TextInput(hint_text='Message text',multiline=True); box.add_widget(number); box.add_widget(message)
        row=BoxLayout(size_hint_y=None,height=dp(46),spacing=dp(6)); pop=Popup(title='OPEN SMS COMPOSER',content=box,size_hint=(.92,.75))
        def launch(*_):
            n=number.text.strip(); m=message.text.strip(); pop.dismiss()
            if not n or not m:return self.log('SYS','Number aur message dono zaroori hain.')
            try:
                from jnius import autoclass
                Intent=autoclass('android.content.Intent'); Uri=autoclass('android.net.Uri'); PythonActivity=autoclass('org.kivy.android.PythonActivity')
                intent=Intent(Intent.ACTION_SENDTO); intent.setData(Uri.parse('smsto:'+n)); intent.putExtra('sms_body',m); PythonActivity.mActivity.startActivity(intent)
                self.log('SYS','SMS composer khul gaya. Send dabane se pehle message check karein.')
            except Exception as e:self.log('SYS','SMS composer launch nahi hua: '+str(e))
        row.add_widget(Button(text='OPEN SMS APP',on_press=launch)); row.add_widget(Button(text='CLOSE',on_press=lambda *_:pop.dismiss())); box.add_widget(row); pop.open()
    def open_settings(self):
        box=BoxLayout(orientation='vertical',padding=dp(10),spacing=dp(6)); fields={}
        for label,key,pw in [('Assistant name','name',False),('Gemini API key','key',True),('Model','model',False)]:
            box.add_widget(Label(text=label,color=MUTED,size_hint_y=None,height=dp(22))); ti=TextInput(text=self.cfg[key],multiline=False,password=pw,size_hint_y=None,height=dp(42)); box.add_widget(ti); fields[key]=ti
        voice_btn=Button(text=f"SPEAK REPLIES: {'ON' if self.cfg['voice'] else 'OFF'}",size_hint_y=None,height=dp(44))
        def toggle_voice(b):self.cfg['voice']=not self.cfg['voice']; b.text=f"SPEAK REPLIES: {'ON' if self.cfg['voice'] else 'OFF'}"
        voice_btn.bind(on_press=toggle_voice); box.add_widget(voice_btn); popup=Popup(title='SETTINGS',content=box,size_hint=(.92,.85))
        def save(*_):
            self.cfg['name']=fields['name'].text.strip() or 'JARVIS'; self.cfg['key']=fields['key'].text.strip(); self.cfg['model']=fields['model'].text.strip() or DEFAULT_MODEL; self.store.put('cfg',**self.cfg); self.title.text=self.cfg['name'].upper(); popup.dismiss(); self.log('SYS','Settings saved.')
        box.add_widget(Button(text='SAVE',size_hint_y=None,height=dp(48),on_press=save)); popup.open()
if __name__=='__main__':JarvisApp().run()
