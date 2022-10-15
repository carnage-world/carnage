import argparse

import uvicorn

from carnage.application import create_app
from carnage.cli import SubparserType


def add_subparser(
    subparsers: SubparserType,
    parents: list[argparse.ArgumentParser],
) -> None:
    """Add all init parsers.
    Args:
        subparsers: subparser we are going to attach to
        parents: Parent parsers, needed to ensure tree structure in argparse
    """
    serve_parser = subparsers.add_parser(
        "serve",
        parents=parents,
        help="Run carnage backend.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    serve_parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host address for carnage server.",
    )
    serve_parser.add_argument(
        "--port",
        default=5050,
        help="Port for carnage server.",
    )

    serve_parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """."""
    config = uvicorn.Config(
        create_app(),
        host=args.host,
        port=args.port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()