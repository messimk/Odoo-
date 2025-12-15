# Mobile Order API - Postman Testing Guide

## 🎯 **3 API Endpoints - Simple & Clean**

---

## 📡 **API Endpoints**

### **1. Get My Orders (Main Endpoint)**
`POST /api/v1/mobile/orders/my-orders`

**Does everything:**
- Get all orders
- Filter by single status
- Filter by multiple statuses
- Pagination

---

### **2. Subscribe to Notifications**
`POST /api/v1/mobile/notifications/subscribe`

---

### **3. Unsubscribe from Notifications**
`POST /api/v1/mobile/notifications/unsubscribe`

---

## 🚀 **Quick Start**

### **Step 1: Login**
```
POST http://localhost:8069/web/session/authenticate

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

**Copy `session_id` from response!**

---

## 📋 **Endpoint 1: Get My Orders**

### **Use Case 1: Get ALL orders**
```
POST http://localhost:8069/api/v1/mobile/orders/my-orders
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
    "orders": [...]
  }
}
```

---

### **Use Case 2: Get orders by SINGLE status**
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

### **Use Case 3: Get orders by MULTIPLE statuses**
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
    "orders": [... orders with "sale" or "done" status ...]
  }
}
```

---

### **Use Case 4: Pagination**
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

---

### **Use Case 5: Filter by date range**
```
Body:
{
  "jsonrpc": "2.0",
  "params": {
    "status": "sale",
    "date_from": "2025-01-01",
    "date_to": "2025-12-31"
  }
}
```

---

## 🔔 **Endpoint 2: Subscribe to Notifications**

```
POST http://localhost:8069/api/v1/mobile/notifications/subscribe
Cookie: session_id=YOUR_SESSION_ID

Body:
{
  "jsonrpc": "2.0",
  "params": {
    "device_token": "test_device_token_12345",
    "platform": "android"
  }
}
```

**Response:**
```json
{
  "result": {
    "success": true,
    "message": "Device registered successfully",
    "user": "testuser1@example.com",
    "platform": "android"
  }
}
```

---

## 🔕 **Endpoint 3: Unsubscribe**

```
POST http://localhost:8069/api/v1/mobile/notifications/unsubscribe
Cookie: session_id=YOUR_SESSION_ID

Body:
{
  "jsonrpc": "2.0",
  "params": {
    "device_token": "test_device_token_12345"
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

## 🧪 **Complete Testing Flow**

### **Test 1: Get All Orders**
```json
{
  "jsonrpc": "2.0",
  "params": {}
}
```
✅ **Expected:** See all user's orders

---

### **Test 2: Filter by Status "sale"**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "status": "sale"
  }
}
```
✅ **Expected:** See only "sale" orders

---

### **Test 3: Filter by Multiple Statuses**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "status": ["sale", "done"]
  }
}
```
✅ **Expected:** See "sale" and "done" orders

---

### **Test 4: Pagination**
```json
{
  "jsonrpc": "2.0",
  "params": {
    "limit": 2,
    "offset": 0
  }
}
```
✅ **Expected:** See first 2 orders, `has_more: true`

---

### **Test 5: User Isolation**
1. Login as User 1 → Get orders
2. Login as User 2 → Get orders
3. ✅ **Expected:** Different orders for each user

---

### **Test 6: Auto-Notification**
1. Register device
2. Confirm an order in Odoo
3. Check logs: `sudo tail -f /var/log/odoo/odoo-server.log`
4. ✅ **Expected:** See notification in logs

---

## 📝 **Summary**

✅ **ONE endpoint** for all order fetching needs
✅ **Filter by status** - single or multiple
✅ **Pagination** support
✅ **Notifications** - subscribe/unsubscribe
✅ **Auto-notify** when order status changes

**Ready to test in Postman! 🚀**
