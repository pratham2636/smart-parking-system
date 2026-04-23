from flask import Flask, render_template, request, redirect, session
import mysql.connector
import threading
import time
from flask import flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret"


# ---------------- DB CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="tiger",
        database="smart_parking"
    )
#-----------UPDATE EXPIRED BOOKINGS--------------
def update_expired_bookings():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    current_time = datetime.now()

    # expired bookings fetch
    cursor.execute("""
        SELECT * FROM bookings
        WHERE end_time < %s AND status='active'
    """, (current_time,))

    expired = cursor.fetchall()

    for b in expired:
        # status update
        cursor.execute("""
            UPDATE bookings 
            SET status='expired'
            WHERE id=%s
        """, (b['id'],))

        # 🔥 SLOT FREE KARO
        cursor.execute("""
            UPDATE parking 
            SET available_slots = available_slots + 1
            WHERE id=%s
        """, (b['parking_id'],))

    db.commit()

    cursor.close()
    db.close()

#-----------BACKGROUND EXPIRY CHECK---------------------
def background_expiry_checker():
    while True:
        try:
            update_expired_bookings()
            print("✅ Auto expiry check done")
        except Exception as e:
            print("❌ Error in background:", e)

        time.sleep(30)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == 'POST':

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # 🔥 VALIDATIONS
        if not name or not email or not password:
            return render_template('register.html', error="All fields required")

        if len(name) < 3:
            return render_template('register.html', error="Name too short")

        if len(password) < 4:
            return render_template('register.html', error="Password must be at least 4 characters")

        db = get_db()
        cursor = db.cursor()

        # 🔥 EMAIL CHECK
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing = cursor.fetchone()

        if existing:
            return render_template('register.html', error="Email already registered")

        # INSERT
        cursor.execute(
            "INSERT INTO users (name,email,password,role) VALUES (%s,%s,%s,%s)",
            (name, email, password, 'user')
        )
        db.commit()
        flash("Registered successfully!", "success")
        return redirect('/login')

    return render_template('register.html')


# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            db = get_db()
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM users WHERE email=%s AND password=%s",
                (email, password)
            )
            user = cursor.fetchone()

            cursor.close()
            db.close()

            if user:
                session['user_id'] = user['id']
                session['role'] = user['role']
                session['user_name'] = user['name']  # 🔥 ADD THIS

                return redirect('/parkings')
            else:
                return "Invalid Login"

        except Exception as e:
            return f"Error: {e}"

    return render_template('login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # 🔥 only admin login
        cursor.execute("""
            SELECT * FROM users 
            WHERE email=%s AND password=%s AND role='admin'
        """, (email, password))

        admin = cursor.fetchone()

        cursor.close()
        db.close()

        if admin:
            session['user_id'] = admin['id']
            session['role'] = admin['role']
            session['user_name'] = admin['name']

            return redirect('/admin')
        else:
            return "❌ Invalid Admin Login"

    return render_template('admin_login.html')

# ---------------- PARKINGS ----------------
@app.route('/parkings')
def parkings():
    if 'user_id' not in session:
        return redirect('/login')

    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM parking")
        data = cursor.fetchall()

        cursor.close()
        db.close()

        return render_template('parkings.html', data=data)

    except Exception as e:
        return f"Error: {e}"


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#----------ADMIN------------------
@app.route('/admin')
def admin():

    if 'user_id' not in session or session.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor(dictionary=True)

    # total users
    cursor.execute("SELECT COUNT(*) as total FROM users WHERE role='user'")
    users = cursor.fetchone()['total']

    # total bookings
    cursor.execute("SELECT COUNT(*) as total FROM bookings")
    bookings = cursor.fetchone()['total']

    # active bookings
    cursor.execute("SELECT COUNT(*) as total FROM bookings WHERE status='active'")
    active = cursor.fetchone()['total']

    # expired bookings
    cursor.execute("SELECT COUNT(*) as total FROM bookings WHERE status='expired'")
    expired = cursor.fetchone()['total']

    # revenue
    cursor.execute("SELECT SUM(amount_paid) as total FROM bookings")
    revenue = cursor.fetchone()['total'] or 0

    # parking data
    cursor.execute("SELECT * FROM parking")
    parking = cursor.fetchall()

    # 🔥 USERS LIST (NEW)
    cursor.execute("SELECT id, name, email, role FROM users")
    users_list = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('admin.html',
        users=users,
        bookings=bookings,
        active=active,
        expired=expired,
        revenue=revenue,
        parking=parking,
        users_list=users_list   # 🔥 IMPORTANT
    )

from datetime import datetime, timedelta
import math

@app.route('/book/<int:pid>', methods=['GET','POST'])
def book(pid):

    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        try:
            start = request.form.get('start')
            end = request.form.get('end')

            if not start or not end:
                return "❌ Please select start and end time"

            start_time = datetime.strptime(start, "%Y-%m-%dT%H:%M")
            end_time = datetime.strptime(end, "%Y-%m-%dT%H:%M")

            # ❗ validation
            if end_time <= start_time:
                return "❌ End time must be greater than start time"

            if start_time < datetime.now():
                return "❌ Cannot book in past"

            db = get_db()
            cursor = db.cursor(dictionary=True)

            # 🔥 UPDATE EXPIRED BOOKINGS
            cursor.execute("""
                SELECT * FROM bookings
                WHERE end_time < %s AND status='active'
            """, (datetime.now(),))

            expired = cursor.fetchall()

            for b in expired:
                cursor.execute("""
                    UPDATE bookings 
                    SET status='expired'
                    WHERE id=%s
                """, (b['id'],))

                cursor.execute("""
                    UPDATE parking 
                    SET available_slots = available_slots + 1
                    WHERE id=%s
                """, (b['parking_id'],))

            # 🔹 parking fetch
            cursor.execute("SELECT * FROM parking WHERE id=%s", (pid,))
            p = cursor.fetchone()

            if not p:
                return "❌ Parking not found"

            # 🔹 slot check
            available_online = p['total_slots'] - p['reserved_slots']

            if p['available_slots'] <= 0 or available_online <= 0:
                return "❌ No slots available"

            # 🔥 SMART SLOT ALLOCATION
            cursor.execute("""
                SELECT slot_no FROM bookings 
                WHERE parking_id=%s AND status='active'
            """, (pid,))

            booked_slots = [b['slot_no'] for b in cursor.fetchall()]

            slot_no = 1
            while slot_no in booked_slots:
                slot_no += 1

            # 🔥 FINAL PRICING LOGIC (₹10 per started hour)
            total_seconds = (end_time - start_time).total_seconds()

            hours = math.ceil(total_seconds / 3600)

            if hours <= 0:
                return "❌ Invalid duration"

            rate_per_hour = 10
            amount = hours * rate_per_hour

            # 🔹 insert booking
            cursor.execute("""
                INSERT INTO bookings 
                (user_id, parking_id, slot_no, start_time, end_time, status, amount_paid)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (
                session['user_id'],
                pid,
                slot_no,
                start_time,
                end_time,
                'active',
                amount
            ))

            # 🔹 update slots
            cursor.execute("""
                UPDATE parking 
                SET available_slots = available_slots - 1 
                WHERE id = %s
            """, (pid,))

            db.commit()

            cursor.close()
            db.close()

            return redirect('/my_bookings')

        except Exception as e:
            return f"❌ Error: {e}"

    return render_template('book.html', pid=pid)

@app.route('/my_bookings')
def my_bookings():

    if 'user_id' not in session:
        return redirect('/login')

    # 👇 MUST (sabse important)
    update_expired_bookings()

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.*, p.name 
        FROM bookings b
        JOIN parking p ON b.parking_id = p.id
        WHERE user_id = %s
    """, (session['user_id'],))

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('my_bookings.html', data=data)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, email, role, phone, created_at 
        FROM users 
        WHERE id=%s
    """, (session['user_id'],))

    user = cursor.fetchone()

    cursor.close()
    db.close()

    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')

        cursor.execute("""
            UPDATE users 
            SET name=%s, phone=%s 
            WHERE id=%s
        """, (name, phone, session['user_id']))

        db.commit()

        return redirect('/profile')

    cursor.execute("SELECT name, phone FROM users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()

    return render_template('edit_profile.html', user=user)

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        old = request.form.get('old')
        new = request.form.get('new')

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT password FROM users WHERE id=%s", (session['user_id'],))
        user = cursor.fetchone()

        if user['password'] != old:
            return "❌ Wrong old password"

        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new, session['user_id']))
        db.commit()

        return redirect('/profile')

    return render_template('change_password.html')

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):

    # 🔐 sirf admin hi delete kare
    if session.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor()

    # ❌ admin delete nahi hona chahiye
    cursor.execute("SELECT role FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    if user and user[0] == 'admin':
        return "Cannot delete admin"

    # ✅ delete user
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect('/admin')

@app.route('/add_parking', methods=['GET', 'POST'])
def add_parking():

    # 🔐 only admin allowed
    if session.get('role') != 'admin':
        return "Access Denied"

    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        total = request.form.get('total')
        reserved = request.form.get('reserved')

        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO parking (name, location, total_slots, reserved_slots, available_slots)
            VALUES (%s,%s,%s,%s,%s)
        """, (name, location, total, reserved, int(total)-int(reserved)))

        db.commit()

        return redirect('/admin')

    return render_template('add_parking.html')

