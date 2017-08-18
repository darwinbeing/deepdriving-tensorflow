# Welcome to the DeepDriving for Tensorflow Project

## Introduction

The DeepDriving project was originally created by the Princeton University. This original project can be found [here](http://deepdriving.cs.princeton.edu). When I first read the corresponding [paper](http://deepdriving.cs.princeton.edu/paper.pdf) I thought: "Hey this is the perfect project for my upcoming semester work on my university". Thus I started to reproduce the results from the paper and to port the AlexNet, used by this project, to Tensorflow. 

As a very first step, I reproduced the results with a more recent caffe implementation. This implementation can be found [here](https://github.com/Netzeband/caffe-deepdriving). In a second step, I created a Tensorflow based deep-learning framework which allows the training and evaluation of neural networks with Tensorflow without much overhead. This implementation is very generic and many different deep-learning tasks can be performed using this framework.

In the end, I was able to port the AlexNet, used by the original project, to a tenesorflow implementation based on my deep-learning framework. On the upcoming wiki-pages, I will describe, how to install the framework and how to use it for deep-learning tasks. Furthermore I will describe how to reproduce the results from the DeepDriving project and how to train an own network to drive on a computer game.

In contrast to the original implementation, I did not use TORCS as computer game, but SpeedDreams, which is a fork of TORCS. SpeedDreams comes with a very nice CMake-based build system, which makes it easy to compile and install the game on Windows. The following descriptions are for Windows and Ubuntu. A DeepDriving-ready implementation of SpeedDreams can be found [here](https://bitbucket.org/Netzeband/deep-speeddreams).

On YouTube, you can find some videos which shows this project in action. Have a lot of fun with driving!

[![Driving in SpeedDreams on 2 Lanes](https://img.youtube.com/vi/lVfPHUkOh3o/0.jpg)](https://www.youtube.com/watch?v=lVfPHUkOh3o)

[![Driving in SpeedDreams on 3 Lanes](https://img.youtube.com/vi/FhuMjHnTL5w/0.jpg)](https://www.youtube.com/watch?v=FhuMjHnTL5w)

## Index

* **Installation on Windows**
    * [Compile the C-Libraries](https://bitbucket.org/Netzeband/deepdriving/wiki/InstallWindowsCompile)
    * [Setup your Python 3 Environment](https://bitbucket.org/Netzeband/deepdriving/wiki/InstallWindowsPython)
* **Installation on Ubuntu**
    * [Compile the C-Libraries](https://bitbucket.org/Netzeband/deepdriving/wiki/InstallUbuntuCompile)
    * [Setup your Python 3 Environment](https://bitbucket.org/Netzeband/deepdriving/wiki/InstallUbuntuPython)
* **The Deep-Learning Framework**
    * [Basics](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepLearningFramework)
    * [Setup and Train Cifar-10 Data](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepLearningCifar10)
* **The DeepDriving Project**
    * [Prepare the DeepDriving-Training-Data](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepDrivingTrainingData)
    * [Train the DeepDriving-Network](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepDrivingTrain)
    * [Evaluate the DeepDriving-Network](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepDrivingEvaluate)
    * [Drive in SpeedDreams](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepDrivingDrive)
    * [Create your own Training-Data](https://bitbucket.org/Netzeband/deepdriving/wiki/DeepDrivingRecord)

## License

Since this project is derived from [DeepDriving](http://deepdriving.cs.princeton.edu), the original license is still valid for all derived code parts. This is especially the code for the Situation-View (C-Library) and the Drive-Controller (C-Libraray). But also the code for normalizing and denormalizing the labels and output of the network. In general there should be a note inside the file, if the corresponding code is derived from the original project.

The remaining python code is under the MIT license and the C/C++ code is under the GNU library.

## Additional Information

* [Results](https://bitbucket.org/Netzeband/deepdriving/wiki/Results)