#!/bin/env python

layers = open('layers.lst','r+')
tffile = open('ft.tf','w+')
otffile = open('oft.tf', 'w+')

for layer in layers.readlines():
  layer = layer.strip()

  ulayer = layer.replace("-","_")
  if layer.startswith('fc-app') or layer.startswith('hk-app'):
    s =  """resource "aws_opsworks_custom_layer" "%s" {
      name                        = "%s"
      short_name                    = "%s"
      stack_id                    = "${aws_opsworks_stack.appstack.id}"
      auto_healing                = false
      custom_security_group_ids   = "${split(",",var.app_security_group_ids)}"
      custom_setup_recipes        = "${var.app_setup_recipes}"
      custom_deploy_recipes       = "${var.app_deploy_recipes}"
      custom_configure_recipes    = "${var.app_configure_recipes}"
      custom_undeploy_recipes     = "${var.app_undeploy_recipes}"
      custom_shutdown_recipes     = "${var.app_shutdown_recipes}"
      system_packages             = "${var.app_system_packages}"
  }"""% (ulayer,layer,layer)
  else:
    s = """resource "aws_opsworks_custom_layer" "%s" {
    name                        = "%s"
    short_name                    = "%s"
    stack_id                    = "${aws_opsworks_stack.appstack.id}"
    auto_healing                = false
    custom_security_group_ids   = "${split(",",var.bg_security_group_ids)}"
    custom_setup_recipes        = "${var.bg_setup_recipes}"
    custom_deploy_recipes       = "${var.bg_deploy_recipes}"
    custom_configure_recipes    = "${var.bg_configure_recipes}"
    custom_undeploy_recipes     = "${var.bg_undeploy_recipes}"
    custom_shutdown_recipes     = "${var.bg_shutdown_recipes}"
    system_packages             = "${var.bg_system_packages}"
  }"""% (ulayer,layer,layer)
  
  p = """output "%s_id" {
    value = "${aws_opsworks_custom_layer.%s.id}"
    description = "The id of the %s layer"
}"""% (ulayer,ulayer,layer)
  tffile.write("{}\n\n".format(s))
  otffile.write("{}\n\n".format(p))

layers.seek(0)

