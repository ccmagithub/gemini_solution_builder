heat_template_version: 2014-10-16

description: >
  A HOT template that holds a VM instance with an attached
  Cinder volume.  The VM does nothing but enable salt agent.

parameters:
  key_name:
    type: string
    description: Name of an existing key pair to use for the instance
    constraints:
      - custom_constraint: nova.keypair
        description: Must name a public key (pair) known to Nova
  flavor:
    type: string
    description: Flavor for the instance to be created
    default: m1.small
    constraints:
      - custom_constraint: nova.flavor
        description: Must be a flavor known to Nova
  image:
    type: string
    description: >
      Name or ID of the image to use for the instance.
      You can get the default from
      http://cloud.fedoraproject.org/fedora-20.x86_64.qcow2
      There is also
      http://cloud.fedoraproject.org/fedora-20.i386.qcow2
      Image should contain cloud-init package for enabling salt agent.
    constraints:
      - custom_constraint: glance.image
        description: Must identify an image known to Glance
  network:
    type: string
    description: The network for the VM
    default: net04
  vol_size:
    type: number
    description: The size of the Cinder volume
    default: 15
  portal_ip:
    type: string
    constraints:
      - allowed_pattern: "([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])"
    description: This is reserved for Gemini portal

resources:
   enable_salt:
    type: OS::Heat::SoftwareConfig
    properties:
      config:
        str_replace:
          template: {get_file: enable_salt.sh}
          params:
            $PORTAL_IP: {get_param: portal_ip}

   iaasvm_cloud_config:
    type: OS::Heat::CloudConfig
    properties:
      cloud_config:
        output:
          all: '| tee -a /var/log/cloud-init-output.log'

  iaasvm_init:
    type: OS::Heat::MultipartMime
    properties:
      parts:
        - config: {get_resource: enable_salt}
        - config: {get_resource: iaasvm_cloud_config}

  instance:
    type: OS::Nova::Server
    properties:
      key_name: { get_param: key_name }
      image: { get_param: image }
      flavor: { get_param: flavor }
      networks: [{network: {get_param: network} }]

  my_vol:
    type: OS::Cinder::Volume
    properties:
      size: { get_param: vol_size }

  vol_att:
    type: OS::Cinder::VolumeAttachment
    properties:
      instance_uuid: { get_resource: instance }
      volume_id: { get_resource: my_vol }
      mountpoint: /dev/vdb

outputs:
  instance_networks:
    description: The IP addresses of the deployed instance
    value: { get_attr: [instance, networks] }

  instance_info:
    value: {get_attr: [instance, show]}

