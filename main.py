import cv2
import numpy as np

video_path = "C:/Users/gsc_prukol/Desktop/test.mp4"
p_frame_thresh = 100  # You may need to adjust this threshold
count_unique_frame = 720
window_name = 'Image'
color_red = (255,0,0)

cap = cv2.VideoCapture(video_path)
example_frame = dict()
index_collision = 0
count_frame = 0
unique_frame_count = 0
ret = True

def get_list(dict, index, limit = 15):
    tmp = list(dict.keys())
    tmp2 = tmp[index:] + tmp[:index]
    return tmp2[:limit]


while ret:
    count_frame += 1
    ret, curr_frame = cap.read()
    curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    if ret:
        unique = True
        if count_frame < count_unique_frame:
            example_frame[count_frame] = curr_frame
        else:
            for frame_index in get_list(example_frame, index_collision):
                diff = cv2.absdiff(curr_frame, example_frame[frame_index])
                non_zero_count = np.max(diff)
                if non_zero_count < p_frame_thresh:
                    index_collision = frame_index
                    unique = False
                    break
            if unique:
                unique_frame_count += 1
                name_image = f"unique_frames/unique_image_{count_frame}.png"
                cv2.imwrite(name_image, curr_frame)
                print(f"Add frame number {unique_frame_count} to unique set.")
            else:
                print(f"Frame is in list, has {unique_frame_count} unique frame, index collision = {index_collision}")
                cv2.putText(curr_frame, f"Frame {count_frame} is exist", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, color_red, 2)


        cv2.imshow(window_name, curr_frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break