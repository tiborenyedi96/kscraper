import logging

from shared.broker import receive_messages

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def main():
    receive_messages()


if __name__ == "__main__":
    main()
