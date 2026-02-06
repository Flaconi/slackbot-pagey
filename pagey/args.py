"""Parse command line arguments."""

import argparse

from .defaults import DEF_DESC, DEF_GITHUB, DEF_NAME, DEF_VERSION


def _get_version() -> str:
    """Return version information."""
    return f"{DEF_NAME}: Version {DEF_VERSION}\n({DEF_GITHUB})"


def get_args() -> argparse.Namespace:
    """Retrieve command line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
        usage=(
            f"{DEF_NAME} [option]\n{DEF_NAME} -v, --version\n{DEF_NAME} -h, --help\n"
        ),
        description=DEF_DESC
        + """

IMPORTANT:
  You will have to export PAGEY_SLACK_TOKEN and PAGEY_PD_TOKEN
  to your environment.

  export PAGEY_SLACK_TOKEN="read-write slack token"
  export PAGEY_PD_TOKEN="read-only pagerduty token"
""",
    )

    misc = parser.add_argument_group("misc arguments")

    misc.add_argument(
        "-v",
        "--version",
        action="version",
        version=_get_version(),
        help="Show version information and exit.",
    )
    misc.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit."
    )

    # Return arguments
    return parser.parse_args()
