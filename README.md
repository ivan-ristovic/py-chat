# py-chat

A simple TCP client-server chat program implemented in Python.

![ss](https://raw.githubusercontent.com/ivan-ristovic/py-chat/master/screenshots/2017-02-24.png)

## Usage

First you need to start a server. It uses port 5000 by default.
```
$ python server.py
```

After that you can connect clients to your server. For example, this will connect you to your local server:
```
$ python client.py localhost 5000
```

Now socialize!

## Known bugs

On Windows there are some errors, I am working on it!
