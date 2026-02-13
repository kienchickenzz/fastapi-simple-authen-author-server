-- ----------
-- Permission
-- ----------
INSERT INTO permissions (code, description)
VALUES
    -- User permissions
    ('user:read',   'Read user information'),
    ('user:create', 'Create new user'),
    ('user:update', 'Update existing user'),
    ('user:delete', 'Delete user'),

    -- Book permissions
    ('book:read',   'Read book information'),
    ('book:create', 'Create new book'),
    ('book:update', 'Update existing book'),
    ('book:delete', 'Delete book'),

    -- Permission permissions
    ('permission:read',   'Read permission information'),
    ('permission:create', 'Create new permission'),
    ('permission:update', 'Update existing permission'),
    ('permission:delete', 'Delete permission'),

    -- Role permissions
    ('role:read',   'Read role information'),
    ('role:create', 'Create new role'),
    ('role:update', 'Update existing role'),
    ('role:delete', 'Delete role')

ON CONFLICT (code) DO NOTHING;


-- ----------
-- Role
-- ----------
INSERT INTO roles (name, description)
VALUES
    ('admin', 'Administrator with full access to user and book'),
    ('user',  'Normal user with CRUD access to book only')
ON CONFLICT (name) DO NOTHING;


-- ----------
-- Role Permission
-- ----------
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code IN (
    'user:read', 'user:create', 'user:update', 'user:delete',
    'book:read', 'book:create', 'book:update', 'book:delete',
    'permission:read', 'permission:create', 'permission:update', 'permission:delete',
    'role:read', 'role:create', 'role:update', 'role:delete'
)
WHERE r.name = 'admin'
ON CONFLICT DO NOTHING;

INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id
FROM roles r
JOIN permissions p ON p.code IN (
    'book:read', 'book:create', 'book:update', 'book:delete'
)
WHERE r.name = 'user'
ON CONFLICT DO NOTHING;


-- ----------
-- User
-- ----------
INSERT INTO users (username, email, password_hash, is_active)
VALUES
    ('admin1', 'admin1@example.com', 'hashed_password', true),
    ('admin2', 'admin2@example.com', 'hashed_password', true),
    ('user1',  'user1@example.com',  'hashed_password', true),
    ('user2',  'user2@example.com',  'hashed_password', true)
ON CONFLICT (username) DO NOTHING;


-- ----------
-- User role
-- ----------
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.name = 'admin'
WHERE u.username IN ('admin1', 'admin2')
ON CONFLICT DO NOTHING;

INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id
FROM users u
JOIN roles r ON r.name = 'user'
WHERE u.username IN ('user1', 'user2')
ON CONFLICT DO NOTHING;
