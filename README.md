# Entry Point

``` bash
$ dvm

usage: dvm [command] [arguments...]

Doppler Virtual Machine CLI

commands:

  apps
    Your enrolled apps

  disenroll
    Disenroll provider in app

  enroll
    Enroll provider in app

  generate-wallet
    Generate a DOP wallet

  login
    Login by using your wallet address. If a provider id is not given, an account will be created.

  register
    Create new user account linked to your wallet address.

  server
    Start provider server

  wallet
    Your wallet address

optional arguments:
  -h, --help     show this help message and exit
  --debug        toggle debug output
  --quiet        suppress all output
  -v, --version  show program's version number and exit
```


# Test Locally

1. Install dependencies

``` bash
$ python3 setup.py install
```

2. Set API Endpoint [OPTIONAL]

``` bash
$ DVM_HOST="http://api.localhost:3030"
```

3. Run CLI locally

``` bash
$ python3 cli
```
