# Average Color Of Frames

Takes an input video and calculates average color of every frame. Calculated colors are presented in single pixel lines, then the image gets resized to given arguments.

## Getting Started
- Install packages with pip
    ```pip install -r requirements.txt```
- Run the program on the video "input.mp4". 
    ```python .\main.py --input "./input.mp4 --output './resources'"```
- Using multiproccesing. 
    ```python .\main.py --input "./input.mp4" --output './resources' --threads enabled```
    An episode of The Office fed into the program:
    ![Random Episode from The Office](./resources/out.png)