# Crop-lines-system
This is a system I built to detect rows of crops in a field given an aerial NDVI image. 

## Notes

![System Output](https://github.com/jbhewitt12/Crop-lines-system/blob/master/example_output.PNG)  
The above image visualizes the output of the program. The white lines are the crop lines, and the red lines are the locations of the lines as determined by the program.  

##### Simplified explanation:
The program first finds the angle of the crop rows using a 2D Fourier Transform. It then creates a line at this angle and finds the average pixel values along the line as the line is moved across the image. If you graph the result, the peaks give the locations of the lines. There are many further fine-tuning and checking steps done to ensure that the program is robust enough to work for noisy and bad data. 

## Requirements

- Python 3
- Numpy  
- Scipy  
- matplotlib  

## To run on the example image:
```bash
cd Crop-lines-system
python run.py
```
