# SCRIPTS

Just a some utilty scripts to get on with things. Description of each script is as found below.

### Build App Template

`build_app_template.py`, is a script to get a list of layers in list file, and take them, and build a `tf`(terraform) file.

### Get Layers and Instance

`get_layers_and_instances.py`, is a script to get a list layers and the number of instances, from opsworks, in that those layers as a csv file. This script also gets the revices in those layers.

### Create Terraform Template for Instances

`create-template.py`, is a script to create terraform template for instances on an opsworks stack. It is two step process. First create the `manifest.yml` file where you specify various things about your instances, the manifest file is itself self descriptive, to create the this file use the following command.

```
python create-template.py init <stack_id>
```

Then once you have edited the file you should be ready to create the terraform template.

```
python create-template.py terraform mainfest.yml
```

Good luck.

