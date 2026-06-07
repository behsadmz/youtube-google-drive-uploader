# 🚀 Google Drive to YouTube Uploader

یک اسکریپت ساده، سریع و قدرتمند برای آپلود مستقیم ویدیوها از **گوگل درایو (Google Drive)** به **یوتیوب (YouTube)** با استفاده از محیط رایگان **Google Colab**. 

بدون نیاز به دانلود ویدیوها روی سیستم شخصی و بدون مصرف ترافیک اینترنت شما؛ همه‌چیز در سرورهای ابری و پرسرعت گوگل انجام می‌شود.

---

## ✨ ویژگی‌های کلیدی

* ⚡ **سرعت گیگابیتی:** انتقال مستقیم اطلاعات بین سرورهای گوگل.
* 📦 **آپلود گروهی (Batch Upload):** آپلود خودکار تمام ویدیوهای موجود در یک پوشه.
* 🏔️ **پشتیبانی از فایل‌های بسیار حجیم:** جلوگیری از پر شدن حافظه (RAM) با قابلیت ارسال تکه‌تکه (Chunked Upload).
* 🔒 **امنیت بالا:** ویدیوهای شما در ابتدا به صورت کاملاً خصوصی (Private) آپلود می‌شوند.

---

## 🛠 پیش‌نیازها (تنظیمات اولیه)

برای استفاده از این کدها، شما به یک **فایل مجوز دسترسی** (کارت شناسایی گوگل) نیاز دارید. این کار فقط یک بار انجام می‌شود:

