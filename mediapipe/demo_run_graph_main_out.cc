// Copyright 2019 The MediaPipe Authors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// An example of sending OpenCV webcam frames into a MediaPipe graph.

#include "mediapipe/framework/calculator_framework.h"
#include "mediapipe/framework/formats/image_frame.h"
#include "mediapipe/framework/formats/image_frame_opencv.h"
#include "mediapipe/framework/port/file_helpers.h"
#include "mediapipe/framework/port/opencv_highgui_inc.h"
#include "mediapipe/framework/port/opencv_imgproc_inc.h"
#include "mediapipe/framework/port/opencv_video_inc.h"
#include "mediapipe/framework/port/parse_text_proto.h"
#include "mediapipe/framework/port/status.h"

#include <iostream>
#include <fstream>
#include <string>

//Take stream from /mediapipe/graphs/hand_tracking/hand_detection_desktop_live.pbtxt
// RendererSubgraph - LANDMARKS:hand_landmarks
#include "mediapipe/calculators/util/landmarks_to_render_data_calculator.pb.h"
#include "mediapipe/framework/formats/landmark.pb.h"

// input and output streams to be used/retrieved by calculators
constexpr char kInputStream[] = "input_video";
constexpr char kOutputStream[] = "output_video";
constexpr char kLandmarksStream[] = "hand_landmarks";
constexpr char kWindowName[] = "MediaPipe";

extern "C" ::mediapipe::Status RunMPPGraph(char* c_video_path,
                                           char* c_coordinates_path,
                                           char* calculator_graph_config_file) {

  std::string calculator_graph_config_contents;
  std::string video_path = c_video_path; // to use rfind() and substr() need to be string

  // Setting input_video name to create txt file later
  int beginIdx = video_path.rfind("/");
  std::string video_name = video_path.substr(beginIdx+1);

  // Search for extension, if found, remove it
  if (video_name.find(".mp4")) {
    size_t lastindex = video_name.find_last_of(".");
    video_name = video_name.substr(0, lastindex);
  }

  std::string coordinates_path = c_coordinates_path + video_name + ".txt";
  std::string output_video_path = "";

  MP_RETURN_IF_ERROR(mediapipe::file::GetContents(
      calculator_graph_config_file, &calculator_graph_config_contents));
  LOG(INFO) << "Get calculator graph config contents: "
            << calculator_graph_config_contents;
  mediapipe::CalculatorGraphConfig config =
      mediapipe::ParseTextProtoOrDie<mediapipe::CalculatorGraphConfig>(
          calculator_graph_config_contents);

  LOG(INFO) << "Initialize the calculator graph.";
  mediapipe::CalculatorGraph graph;
  MP_RETURN_IF_ERROR(graph.Initialize(config));

  LOG(INFO) << "Initialize the camera or load the video.";
  cv::VideoCapture capture;
  const bool load_video = !video_path.empty();
  if (load_video) {
    capture.open(video_path);
  } else {
    capture.open(0);
  }
  RET_CHECK(capture.isOpened());

  cv::VideoWriter writer;
  const bool save_video = !output_video_path.empty();
  if (save_video) {
    LOG(INFO) << "Prepare video writer.";
    cv::Mat test_frame;
    capture.read(test_frame);                    // Consume first frame.
    capture.set(cv::CAP_PROP_POS_AVI_RATIO, 0);  // Rewind to beginning.
    writer.open(output_video_path,
                mediapipe::fourcc('a', 'v', 'c', '1'),  // .mp4
                capture.get(cv::CAP_PROP_FPS), test_frame.size());
    RET_CHECK(writer.isOpened());
  }

  // pollers to retrieve streams from graph
  // output stream (i.e. rendered landmark frame)
  ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller poller,
                   graph.AddOutputStreamPoller(kOutputStream));
  // hand landmarks stream
  ASSIGN_OR_RETURN(mediapipe::OutputStreamPoller poller_landmark,
            graph.AddOutputStreamPoller(kLandmarksStream));

  LOG(INFO) << "Start running the calculator graph.";
  MP_RETURN_IF_ERROR(graph.StartRun({}));

  LOG(INFO) << "Start grabbing and processing frames.";
  size_t frame_timestamp = 0;
  bool grab_frames = true;
  while (grab_frames) {
    // Capture opencv camera or video frame.
    cv::Mat camera_frame_raw;
    capture >> camera_frame_raw;
    if (camera_frame_raw.empty()) break;  // End of video.
    cv::Mat camera_frame;
    cv::cvtColor(camera_frame_raw, camera_frame, cv::COLOR_BGR2RGB);
    if (!load_video) {
      cv::flip(camera_frame, camera_frame, /*flipcode=HORIZONTAL*/ 1);
    }

    // Wrap Mat into an ImageFrame.
    auto input_frame = absl::make_unique<mediapipe::ImageFrame>(
        mediapipe::ImageFormat::SRGB, camera_frame.cols, camera_frame.rows,
        mediapipe::ImageFrame::kDefaultAlignmentBoundary);
    cv::Mat input_frame_mat = mediapipe::formats::MatView(input_frame.get());
    camera_frame.copyTo(input_frame_mat);

    // Send image packet into the graph.
    MP_RETURN_IF_ERROR(graph.AddPacketToInputStream(
        kInputStream, mediapipe::Adopt(input_frame.release())
                          .At(mediapipe::Timestamp(frame_timestamp++))));

    // Get the graph result packet, or stop if that fails.
    mediapipe::Packet packet;
    mediapipe::Packet landmark_packet;

    //Polling the poller to get landmark packet
    if (!poller.Next(&packet)) break;
    if (!poller_landmark.Next(&landmark_packet)) break;

    // Use packet.Get to recover values from packet
    auto& output_frame = packet.Get<mediapipe::ImageFrame>();

    // Deduce type of "landmark_packet"
    auto &output_landmarks = landmark_packet.Get < mediapipe::NormalizedLandmarkList > ();

    // Convert back to opencv for display or saving.
    cv::Mat output_frame_mat = mediapipe::formats::MatView(&output_frame);
    cv::cvtColor(output_frame_mat, output_frame_mat, cv::COLOR_RGB2BGR);
    if (save_video) {
      writer.write(output_frame_mat);
    }
    
    // Save landmark coordinate values into a text file
    std::ofstream landmarks_coordinates(coordinates_path, std::ios::out | std::ios_base::app);

    // Loop over landmarks list
    for (int i = 0; i < output_landmarks.landmark_size(); ++i) {
      const mediapipe::NormalizedLandmark& landmark = output_landmarks.landmark(i);
      landmarks_coordinates << landmark.x();
      landmarks_coordinates << " ";
      landmarks_coordinates << landmark.y();
      landmarks_coordinates << " ";
    }
  }

  // filetest.close();
  LOG(INFO) << "Shutting down.";
  if (writer.isOpened()) writer.release();
  MP_RETURN_IF_ERROR(graph.CloseInputStream(kInputStream));
  return graph.WaitUntilDone();
}

// int main() {
//   ::mediapipe::Status run_status = RunMPPGraph("video-input");
//   if (!run_status.ok()) {
//     LOG(ERROR) << "Failed to run the graph: " << run_status.message();
//   } else {
//     LOG(INFO) << "Success!";
//   }
//   return 0;
// }
