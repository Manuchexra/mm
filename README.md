📘 API HUJJATI — Online Course Platform
Bu loyiha — foydalanuvchilarga onlayn kurslarni ko‘rish, yozilish, darslarni yakunlash, reyting berish va kurslar bilan interaktiv ishlash imkonini beruvchi backend tizimdir. Ushbu hujjatda mavjud barcha REST API endpointlar va ularning vazifalari keltirilgan.

🔐 AUTHENTICATION & USER MANAGEMENT
📌 Vazifasi:
Foydalanuvchi ro‘yxatdan o‘tadi

Login qiladi va JWT token oladi

Profil ma’lumotlarini yangilaydi

Method	Endpoint	Description
POST	/api/auth/register/	Ro‘yxatdan o‘tish
POST	/api/auth/login/	JWT token olish
GET	/api/auth/profile/	Profilni ko‘rish (token kerak)
PUT	/api/auth/profile/	Profilni tahrirlash (token kerak)
🎓 COURSES — Kurslar boshqaruvi
📌 Vazifasi:
Kurslar yaratish, ko‘rish, yangilash

Kurs ichidagi bo‘lim va darslarni strukturalash

Frontend'da asosiy kontent manbasi sifatida ishlatiladi

Method	Endpoint	Description
GET	/api/courses/	Kurslar ro‘yxati
GET	/api/courses/<id>/	Kurs tafsiloti
POST	/api/courses/	Yangi kurs yaratish (instructor)
PUT	/api/courses/<id>/	Kursni tahrirlash
DELETE	/api/courses/<id>/	Kursni o‘chirish
🗂️ CATEGORIES — Kurs Toifalari
📌 Vazifasi:
Kurslarni toifalarga ajratish (Frontend, Backend, Mobile, Design...)

Filterlash va izlash uchun ishlatiladi

Method	Endpoint	Description
GET	/api/categories/	Toifalar ro‘yxati
🧩 SECTIONS & LESSONS — Kurs tuzilmasi
📌 Vazifasi:
Kurslarni mavzular (bo‘lim) va darslar (lesson) bo‘yicha strukturalash

Har bir darsda video yoki kontent bo‘lishi mumkin

Method	Endpoint	Description
GET	/api/sections/	Bo‘limlar ro‘yxati
GET	/api/lessons/	Darslar ro‘yxati
POST	/api/sections/	Kursga bo‘lim qo‘shish
POST	/api/lessons/	Bo‘limga dars qo‘shish
🧑‍🎓 ENROLLMENTS — Kursga yozilish va progress
📌 Vazifasi:
Foydalanuvchi kursga yoziladi (purchase bo‘lishi mumkin)

Har bir dars uchun yakun holati kuzatiladi (progress tracking)

Foydalanuvchi progressiga qarab sertifikat chiqarish mumkin

Method	Endpoint	Description
GET	/api/enrollments/	Mening yozilgan kurslarim
POST	/api/enrollments/	Kursga yozilish
GET	/api/enrollments/my/	Foydalanuvchining kurslari
GET	/api/enrollments/progress/<id>/	Kursdagi darslar progressi
POST	/api/enrollments/complete/<id>/	Darsni yakunlash
⭐ REVIEWS — Izoh va baho
📌 Vazifasi:
Foydalanuvchi kursga reyting (yulduz) va izoh qoldiradi

Kurs o‘rtacha bahosini aniqlash uchun ishlatiladi

Faqat kursga yozilgan foydalanuvchilar izoh qoldiradi

Method	Endpoint	Description
GET	/api/reviews/	Barcha izohlar
GET	/api/reviews/?course=3	Muayyan kursga izohlar
POST	/api/reviews/	Izoh + reyting berish (token kerak)
PUT	/api/reviews/<id>/	Izohni yangilash
DELETE	/api/reviews/<id>/	Izohni o‘chirish
🔒 AUTHORIZATION
JWT Authentication ishlatiladi

Authorization: Bearer <access_token> header orqali token yuboriladi

POST, PUT, DELETE uchun token majburiy

GET metodlarining ba'zilari IsAuthenticatedOrReadOnly bo‘lib, token ixtiyoriy

🧭 Kutilayotgan modullar (rejalashtirilgan)
Modul	Tavsifi
📝 Wishlist	Kurslarni saqlab qo‘yish (sevimlilar)
💳 Payments	Kurslar uchun onlayn to‘lov qilish (Payme, Click, Stripe)
📄 Certificates	Tugallangan kurslar uchun PDF sertifikat
🔔 Notifications	Yangi darslar yoki kurs yangiliklari uchun xabarnoma
🔍 Filters & Search	Kurslarni kategoriya, baho, kalit so‘z bo‘yicha filterlash