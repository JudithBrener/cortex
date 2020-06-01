[![Build Status](https://travis-ci.com/JudithBrener/cortex.svg?branch=master)](https://travis-ci.com/JudithBrener/cortex)
[![codecov](https://codecov.io/gh/JudithBrener/cortex/branch/master/graph/badge.svg)](https://codecov.io/gh/JudithBrener/cortex)
# Cortex
## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:JudithBrener/cortex.git
    ...
    $ cd cortex/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    $ # This may take up to few minutes the first time
    ...
    $ source .env/bin/activate
    [cortex] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:

    ```sh
    $ pytest tests/
    ...
    ```
    
## Quick Start
1. Run all services together:

    ```sh
    $ ./scripts/run-pipeline.sh
    $ # This may take up to few minutes the first time
    ```
    
2. Upload a sample (.mind or .mind.gz file):
   Use --help flag for help.

    ```sh
    $ python -m cortex.client upload-sample <path_to_mind_file>
    ```
    
3. Go to 'http://localhost:8080' to see all mind thoughts. 

    ```sh
    $ python -m cortex.client upload-sample <path_to_mind_file>
    ```
    
4. Alternatively use the CLI to see the data:

    ```sh
    $ python -m cortex.cli get-users
    [{'user_id': '6', 'username': 'Judith Brener'}]
    ...
    ```
## Adding new parser
Add your parser file in parsers package.
- The file name must start with `parser_` e.g. `parser_pose.py`

Parser can be implemented as a function or a class:
- Function:
    
    Function name must be of the form `parse_<parser-name>` 
    
    Function Module must have an attribute called `field`
        
  ```python
  def parse_pose(message):
    ...
  parse_pose.field = 'pose'
  ```
  
- Class:

    Class must have an attribute called `field`

    Class must have the parsing static method called `parse`
    
  ```python
  class ColorImageParser:
    field = 'color_image'

    @staticmethod
    def parse(message):
      ...
  ```

## Usage

The `cortex` packages provides the following components:
Each exposes an API and CLI to use.

- `Client`

    Enables to upload cognition thoughts.

    ```pycon
    >>> from cortex.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
    … # upload path to host:port
    ```
    
  ```sh
  $ python -m cortex.client upload-sample \
      -h/--host '127.0.0.1'               \
      -p/--port 8000                      \
      'snapshot.mind.gz'
  …
  ```

- `Server`

    Receives thoughts from the client and publishes them to a message queue.

    ```pycon
    >>> from cortex.server import run_server
    >>> def print_message(message):
    ...     print(message)
    >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
    … # listen on host:port and pass received messages to publish
    ```
    
  ```sh
  $ python -m cortex.server run-server \
      -h/--host '127.0.0.1'            \
      -p/--port 8000                   \
      'rabbitmq://127.0.0.1:5672/'
  ```

- `Parsers`

    Parses thoughts data as as consumed from the message queue (JSON), and returns the result.

    ```pycon
    >>> from cortex.parsers import run_parser
    >>> data = … 
    >>> result = run_parser('pose', data)
    ```
    
  ```sh
  $ python -m cortex.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
  ```
  
  CLI also support running the parser as a service, which works with a message queue indefinitely.
  Consuming thoughts from a message queue and publishes parsed results to dedicated topics.
  
  ```sh
  $ python -m cortex.saver run-saver  \
      'mongodb://127.0.0.1:27017'     \
      'rabbitmq://127.0.0.1:5672/'
  ```
- `Saver`

    Saves parsed thoughts, as consumed from the message queue (JSON), to a database.
    
    ```pycon
    >>> from cortex.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
    ```
  
  ```sh
  $ python -m cortex.saver save                  \
      -d/--database 'mongodb://127.0.0.1:27017'  \
      'pose'                                     \
      'pose.result' 
  ```
  
  CLI also support running the saver as a service, which works with a message queue indefinitely; 
  th saver subscribes to all the relevant topics it is capable of consuming
  
  ```sh
  $ python -m cortex.saver run-saver  \
      'mongodb://127.0.0.1:27017'     \
      'rabbitmq://127.0.0.1:5672/'
  ```
- `API`

    RESTful API which exposes the parsed thoughts.

    ```pycon
    >>> from cortex.api import run_api_server
    >>> run_api_server(
    ...     host = '127.0.0.1',
    ...     port = 5000,
    ...     database_url = 'mongodb://127.0.0.1:27017',
    ... )
    … # listen on host:port and serve data from database_url
    ```
    
  ```sh
  $ python -m cortex.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'mongodb://127.0.0.1:27017'
  ```

- `CLI`

    Consumes the API and reflects it
    
  ```sh
  $ python -m cortex.cli get-users
    …
    $ python -m cortex.cli get-user 1
    …
    $ python -m cortex.cli get-snapshots 1
    …
    $ python -m cortex.cli get-snapshot 1 2
    …
    $ python -m cortex.cli get-result 1 2 'pose'
    …
  ```
  
- `GUI`

    Consumes the API and provides a graphical user interface to view the thoughts.

    ```pycon
    >>> from cortex.gui import run_server
    >>> run_server(
    ...     host = '127.0.0.1',
    ...     port = 8080,
    ...     api_host = '127.0.0.1',
    ...     api_port = 5000,
    ... )
    ```
    
  ```sh
  $ python -m cortex.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
  ```

All CLI commands accept the `--help` flag.

If Error occurs, full traceback is shown and the program exits with a
non-zero code.
