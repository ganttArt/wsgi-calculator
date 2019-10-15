"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return str(args[0][0] + args[0][1])

def subtract(*args):
    ''' Returns a STRING with the value arg1 - arg2 '''
    return str(args[0][0] - args[0][1]) 

def divide(*args):
    """ Returns a STRING with the value arg1 / arg2 """
    return str(args[0][0] / args[0][1])

def multiply(*args):
    ''' Returns a STRING with the value arg1 * arg2 '''
    return str(args[0][0] * args[0][1])

def home(*args):
    ''' Returns a STRING with a description of how to use the calculator'''
    description = """
<h1>How to use the Calculator</h1>
<body>http://localhost:8080/multiply/3/5   => 15<br>
  http://localhost:8080/add/23/42      => 65<br>
  http://localhost:8080/subtract/23/42 => -19<br>
  http://localhost:8080/divide/22/11   => 2<br>
  http://localhost:8080/               => this page<br>

</body>
    """
    return description

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': home,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    
    if func_name == '':
        args = None
    else:
        args = [int(path[1]), int(path[2])]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        print(path)
        func, args = resolve_path(path)
        body = func(args)
        status = "200 OK"
    except ZeroDivisionError:
        status = "500 Internal Server Error"
        body = "<h1>DO NOT DIVIDE BY 0!!!</h1>"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()