@app.route('/delete_parking/<int:pid>')
def delete_parking(pid):

    if session.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM parking WHERE id=%s", (pid,))
    db.commit()

    return redirect('/admin')

@app.route('/edit_parking/<int:pid>', methods=['GET', 'POST'])
def edit_parking(pid):

    if session.get('role') != 'admin':
        return "Access Denied"

    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        total = int(request.form.get('total'))
        reserved = int(request.form.get('reserved'))

        available = total - reserved

        cursor.execute("""
            UPDATE parking 
            SET total_slots=%s, reserved_slots=%s, available_slots=%s
            WHERE id=%s
        """, (total, reserved, available, pid))

        db.commit()
        return redirect('/admin')

    cursor.execute("SELECT * FROM parking WHERE id=%s", (pid,))
    parking = cursor.fetchone()

    return render_template('edit_parking.html', parking=parking)

from datetime import datetime
import math

@app.route('/payment/<int:pid>', methods=['POST'])
def payment(pid):

    start = request.form.get('start')
    end = request.form.get('end')

    if not start or not end:
        return "❌ Please select time"

    start_time = datetime.strptime(start, "%Y-%m-%dT%H:%M")
    end_time = datetime.strptime(end, "%Y-%m-%dT%H:%M")

    # ❗ validation
    if end_time <= start_time:
        return "❌ Invalid time selection"

    if start_time < datetime.now():
        return "❌ Cannot book in past"

    # 💰 pricing (₹10 per started hour)
    total_seconds = (end_time - start_time).total_seconds()
    hours = math.ceil(total_seconds / 3600)
    amount = hours * 10

    return render_template('payment.html',
        pid=pid,
        start=start,
        end=end,
        amount=amount
    )

@app.route('/confirm_booking/<int:pid>', methods=['POST'])
def confirm_booking(pid):

    if 'user_id' not in session:
        return redirect('/login')

    try:
        start = request.form.get('start')
        end = request.form.get('end')
        amount = int(request.form.get('amount'))
        method = request.form.get('method')

        start_time = datetime.strptime(start, "%Y-%m-%dT%H:%M")
        end_time = datetime.strptime(end, "%Y-%m-%dT%H:%M")

        db = get_db()
        cursor = db.cursor(dictionary=True)

        # 🔥 UPDATE EXPIRED BOOKINGS FIRST
        cursor.execute("""
            SELECT * FROM bookings
            WHERE end_time < %s AND status='active'
        """, (datetime.now(),))

        expired = cursor.fetchall()

        for b in expired:
            cursor.execute("UPDATE bookings SET status='expired' WHERE id=%s", (b['id'],))
            cursor.execute("""
                UPDATE parking 
                SET available_slots = available_slots + 1
                WHERE id=%s
            """, (b['parking_id'],))

        # 🔹 parking fetch
        cursor.execute("SELECT * FROM parking WHERE id=%s", (pid,))
        p = cursor.fetchone()

        if not p:
            return "❌ Parking not found"

        if p['available_slots'] <= 0:
            return "❌ No slots available"

        # 🔥 SLOT ALLOCATION
        cursor.execute("""
            SELECT slot_no FROM bookings 
            WHERE parking_id=%s AND status='active'
        """, (pid,))

        booked_slots = [b['slot_no'] for b in cursor.fetchall()]

        slot_no = 1
        while slot_no in booked_slots:
            slot_no += 1

        # 🔹 insert booking
        cursor.execute("""
            INSERT INTO bookings 
            (user_id, parking_id, slot_no, start_time, end_time, status, amount_paid, payment_method)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            session['user_id'],
            pid,
            slot_no,
            start_time,
            end_time,
            'active',
            amount,
            method
        ))

        # 🔹 update slots
        cursor.execute("""
            UPDATE parking 
            SET available_slots = available_slots - 1
            WHERE id=%s
        """, (pid,))

        db.commit()

        cursor.close()
        db.close()

        return redirect('/my_bookings')

    except Exception as e:
        return f"❌ Error: {e}"


# ---------------- RUN ----------------
if __name__ == '__main__':
    t = threading.Thread(target=background_expiry_checker)
    t.daemon = True
    t.start()

    app.run(debug=True)