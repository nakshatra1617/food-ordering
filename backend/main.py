from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection
from models import PlaceOrder, CustomerCreate, SignupModel, LoginModel
import bcrypt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# RESTAURANTS
# ─────────────────────────────────────────

@app.get("/restaurants")
def get_restaurants():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM restaurants")
    data = cursor.fetchall()
    conn.close()
    return data


# ─────────────────────────────────────────
# MENU ITEMS
# ─────────────────────────────────────────

@app.get("/menu/{restaurant_id}")
def get_menu(restaurant_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM menu_items WHERE restaurant_id = %s AND is_available = TRUE",
        (restaurant_id,)
    )
    data = cursor.fetchall()
    conn.close()
    return data


# ─────────────────────────────────────────
# CUSTOMERS
# ─────────────────────────────────────────

@app.post("/customers")
def create_customer(customer: CustomerCreate):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO customers (name, email, phone, address) VALUES (%s, %s, %s, %s)",
            (customer.name, customer.email, customer.phone, customer.address)
        )
        conn.commit()
        return {"message": "Customer created", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


# ─────────────────────────────────────────
# PLACE ORDER
# ─────────────────────────────────────────

@app.post("/orders")
def place_order(order: PlaceOrder):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        total = 0

        for item in order.items:
            cursor.execute("SELECT price FROM menu_items WHERE id = %s", (item.menu_item_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
            total += result["price"] * item.quantity

        cursor.execute(
            "INSERT INTO orders (customer_id, restaurant_id, total_amount) VALUES (%s, %s, %s)",
            (order.customer_id, order.restaurant_id, total)
        )
        order_id = cursor.lastrowid

        for item in order.items:
            cursor.execute("SELECT price FROM menu_items WHERE id = %s", (item.menu_item_id,))
            price = cursor.fetchone()["price"]
            cursor.execute(
                "INSERT INTO order_items (order_id, menu_item_id, quantity, price_at_order) VALUES (%s, %s, %s, %s)",
                (order_id, item.menu_item_id, item.quantity, price)
            )

        conn.commit()
        return {"message": "Order placed successfully!", "order_id": order_id, "total": total}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# ─────────────────────────────────────────
# GET ORDER HISTORY
# ─────────────────────────────────────────

@app.get("/orders/{customer_id}")
def get_orders(customer_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT o.id as order_id, o.status, o.total_amount, o.created_at,
               r.name as restaurant_name
        FROM orders o
        JOIN restaurants r ON o.restaurant_id = r.id
        WHERE o.customer_id = %s
        ORDER BY o.created_at DESC
    """, (customer_id,))

    orders = cursor.fetchall()

    for order in orders:
        cursor.execute("""
            SELECT mi.name, oi.quantity, oi.price_at_order
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE oi.order_id = %s
        """, (order["order_id"],))
        order["items"] = cursor.fetchall()

    conn.close()
    return orders


# ─────────────────────────────────────────
# SIGNUP
# ─────────────────────────────────────────

@app.post("/signup")
def signup(data: SignupModel):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM customers WHERE email = %s", (data.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO customers (name, email, phone, address, password) VALUES (%s, %s, %s, %s, %s)",
            (data.name, data.email, data.phone, data.address, hashed.decode("utf-8"))
        )
        conn.commit()
        return {"message": "Account created successfully!", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()


# ─────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────

@app.post("/login")
def login(data: LoginModel):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM customers WHERE email = %s", (data.email,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="Email not found")

        if not bcrypt.checkpw(data.password.encode("utf-8"), user["password"].encode("utf-8")):
            raise HTTPException(status_code=401, detail="Incorrect password")

        return {
            "message": "Login successful",
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()



'''
## After updating both files:

Your terminal running uvicorn will **auto-reload** since we used `--reload` flag. You'll see:
```
WARNING:  StatReload detected changes in 'main.py'. Reloading...
INFO:     Application startup complete.'''