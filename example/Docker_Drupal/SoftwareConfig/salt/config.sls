apache2:
  file.managed:
    - source: salt://drupal/files/settings.php
    - name: /usr/share/drupal7/sites/default/settings.php
    - mode: 644
    - user: www-data
    - group: www-data
    - template: jinja
    - defaults:
      ALF_IP: {{ pillar['drupal']['ARG1'] }}
    - order: 1

  service:
    - running
    - enable: True
    - reload: True
    - order: -1

/etc/init.d/apache2 restart:
  cmd.run:
    - order: 3
