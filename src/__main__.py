"""
Entry point của FastAPI application.

Cung cấp các subcommands:
- server: Khởi chạy FastAPI server (default)
- admin:create: Tạo admin user qua interactive CLI
"""

import argparse
from pathlib import Path

import uvicorn

from src.logger.LoggerConfig import LoggerConfig
from src.logger.LoggerFactory import LoggerFactory


# Khởi tạo logger singleton ngay khi module được load
_logger_config = LoggerConfig(project_root=Path(__file__).parent.parent)
_logger_factory = LoggerFactory(_logger_config)
logger = _logger_factory.get_instance()


def run_server(args: argparse.Namespace) -> None:
    """
    Khởi chạy FastAPI server với uvicorn.

    Args:
        args (argparse.Namespace): Parsed arguments chứa debug flag.
    """
    logger.info("Starting application...")
    logger.info(f"Debug mode: {args.debug}")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=args.debug,
        log_level="debug" if args.debug else "info",
        ws="none",
    )


def run_admin_create(args: argparse.Namespace) -> None:
    """
    Chạy interactive CLI để tạo admin user.

    Args:
        args (argparse.Namespace): Parsed arguments (không sử dụng).
    """
    from src.admin.cli import run_create_admin
    run_create_admin()


def main() -> None:
    """
    Entry point chính, parse arguments và dispatch subcommand.
    """
    parser = argparse.ArgumentParser(
        description="FastAPI Application Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python -m src                  # Start server (default)
  uv run python -m src server           # Start server explicitly
  uv run python -m src server --debug   # Start server in debug mode
  uv run python -m src admin:create     # Create admin user interactively
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # =================================================================
    # Subcommand: server (default)
    # =================================================================
    server_parser = subparsers.add_parser(
        "server",
        help="Start the FastAPI server",
    )
    server_parser.add_argument(
        "--debug",
        action="store_true",
        help="Chạy ở chế độ debug với hot reload",
    )
    server_parser.set_defaults(func=run_server)

    # =================================================================
    # Subcommand: admin:create
    # =================================================================
    admin_create_parser = subparsers.add_parser(
        "admin:create",
        help="Create admin user interactively",
    )
    admin_create_parser.set_defaults(func=run_admin_create)

    # Parse arguments
    args = parser.parse_args()

    # Nếu không có subcommand, mặc định chạy server
    if args.command is None:
        # Chạy server với default debug=False
        args.debug = False
        run_server(args)
    else:
        # Dispatch đến subcommand tương ứng
        args.func(args)


if __name__ == "__main__":
    main()
