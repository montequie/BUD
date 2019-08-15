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
asdf
```

Bla

Now, Install *pip* and *butter.mas.api*
```
asd
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
        "turntwo"
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
```
"IP": "192.168.0.111",
```
The IP address key `("IP")` is mandatory and can be extracted either from the Butter.MAS application or from the router site, in the latter case reach Iddo for further help, the value of this field is simply a string.
Make sure that the IP address inserted in the value of this key is made of 4 digits in the range of 0-255 seperated with 3 dots (usually in the miLAB the ip addresses are of the form 192.168.0.X where X changes).

#### Motor Names
```
"MOTOR_NAMES": [
    "turnone",
    "turntwo",
    "leanone",
    "leantwo"
  ],
```
The Motor Names key is also mandatory, the names that appears there are the names that were given in the Butter.MAS application, so make sure to get them right!
The values of the motor names are seperated with commas ',' as you can see in the example and all of them together inside a list [].

#### Shortcuts
```
"SHORTCUTS": [
    {
      "key": "1",
      "module": "experiment",
      "function": "_play_animation",
      "help": "play animation - Welcome_New",
      "args": "Welcome_New"
    }
```
The Shortcuts' value is also a list which contains the keyboard keys that the system will be 'listening' to.
Once the PM pressed a key that is inside one of the shortcuts, like "1" in the example, a function will execute - in our case the function `_play_animation` from the module `experiment` will run with the arguments `Welcome_New`. In other words, pressing "1" will cause Butter to play the animation Welcome_New on BUD.
Every key that is supported can be found [here](https://github.com/boppreh/keyboard), *in future development this keyboard mechanism will change*.
To play other animation in this case, the args key needs to be changed - just make sure the animation is indeed on the target robot (you can do that by running a command in Butter terminal TODO: BLA BLA).

Another type of keyboard shortcut look almost the same but some values are different:
```
{
      "key": "t",
      "module": "experiment",
      "function": "_disable_torque",
      "help": "disable torque for all turn motors",
      "args": [
        "turnone",
        "turntwo"
      ]
    }
```
The above execute a disable torque command to the 2 motor that their names can be found in args.
As you may notice the **args** key now contains a list, no worries, the args need to be in correlation with the function it execute, so make sure that **args** values matched the **function**.

### Editting the Config
When editting the config file you need to make sure that you didn't break the structure of the JSON and that you didn't broke the interface with the function.

#### Json Validator
[A Json Formatter & Validator](https://jsonformatter.curiousconcept.com/) like this site can help you make sure that you didn't ruin the structre, if you did you must fix it otherwise the system won't run.

#### Breaking the Interface
Don't do that.

### Generating a New Config - TODO
Under the *Essentials* folder you can see the file `create_config.py`, TODO: Bla Bla.

#### Configuration Location - TODO

## Running the System - TODO

