import multiprocessing
from multiprocessing.queues import Queue

from engine.frame import Frame


class base_game_process(multiprocessing.Process):

    def __init__(self, name="engine_sub_process"):
        super().__init__(name=name)
        self.frame_queue: Queue[Frame] = multiprocessing.Queue()
        self.is_started = False

    def start(self) -> None:
        self.is_started = True
        return super().start()

    def stop(self):
        self.is_started = False

    def update(self, frame: Frame):
        """Updates the process with given Frame"""
        self.frame_queue.put(frame)

    def run(self):
        """Main loop method.
        Process will wait for engine's Frames
        and will call run_specific(frame)"""
        while self.is_started:
            frame = self.frame_queue.get()
            self.run_specific(frame)

    def run_specific(self, frame: Frame):
        """This method must be overrided in derived class
        In this method will use engine's given frame to do actions"""
        raise Exception("base_game_process.run_specific() method must be defined in derived process classes")
