# README

## About This Project
This is the API design project mandated by the EEE3097S course at UCT, created by William Bourn and Declan Molloy, to demonstrate the use of IoT technology in a particular field
of work. For this project, it was decided that security and remote access would be the focus and, thus, this API was designed for use with the EOZ IP40 keypad and RS Pro 105N
Lock. This repository also contains a simple demonstrator system to show how a Raspberry Pi may be configured to host an HTTP server and act remotely via a mobile application.

!N.B.: This demonstrator is meant to demonstrate only the remote accessibility of the device in question. It should not be used unaltered for security purposes because, due to a
lack of time and expertise, the demonstrator lacks conventional and necessary security measures, such as end-to-end encryption, or end user authentication, which means any user
on a network can access the device so long as they are aware of its IP address.

## Licence
See LICENCE for details.

## Contributing
See CONTRIBUTING for details.

## Getting Started

### Prerequisite
For the API prerequisites, see the README of the the API at https://github.com/WilliamBourn/EEE3097S-API-Design-Project. 

### Installation
To install the library, create a local directory and initialize a git repository.
```sh
git init
```
Perform a pull request from the directory url.
```sh
git pull https://github.com/WilliamBourn/EEE3097S-Project.git
```
!N.B.: the mobile application code has been bundled with the server code in this repository. The mobile application code is not necessary for the demonstrator side to function
and may be deleted at user discretion to save space.

## Usage
See docs for setup instructions and how to use the demonstrator.

## Contact
If there are concerns or questions about this API, please contact the owner of the repository at:
willjbourn@gmail.com
