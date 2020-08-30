import cv2
import numpy as np
import time

video_path = "E:/test.mp4"
p_frame_thresh = 5  # You may need to adjust this threshold
count_unique_frame = 720
start_frame_number = 296000
window_name = 'Image'
color_blue = (255, 0, 0)
update_fps = 100
cap = cv2.VideoCapture(video_path)
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame_number)
example_frame = list()
index_collision = 0
count_frame = 0
unique_frame_count = 0
ret = True
time_start = time.time()
fps = 1
frame_index = 0
min_index = count_unique_frame
def get_list(dict, index, limit = 3, last = 1):
    tmp = list(dict.keys())
    index = index - last
    if index < 0:
        index = len(tmp) + index

    tmp2 = tmp[index:] + tmp[:index]

    return tmp2[:limit]

while ret:
    count_frame += 1
    if count_frame % update_fps == 0:
        current_time = time.time()
        fps = int(update_fps / (current_time - time_start))
        print(f"fps = {fps}")
        time_start = current_time

    ret, curr_frame = cap.read()
    curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    if count_frame == 1:
        prev_frame = curr_frame
        prev_diff = cv2.subtract(curr_frame, curr_frame)
        prev_prev_diff = cv2.subtract(curr_frame, curr_frame)
        prev_prev_prev_diff = cv2.subtract(curr_frame, curr_frame)
    diff_with_prev = cv2.absdiff(curr_frame, prev_frame)
    ret_diff, diff_with_prev = cv2.threshold(diff_with_prev, 2, 255, 0)
    if ret:
        unique = True
        # unique = False
        if count_frame <= count_unique_frame:
            example_frame.append(curr_frame)
            diff = diff2 = diff3 = diff4 = diff5 = curr_frame
        else:
            # for frame_index in get_list(example_frame, index_collision):
            for i in range(5):
                diff = cv2.absdiff(curr_frame, example_frame[frame_index])  # різниця з прикладом
                non_zero_count = np.mean(diff)
                if non_zero_count < p_frame_thresh:
                    diff2 = cv2.subtract(diff,
                                         diff_with_prev)  # різниця з прикладом - маска по різниці з попереднім кадром
                    diff3 = cv2.min(diff2, prev_diff)  # мінімум з поточного порівняння та попереднього
                    diff4 = cv2.min(diff3, prev_prev_diff)  # мінімум з поточного порівняння та двох попереднього
                    diff5 = cv2.min(diff4, prev_prev_prev_diff)  # мінімум з поточного порівняння та двох попереднього
                    prev_prev_prev_diff = prev_prev_diff
                    prev_prev_diff = prev_diff
                    prev_diff = diff2
                    unique = False
                    frame_index = (frame_index - 2) % len(example_frame)
                    break
                else:
                    frame_index = (frame_index + 1) % len(example_frame)

            if unique:
                unique_frame_count += 1
                # name_image = f"unique_frames/unique_image_{count_frame + start_frame_number}.png"
                # cv2.imwrite(name_image, curr_frame)
                print(f"Add frame number {unique_frame_count} to unique set.")
            # else:
            #     # cv2.putText(curr_frame, f"FPS: {fps}, frame {count_frame + start_frame_number} is exist", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_blue, 2)
            #     # cv2.putText(diff, f"FPS: {fps}, frame {count_frame + start_frame_number} is exist, index = {frame_index}", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color_blue, 2)
            if 297200 < count_frame + start_frame_number and count_frame + start_frame_number < 297260:
                # cv2.imwrite(f"unique_frames/unique_image_diff_{count_frame + start_frame_number}_with_prev.png", diff_with_prev)
                cv2.imwrite(f"unique_frames/unique_image_diff_{count_frame + start_frame_number}_5.png", diff5)
                cv2.imwrite(f"unique_frames/unique_image_diff_{count_frame + start_frame_number}_4.png", diff4)
                cv2.imwrite(f"unique_frames/unique_image_diff_{count_frame + start_frame_number}_3.png", diff3)
                cv2.imwrite(f"unique_frames/unique_image_diff_{count_frame + start_frame_number}_2.png", diff2)
                cv2.imwrite(f"unique_frames/unique_image_diff_{count_frame + start_frame_number}.png", diff)
                print(f"frame {count_frame + start_frame_number}, max_pixel = {np.max(diff5)}, mean = {np.mean(diff5)}")

        cv2.imshow(window_name, diff)
        prev_frame = curr_frame
        # cv2.imshow(window_name, curr_frame)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q") or key == ord("й"):
            break