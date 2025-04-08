
# 🔐 AUTH API-lari - Foydalanuvchi boshqaruvi

Ushbu loyiha Django REST Framework asosida qurilgan **AUTH (Authentication/Authorization)** moduli bilan foydalanuvchilarni boshqarishni ta’minlaydi. Quyidagi funksiyalarni o‘z ichiga oladi:

- ✅ Ro‘yxatdan o‘tish
- ✅ Tasdiqlash kodi yuborish va tekshirish
- ✅ Parol o‘rnatish yoki tiklash
- ✅ Tizimga kirish (JWT tokenlar asosida)
- ✅ Foydalanuvchi ma’lumotlarini ko‘rish va yangilash
- ✅ Admin uchun foydalanuvchilar ro‘yxati

---

## 🌐 Swagger orqali test qilish

URL: [https://manuchehra.pythonanywhere.com/swagger/](https://manuchehra.pythonanywhere.com/swagger/)

Swagger sahifasi orqali barcha endpointlarni to‘g‘ridan-to‘g‘ri sinovdan o‘tkazishingiz mumkin.

---

## 📚 API-lar ro‘yxati va vazifalari

### 1. `POST /auth/register/` – Ro‘yxatdan o‘tish
Foydalanuvchi telefon raqam yoki email orqali ro‘yxatdan o‘tadi.

#### 🧪 JSON so‘rov:
```json
{
  "phone_or_email": "user@example.com",
  "full_name": "Ism Familiya"
}
```
📌 Tasdiqlash kodi yuboriladi.

---

### 2. `POST /auth/confirm/` – Tasdiqlash kodi yuborish
Foydalanuvchi yuborilgan kod va parolni kiritadi.

#### 🧪 JSON so‘rov:
```json
{
  "phone_or_email": "user@example.com",
  "confirmation_code": "123456",
  "password": "YangiParol123!"
}
```
📌 Akkount faollashadi va login qilish mumkin bo‘ladi.

---

### 3. `POST /auth/login/` – Tizimga kirish
Foydalanuvchi login qiladi va JWT tokenlar oladi.

#### 🧪 JSON so‘rov:
```json
{
  "phone_or_email": "user@example.com",
  "password": "YangiParol123!"
}
```

#### 📥 Javob:
```json
{
  "access": "ACCESS_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

---

## 🔄 Parolni tiklash – 3 bosqich

### 4.1 `POST /auth/reset-password/` – Kod yuborish
```json
{
  "phone_or_email": "user@example.com"
}
```

### 4.2 `POST /auth/reset-password-verify/` – Kodni tasdiqlash
```json
{
  "phone_or_email": "user@example.com",
  "confirmation_code": "123456"
}
```

### 4.3 `POST /auth/reset_password_finish/` – Yangi parolni o‘rnatish
```json
{
  "phone_or_email": "user@example.com",
  "new_password": "YangiParol123!"
}
```

📌 Bu uch bosqich "Parolni unutdingizmi?" funksiyasini to‘liq bajaradi.

---

### 5. `GET /auth/user-account/{id}` – Foydalanuvchi ma’lumotlarini olish
- Ma’lumot olish uchun `id` kerak bo‘ladi.
- Token talab qilinadi (Authorization: Bearer ...)

---

### 6. `PUT/PATCH /auth/users-update/` – Profilni yangilash

#### 🧪 JSON so‘rov:
```json
{
  "full_name": "Yangi Ism Familiya"
}
```
- `PUT`: to‘liq yangilaydi.
- `PATCH`: faqat kerakli maydon(lar)ni.

---

### 7. `GET /auth/users-list/` – Foydalanuvchilar ro‘yxati (admin uchun)
Tizimdagi barcha foydalanuvchilar ro‘yxatini olish uchun ishlatiladi. Admin roli kerak.

---

## 🔐 Token ishlatish

Login so‘rovdan keyin sizga quyidagi tokenlar keladi:

```json
{
  "access": "ACCESS_TOKEN",
  "refresh": "REFRESH_TOKEN"
}
```

Token bilan himoyalangan endpointga so‘rov yuborish uchun headerga quyidagicha yoziladi:

```
Authorization: Bearer ACCESS_TOKEN
```

---

## 🧪 Test qilish bo‘yicha tavsiyalar

- [Swagger](https://manuchehra.pythonanywhere.com/swagger/) orqali har bir endpointni sinovdan o‘tkazing.
- `Postman` orqali tokenlar bilan foydalanishni mashq qiling.
- `curl` orqali terminalda ishlatib ko‘ring.

---

## 📎 Qo‘shimcha izoh

Ushbu AUTH moduli istalgan veb-ilova yoki mobil ilovaga qulay qo‘shilishi mumkin. Foydalanuvchilarni ro‘yxatdan o‘tkazish, identifikatsiya qilish va ularni boshqarish jarayonlarini tez va ishonchli avtomatlashtirish imkonini beradi.
