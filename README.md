# passwordgen-dash

A password generator implemented as a dash app. It is live at [http://password.stromsy.com](http://password.stromsy.com).
It is on a Heroku free dyn, so it might take a moment to load.

Security was not taken into consideration in this app so I do not advise using
http://password.stromsy.com for sensitive purposes. If you like it, clone it
and run the server on a local machine.

The goal is to generate randomized, easy to type and easy to read passwords.

"Easy to type" means:
1. Alternating between keys typed by the left hand and right hand
1. Avoiding keys that require moving the hands too far away from the home row
1. If the previous letter required the Shift key, the next letter will not use
the pinky finger (and vice versa)

"Easy to read" simply means avoiding letters that are easily mistaken for other
letters, such as 1/l, 0/O, etc.
