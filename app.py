import os
from flask import Flask
if os.path.exists("env.py"):
    import env


app = Flask(__name__) # create instance of Flask in a variable called "app"


@app.route("/") # the forward slash "/" refers to the default route
def hello():
    return "Hello World...Again!"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True) # IMPORTANT - Make sure to change to 
                        #"debug=False" prior to actual deployment
