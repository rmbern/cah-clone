# CAH-CLONE
A variation of Cards Against Humanity where the players write the answers to the questions!

## Dependencies

### Server

CAH-CLONE is designed to run on a Linux host connected to the internet behind a NAT router with the following software installed:

* python-3.5 or higher
  * venv
  * pip
  * The python-3 binary must be pointed to with the command "python3". Distributions that point "python" to a python-3 binary by default are not supported.
  * As part of the build process, CAH-CLONE will install Flask and uWSGI into a virtual enviornment.
* docker
  * The user running the server must be added to the `docker` group.

Although explicitly tested on Ubuntu 16 and Debian 9, any Linux distribution with the above dependencies installed should be capable of running CAH-CLONE.

### Client
Clients requre a Firefox web browser (other browsers most likely supported but not tested) to connect to the server.

## Install\How to play

* First, determine the NAT ip address of the Linux server. This is most easily done with the command `ip addr`.
  * The NAT ip address will start with either 192, 172, or 10, and will be of the form `inet xx.xx.xx.xx` in the output of `ip addr`.

* Next, clone this repository on a Linux machine as described above. Then, build it using `build.bash`. From there run the server using the command `docker run -p 5000:5000 cah`

* The clients then connect to the host Linux machine by its NAT ip address over port 5000 via Firefox (eg. enter `http://$host_address:5000` in the navigation bar).

* Players then enter a unique name and then click "login". They will be taken to a ready menu.

* Do not press ready until all players have logged in! Once all have logged in, click "ready", and follow the menu prompts in the browser.

* Enjoy, and have fun!
