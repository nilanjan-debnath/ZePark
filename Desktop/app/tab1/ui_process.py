import datetime
import queue
import logging

ui_updates = queue.Queue()


def ui_worker(tab1_instance):
    logging.info("UIProcess: started")
    while True:
        if ui_updates.not_empty:
            index, status = ui_updates.get()
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if status == 0:
                tab1_instance.slots[index - 1].clear_parking_details(emptied_time=time)
            elif status == 2:
                tab1_instance.slots[index - 1].add_parking_details(parking_time=time)
            ui_updates.task_done()
            logging.info(f"UIProcess: {index=} {status=}")
