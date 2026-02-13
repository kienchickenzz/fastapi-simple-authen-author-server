"""
CLI commands cho admin management.

Cung cấp interactive command để tạo admin user mà không cần
expose credentials trong env hoặc command line.
"""

import asyncio
import getpass
import re
import sys
from os import environ

from dotenv import load_dotenv

from src.config import Config
from src.base.engine_factory import EngineFactory
from src.admin.service import AdminService


def validate_email(email: str) -> bool:
    """
    Validate email format đơn giản.

    Args:
        email (str): Email cần validate.

    Returns:
        bool: True nếu email hợp lệ.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


async def create_admin_interactive() -> None:
    """
    Interactive CLI để tạo admin user.

    Prompts user nhập:
    - Username
    - Email
    - Password (hidden)
    - Confirm password (hidden)

    Validates input và tạo admin user với Admin role.
    """
    print("\n=== Create Admin User ===\n")

    # Prompt username
    username = input("Username: ").strip()
    if not username:
        print("Error: Username cannot be empty")
        sys.exit(1)

    if len(username) < 3:
        print("Error: Username must be at least 3 characters")
        sys.exit(1)

    # Prompt email
    email = input("Email: ").strip()
    if not email:
        print("Error: Email cannot be empty")
        sys.exit(1)

    if not validate_email(email):
        print("Error: Invalid email format")
        sys.exit(1)

    # Prompt password (hidden)
    password = getpass.getpass("Password: ")
    if not password:
        print("Error: Password cannot be empty")
        sys.exit(1)

    if len(password) < 6:
        print("Error: Password must be at least 6 characters")
        sys.exit(1)

    # Confirm password
    confirm_password = getpass.getpass("Confirm Password: ")
    if password != confirm_password:
        print("Error: Passwords do not match")
        sys.exit(1)

    # Load config và khởi tạo database
    load_dotenv('.env')
    config = Config(environ)

    print("\nConnecting to database...")

    engine_factory = EngineFactory(config=config)

    try:
        await engine_factory.__aenter__()
        db_engine = engine_factory.create_engine("DB")

        admin_service = await AdminService.create_instance(db_engine)

        print("Creating admin user...")
        user_id = await admin_service.create_admin(
            username=username,
            email=email,
            password=password,
        )

        print(f"\nSuccess! Admin user created:")
        print(f"  - ID: {user_id}")
        print(f"  - Username: {username}")
        print(f"  - Email: {email}")
        print(f"  - Role: Admin")

    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

    finally:
        await engine_factory.__aexit__(None, None, None)


def run_create_admin() -> None:
    """
    Entry point cho CLI command.

    Chạy async function trong event loop.
    """
    asyncio.run(create_admin_interactive())
