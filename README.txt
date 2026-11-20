JARVIS MOBILE - UPDATED STARTER

Included:
- Gemini AI chat (API key required)
- Speech input/output (availability depends on Android speech services)
- READ TEXT: paste copied text and let JARVIS read it aloud
- SMS: enter number and message; opens Android SMS app with a draft. YOU must review and tap Send.
- STOP / mute controls
- GitHub Actions APK workflow

SCREEN / NOTIFICATION READING:
This starter APK does not automatically read the screen or intercept notifications. Android requires a properly registered Accessibility Service and/or Notification Listener, explicit user permission, and app-specific implementation. A safe manual method for now:
1) In the app you want to read, select and Copy the text (where supported).
2) Open JARVIS > READ TEXT > paste > READ / SPEAK.

Notification access and screen-control service are NOT enabled in this starter build. Avoid granting accessibility to unknown apps. Android accessibility services can see sensitive screen content; only use a trusted, locally installed app.

BUILD:
1. Extract this ZIP.
2. Upload the folder contents to a GitHub repository (including .github/workflows).
3. Open repository Actions > Build APK > Run workflow (or wait for push build).
4. Download the jarvis-apk artifact from completed workflow.
5. Install APK and allow microphone permission. Add your Gemini API key via SET.

SMS:
Tap SMS, enter phone number and text, then OPEN SMS APP. The SMS app opens with a draft. Review it and send manually. JARVIS does not silently send messages.

Build workflow/config are starter files and have not been validated with a real APK build in this package.
