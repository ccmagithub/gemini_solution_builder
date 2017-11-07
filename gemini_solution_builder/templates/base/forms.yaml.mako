create_site:
  - parameter: private_network
    forms: ChoiceField
    label: Network
    # TODO We need to define general syntex on YAML for network
    widget:
      forms: Select
      attrs:
        - class: form-control
        - required: required
  - parameter: image
    forms: ChoiceField
    label: VM Image
    choices:
        - Windows7-2017.2.0: Windows7-2017.2.0
        - Ubuntu14.04-2017.2.0: Ubuntu14.04-2017.2.0
    widget:
      forms: Select
      attrs:
        - class: form-control
  - parameter: flavor
    forms: ChoiceField
    label: Server Size
    choices:
        - 1core2GBmemory20GBdisk: 1core2GBmemory20GBdisk
        - 2cores4GBmemory40GBdisk: 2cores4GBmemory40GBdisk
        - 4cores8GBmemory80GBdisk: 4cores8GBmemory80GBdisk
        - 8cores16GBmemory160GBdisk: 8cores16GBmemory160GBdisk
    widget:
      forms: Select
      attrs:
        - class: form-control
