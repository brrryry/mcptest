## MCP Test
This is a repository that was made in order to simulate simple MCP tool usage.

### Setting up the Server
- Go into the server directory (``cd server``)
- (OPTIONAL) Create your [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements (``pip install -r requirements.txt``)
- Run using ``python weather.py``

### Setting up the Client
- Go into the client directory (``cd client``)
- (OPTIONAL) Create your [virtual environment](https://docs.python.org/3/library/venv.html)
- Install requirements (``pip install -r requirements.txt``)
- Rename ``.env.example`` to ``.env``!
- Replace the "\<your-api-key\>" in `.env` with a [valid Anthropic API key](https://console.anthropic.com)!
- Run using ``python client.py ../server/weather.py``

NOTE: As of current, this connectivity between the client and server has NOT been tested due to the abscence of a free LM (mannnnn....).