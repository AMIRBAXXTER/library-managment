<p align="center"><a href="#persian-version">فارسی</a> </p>

---

## **English Version**

---

### **README - Library Management System** 📚

---

## **🏗 Project Introduction**
This project is a simple library management system developed in **Python**, allowing you to efficiently manage information related to users 📇, books 📖, and **loans** 🔄.  
The system architecture is designed with a focus on **clean architecture** and **data security** to provide an optimized experience in managing library resources.

---

## **✨ Features**
### **1. User Management**
- 👩‍💻 Create, edit, and delete users.
- 🔐 User authentication based on username and password.
- 🛡 Security using advanced password hashing algorithms.
- 👑 Ability to assign admin users with special permissions.

### **2. Book Management**
- 📚 Add, edit, and delete books.
- 🔍 Store critical information such as title, author, genre, and ISBN.
- ✅ Manage book availability status (available or unavailable).

### **3. Loan Management**
- 📥 Record loan requests from users.
- 📤 Manage loan status (pending, approved, returned, etc.).
- 🗓 Track key dates like loan request date and return date.

### **4. Advanced Features in Text-Based User Interface**
- 🔄 Navigate back to the previous menu at any time.
- 🔁 Allow repeated selections until the user decides to exit.
- 📜 Neat and readable separators and messages (to enhance clarity during execution and interaction).

### **5. Security and Validation**
- 🛡 Protect sensitive information by hashing passwords using `bcrypt`.
- 🏅 Enforce strong password validation (minimum 8 characters, including uppercase, lowercase, numbers, and special characters).
- 🚫 Prevent duplicate entries for users or books.

### **6. Persistent Data Management**
- 💽 Manage data using a lightweight JSON-based database.
- ♾️ Use the **Singleton Pattern** to ensure data consistency during runtime.
- 💾 Automatically save data securely when closing the program.

---

## **🗂 Project Structure**
The structure is neatly and systematically designed to make code maintenance and development easier:
```
Library Management System/
│
├── config.py           # Default settings like admin credentials and separators
├── main.py             # Entry point of the program
├── models.py           # Information models for users, books, and loans
├── controllers.py      # Management controllers
├── json_database.py    # JSON database for accessing and managing data
├── utils.py            # Utilities (hashing, validation, etc.)
└── menu.py             # Main menu system for user interactions
```

---

