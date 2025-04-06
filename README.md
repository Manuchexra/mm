# 📘 API Documentation — Online Course Platform

Bu loyiha foydalanuvchilarga onlayn kurslar bilan ishlash imkonini beruvchi zamonaviy e-learning backend platformasidir. Ushbu hujjatda barcha mavjud REST API endpointlar, ularning vazifasi va ishlatilishi bayon etilgan.

---

## 🔐 Authentication & User Management

Foydalanuvchilar tizimga ro‘yxatdan o‘tadi, login qiladi va JWT token orqali himoyalangan API’larga murojaat qiladi.

| Method | Endpoint             | Description                         |
|--------|----------------------|-------------------------------------|
| POST   | `/api/auth/register/` | Foydalanuvchi ro‘yxatdan o‘tadi     |
| POST   | `/api/auth/login/`    | JWT token olish (login)             |
| GET    | `/api/auth/profile/`  | Profil ma’lumotlarini ko‘rish       |
| PUT    | `/api/auth/profile/`  | Profilni yangilash                  |

---

## 🎓 Courses API

Kurslar — tizimdagi asosiy o‘quv modullari bo‘lib, har biri bo‘limlar va darslardan iborat. Administratorlar yoki instructor’lar tomonidan boshqariladi.

| Method | Endpoint              | Description                                |
|--------|-----------------------|--------------------------------------------|
| GET    | `/api/courses/`       | Kurslar ro‘yxati                           |
| GET    | `/api/courses/<id>/`  | Kurs tafsiloti                             |
| POST   | `/api/courses/`       | Yangi kurs yaratish                        |
| PUT    | `/api/courses/<id>/`  | Kursni tahrirlash                          |
| DELETE | `/api/courses/<id>/`  | Kursni o‘chirish                           |

---

## 🗂️ Course Categories

Kurslar toifalarga ajratiladi (masalan: Frontend, Backend, Mobile...). Toifalar filter va UI dizaynlar uchun foydali.

| Method | Endpoint            | Description                  |
|--------|---------------------|------------------------------|
| GET    | `/api/categories/`  | Kurs toifalari ro‘yxati      |

---

## 🧩 Sections & Lessons

Kurs ichida mavzular bo‘limlarga ajratiladi. Har bir bo‘limda bir nechta dars (lesson) bo‘ladi. Har bir lesson video, matn yoki har ikkisini o‘z ichiga oladi.

| Method | Endpoint          | Description                         |
|--------|-------------------|-------------------------------------|
| GET    | `/api/sections/`  | Bo‘limlar ro‘yxati                  |
| GET    | `/api/lessons/`   | Darslar ro‘yxati                    |
| POST   | `/api/sections/`  | Bo‘lim yaratish                     |
| POST   | `/api/lessons/`   | Dars yaratish                       |

---

## 🧑‍🎓 Enrollments API

Foydalanuvchi kursga yoziladi va progressi kuzatib boriladi. Har bir dars yakunlanganda foiz hisoblanadi.

| Method | Endpoint                           | Description                                  |
|--------|------------------------------------|----------------------------------------------|
| GET    | `/api/enrollments/`                | Kursga yozilganlar (auth user)               |
| POST   | `/api/enrollments/`                | Kursga yozilish                              |
| GET    | `/api/enrollments/my/`             | Mening kurslarim                             |
| GET    | `/api/enrollments/progress/<id>/`  | Dars progressi (kurs bo‘yicha)               |
| POST   | `/api/enrollments/complete/<id>/`  | Darsni tamomlash                             |

---

## ⭐ Course Reviews API

Foydalanuvchi kursni baholaydi (1-5 yulduz) va izoh qoldiradi. Kurs bahosi foydalanuvchi fikriga qarab aniqlanadi.

| Method | Endpoint                | Description                                 |
|--------|-------------------------|---------------------------------------------|
| GET    | `/api/reviews/`         | Barcha izohlar                              |
| GET    | `/api/reviews/?course=3`| Kursga tegishli izohlar                     |
| POST   | `/api/reviews/`         | Yangi izoh va baho qo‘shish                 |
| PUT    | `/api/reviews/<id>/`    | Izohni yangilash                            |
| DELETE | `/api/reviews/<id>/`    | Izohni o‘chirish                            |

---

## 🔐 Authentication & Permissions

- `JWT` token orqali barcha maxfiy API’lar himoyalangan.
- Token `Authorization: Bearer <access_token>` header orqali yuboriladi.
- `POST`, `PUT`, `DELETE` metodlari uchun token majburiy.
- Ba’zi `GET` API’lar `AllowAny` yoki `IsAuthenticatedOrReadOnly`.

---

## 🚀 Qo‘shiladigan modullar (Rejalashtirilgan)

- ✅ **Wishlist** — Sevimli kurslarni saqlab qo‘yish
- ✅ **Payments** — Kurs uchun to‘lov qilish (Payme, Stripe, Click)
- ✅ **Certificates** — Kurs tugagach avtomatik sertifikat olish
- ✅ **Search/Filter** — Kurslarni izlash va filterlash
- ✅ **Notifications** — Yangi darslar yoki kurs eslatmalari

---

## 📎 Eslatma

- Barcha API'lar `RESTful` tarzda yaratilgan va `ViewSet` / `APIView` arxitekturasi asosida qurilgan.
- Serializers orqali validation va avto-assign ishlari amalga oshirilgan (masalan: `request.user`).

---

```bash
# Misol: Auth login qilish
curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'
