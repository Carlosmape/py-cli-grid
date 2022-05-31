from abc import abstractmethod
import multiprocessing
from multiprocessing.queues import Queue
from time import time

from engine.frame import Frame


class base_game_process(multiprocessing.Process):

    def __init__(self, name="engine_sub_process"):
        super().__init__(name=name)
        self.frame_queue: Queue[Frame] = multiprocessing.Queue()
        self.is_started = False
        # Measurement related
        self.fps_avg = 0
        self.frame_count = 0

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
            begin_frame_process = time()
            frame = self.frame_queue.get()
            self.run_specific(frame)
            frame_delta = time() - begin_frame_process
            self.frame_count += 1
            self.fps_avg += (frame_delta - self.fps_avg)/self.frame_count;

    @abstractmethod
    def run_specific(self, frame: Frame):
        """This method must be overrided in derived class
        In this method will use engine's given frame to do actions"""
        pass
