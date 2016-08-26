# lihax
Aman, Midori, Yifan and Jacob's Lihacks 2016 project. 

## Unity Installation:  
  
## Python Installation:  

1. Make sure that you have the latest version of [Python 2.7](https://www.python.org/downloads/) installed. It's important that you have Python 2.7 installed, and **NOT** Python 3.  

1. Once you've installed Python, make sure that your Python installation path (usually `C:\Python27`) and the underlying 'Scripts' path (usually `C\Python27\Scripts`) are at the top of your `%PATH%` environment variable.  

1. Open a cmd window and type `pip list`. You should see **at least** a version of pip and a version of Setuptools, but if you don't you can get pip by running [this script](https://bootstrap.pypa.io/get-pip.py) and you can then get Setuptools by running `pip install setuptools`. If you get a message saying you need to update one or the other, please do so.  

1. Run `pip install virtualenv` if you don't already see it when you run `pip list`. Create a folder somewhere on your computer (it doesn't matter where) and cd there using cmd. This directory will contain your Python executables and libraries (or in case you're using an IDE, an interpreter for your project). Type `virtualenv` and your Python environment will be created.  

1. While in your environment folder, run `\Scripts\activate` and you should now see the command line heading change to the name of your environment folder. Copy the file `requirements.txt` from the learn repo directory into your environment folder and while in your environment type `pip install -r requirements.txt`, and you should now have all of the libraries needed in your environment. You can always check the libraries you have by running `pip list`.

1. Be sure to set the Python executable inside the `[Environment Folder]\Scripts` directory as your Python interpreter if you are using an IDE.  

Refer to [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for troubleshooting! 
