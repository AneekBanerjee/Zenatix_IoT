import requests as req


def get_resp():
    """
    Collect response using "GET" method of localhost server in JSON format
    using request library
    """
    resp_g,resp_h = "",""
    try:
        resp_g = req.get("http://localhost:8000/")
        resp_h = req.head("http://localhost:8000/")

        print(resp_g.url)
        print(resp_g.text)
        print(resp_g.status_code)

        print(resp_h.headers['server'])
        print(resp_h.headers['Date'])
        print(resp_h.headers['Content-type'])

    except Exception as e:
        print(e)
        resp_g,resp_h = "unavailable","unavailable"

    return resp_g,resp_h

if __name__ == "__main__":
    r,h = get_resp()
    print(r)
    print(h)