# Mobile Order API - Simple & Clean

Fetch user's sales orders with optional status filtering.

---

## 🎯 **ONE Endpoint - Does Everything**

```
POST /api/v1/mobile/orders/my-orders
```

**Features:**
- ✅ Fetch logged-in user's sales orders
- ✅ Filter by single status
- ✅ Filter by multiple statuses
- ✅ Pagination support
- ✅ User isolation (secure)

---

## 🚀 **Installation**

```bash
# Restart Odoo
sudo systemctl restart odoo17

# Then in Odoo:
# Apps → Update Apps List → Search "Mobile Order API" → Install
```

---

## 📋 **Postman Testing**

### **Step 1: Login**

```
POST http://localhost:8069/web/session/authenticate
Content-Type: application/json

Body:
{
  "jsonrpc": "2.0",
  "params": {
    "db": "odoo17",
    "login": "testuser1@example.com",
    "password": "password123"
  }
}
```

**Save `session_id` from response!**

---

### **Step 2: Get All Orders**

```
POST http://localhost:8069/api/v1/mobile/orders/my-orders
Content-Type: application/json
Cookie: session_id=YOUR_SESSION_ID

Body:
{
  "jsonrpc": "2.0",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "success": true,
    "user": "testuser1@example.com",
    "partner": "Test User One",
    "total": 4,
    "count": 4,
    "status_filter": "all",
    "orders": [
      {
        "id": 15,
        "name": "SO015",
        "state": "sale",
        "state_label": "Sales Order",
        "partner_name": "Test User One",
        "amount_total": 1500.0,
        "date_order": "2025-12-14T10:30:00"
      }
    ]
  }
}
```

---

### **Step 3: Filter by Single Status**

```
Body:
{
  "jsonrpc": "2.0",
  "params": {
    "status": "sale"
  }
}
```

**Response:**
```json
{
  "result": {
    "success": true,
    "status_filter": "sale",
    "total": 2,
    "orders": [... only "sale" orders ...]
  }
}
```

---

### **Step 4: Filter by Multiple Statuses**

```
Body:
{
  "jsonrpc": "2.0",
  "params": {
    "status": ["sale", "done"]
  }
}
```

**Response:**
```json
{
  "result": {
    "success": true,
    "status_filter": ["sale", "done"],
    "total": 3,
    "orders": [... "sale" and "done" orders ...]
  }
}
```

---

### **Step 5: Pagination**

```
Body:
{
  "jsonrpc": "2.0",
  "params": {
    "limit": 10,
    "offset": 0
  }
}
```

**Response:**
```json
{
  "result": {
    "total": 25,
    "count": 10,
    "offset": 0,
    "limit": 10,
    "has_more": true,
    "orders": [... first 10 orders ...]
  }
}
```

---

## 📊 **Order Status Values**

| Status | Description |
|--------|-------------|
| `draft` | Quotation |
| `sent` | Quotation Sent |
| `sale` | Sales Order (Confirmed) |
| `cancel` | Cancelled |

---

## 🔐 **Security**

- ✅ Each user sees ONLY their own orders
- ✅ Session-based authentication required
- ✅ Filter by `partner_id` ensures data isolation

**How it works:**
```python
current_user = request.env.user
partner = current_user.partner_id
domain = [('partner_id', '=', partner.id)]  # User's orders only
```

---

## 🧪 **Testing Scenarios**

### **Test 1: User Isolation**
1. Login as User 1 → Get orders
2. Login as User 2 → Get orders
3. ✅ **Expected:** Different orders for each user

### **Test 2: Status Filtering**
1. Get all orders → See all statuses
2. Filter by "sale" → See only "sale" orders
3. Filter by ["sale", "done"] → See both statuses

### **Test 3: Pagination**
1. Set limit=2, offset=0 → Get first 2 orders
2. Set limit=2, offset=2 → Get next 2 orders
3. Check `has_more` field

---

## 📝 **Module Structure**

```
mobile_order_api/
├── __init__.py
├── __manifest__.py
├── README.md
├── controllers/
│   ├── __init__.py
│   └── mobile_order_controller.py  ← 1 endpoint
├── models/
│   └── __init__.py                 ← Empty (no models needed)
└── security/
    └── ir.model.access.csv         ← Empty
```

---

## ✅ **Summary**

- **1 Endpoint:** `/api/v1/mobile/orders/my-orders`
- **Get all orders:** `{}`
- **Filter by status:** `{"status": "sale"}`
- **Multiple statuses:** `{"status": ["sale", "done"]}`
- **Pagination:** `{"limit": 10, "offset": 0}`

**Ready to test in Postman! 🚀**
