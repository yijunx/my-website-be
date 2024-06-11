# my-website-be
a monolith one.. not going to be too complicated


# steps to setup poetry

* create network, because the FE will need to stay at same network for "internal" calls using the dns provided by docker! otherwise only external calls can be used. but since we are simulating a kubernetes env, so this is important.

    ```
    docker network create -d bridge my-website 
    ```

* get the .devcontainer
* reopen in devcon
* poetry init
* install stuff

    normal stuff:
    `poetry add xxxx` or `poetry add -G dev xxxx`


    install using git from private repo through ssh (just example pasted from poetry)

    poetry add git+ssh://git@github.com:sdispater/pendulum.git#develop
    poetry add git+ssh://git@github.com:sdispater/pendulum.git#2.0.5

* about files
