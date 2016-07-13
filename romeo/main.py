###############################################################################
# Author: Daniil Budanov
# Contact: danbudanov@gmail.com
# Summer Internship - 2016
###############################################################################
# Title: main.py
# Project: Romeo Robot
# Description:
#   - Instantiates server
#   - creates routes for API
#   - runs server
# Last Modified: 7.13.2016
###############################################################################
from robot import *

# instantiate Flask server
app = Flask(__name__)
api = Api(app)

# create routes for Flask API
api.add_resource(Start, '/actions/start')
api.add_resource(Stop, '/actions/stop')
api.add_resource(LongTurn, '/actions/longturn')
api.add_resource(PointTurn, '/actions/pointturn')
api.add_resource(Wheels, '/actions/wheels/<wheel_number>')
api.add_resource(Forward, '/actions/forward', '/actions/forwards')
api.add_resource(Path, '/paths/administer/<path_name>', '/paths/administer')
api.add_resource(ExecutePath, '/paths/execute/<path_name>')

# Run flask server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) # host makes server accessible on network
