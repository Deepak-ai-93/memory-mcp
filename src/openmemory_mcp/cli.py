import argparse
import json
import sys
from datetime import datetime
from typing import Any

from openmemory_mcp.models import MemoryType
from openmemory_mcp.server import build_service


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2))


def handle_remember(args: argparse.Namespace) -> None:
    service = build_service()
    result = service.remember(
        project=args.project,
        content=args.content,
        memory_type=args.type,
        tags=args.tags.split(",") if args.tags else None,
    )
    print_json(result)


def handle_search(args: argparse.Namespace) -> None:
    service = build_service()
    result = service.search_memory(
        project=args.project,
        query=args.query,
        limit=args.limit,
    )
    print_json(result)


def handle_decision_add(args: argparse.Namespace) -> None:
    service = build_service()
    result = service.add_decision(
        project=args.project,
        decision=args.decision,
        reason=args.reason,
    )
    print_json(result)


def handle_decision_list(args: argparse.Namespace) -> None:
    service = build_service()
    result = service.get_decisions(project=args.project)
    print_json(result)


def handle_context(args: argparse.Namespace) -> None:
    service = build_service()
    result = service.project_context(project=args.project)
    print_json(result)


def handle_timeline(args: argparse.Namespace) -> None:
    service = build_service()
    start = datetime.fromisoformat(args.start) if args.start else None
    end = datetime.fromisoformat(args.end) if args.end else None
    result = service.timeline(
        project=args.project,
        start=start,
        end=end,
        limit=args.limit,
    )
    print_json(result)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="openmemory-mcp",
        description="OpenMemory MCP Management CLI",
    )
    subparsers = parser.add_subparsers(dest="command", help="Management commands")

    # Remember
    remember_parser = subparsers.add_parser("remember", help="Store a project memory")
    remember_parser.add_argument("--project", required=True, help="Project name")
    remember_parser.add_argument("--content", required=True, help="Memory content")
    remember_parser.add_argument(
        "--type",
        default="fact",
        choices=[t.value for t in MemoryType],
        help="Memory type",
    )
    remember_parser.add_argument("--tags", help="Comma-separated tags")
    remember_parser.set_defaults(func=handle_remember)

    # Search
    search_parser = subparsers.add_parser("search", help="Search project memories")
    search_parser.add_argument("--project", required=True, help="Project name")
    search_parser.add_argument("--query", required=True, help="Search query")
    search_parser.add_argument("--limit", type=int, default=10, help="Results limit")
    search_parser.set_defaults(func=handle_search)

    # Decision Add
    dec_add_parser = subparsers.add_parser("add-decision", help="Add a project decision")
    dec_add_parser.add_argument("--project", required=True, help="Project name")
    dec_add_parser.add_argument("--decision", required=True, help="Decision content")
    dec_add_parser.add_argument("--reason", required=True, help="Rationale for decision")
    dec_add_parser.set_defaults(func=handle_decision_add)

    # Decision List
    dec_list_parser = subparsers.add_parser("decisions", help="List project decisions")
    dec_list_parser.add_argument("--project", required=True, help="Project name")
    dec_list_parser.set_defaults(func=handle_decision_list)

    # Project Context
    context_parser = subparsers.add_parser("context", help="Get project summary context")
    context_parser.add_argument("--project", required=True, help="Project name")
    context_parser.set_defaults(func=handle_context)

    # Timeline
    timeline_parser = subparsers.add_parser("timeline", help="Get project event timeline")
    timeline_parser.add_argument("--project", required=True, help="Project name")
    timeline_parser.add_argument("--start", help="Start date (ISO format)")
    timeline_parser.add_argument("--end", help="End date (ISO format)")
    timeline_parser.add_argument("--limit", type=int, default=100, help="Results limit")
    timeline_parser.set_defaults(func=handle_timeline)

    # Serve (Existing functionality)
    serve_parser = subparsers.add_parser("serve", help="Start the MCP server (default)")
    serve_parser.set_defaults(command="serve")

    # If no arguments or 'serve', we'll default to starting the server in server.py
    # But here we handle management commands.
    
    # Check if we should default to 'serve' if no command provided
    if len(sys.argv) == 1:
        from openmemory_mcp.server import main as server_main
        server_main()
        return

    args = parser.parse_args()
    if args.command == "serve":
        from openmemory_mcp.server import main as server_main
        server_main()
    elif hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
