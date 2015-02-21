<snippet>
  <content>
# Two-phases-commit

The first project in Distributed Computing: Two phases commit

## Installation
##### Have to make sure the following tools available in both server and client machines. 

1. sqlite3
2. python
3. fabric

##### Have Fabric ready to streamline client processes. 
In this project, fabfile will be run on server machine for simplicity. 


## Environment Setup

1. Run command: python server.py
2. Now the server is up
3. vim ClientSetUp.py, change proxy_id to ip of server you just set up  
    ```
      proxy_id = <server_ip>
    ```
4. vim fabfile.py, set env.host to server ip and all client ip
    ` env.hosts = [<server_ip>, <client1_ip>, ..., <clientN_ip>] `
5. vim fabfile.py, define server/client roles
   ```
       env.roledefs.update({
       'server': [<server_ip>],
       'client': [<client1_ip>, ..., <clientN_ip>]
       }) 
    ```
6. Run command `fab setup` to put the python files to clients and create tables in sqlite.
7. Now everything is up and running! Start your exploration!

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
