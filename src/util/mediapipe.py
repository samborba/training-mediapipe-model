import ctypes
import logging
import os

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class MediapipeManager():
    def __init__(self, coordinates_folder, output_folder):
        self.coordinates_folder = coordinates_folder.encode("utf-8")
        self.output_folder = output_folder.encode("utf-8")
        self._graph_path = "mediapipe/graphs/hand_tracking/hand_tracking_desktop_live.pbtxt".encode("utf-8")
        self._binary_path = "src/libs/coordinates_mediapipe.so".encode("utf-8")

    def run_mediapipe(self, video_path):
        func = ctypes.cdll.LoadLibrary(self._binary_path)
        func.RunMPPGraph.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

        logging.info("Reaching video file.")
        if not os.path.exists(video_path):
            raise FileExistsError

        logging.info("Applying hand-tracking to the video.")
        try:
            func.RunMPPGGraph("".encode("utf-8"), video_path.encode("utf-8"),
                            self.coordinates_folder,
                            self._graph_path)
            logging.info("Done.")
        except ProcessLookupError as e:
            print(e)

