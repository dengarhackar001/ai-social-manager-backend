AI Social Manager Backend (পরীক্ষামূলক)

1) Python 3.10+ সার্ভারে backend ফোল্ডার আপলোড করো।
2) pip install -r requirements.txt
3) সার্ভারের environment variables-এ OPENAI_API_KEY এবং চাইলে OPENAI_MODEL সেট করো। .env.example কেবল নমুনা; production-এ secret manager/environment ব্যবহার করো।
4) চালাও: uvicorn main:app --host 0.0.0.0 --port 8000
5) HTTPS reverse proxy/domain দিয়ে প্রকাশ করো। Android অ্যাপে শুধু https://your-domain URL বসাবে।
6) /health দিয়ে health check, /generate দিয়ে AI কনটেন্ট তৈরি হবে।

নিরাপত্তা:
- OpenAI API key কখনো Android APK, Java source, Git repository বা ব্যবহারকারীর ফোনে রাখবে না।
- Production-এ authentication, rate limiting, usage limits, abuse monitoring এবং HTTPS বাধ্যতামূলক করো।
- এই backend এখনো user login, billing, social platform OAuth বা auto-publishing করে না।
- Model availability/account access অনুযায়ী OPENAI_MODEL পরিবর্তন করতে হতে পারে।
