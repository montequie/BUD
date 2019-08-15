# Butter for the people




## Getting Started

Bla Bla

### Prerequisites

Bla Bla

### Installing

#### Butter Windows Application

#### Python 3.7 and butter.mas.api

Bla

```
$ sudo yum install gcc openssl-devel bzip2-devel libffi libffi-devel
$ cd /root 
$ wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
$ tar xzf Python-3.7.0.tgz
$ cd Python-3.7.0
$ ./configure --enable-optimizations
$ sudo make altinstall
$ rm -f /root/Python-3.7.0.tgz
```

Bla

Now, Install *pip* and *butter.mas.api*
```
$ pip3.7 install --upgrade pip --user
$ pip3.7 install butter.mas.api --user
```

## Configuration

Every experiment has a configuration file AKA `config`.
The config file is a [.JSON](https://en.wikipedia.org/wiki/JSON) file (key: value), contains data of keyboard shortcuts, motor names and more.

### Config File
This is a 'this' BUD config file, contains Butter's IP address, 4 motor names and 3 keyboard shortcuts:
```
{
  "IP": "192.168.0.111",
  "MOTOR_NAMES": [
    "turnone",
    "turntwo",
    "leanone",
    "leantwo"
  ],
  "SHORTCUTS": [
    {
      "key": "1",
      "module": "experiment",
      "function": "_play_animation",
      "help": "play animation - Welcome_New",
      "args": "Welcome_New"
    },
    {
      "key": "t",
      "module": "experiment",
      "function": "_disable_torque",
      "help": "disable torque for all turn motors",
      "args": [
        "turnone",
        "turntwo",
        "turnthree",
        "turnfour"
      ]
    },
    {
      "key": "f",
      "module": "experiment",
      "function": "_fix_goal_position",
      "help": "fix positions for all turn motors to 0 with minimum speed and acceleration",
      "args": {
        "turnone": {
          "goal_acceleration": 1,
          "moving_speed": 10,
          "goal_position": 2048
        },
        "turntwo": {
          "goal_acceleration": 1,
          "moving_speed": 10,
          "goal_position": 2048
        }
      }
    }
  ]
}
```
We will go through each section of the config file and explain how to modify it or to extend it.

#### IP
The IP address key `("IP")` is mandatory and can be extracted either from the Butter.MAS application or from the router site, in the latter case reach Iddo for further help, the value of this field is simply a string.
Make sure that the IP address inserted in the value of this key is made of 4 digits in the range of 0-255 seperated with 3 dots (usually in the miLAB the ip addresses are of the form 192.168.0.X where X changes).

#### Motor Names
The Motor Names key is also mandatory, the names that appears there are the names that were given in the Butter.MAS application, so make sure to get them right!
The values of the motor names are seperated with commas ',' as you can see in the example and all of them together inside a list [].

#### Shortcuts