1. به [Google Cloud Console](https://console.cloud.google.com/) بروید.
2. یک پروژه جدید بسازید و **YouTube Data API v3** را فعال (Enable) کنید.
3. از منوی سمت چپ به بخش **OAuth consent screen** بروید. در بخش **Test users**، ایمیل کانال یوتیوب خود را اضافه کنید (این کار برای رفع خطای `Error 403: access_denied` الزامی است).
4. به بخش **Credentials** بروید و یک **OAuth client ID** جدید بسازید (نوع Application را روی `Web application` بگذارید).
5. در بخش `Authorized redirect URIs` آدرس `https://google.com` را وارد کنید.
6. فایل را دانلود کنید و نام آن را دقیقاً به `client_secrets.json` تغییر دهید.

---

## 💻 نحوه استفاده در Google Colab

۱. وارد سایت [Google Colab](https://colab.research.google.com/) شوید و یک Notebook جدید بسازید.
۲. از منوی سمت چپ (بخش Files)، روی آیکون **Mount Drive** کلیک کنید تا درایو شما متصل شود.
۳. فایل `client_secrets.json` (که در مرحله قبل ساختید) را در همان منوی سمت چپ آپلود کنید.
۴. یک کادر کد جدید باز کنید و ابزارهای لازم را نصب و اجرا کنید:

```python
!pip install google-api-python-client google-auth-oauthlib google-auth-httplib2
```

۵. **انتخاب و اجرای اسکریپت آپلود:**
حالا یک کادر کد (Code +) جدید در کولب باز کنید. بسته به نیاز خود، **فقط یکی** از کدهای زیر را کپی کرده و اجرا کنید:

🔹 **حالت اول: آپلود یک ویدیوی معمولی**
این حالت برای ویدیوهای روزمره و زیر ۸ گیگابایت بسیار سریع و مناسب است. در خطوط اول کد، آدرس ویدیوی خود در گوگل درایو را قرار دهید و دکمه Play را بزنید:

```python
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow

video_path = "/content/drive/MyDrive/video.mp4" # مسیر ویدیوی شما
video_title = "Your Video Title"
video_description = "Uploaded via Colab"

flow = Flow.from_client_secrets_file('client_secrets.json', scopes=['[https://www.googleapis.com/auth/youtube.upload](https://www.googleapis.com/auth/youtube.upload)'], redirect_uri='[https://google.com](https://google.com)')
auth_url, _ = flow.authorization_url(prompt='consent')
print("1. Verify here:", auth_url)
code = input("\n2. Paste code: ")
flow.fetch_token(code=code)

youtube = build('youtube', 'v3', credentials=flow.credentials)
print("Uploading...")

request = youtube.videos().insert(
    part="snippet,status",
    body={"snippet": {"title": video_title, "description": video_description, "categoryId": "22"}, "status": {"privacyStatus": "private"}},
    media_body=MediaFileUpload(video_path)
)
request.execute()
print("✅ Upload completed!")
```

🔹 **حالت دوم: آپلود فایل‌های بسیار حجیم (Chunked)**
اگر ویدیوی شما بسیار سنگین است، این کد فایل را تکه‌تکه (مثلاً تکه‌های ۲۵۶ مگابایتی) به سرور می‌فرستد تا حافظه (RAM) سیستم پر نشود. در این روش، درصد پیشرفت آپلود هم به شما نمایش داده می‌شود:

```python
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow

video_path = "/content/drive/MyDrive/large_video.mp4" # مسیر ویدیوی حجیم
chunk_size_mb = 256 # بهترین سایز برای کولب

flow = Flow.from_client_secrets_file('client_secrets.json', scopes=['[https://www.googleapis.com/auth/youtube.upload](https://www.googleapis.com/auth/youtube.upload)'], redirect_uri='[https://google.com](https://google.com)')
auth_url, _ = flow.authorization_url(prompt='consent')
print("1. Verify here:", auth_url)
code = input("\n2. Paste code: ")
flow.fetch_token(code=code)

youtube = build('youtube', 'v3', credentials=flow.credentials)
media = MediaFileUpload(video_path, chunksize=chunk_size_mb * 1024 * 1024, resumable=True)

request = youtube.videos().insert(
    part="snippet,status",
    body={"snippet": {"title": "Large Video", "categoryId": "22"}, "status": {"privacyStatus": "private"}},
    media_body=media
)

response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Uploading... {int(status.progress() * 100)}%")
print("✅ Large upload completed!")
```

🔹 **حالت سوم: آپلود گروهی یک پوشه کامل (Batch Upload)**
برای زمانی که می‌خواهید چندین ویدیو را با یک کلیک آپلود کنید. آدرس پوشه حاوی ویدیوها را در متغیر `folder_path` قرار دهید. سیستم تمام فایل‌های `.mp4` را پیدا کرده و عنوان فایل را به عنوان اسم ویدیو ثبت می‌کند:

```python
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow

folder_path = "/content/drive/MyDrive/VideoFolder" # مسیر پوشه شما

flow = Flow.from_client_secrets_file('client_secrets.json', scopes=['[https://www.googleapis.com/auth/youtube.upload](https://www.googleapis.com/auth/youtube.upload)'], redirect_uri='[https://google.com](https://google.com)')
auth_url, _ = flow.authorization_url(prompt='consent')
print("1. Verify here:", auth_url)
code = input("\n2. Paste code: ")
flow.fetch_token(code=code)
youtube = build('youtube', 'v3', credentials=flow.credentials)

for file_name in os.listdir(folder_path):
    if file_name.endswith(".mp4"):
        full_path = os.path.join(folder_path, file_name)
        video_title = file_name.replace(".mp4", "")
        print(f"Uploading: {file_name} ...")
        
        request = youtube.videos().insert(
            part="snippet,status",
            body={"snippet": {"title": video_title, "categoryId": "22"}, "status": {"privacyStatus": "private"}},
            media_body=MediaFileUpload(full_path)
        )
        request.execute()
        print(f"✅ Success: {file_name}")
print("✅ All videos uploaded successfully!")
```

---

### 🔑 مرحله نهایی: تایید انتقال
بعد از اجرای هر کدام از کدهای بالا، سیستم از شما یک تاییدیه نهایی می‌خواهد:
1. روی لینکی که در خروجی کولب به شما می‌دهد کلیک کنید.
*(نکته: اگر با صفحه `Google hasn't verified this app` روبرو شدید، روی **Advanced** کلیک کرده و سپس گزینه **(Go to yt (unsafe** را انتخاب کنید).*
2. در صفحه سفیدِ گوگل، کدی که در نوار آدرس (بعد از عبارت `=code`) قرار دارد را کپی کنید.
3. به محیط کولب برگردید، کد را در کادر خالی بچسبانید و دکمه `Enter` کیبورد را بزنید تا انتقال آغاز شود!

---

## ⚠️ نکات بسیار مهم

> **جلوگیری از تبدیل ویدیو به Shorts:** یوتیوب ویدیوهای عمودی را به طور خودکار به عنوان "شورت ویدیو" می‌شناسد. اگر می‌خواهید ویدیو به صورت معمولی آپلود شود، قبل از آپلود، آن را در یک قاب افقی (نسبت ۱۶:۹) قرار دهید.

> **محدودیت آپلود گروهی:** در روش آپلود گروهی، به دلیل محدودیت‌های روزانه رایگان گوگل (Quota Limit)، مجاز هستید روزانه حدود ۶ ویدیو آپلود کنید. 

---
*ساخته شده برای ساده‌سازی فرآیند انتقال فایل‌های دیجیتال.*
