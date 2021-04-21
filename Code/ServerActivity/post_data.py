import requests as req


def post_value(data):
    """
    Send sensor data using "POST" method of localhost server
    using request library
    """
    resp = ""
    try:
        resp = req.post("http://localhost:8000/", json=data)

        print(resp.url)
        print(resp.text)
        print(resp.status_code)
    except Exception as e:
        print(e)
        resp = "unavailable"

    return resp

if __name__ == "__main__":
    data_1 = {'name': 'Peter', 'age': 23}
    post_value(data_1)