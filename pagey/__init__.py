"""Main file for pagey."""

from .args import *
from .pagerduty import *


def main() -> None:
    """Run main entrypoint."""
    cmd_args = get_args()

    response = fetch_schedules(cmd_args.pd_token)
    print(response)


if __name__ == "__main__":
    main()
