The below describes how to set up a MacOS operating system for the program 
and involves pasting 4 lines into the command prompt in succession.

At this point you should be able to navigate to my script matrix.py
using your Terminal, and run it successfully by typing "python matrix.py"

*****************************************************************************

To make this program run on the Mac OS:

1. Have Homebrew

Refer to this web page: http://brew.sh/
There should be only one step involved if you're logged in as an Administrator:

Paste the following at a Terminal prompt:
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"


2. Have Pillow [a fork of the Python Imaging Library] for the Mac OS

Refer to this web page: pillow.readthedocs.org/en/latest/installation.html
There should be only one step involved if you're logged in as an Administrator:

First paste the following at a Terminal prompt:
sudo easy_install pip

Then: 
brew install libtiff libjpeg webp little-cms2

Then:
pip install pillow

*****************************************************************************

Configuration files are in the config folder, 
Output is in the output .txt file in the output folder. 
