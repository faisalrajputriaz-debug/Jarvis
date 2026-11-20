package com.faizan.ai;
import android.service.notification.*;
import android.app.Notification;
import android.os.Bundle;
import android.content.Intent;
import android.app.RemoteInput;
public class MyNotificationListener extends NotificationListenerService {
 public static volatile String sender="", message="";
 private static volatile Notification.Action replyAction;
 public void onNotificationPosted(StatusBarNotification n){
  if(n==null||n.getNotification()==null||!"com.whatsapp".equals(n.getPackageName()))return;
  Bundle e=n.getNotification().extras;if(e==null)return;
  CharSequence t=e.getCharSequence(Notification.EXTRA_TITLE),m=e.getCharSequence(Notification.EXTRA_TEXT);
  sender=t==null?"":t.toString();message=m==null?"":m.toString();replyAction=null;
  Notification.Action[] aa=n.getNotification().actions;
  if(aa!=null)for(Notification.Action a:aa)if(a!=null&&a.getRemoteInputs()!=null&&a.getRemoteInputs().length>0&&a.actionIntent!=null){replyAction=a;break;}
 }
 // Call only after showing contact + exact draft and user confirms.
 public boolean sendConfirmedReply(String draft){
  Notification.Action a=replyAction;if(a==null||draft==null||draft.trim().isEmpty())return false;
  RemoteInput[] ri=a.getRemoteInputs();Intent fill=new Intent();Bundle b=new Bundle();
  for(RemoteInput x:ri)b.putCharSequence(x.getResultKey(),draft);
  RemoteInput.addResultsToIntent(ri,fill,b);
  try{a.actionIntent.send(this,0,fill);return true;}catch(Exception ex){return false;}
 }
}
