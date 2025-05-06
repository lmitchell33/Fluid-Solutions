# **Fluid-Solutions: Blood Volume Status Monitor**

## **Overview**

This is our senior capstone project and it is a desktop application using an XGBoost model to estimate blood volume status based on vital signs and patient metrics. The XGBoost model was custom developed using the MIMIC-IV dataset of ICU vital signs and has an accuracy of approximately 96%. The application provides an easy-to-use graphical interface for inputting vital signs, displaying predictions, and visualizing the entered data. The tool is inteded to be used in the ICU, specifically within a vitals monitor or a on a smaller screen/laptop and is designed to be plug-and-play with little to no installation.

## **Built With**

- **Containerization:** Docker
- **Programming Languages:** Python, Bash
- **Framework:** PyQT6
- **Operating System:** Unix/Linux (Raspbian & Ubuntu)

## **Getting Started**

Follow these steps to setup and run the desktop application on your machine.

### Installation

NOTE: This guide assumes you have both python and pip installed

1. Clone the repository

```sh
git clone https://github.com/lmitchell33/Fluid-Solutions.git && cd Fluid-Solutions
```

2. Install the requirements

```sh
pip install -r requirements.txt
```

3. Change into the app directory

```sh
ch app/
```

4. Initalize the Database
```sh
python3 app.py --initdb
```

4. Start the app (note, you must be in the app directory)

```sh
python3 app.py
```

### Faking the vitals montior
Becuase we did not have access to a real vitals montior, and we still needed to demonstrate how the tool works and what it does, we decided to fake the vitals monitor. This was done by creating a Docker container running a python script which will 'act' as a vitals monitor. The steps to run this are found below:

If Docker is not installed, please refer to the docker documentation for installation steps

1. Start the Docker daemon

2. Change into the vitals agent directory (assuming you are in the ~/Fluid-Solutions directory)
```sh
ch vitals_agent/
```

3. Build the docker container
```sh
docker build -t [name]
```

4. Run the container
```sh
docker run --network=host [name]
```

## **Acknowledgements**

- **Dr. Leda Kloudas**  
  _Ph.D., Bioengineering,_  
  Duquesne University, School of Science and Engineering  
  _Project Mentor_

- **Dr. Leda Kloudas**  
  _Ph.D., Applied Mathematics,_  
  Duquesne University, School of Science and Engineering  
  _Machine Learning Mentor_

- **Jake Graham**  
   _Critical Care PA-C_  
   UPMC Presbyterian  
   _Clinical Mentor_
