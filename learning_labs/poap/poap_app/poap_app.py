from flask import Flask, render_template, request
from flask_restful import Resource, Api
import yaml
from jinja2 import Environment, FileSystemLoader
import os.path

app = Flask(__name__)
api = Api(app)

switch_id = {}

def render_conf(cwd, switch):
    # Set up the templates info for rendering device config
    TEMPLATE_ENVIRONMENT = Environment(
        autoescape=False,
        loader=FileSystemLoader(os.path.join(cwd, 'templates')),
        trim_blocks=False)
    
    out_file = os.path.join(cwd, ('templates/' + switch['id'] + '.cfg'))
    with open(out_file, 'w') as fh:
        config = TEMPLATE_ENVIRONMENT.get_template('conf_nxv.j2').render(switch)
        fh.write(config)

    # Return device specific info needed for OS install
    switch_info = {}
    switch_info['system_image'] = switch['system_image']
    switch_info['kickstart_image'] = switch['kickstart_image']
        
    return(switch_info)


class SwitchID(Resource):

    def get(self, s_no):
        return {s_no: switch_id['s_no']}

    def put(self, s_no):
        """build out the config file, based on the Serial No. Return the following:
         1. Name of the config file (after creating it) 2. Name of the
         system image 3. IP address of the tftp server
        """
        cwd = os.path.dirname(os.path.abspath(__file__))
        poap_info = {}
        switch_id[s_no] = request.form['data']
        # If the MAC address is known but the S_NO is not,
        # use the mac address and S_NO to populate the podvars.yaml file
        with open(os.path.join(cwd,'podvars.yml')) as fh:
            vars = yaml.load(fh)

        for switch in vars['switches']:
            if switch.get('id') == s_no: # Operator is using the serial number
                poap_info.update(render_conf(cwd, switch))
            elif switch.get('id') == request.form['data']: # Operator is using the MAC
                switch['id'] = s_no # Use the s_no to render the config
                poap_info.update(render_conf(cwd, switch))
            #End For loop
            
        poap_info['tftp_server'] = vars['pod']['tftp_server']
        poap_info['config_file'] = s_no + '.cfg'
        poap_info['http_server'] = vars['pod']['http_server']
        poap_info['config_protocol'] = vars['pod']['protocol']
        print(poap_info)
        return(poap_info)



api.add_resource(SwitchID, '/<string:s_no>')


@app.route('/conf/<s_no>')
def return_conf(s_no):
    return render_template(s_no + '.cfg')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
