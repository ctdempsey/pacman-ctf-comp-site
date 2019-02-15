# PacMan CTF Competition Web App
This is a Python Flask web app built to facilitate testing of AI agents for UC Berkeley's Intro to AI course Capture the Flag contest project. This allows participants to test their agents against each other online, without exposing or giving away their code.

It was originally put together in a few hours because my university AI subject was using it as an assignment, and there wasn't an easy way to test how submissions compared to everyone else's. However, though it has been tested to work locally, I was unable to get it setup and working online before the assignment deadline without dedicating more time to it than to the actual assignment. Thus the code is provided as is, and may require additional modification if anyone wants to use it.

The contest's rules and code are found [here](https://inst.eecs.berkeley.edu/~cs188/pacman/contest.html).

## Requirements
#### For the PacMan contest code
 - Python 2.7

#### For the Web App code
 - Python 3
 - Flask 1.0.2 or higher
 - Werkzeug 0.12.0 or higher
 - Celery 4.0.0 or higher

## Setup
The web app uses the Celery python library to manage the task queue of contests and concurrency. Instructions for setting up and using this library are found [here](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html). The relevant Python arguments that need changing can be found in the main.py file.

As listed in the requirements, this app requires both Python2 and Python3 installed and configured so that Python2 code will run using the `python2` command on your system. This is due to the web app code being written in Python3, but the PacMan contest code written in Python2.

Other than that the app is a basic Flask app, with instructions for running it locally found [here](http://flask.pocoo.org/docs/1.0/quickstart/), and instructions for different methods of deploying it to a web server found [here](flask.pocoo.org/docs/1.0/deploying/).

## Licenses
#### For the PacMan contest code
Licensing Information:  You are free to use or extend these projects for educational purposes provided that (1) you do not distribute or publish solutions, (2) you retain this notice, and (3) you provide clear attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley. The core projects and autograders were primarily created by John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu). Student side autograding was added by Brad Miller, Nick Hay, and Pieter Abbeel (pabbeel@cs.berkeley.edu).

#### For the Web App code
MIT License

Copyright (c) 2018 Cameron Dempsey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
