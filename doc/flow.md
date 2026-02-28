┌─────────────────────────────────────────────────────────────────────────────┐
│ Permissions embedded trong token                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Sign-in                          Protected Endpoint                        │
│  ───────                          ──────────────────                        │
│  1. Validate credentials          1. Decode token                           │
│  2. Query permissions từ DB       2. Check permission từ token.permissions  │
│  3. Create token WITH permissions 3. Process request                        │
│  4. Return token                     (KHÔNG query DB!)                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


Token Structure 
```json
{
    "sub": "1",
    "username": "admin",
    "permissions": ["user:read", "user:create", "user:update", "book:read"],
    "exp": 1234567890,
    "iat": 1234567800
}
