import logging


def set_logging_config() -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename="runtime.log",
    )

    # logging.debug("This is a debug message. ")
    # logging.info("This is an info message." )
    # logging.warning("This is a warning message.")
    # logging.error ("This is an error message." )
    # logging.critical("This is a critical message." )
