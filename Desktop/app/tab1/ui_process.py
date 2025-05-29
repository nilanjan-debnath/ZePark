import datetime
import time
import queue
import logging

ui_updates = queue.Queue()


def ui_worker(tab1_instance):
    logging.info("UIProcess: started")
    while True:
        if ui_updates.not_empty:
            index, status = ui_updates.get()
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            list_len = len(tab1_instance.slots)
            if index - 1 > list_len:
                logging.warning(
                    f"UIProcess: list index out of range {list_len=} {index=} {status=}"
                )
            else:
                if status == 0:
                    tab1_instance.slots[index - 1].clear_parking_details(
                        emptied_time=time_now
                    )
                elif status == 2:
                    tab1_instance.slots[index - 1].add_parking_details(
                        parking_time=time_now
                    )
                logging.info(f"UIProcess: {index=} {status=}")
            ui_updates.task_done()

        time.sleep(0.01)
