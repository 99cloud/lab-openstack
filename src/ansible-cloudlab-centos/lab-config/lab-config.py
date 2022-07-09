labs = [i.split() for i in open(r'lab.txt') if i.strip()]
labs = [('coa%03d' % int(i[0]), i[3]) for i in labs]

aStr = '''
Host %s
    HostName        %s
    User            root
    IdentityFile    ~/.ssh/coa-key.key
    ProxyCommand    ssh dev99 -W %%h:%%p
'''

print(labs)

for i in labs:
    print(aStr % i, end='')

print('\n')
print('[coalab]')
for i in labs:
    print(i[0])

# ansible -i lab.ini coalab -m ping
# ansible -i lab.ini coalab -m shell -a 'virsh list --all'
# ansible -i lab.ini coalab -m shell -a 'virsh snapshot-list openstack-devstack'
# ansible -i lab.ini coalab -m shell -a 'virsh snapshot-revert openstack-devstack --snapshotname openstack-ready'
