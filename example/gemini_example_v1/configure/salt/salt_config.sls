logstash-forwarder:
  file.managed:
    - source: salt://logstash/files/linux/logstash-forwarder.conf
    - name: /etc/logstash-forwarder.conf
    - mode: 644
    - user: www-data
    - group: www-data
    - template: jinja
    - defaults:
      paths: {{ pillar['logstash']['PATHS'] }}
      inst_uuid: {{ pillar['logstash']['INST_UUID'] }}
      server_ip: {{ pillar['logstash']['SERVER_IP'] }}
      server_port: {{ pillar['logstash']['SERVER_PORT'] }}
    - order: 1

  service:
    - running
    - enable: True
    - reload: True
    - order: -1

create_folder:
  file.directory:
    - name: /etc/pki/tls/certs/logstash-forwarder/
    - makedirs: True
    - order: 1

ssl-ca:
  file.managed:
    - source: salt://logstash/files/{{ pillar['logstash']['TENANT_ID'] }}.crt
    - name: /etc/pki/tls/certs/logstash-forwarder/logstash-forwarder.crt
    - order: 2

/etc/init.d/logstash-forwarder restart:
  cmd.run:
    - order: 3