## **⚙️ Requirements**
1. Install **Python 3.8** or later:  
   To download Python: [Download Python](https://www.python.org/downloads/)
2. Install the required libraries:  
   To run the program, install the following dependencies:  
   ```bash
   pip install bcrypt
   ```

---

## **🚀 How to Run the Project**
1. **Program Execution:**  
   Run the program using the following command:  
   ```bash
   python main.py
   ```

2. **Access the Program Interface:**  
   - Use the following default credentials to log in:
     - **Username:** `admin`
     - **Password:** `admin`

3. **Data Management:**  
   - Use the program's simple yet powerful menu to perform various operations, such as adding users, registering books, or managing loans.

---

## **⚠️ Important Security Notes**
- Make sure to change the default admin password (`admin`) after the first run.
- Sensitive information like passwords is only stored in hashed form in the system, ensuring complete security.

---

<p align="center"> <a href="#english-version">English</a>
</p>
---

## **Persian Version**

---

### **README - سیستم مدیریت کتابخانه** 📚

---

## **🏗 معرفی پروژه**
این پروژه یک سیستم مدیریت کتابخانه ساده است 
و با زبان Python توسعه داده شده است و به شما این امکان را می‌دهد تا اطلاعات مربوط به کاربران 📇، کتاب‌ها 📖 و امانت‌ها 🔄 را به خوبی مدیریت کنید.  
ساختار این سیستم با تمرکز بر **معماری تمیز** و **امنیت داده‌ها** طراحی شده تا تجربه‌ای بهینه از مدیریت منابع کتابخانه برای شما فراهم کند.

---

## **✨ ویژگی‌های پروژه**
### **1. مدیریت کاربران**
- 👩‍💻 امکان ایجاد، ویرایش و حذف کاربران.
- 🔐 احراز هویت کاربران بر اساس نام کاربری و رمز عبور.
- 🛡 امنیت با استفاده از الگوریتم‌های پیشرفته هش رمز عبور.
- 👑 قابلیت تعیین کاربران مدیر (Admin) با دسترسی‌های خاص.

### **2. مدیریت کتاب‌ها**
- 📚 قابلیت افزودن، ویرایش و حذف کتاب‌ها.
- 🔍 ذخیره اطلاعات مهمی مانند عنوان، نویسنده، ژانر و کد شابک (ISBN).
- ✅ بررسی و مدیریت وضعیت دسترسی (موجود یا ناموجود).

### **3. مدیریت امانت‌ها**
- 📥 ثبت درخواست امانت توسط کاربران.
- 📤 مدیریت وضعیت امانت (در حال انتظار، تأیید شده، بازگشتی و ...).
- 🗓 ثبت تاریخ‌های کلیدی مانند تاریخ درخواست و بازگشت کتاب.

### **4. امکانات پیشرفته در رابط کاربری متنی**
- 🔄 قابلیت برگشت به منوی قبلی در هر زمان.
- 🔁 امکان انتخاب چندباره بین گزینه‌ها تا زمانی که کاربر خارج شود.
- 📜 پیام‌ها و جداساز‌های زیبا و خوانا (برای وضوح بیشتر اجرا و پیام‌ها).

### **5. امنیت و اعتبارسنجی**
- 🛡 محافظت از اطلاعات حساس با استفاده از هش کردن رمز عبور از طریق `bcrypt`.
- 🏅 اعتبارسنجی رمز عبور با استانداردهای بالا (حداقل 8 کاراکتر، ترکیب حروف بزرگ، کوچک، اعداد و کاراکترهای خاص).
- 🚫 جلوگیری از ثبت کاربران یا کتاب‌های تکراری.

### **6. ذخیره‌سازی و مدیریت پایدار داده‌ها**
- 💽 مدیریت داده‌ها با پایگاه‌داده‌ی سبک JSON.
- ♾️ استفاده از **الگوی Singleton** برای یکپارچگی در طول اجرا.
- 💾 ذخیره خودکار و مطمئن اطلاعات هنگام بستن برنامه.

---

## **🗂 ساختار پروژه**
به طور منظم و تمیز طراحی شده است تا توسعه و نگهداری کد آسان‌تر باشد:
```
Library Management System/
│
├── config.py           # تنظیمات پیش‌فرض مانند ادمین و جداکننده‌ها
├── main.py             # نقطه شروع برنامه
├── models.py           # مدل‌های اطلاعاتی کاربران، کتاب‌ها و امانت‌ها
├── controllers.py      # کنترلرهای مدیریتی
├── json_database.py    # پایگاه‌داده JSON و دسترسی به داده‌ها
├── utils.py            # ابزارهای کمکی (هش، اعتبارسنجی و ...)
└── menu.py             # سیستم منوی اصلی برای تعامل با کاربر
```

---

## **⚙️ پیش‌نیازها**
1. نصب **پایتون 3.8** یا بالاتر:  
   برای نصب پایتون: [دانلود پایتون](https://www.python.org/downloads/)
2. نصب کتابخانه‌های موردنیاز:  
   برای اجرای برنامه، باید وابستگی‌های زیر را نصب کنید:  
   ```bash
   pip install bcrypt
   ```

---

## **🚀 آموزش اجرای پروژه**
1. **کلید اجرای برنامه:**  
   با دستور زیر برنامه را اجرا کنید:  
   ```bash
   python main.py
   ```

2. **ورود به محیط برنامه:**  
   - از اطلاعات پیش‌فرض زیر برای ورود استفاده کنید:
     - **نام کاربری:** `admin`
     - **رمز عبور:** `admin`

3. **مدیریت داده‌ها:**  
   - از منوی ساده اما قدرتمند برنامه برای انجام عملیات مختلف، مانند افزودن کاربر، ثبت کتاب یا مدیریت امانت‌ها استفاده کنید.

---

## **⚠️ نکات امنیتی مهم**
- حتماً پس از اولین اجرا، رمز عبور پیش‌فرض مدیر (`admin`) را تغییر دهید.
- اطلاعات حساس مانند رمز عبور، تنها به صورت هش شده در سیستم ذخیره می‌شود؛ بنابراین کاملاً امن هستند.

---