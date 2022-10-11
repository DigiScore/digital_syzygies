# digital_syzygies
Network, EEG composition by Andrew Hugill and team.
Software developed by Craig Vear (2022)

# Installation A - the Digital Syzygies app
Step 1 - Download the Zip file using the drop down menu in the green "Code" button above

Step 2 - Open the Zip folder and navigate to folder digital_syzygies-main/dist/main

Step 3 - Double click on file "main" [Mac users may need to unblock app in 'Security & Privacy' in System Preferences] 


# Installation B - Python Library
Step 1 - created Python virtual environment (venv)

Digital Syzygies requires a minimum [Python version of 3.7](https://www.python.org/downloads/). 
If you don't have it you'll need to first install it, then [set up a virtual environment](https://realpython.com/python-virtual-environments-a-primer/) with it. 

Step 2 - download Digital Syzygies and dependent libraries

Inside your venv download the Digital Syzygies code:

```
git clone https://github.com/DigiScore/digital_syzygies.git
```

Then move your Terminal into that folder:
```
cd digital_syzygies
```

Then install the required libraries using the following commands:
```
pip install playsound
 
pip install PyQt5

pip install websocket-client

pip3 install PyObjC

```

Step 3 - connect headset to EMOTIV Launcher

Step 4 - run main.py in Python 3
```
python3 main.py
```





