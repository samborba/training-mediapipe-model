import ctypes
import logging
import os

logging.basicConfig(filename="execution.log", filemode='a',
                    format='[%(asctime)s] # %(message)s', level=logging.INFO)

class MediapipeManager():
    def __init__(self, output_folder):
        self.output_folder = output_folder.encode("utf-8")
        self._graph_path = "mediapipe/graphs/hand_tracking/hand_tracking_desktop_live.pbtxt".encode("utf-8")
        self._binary_path = os.path.abspath("src/lib/coordinates_mediapipe.so").encode("utf-8")

    def run_mediapipe(self, video_path):
        func = ctypes.cdll.LoadLibrary(self._binary_path)
        func.RunMPPGraph.argtypes = [ctypes.c_char_p,
                                     ctypes.c_char_p,
                                     ctypes.c_char_p,
                                     ctypes.c_char_p]
        file_name = video_path.split("/")[-1]

        logging.info("Reaching %s file.", file_name)
        if not os.path.exists(video_path):
            raise FileExistsError

        logging.info("Applying mediapipe hand-tracking.")
        try:
            func.RunMPPGraph("".encode("utf-8"),
                             video_path.encode("utf-8"),
                             self.output_folder,
                             self._graph_path)
        except ProcessLookupError:
            print(ProcessLookupError)
