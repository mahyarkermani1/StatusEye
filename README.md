# What does this tool do?
This is a python script to send **GET requests** to a url address at time intervals entered by the user.
You can run the program by entering the url address and a number per second. Then the script will send a request to the entered address in the time frame set by you.
Tool features:
- [x] Interactive and user-friendly environment
- [x] Show logs on the page
- [x] Checking the connection to the entered address
- [x] Display the time, number, address and status code after each request
- [x] Notifies the user if the link expires

# The purpose of this tool
When working on labs like [**portswigger**](https://portswigger.net/), if a request is not sent to the lab address created for you within certain time intervals, the link of that lab will expire.
Therefore, this is a simple script to send get requests to the entered url address in a specified time frame, so that the laboratory link does not expire while working on the target or writing your notions.

# How to install and use
Clone the tool and run the scan.py script with Python.
The tool contains an interactive environment where the user can use the script by entering inputs.

```
git clone https://github.com/mahyarkermani1/StatusEye.git
cd StatusEye
python3 scan.py
```

# Images of the tool environment
In this example, we entered a personal link in our Brett Suiter Lab and told it to send a get request to the entered address every 30 seconds, to prevent the link from expiring.

<img src="https://github.com/mahyarkermani1/StatusEye/images/menu.png" width="30%"></img> <img src="https://github.com/mahyarkermani1/StatusEye/images/requests.png" width="30%"></img> <img src="https://github.com/mahyarkermani1/StatusEye/images/back.png" width="30%"></img>
