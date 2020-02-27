import ctypes
import logging
import os

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class MediapipeManager():
    def __init__(self, output_folder):
        self.output_folder = output_folder.encode("utf-8")
        self._graph_path = " ".encode("utf-8")
        self._binary_path = os.path.abspath("libs/coordinates_mediapipe.so").encode("utf-8")

    def run_mediapipe(self, video_path):
        func = ctypes.cdll.LoadLibrary(self._binary_path)
        func.RunMPPGraph.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

        logging.info("Reaching video file.")
        if not os.path.exists(video_path):
            raise FileExistsError

        logging.info("Starting mediapipe hand-tracking.")
        try:
            func.RunMPPGraph("".encode("utf-8"),
                              video_path.encode("utf-8"),
                              self.output_folder,
                              self._graph_path)
            logging.info("Done.")
        except ProcessLookupError as e:
            print(e)

