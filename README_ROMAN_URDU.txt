FAIZAN AI - NATIVE ANDROID STARTER

ZIP mein native Java Android project + GitHub Actions APK workflow hai.

BUILD:
1) ZIP extract karein.
2) Is ZIP ke andar ke tamam files/folders apni GitHub repository ke ROOT mein upload karein. Hidden .github folder bhi upload hona chahiye.
3) GitHub > Actions > 'Faizan AI APK Build' > Run workflow.
4) Build successful ho to run khol kar Artifacts mein 'Faizan-AI-APK' download karein.
5) ZIP extract karein; app-debug.apk install karein.

APP PERMISSIONS:
App khol kar Enable Notification Access aur Enable Screen Reading buttons dabayein. Android Settings mein Faizan AI ko manually enable karein. Microphone permission allow karein.

FEATURES PRESENT:
- Urdu speech recognition starter + text-to-speech response
- WhatsApp notification preview reader (sender/title + preview)
- Accessibility service starter that reads visible UI text exposed by Android
- GitHub Actions workflow for cloud APK build

LIMITS / HONEST NOTES:
- Ye native starter project hai, complete commercial A-to-Z AI agent nahi.
- AI chat ke liye secure backend aur provider API integration abhi add karni hogi. API key APK mein hardcode na karein.
- WhatsApp reply action detect karne ka helper included hai, lekin app UI mein recipient/draft confirmation flow abhi wire nahi. Reply sirf notification mein inline RemoteInput action ho to possible hai.
- Accessibility cannot read every app, protected screen, password, or secure content. Android permission user khud Settings mein enable kare.
- Screen taps, calls, SMS sending, social media posting, uploads, and background phone control are not implemented; each needs separate permissions, user confirmation, and testing.
- Android/WhatsApp versions aur device restrictions se behavior vary kar sakta hai.

Package: com.faizan.ai
App label: Faizan AI
Minimum Android: 8.0 (API 26)
Compile/Target SDK: 35
