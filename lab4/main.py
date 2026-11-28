"""Entry point for Laboratory Work 4 console application."""

from lab4.cli import Lab4CLI


def main() -> None:
    """Launch the Lab 4 interactive CLI."""
    cli = Lab4CLI()
    cli.run()


if __name__ == "__main__":
    main()
