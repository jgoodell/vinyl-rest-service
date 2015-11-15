import sys
import requests


if __name__ == "__main__":

    if len(sys.argv) == 3:
        method = sys.argv[1]
        uri = sys.argv[2]
    else:
        print("Usage:")
        print("%s <method> <uri>" % sys.argv[0])
        print("example: %s POST http://localhost:5000/archive/Weezer/Weezer/1994/" % sys.argv[0])
        sys.exit(1)

    if method.upper() == "GET":
        response = requests.get(uri)
    elif method.upper() == "POST":
        response = requests.post(uri)
    elif method.upper() == "PUT":
        response = requests.put(uri)
    elif method.upper() == "DELETE":
        response = requests.delete(uri)
    else:
        print("Usage:")
        print("%s <method> <uri>" % sys.argv[0])
        print("example: %s POST http://localhost:5000/archive/Weezer/Weezer/1994/" % sys.argv[0])
        sys.exit(1)
    
    print(response.status_code)
    print(response.text)
    sys.exit(0)
