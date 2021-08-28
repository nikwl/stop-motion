import cv2
import numpy as np


# def composite(frame, frame_list, idx, num):
#     num = min(num, len(frame_list)-(idx-1))
#     print(len(frame_list)-(idx-1))
#     num = max(num, 0)
#     print(idx)
#     print(num)
#     img_acc = frame.astype(np.float)
#     for i in range(num):
#         img_acc += frame_list[(idx-1) - i]
#     img_acc /= (num + 1)
#     return img_acc.astype(np.uint8)


def composite(frame, frame_list, idx):
    img1 = frame
    img2 = frame_list[idx]

    img1 = (img1 / 2).astype(np.uint8)
    img2 = (img2 / 2).astype(np.uint8)
    return img1 + img2


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")

frame_list = []
frame_list_ptr = -1

play_video = False

im_shape = (480, 640, 3)

frame_list.append(np.ones(im_shape)*255)
frame_list_ptr += 1

while True:
    # Get current frame 
    _, frame = cap.read()
    frame = frame.copy()
    print('Index: {}'.format(frame_list_ptr))

    # Process user input
    user_input = cv2.waitKey(1)
    if user_input & 0xFF == ord('q'):
        break
    elif user_input & 0xFF == 81:
        #print('user pressed left arrow')

        if frame_list_ptr >= 1:
            frame_list_ptr -= 1

    elif user_input & 0xFF == 83:
        #print('user pressed right arrow')

        if frame_list_ptr < len(frame_list)-1:
            frame_list_ptr += 1
    
    elif user_input & 0xFF == 82:
        #print('user pressed up arrow')

        # Append the current frame to the temporary buffer
        if frame_list_ptr == len(frame_list)-1:
            frame_list.append(frame.copy())
            frame_list_ptr += 1
        else:
            frame_list[frame_list_ptr] = frame
            frame_list_ptr += 1 
    elif user_input & 0xFF == 84:
        #print('user pressed down arrow')
        play_video = True
        break
            
    cv2.imshow('Webcam', composite(frame, frame_list, frame_list_ptr))

del frame_list[0]

speed_ptr = 5
while play_video:

    for frame in frame_list:
        
        cv2.imshow('Webcam', frame)
        user_input = cv2.waitKey(speed_ptr)

        if user_input & 0xFF == ord('q'):
            play_video = False
            break
        elif user_input & 0xFF == 81:
            #print('user pressed left arrow')
            speed_ptr += 5
        elif user_input & 0xFF == 83:
            #print('user pressed right arrow')
            speed_ptr = max(speed_ptr-5, 0)


cap.release()
cv2.destroyAllWindows()