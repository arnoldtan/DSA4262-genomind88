# Running on AWS Instance

- [Installation of Python 3.10 and pip](#python-installation)
- [Installing git and Cloning Repository](#git-installation)
- [Installing Packages and Running the Model](#packages-installation-and-model-execution)
- [Example Dataset and Output](#example-dataset-and-output)

## Installation of Python 3.10 and pip

Python 3.10 is required for this project to ensure compatibility with the latest packages. Please execute the following commands on your AWS instance:

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt install -y python3.10 python3.10-distutils
sudo ln -sf /usr/bin/python3.10 /usr/bin/python
curl -O https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

Checking if everything is installed correctly:

```
python --version
# python 3.10.15
python -m pip --version
# pip 24.3.1 from /home/ubuntu/.local/lib/python3.10/site-packages/pip (python 3.10)
```

## Installing git and Cloning Repository

To clone the repository onto the AWS instance, it is necessary to install Git. Please execute the following command:

```
sudo apt install git
```

Afterwards, you can clone the repository by using the commands below:

```
git clone <repository_link>
```

## Installing Packages and Running the Model

To install the required packages, navigate to the Git repository folder and execute the following command:

```
python -m pip install -r requirements.txt
```

This command will read the requirements.txt file and install all the necessary Python packages listed within it.

To run the model, execute the following command:

```
python predict.py --dataset <dataset_path> --model <model_path> --output <output_path[OPTIONAL]>
```

In this command:

- `<dataset_path>` should point to your input dataset, which must be in JSON format.

- `<model_path>` refers to the location of the pre-trained model file, which must be in the Joblib format (.joblib).

- The `<output_path>` must is optional and specifies where you would like the prediction results to be saved. If you do not provide this argument, the output will default to the name `output.csv` in the same directory.

For further assistance, you can run `python predict.py -h` to view additional information.

## Example Dataset and Output

An example dataset `example.json` has been included, with its corresponding output prediction `example_output.csv`. To replicate this, execute the following command:

```
python predict.py --dataset example/example.json --model model/model.joblib --output example/output.csv
```
