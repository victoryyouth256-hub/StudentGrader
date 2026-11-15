from logic import *


def main() -> None:
    """Creates the application window and runs it."""
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()
