# AWS Lambda Shared Layers

This repository is hosting the code from the following blog post: [AWS Lambda & Shared layers for Python](https://www.flaneer.com/blog/aws-lambda-shared-layers-for-python). 

The goal of this repository is to provide simple and effective tools to easily manage Lambda Shared layers, even with multiple AWS accounts or libraries. The Flaneer team will try to update it when internal changes to our own tools are made.

This repository does not currently reflect the state of our tools, but is a good starting point to automatically build and package large serverless shared layers.

### Usage

You can simply use the main function, `building_layer.py` with the following command:
```
python3 building_layer.py --layer_name test-shared-layer-1
```

Make sure to update the default value of your bucket name for example.
You can change the libraries to install in the `requirements.txt` file.