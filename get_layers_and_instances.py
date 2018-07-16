#!/bin/env python
import boto3

opsworks = boto3.client('opsworks')
first_stack = "xxxx-xxx-xxxx-xxxxx-xxxxxx"
second_stack = "nnnnn-nnn-nnnn-nnnnn-nnnnn"

first_layers = opsworks.describe_layers(StackId=first_stack)
second_layers = opsworks.describe_layers(StackId=second_stack)

layers_csv = open('layers.csv', 'w+')
layers_csv.write("LAYERS;INSTANCES;SETUP;CONFIGURE;DEPLOY;UNDEPLOY;SHUTDOWN;LAYER_SETTINGS\n")
layers_csv.write("FIRSTSTACK;--;--;--;--;--;--;--\n")
for layer in first_layers['Layers']:
  instances = opsworks.describe_instances(LayerId=layer['LayerId'])
  n_instances = len(instances['Instances'])
  setup = (",").join(layer['CustomRecipes']['Setup'])
  configure = (",").join(layer['CustomRecipes']['Configure'])
  deploy = (",").join(layer['CustomRecipes']['Deploy'])
  undeploy = (",").join(layer['CustomRecipes']['Undeploy'])
  shutdown = (",").join(layer['CustomRecipes']['Shutdown'])
  if 'CustomJson' in layer.keys():
    custom_json = layer['CustomJson']
  else:
    custom_json = "--"

  layers_csv.write("{};{};{};{};{};{};{};{}\n".format(layer['Name'],n_instances,setup,configure,deploy,undeploy,shutdown,custom_json ))


layers_csv.write("SECONDSTACK;--;--;--;--;--;--;--\n")
for layer in second_layers['Layers']:
  instances = opsworks.describe_instances(LayerId=layer['LayerId'])
  n_instances = len(instances['Instances'])
  setup = (",").join(layer['CustomRecipes']['Setup'])
  configure = (",").join(layer['CustomRecipes']['Configure'])
  deploy = (",").join(layer['CustomRecipes']['Deploy'])
  undeploy = (",").join(layer['CustomRecipes']['Undeploy'])
  shutdown = (",").join(layer['CustomRecipes']['Shutdown'])
  if 'CustomJson' in layer.keys():
    custom_json = layer['CustomJson']
  else:
    custom_json = "--"
  
  layers_csv.write("{};{};{};{};{};{};{};{}\n".format(layer['Name'],n_instances,setup,configure,deploy,undeploy,shutdown,custom_json ))

layers_csv.flush()
layers_csv.close()