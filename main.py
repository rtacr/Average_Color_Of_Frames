from threading import Thread
import cv2   
import numpy as np
import argparse

def get_args():
    parser = argparse.ArgumentParser(description="Average Color Of Frames")
    parser.add_argument("--input",          type=str, help='Video path')
    parser.add_argument("--threads",        type=str, default='disabled', help="Enable multithread processing",
                                                choices=['enabled', 'disabled'])
    parser.add_argument("--output",         type=str, default='.', help="Output path")
    parser.add_argument("--output-width",   type=int, default=1920, help="Image width. Defaults to 1920")
    parser.add_argument("--output-height",  type=int, default=1080, help="Image height. Defaults to 1080")

    args = parser.parse_args()

    if args.input == None:
        parser.print_help()
        quit()
    
    return args


def frame_average_color(frame):
    _, _, c = frame.shape

    avg_red = np.average(frame[:, :, 2])    
    avg_green = np.average(frame[:, :, 1])
    avg_blue = np.average(frame[:, :, 0])    
    avg_bgr = np.array((int(avg_blue), int(avg_green), int(avg_red)))

    return avg_bgr


def main():
    args = get_args()
       
    out_h = args.output_height
    out_w = args.output_width
    cap = cv2.VideoCapture(args.input)
    total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    thread_count = 1

    if args.threads == 'enabled':
        # Figure out how many threads to use
        # minimum of 20 frames per thread.
        if total_frame_count < 100:
            thread_count = 1
        elif total_frame_count < 200:
            thread_count = int(20 / total_frame_count)
        else: 
            thread_count = 200

    frame_per_thread = int(total_frame_count / thread_count)

    _, frame = cap.read()
    h, w,c = frame.shape

    final_image = np.ones((out_h, total_frame_count, c), dtype=np.uint8) * [0,0,0]
    # Single 1's line for multiplying with the average color
    vertical_line =  np.ones((out_h, c), dtype=np.uint8)

    # Each Thread will execute this function.
    def thread_job(st):         
        cap.set(cv2.CAP_PROP_POS_FRAMES, st)

        i = 0
        while(True):
            ret, frame = cap.read()

            if (not ret or i >= frame_per_thread):
                break 
            avg_bgr = frame_average_color(frame)
            final_image[:, st + i-1, :] = avg_bgr * vertical_line  
            i += 1

    threads = list()
    for i in range(0, total_frame_count, frame_per_thread):
        x = Thread(target=thread_job(i))
        x.start()
        threads.append(x)

    for x in threads:
        x.join()

    img = np.array(final_image, dtype=np.uint8)
    img = cv2.resize(img, (out_w, out_h))
    cv2.imwrite(args.output + '/out.png', img) 

if __name__ == "__main__":
    main()