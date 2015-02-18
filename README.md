<snippet>
  <content>
# Two-phases-commit

The first project in Distributed Computing: Two phases commit

## Installation

TODO: Describe the installation process

## Usage

##### Server Side
1. Fetch IP address of server.
   - MAC users: /sbin/ifconfig en0 | grep 'inet '| cut -d ' ' -f 2
   - Linux users: $ /sbin/ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'
2. Run bash command: python server.py <ip_address> 
3. Now the server is up

##### Client Side
1. 



## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

TODO: Write license
  <tabTrigger>readme</tabTrigger>
</snippet>
