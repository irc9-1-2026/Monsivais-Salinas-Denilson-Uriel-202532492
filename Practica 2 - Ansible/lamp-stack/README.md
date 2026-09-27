# Stack LAMP con Ansible — Infraestructura del usuario

## Mapeo de infraestructura

| Nombre    | IP             | Grupo(s) inventario      | Roles aplicados |
|-----------|----------------|---------------------------|------------------|
| Ansible_3 | 192.168.5.23   | `control`, `lamp`         | `common`         |
| Ansible_1 | 192.168.5.21   | `dbservers`, `lamp`       | `common`, `db`   |
| Ansible_2 | 192.168.5.22   | `webservers`, `lamp`      | `common`, `web`  |

Ansible_3 es el nodo de control (donde ejecutas `ansible-playbook`). Se conecta a
sí mismo con `ansible_connection=local`, por eso no necesita SSH ni usuario remoto.

## 1. Requisitos previos

En **Ansible_3** (192.168.5.23):

```bash
sudo dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
sudo dnf install -y ansible

ansible-galaxy collection install -r requirements.yml
```

Debes poder conectarte por SSH sin contraseña (clave pública) desde Ansible_3
hacia Ansible_1 y Ansible_2, como el usuario `root` (o ajusta `ansible_user`
en el `inventory` y usa `--become` con `--ask-become-pass` si usas un usuario
normal):

```bash
ssh-copy-id root@192.168.5.21
ssh-copy-id root@192.168.5.22
```

## 2. Verifica la conectividad

```bash
cd lamp-stack
ansible all -m ping
```

Deberías ver `pong` para `ansible1`, `ansible2` y `ansible3`.

## 3. Revisa/edita las contraseñas de MySQL

Antes de ejecutar en serio, cambia los valores de `group_vars/dbservers.yml`
(`mysql_root_password` y `mysql_users[0].password`). Para un entorno real,
usa `ansible-vault`:

```bash
ansible-vault encrypt group_vars/dbservers.yml
```

Y luego ejecuta el playbook con `--ask-vault-pass`.

## 4. Ejecuta el playbook

```bash
# Simulación (no cambia nada, solo muestra qué haría)
ansible-playbook site.yml --check --diff

# Ejecución real
ansible-playbook site.yml
```

## 5. Verifica el resultado

- Web (Ansible_2): abre `http://192.168.5.22/info.php` — deberías ver la
  información de PHP.
- DB (Ansible_1): desde Ansible_2, prueba la conexión remota:

  ```bash
  mysql -h 192.168.5.21 -u webapp_user -p webapp
  ```

## 6. Ejecutar solo una parte

```bash
ansible-playbook site.yml --limit webservers   # solo Ansible_2
ansible-playbook site.yml --limit dbservers    # solo Ansible_3
ansible-playbook site.yml --tags common        # (si agregas tags a las tareas)
```

## Notas sobre los cambios respecto al desafío original

- Se reemplazó `ntp`/`ntpd` por `chrony`/`chronyd` (estándar en RHEL 8/9;
  `ntpd` está obsoleto).
- Se usó `python3-PyMySQL` en vez de depender del cliente MySQL clásico,
  requerido por los módulos `community.mysql.*` en Python 3.
- El firewall de MySQL en Ansible_3 ahora solo permite tráfico desde la IP
  del webserver (`192.168.5.22`) en vez de abrir el puerto 3306 a cualquier
  origen.
- Se agregó `requirements.yml` porque los módulos `firewalld`, `timezone`,
  `selinux` y `mysql_user`/`mysql_db` viven en colecciones externas
  (`community.general`, `ansible.posix`, `community.mysql`) desde Ansible 2.10+.
