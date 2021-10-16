# Keras OCR Training

## Data Preparation

The data folder is like:

```
├── data
	├── images 
	│	├── 001.jpg
	│	├── 002.jpg
	│	├── 003.jpg
	│	.
	│	.
	│	.
	│	└── 100.jpg
	└── labels
		├── 001.csv
		├── 002.csv
		├── 003.csv
		.
		.
		.
		└── 100.csv
```

Images under data/images/ should be in an increasing order. For instance, if you have 100 images, you can name them from 001.jpg to 100.jpg. If you have 1000 images, you can name them from 0001.jpg to 1000.jpg.

Every label under data/labels/ correspond to the image file under data/images/ of the same name. For example, data/images/001.jpg is corresponding to data/labels/001.csv. Labels should be in csv format. Template image file(001.jpg) and its corresponding label file(001.csv) are shown below:

001.jpg

<img src="..\assets\000.png" width=30%>

001.csv

```
0,r,469,117,498,125,483,169,454,161
0,i,503,111,524,117,503,175,483,169
0,t,525,116,556,125,533,184,503,176
1,t,46,104,78,113,77,171,46,163
1,e,78,126,121,137,118,182,77,171
2,n,278,178,324,190,315,231,271,220
2,w,324,191,382,207,372,246,315,231
```

The first column is group index, you can see that the 3 alphabets "rit" are close to each other in the above image, so all of them have group index 0. The group index starts from 0. The second column is the character. From the third column to the last column, they are the coordinates of the four corners corresponding to that character in clockwise order starting from the top left, $(x_1,y_1,x_2,y_2,y_3,y_3,x_4,y_4)$, where $0\leq x_i\leq w$ and $0\leq y_i\leq h$. h and w are the height and width of that image, and (x=0,y=0) is located at the upper left corner of the image.

The illustration of the coordinates of the four corners of character c. Note that the shape of the bounding coordinates are not restricted to rectangular.

```
    (x1,y1)----------(x2,y2)
    	|               |
    	|               |
    	|      C        | 
    	|               |
    (x4,y4)----------(x3,y3)
```

## Parameter Selection

There are several parameters you should select before training. Here we provide some information about them. 

### Alphabet (alphabet)

The characters you want to recognize. For example, if you want to recognize both numbers and alphabets, you can input 0123456789abcdefghijklmnopqrstuvwxyz.

### Detector Batch Size (detector_batch_size)

Integer. The batch size used to train the image detector. The image detector detects the location of the group of texts.

### Recognizer Batch Size (recognizer_batch_size)

Integer. The batch size used to train the image recognizer. The recognizer expects images to already be cropped to single lines of text. It can be trained to predict the characters in the line of the image.

### Recognizer Epoch (recognizer_epoch)

Integer. Number of epochs to train the recognizer model.

### Detector Epoch (detector_epoch)

Integer. Number of epochs to train the detector model.  

### Recognizer Learning Rate (recognizer_learning_rate)

The initial learning rate used to train the recognizer. It controls the step-size in updating the weights. One suggested initial learning rate is 1e-5.

### Detector Learning Rate (detector_learning_rate)

The initial learning rate used to train the detector. It controls the step-size in updating the weights. One suggested initial learning rate is 1e-5.

### 