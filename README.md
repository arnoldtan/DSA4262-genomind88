# Running on AWS Instance

## Installing Python

For this project, Python 3.10 is necessary for the latest packages. Run the following commands on your AWS Instance:

```
sudo apt update
sudo apt upgrade
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.10
sudo ln -sf /usr/bin/python3.10 /usr/bin/python
```

## Installing git and cloning repository

To clone this repository into the AWS Instance, installing git is necessary. Run the following commands on your AWS Instance:

```
sudo apt install git
```

Afterwards, you can clone the repository by using the commands below:

```
git clone https://github.com/arnoldtan/DSA4262-genomind88.git
```
