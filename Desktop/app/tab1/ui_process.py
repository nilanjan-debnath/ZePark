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
            try:
                if status == 0:
                    tab1_instance.slots[index - 1].clear_parking_details(
                        emptied_time=time_now
                    )
                    tab1_instance.empty_count += 1
                    tab1_instance.parked_count -= 1
                elif status == 2:
                    tab1_instance.slots[index - 1].add_parking_details(
                        parking_time=time_now
                    )
                    tab1_instance.empty_count -= 1
                    tab1_instance.parked_count += 1
                else:
                    tab1_instance.slots[index - 1].add_booking_details(
                        user_name="User Name",
                        car_no="WB 26DQ 0333",
                        booking_time=time_now,
                    )
                    tab1_instance.empty_count -= 1
                    tab1_instance.booked_count += 1

                tab1_instance.count_box_widget.refresh_count(
                    tab1_instance.parked_count,
                    tab1_instance.booked_count,
                    tab1_instance.empty_count,
                )

                logging.info(f"UIProcess: {index=} {status=}")
            except Exception as e:
                list_len = len(tab1_instance.slots)
                logging.warning(
                    f"UIProcess: list index out of range {list_len=} {index=} {status=} {e}"
                )

            ui_updates.task_done()

        time.sleep(0.01)
