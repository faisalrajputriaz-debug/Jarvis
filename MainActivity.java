package com.faizan.ai;
import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.provider.Settings;
import android.speech.RecognizerIntent;
import android.speech.tts.TextToSpeech;
import android.view.Gravity;
import android.view.View;
import android.widget.*;
import java.util.*;
public class MainActivity extends Activity {
 private TextView status; private TextToSpeech tts; private static final int SPEECH=9;
 public void onCreate(Bundle b){super.onCreate(b);
  tts=new TextToSpeech(this,s->{if(s==TextToSpeech.SUCCESS)tts.setLanguage(new Locale("ur","PK"));});
  LinearLayout l=new LinearLayout(this); l.setOrientation(1); l.setPadding(24,40,24,24); l.setBackgroundColor(0xFF071426);
  TextView h=new TextView(this); h.setText("FAIZAN AI"); h.setTextSize(30); h.setTextColor(0xFF55C7FF); h.setGravity(Gravity.CENTER); l.addView(h);
  status=new TextView(this); status.setTextColor(-1); status.setTextSize(17); status.setPadding(8,28,8,28); status.setText("Assalam-o-alaikum! Main Faizan AI hoon."); l.addView(status);
  button(l,"Voice Command",v->voice());
  button(l,"Latest WhatsApp Message",v->{String s=MyNotificationListener.sender,m=MyNotificationListener.message;say(s.isEmpty()?"Koi notification preview available nahi.":s+" ka message: "+m);});
  button(l,"Enable Notification Access",v->startActivity(new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS)));
  button(l,"Enable Screen Reading",v->startActivity(new Intent(Settings.ACTION_ACCESSIBILITY_SETTINGS)));
  button(l,"Read Visible Screen Text",v->say(MyAccessibilityService.screenText.isEmpty()?"Screen text available nahi.":MyAccessibilityService.screenText));
  ScrollView sv=new ScrollView(this); sv.addView(l); setContentView(sv);
  if(android.os.Build.VERSION.SDK_INT>=33 && checkSelfPermission("android.permission.POST_NOTIFICATIONS")!=0) requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"},2);
  if(checkSelfPermission("android.permission.RECORD_AUDIO")!=0) requestPermissions(new String[]{"android.permission.RECORD_AUDIO"},3);
 }
 void button(LinearLayout l,String s,View.OnClickListener c){Button b=new Button(this);b.setText(s);l.addView(b);b.setOnClickListener(c);}
 void voice(){Intent i=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);i.putExtra(RecognizerIntent.EXTRA_LANGUAGE,"ur-PK");try{startActivityForResult(i,SPEECH);}catch(Exception e){say("Voice recognition available nahi.");}}
 protected void onActivityResult(int q,int r,Intent d){super.onActivityResult(q,r,d);if(q==SPEECH&&r==RESULT_OK&&d!=null){ArrayList<String>a=d.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);if(a!=null&&!a.isEmpty()){String x=a.get(0).toLowerCase(Locale.ROOT);if(x.contains("message")||x.contains("msg"))say(MyNotificationListener.sender+" ka message: "+MyNotificationListener.message);else if(x.contains("screen"))say(MyAccessibilityService.screenText);else say("Aap ne kaha: "+a.get(0));}}}
 void say(String s){status.setText(s);if(tts!=null)tts.speak(s,TextToSpeech.QUEUE_FLUSH,null,"faizan");}
 protected void onDestroy(){if(tts!=null){tts.stop();tts.shutdown();}super.onDestroy();}
}
