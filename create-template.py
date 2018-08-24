#!/usr/bin
import boto3
import yaml
import click

@click.group()
def terraforming():
  pass

opsworks = boto3.client('opsworks')

@terraforming.command(help='Create the manifest from the stack')
@click.argument('stack_id')
def init(**kwargs):
  stack_id = kwargs['stack_id']
  layers = opsworks.describe_layers(StackId=stack_id)
  yml = open('manifest.yml', 'w+')
  yml.write("---\n")
  yml.write('stack_id: {} # Stack Id of the stack to use\n'.format(stack_id))
  yml.write('os:     # Instance os type\n')
  yml.write('ami:    # Instance of which ami\n')

  layer_dict = {}
  for layer in layers['Layers']:
    layer_dict[layer['Shortname']] = layer['LayerId']
  
  layers_sorted = sorted(layer_dict)

  for layer in layers_sorted:
    shortname = layer
    id = layer_dict[layer]
    prefix = "-".join(shortname.split("-")[2:]) if shortname.split("-")[2:] else "fc-app" if  shortname.find("fc") == 0 else "app"   
    yml.write('{}:\n'.format(shortname))
    yml.write('  id: {}  # LayerId\n'.format(id))
    yml.write('  prefix: {}- # Instance hostname prefix\n'.format(prefix))
    yml.write('  count: 0 # Instance count\n')
    yml.write('  type:   # Instance type\n')
    yml.write('  subnets: [] # Instance in which subnet\n')

  yml.write('special_instances:\n')
  yml.write('  - instance: # Name of the instance\n')
  yml.write('    id:       # LayerId\n'.format(id))
  yml.write('    type:     # Instance type\n')
  yml.write('    subnet:   # Instance in which subnet\n')

  yml.flush()
  yml.close()


# resource "aws_opsworks_instance" "my-instance" {
#   stack_id = "${aws_opsworks_stack.main.id}"

#   layer_ids = [
#     "${aws_opsworks_custom_layer.my-layer.id}",
#   ]

#   instance_type = "t2.micro"
#   os            = "Amazon Linux 2015.09"
#   state         = "stopped"
# }

@terraforming.command(help='Create the terraform template provided manifest.yml')
@click.argument('manifest', default='manifest.yml')
def terraform(**kwargs):
  yml = yaml.load(open(kwargs['manifest'],'r+'))
  tf_template = open('main.tf','w+')
  ami = yml.pop('ami')
  os = yml.pop('os')
  stack_id = yml.pop('stack_id')
  special_instances = yml.pop('special_instances')
  for key in yml.keys():
    count = yml[key]['count']
    prefix = yml[key]['prefix']
    layer_id = yml[key]['id']
    instance_type = yml[key]['type']
    for x in range(count):
      subnet = yml[key]['subnets'][x%len(yml[key]['subnets'])]
      tf_template.write('resource "aws_opsworks_instance" "{0}{1}" '.format(prefix, x))
      tf_template.write('{\n')
      tf_template.write('  stack_id = "{}"\n'.format(stack_id))
      tf_template.write('  layer_ids = ["{}",]\n'.format(layer_id))
      tf_template.write('  instance_type = "{}"\n'.format(instance_type))
      tf_template.write('  os = "{}"\n'.format(os))
      tf_template.write('  ami = "{}"\n'.format(ami))
      tf_template.write('  state = "${var.state}"\n')
      tf_template.write('  root_block_device = "ebs"\n')
      tf_template.write('  subnet_id = "{}"\n'.format(subnet))
      tf_template.write('}\n\n')
    
  for instance in special_instances:
    layer_id = instance['id']
    instance_type = instance['type']
    name = instance['instance']
    subnet = instance['subnet']
    tf_template.write('resource "aws_opsworks_instance" "{}" '.format(name))
    tf_template.write('{\n')
    tf_template.write('  stack_id = "{}"\n'.format(stack_id))
    tf_template.write('  layer_ids = ["{}",]\n'.format(layer_id))
    tf_template.write('  instance_type = "{}"\n'.format(instance_type))
    tf_template.write('  os = "{}"\n'.format(os))
    tf_template.write('  ami = "{}"\n'.format(ami))
    tf_template.write('  state = "${var.state}"\n')
    tf_template.write('  root_block_device = "ebs"\n')
    tf_template.write('  subnet_id = "{}"\n'.format(subnet))
    tf_template.write('}\n\n')

  tf_template.flush()
  tf_template.close()

if __name__ == "__main__":
  terraforming()