package com.faizan.ai;
import android.accessibilityservice.AccessibilityService;
import android.view.accessibility.*;
public class MyAccessibilityService extends AccessibilityService {
 public static volatile String screenText="";
 public void onAccessibilityEvent(AccessibilityEvent e){AccessibilityNodeInfo root=getRootInActiveWindow();if(root==null)return;StringBuilder b=new StringBuilder();collect(root,b);screenText=b.toString().trim();root.recycle();}
 private void collect(AccessibilityNodeInfo n,StringBuilder b){if(n==null||b.length()>4000)return;CharSequence t=n.getText();if(t!=null&&t.length()>0)b.append(t).append(". ");for(int i=0;i<n.getChildCount();i++){AccessibilityNodeInfo c=n.getChild(i);if(c!=null){collect(c,b);c.recycle();}}}
 public void onInterrupt(){}
}
