# Object Detection

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
	└── label.txt
```

Images under data/images/ should be in an increasing order. For instance, if you have 100 images, you can name them from 001.jpg to 100.jpg. If you have 1000 images, you can name them from 0001.jpg to 1000.jpg.

data/label.txt represents labels corresponding to every image under data/image/ in an increasing order, and every label is separated by one line break (\n). The label should be one of 1...C-1, where C is the number of class for the model to predict. For instance, if data folder is like

```
├── data/
	├── images/ 
	│	├── 001.jpg
	│	├── 002.jpg
	│	└── 003.jpg
	└── label.txt
```

and  label.txt is like

```
1
2
3
```

It means that the class of 001.jpg is 1, 002.jpg is 2, 003.jpg is 3.

## Parameter Selection

There are several parameters you should select before training. Here we provide some information about them. They are basically modified from [Keras API documentation](https://keras.io/api/).

### Model (model_name)

The pretrained convolutional neuron network model you would like to use for training. The table below provides some model information originated from [Keras Applications](https://keras.io/api/applications/). The top-1 and top-5 accuracy refers to the model's performance on the ImageNet validation dataset.

| Model             | Size (MB) | Top-1 Accuracy | Top-5 Accuracy | Parameters  | Depth | Time (ms) per inference step (CPU) | Time (ms) per inference step (GPU) |
| ----------------- | --------- | -------------- | -------------- | ----------- | ----- | ---------------------------------- | ---------------------------------- |
| Xception          | 88        | 0.790          | 0.945          | 22,910,480  | 126   | 109.42                             | 8.06                               |
| VGG16             | 528       | 0.713          | 0.901          | 138,357,544 | 23    | 69.5                               | 4.16                               |
| VGG19             | 549       | 0.713          | 0.900          | 143,667,240 | 26    | 84.75                              | 4.38                               |
| ResNet50          | 98        | 0.749          | 0.921          | 25,636,712  | -     | 58.2                               | 4.55                               |
| ResNet101         | 171       | 0.764          | 0.928          | 44,707,176  | -     | 89.59                              | 5.19                               |
| ResNet152         | 232       | 0.766          | 0.931          | 60,419,944  | -     | 127.43                             | 6.54                               |
| ResNet50V2        | 98        | 0.760          | 0.930          | 25,613,800  | -     | 45.63                              | 4.42                               |
| ResNet101V2       | 171       | 0.772          | 0.938          | 44,675,560  | -     | 72.73                              | 5.43                               |
| ResNet152V2       | 232       | 0.780          | 0.942          | 60,380,648  | -     | 107.5                              | 6.64                               |
| InceptionV3       | 92        | 0.779          | 0.937          | 23,851,784  | 159   | 42.25                              | 6.86                               |
| InceptionResNetV2 | 215       | 0.803          | 0.953          | 55,873,736  | 572   | 130.19                             | 10.02                              |
| MobileNet         | 16        | 0.704          | 0.895          | 4,253,864   | 88    | 22.6                               | 3.44                               |
| MobileNetV2       | 14        | 0.713          | 0.901          | 3,538,984   | 88    | 25.9                               | 3.83                               |
| DenseNet121       | 33        | 0.750          | 0.923          | 8,062,504   | 121   | 77.14                              | 5.38                               |
| DenseNet169       | 57        | 0.762          | 0.932          | 14,307,880  | 169   | 96.4                               | 6.28                               |
| DenseNet201       | 80        | 0.773          | 0.936          | 20,242,984  | 201   | 127.24                             | 6.67                               |
| NASNetMobile      | 23        | 0.744          | 0.919          | 5,326,716   | -     | 27.04                              | 6.7                                |
| NASNetLarge       | 343       | 0.825          | 0.960          | 88,949,818  | -     | 344.51                             | 19.96                              |
| EfficientNetB0    | 29        | -              | -              | 5,330,571   | -     | 46                                 | 4.91                               |
| EfficientNetB1    | 31        | -              | -              | 7,856,239   | -     | 60.2                               | 5.55                               |
| EfficientNetB2    | 36        | -              | -              | 9,177,569   | -     | 80.79                              | 6.5                                |
| EfficientNetB3    | 48        | -              | -              | 12,320,535  | -     | 139.97                             | 8.77                               |
| EfficientNetB4    | 75        | -              | -              | 19,466,823  | -     | 308.33                             | 15.12                              |
| EfficientNetB5    | 118       | -              | -              | 30,562,527  | -     | 579.18                             | 25.29                              |
| EfficientNetB6    | 166       | -              | -              | 43,265,143  | -     | 958.12                             | 40.45                              |
| EfficientNetB7    | 256       | -              | -              | 66,658,687  | -     | 1578.9                             | 61.62                              |

### Number of Classes (num_classes)

The number of classes for the model to predict.

### Image Size (imgsz)

All input images will be resize to (height=imgsz,width=imgsz,channel=3) before feeding into the model. One suggested imgsz is 224.

### Learning Rate (lr)

The initial learning rate used. It controls the step-size in updating the weights. One suggested initial learning rate is 0.001.

### Validation Fraction (val_frac)

The fraction of data to use not for training but for validating the model accuracy on those unseen data. One suggested value is 0.1.

### Optimizer (optimizer)

The optimizer is the algorithm you use to perform gradient descent to optimize your model.

The following are descriptions for supported optimizers originated from [Keras Applications](https://keras.io/api/optimizers/)

* SGD

  Simple gradient descent optimizer.

* RMSprop

  The gist of RMSprop is to:

  - Maintain a moving (discounted) average of the square of gradients
  - Divide the gradient by the root of this average

  This implementation of RMSprop uses plain momentum, not Nesterov momentum.

* Adam

  Adam optimization is a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments.

  According to [Kingma et al., 2014](http://arxiv.org/abs/1412.6980), the method is "*computationally efficient, has little memory requirement, invariant to diagonal rescaling of gradients, and is well suited for problems that are large in terms of data/parameters*".

* Adadelta

  Adadelta optimization is a stochastic gradient descent method that is based on adaptive learning rate per dimension to address two drawbacks:

  - The continual decay of learning rates throughout training.
  - The need for a manually selected global learning rate.

  Adadelta is a more robust extension of Adagrad that adapts learning rates based on a moving window of gradient updates, instead of accumulating all past gradients. This way, Adadelta continues learning even when many updates have been done. 

* Adagrad

  Adagrad is an optimizer with parameter-specific learning rates, which are adapted relative to how frequently a parameter gets updated during training. The more updates a parameter receives, the smaller the updates.

* Adamax

  It is a variant of Adam based on the infinity norm. Default parameters follow those provided in the paper. Adamax is sometimes superior to adam, specially in models with embeddings.

* Nadam

  Much like Adam is essentially RMSprop with momentum, Nadam is Adam with Nesterov momentum.

* Ftrl

  "Follow The Regularized Leader" (FTRL) is an optimization algorithm developed at Google for click-through rate prediction in the early 2010s. It is most suitable for shallow models with large and sparse feature spaces. The algorithm is described by [McMahan et al., 2013](https://research.google.com/pubs/archive/41159.pdf). 

### Batch Size (batch_size)

Integer. Number of samples per gradient update. 

### Epoch

Integer. Number of epochs to train the model. An epoch is an iteration over the entire `x` and `y` data provided. 

### Label Path (label_path)

The path where label.txt locates. Its default should be data/label.txt.

### Image Path (image_path)

The path where images/ folder locates. Its default should be data/images/.



