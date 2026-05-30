import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.videoplayer import VideoPlayer

class PremiumSubtitleApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10)
        
        self.add_widget(Label(text="AI Movie Subtitle Creator", font_size=22, size_hint_y=None, height=45))
        
        self.link_input = TextInput(hint_text="အွန်လိုင်း ဗီဒီယိုလင့်ခ် (Link) ထည့်ရန်နေရာ...", multiline=False, size_hint_y=None, height=45)
        self.add_widget(self.link_input)
        
        self.file_chooser = FileChooserIconView(filters=['*.mp4', '*.mkv'])
        self.add_widget(self.file_chooser)
        
        self.status_label = Label(text="ဗီဒီယိုရွေးချယ်ပြီး အောက်ကခလုတ်ကို နှိပ်ပါ", font_size=14, size_hint_y=None, height=35)
        self.add_widget(self.status_label)
        
        self.main_btn = Button(text="🎬 မြန်မာစာတန်းထိုး စတင်ဖန်တီးမည်", size_hint_y=None, height=55, background_color=(0, 0.6, 0.8, 1))
        self.main_btn.bind(on_press=self.upload_to_server)
        self.add_widget(self.main_btn)
        
        self.result_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        self.watch_btn = Button(text="👁️ Watch (ချက်ချင်းကြည့်မယ်)", background_color=(0, 0.7, 0.3, 1))
        self.watch_btn.bind(on_press=self.play_premium_video)
        self.download_btn = Button(text="📥 Download (Hardsub သိမ်းမယ်)", background_color=(0.8, 0.2, 0.2, 1))
        
        self.srt_url = ""
        self.video_source = ""

    def upload_to_server(self, instance):
        selected = self.file_chooser.selection
        video_link = self.link_input.text.strip()
        
        if not selected and not video_link:
            self.status_label.text = "⚠️ ဗီဒီယိုဖိုင် ရွေးပါ သို့မဟုတ် လင့်ခ်ထည့်ပါ"
            return
            
        self.status_label.text = "🚀 ဗီဒီယိုကို Cloud ဆာဗာသို့ ပို့ဆောင်နေပါသည်..."
        SERVER_URL = "https://gradio.live"
        
        try:
            if selected:
                self.video_source = selected
                with open(self.video_source, 'rb') as f:
                    files = {'data': (os.path.basename(self.video_source), f, 'video/mp4')}
                    response = requests.post(SERVER_URL, files=files, timeout=1200)
            
            if response.status_code == 200:
                result_data = response.json()
                self.srt_url = result_data['data']['url']
                self.add_widget(self.result_layout)
                self.result_layout.add_widget(self.watch_btn)
                self.result_layout.add_widget(self.download_btn)
                self.status_label.text = "✅ ပြီးပါပြီ။ Premium Player ဖြင့် ချက်ချင်း ကြည့်ရှုနိုင်ပါပြီ။"
            else:
                self.status_label.text = "❌ ဆာဗာအမှားအယွင်း ရှိပါသည်။"
        except Exception as e:
            self.status_label.text = f"❌ ချိတ်ဆက်မှုမရပါ- {str(e)}"

    def play_premium_video(self, instance):
        self.clear_widgets()
        player = VideoPlayer(source=self.video_source, state='play', options={'allow_stretch': True})
        self.add_widget(player)

class MainApp(App):
    def build(self):
        return PremiumSubtitleApp()

if __name__ == '__main__':
    MainApp().run()
