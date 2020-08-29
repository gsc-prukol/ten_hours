import cv2
import numpy as np

video_path = "C:/Users/gsc_prukol/Desktop/test.mp4"
p_frame_thresh = 100  # You may need to adjust this threshold
count_unique_frame = 900
scip_frame = 300;
window_name = 'Image'
color_red = (255,0,0)
cap = cv2.VideoCapture(video_path)
# Read the first frame.
ret, prev_frame = cap.read()
prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
unique_frame = list()
unique_frame.append(prev_frame)
for i in range(scip_frame):
    ret, curr_frame = cap.read()
    if not ret:
        break

while ret:
    ret, curr_frame = cap.read()
    curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    #  cv2.imshow(window_name, curr_frame)
    if ret:
        unique = True
        for frame in unique_frame:
            diff = cv2.absdiff(curr_frame, frame)
            non_zero_count = np.max(diff)
            if non_zero_count < p_frame_thresh:
                unique = False
                break
        if unique:
            unique_frame.append(curr_frame)
            print(f"Add frame number {len(unique_frame)} to unique set.")
        else:
            print(f"Frame is in list, has {len(unique_frame)} unique frame")
            cv2.putText(curr_frame, "Frame is in list", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, color_red, 2)

        cv2.imshow(window_name, curr_frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break