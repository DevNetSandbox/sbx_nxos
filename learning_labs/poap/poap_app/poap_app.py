from flask import Flask, render_template, request
from flask_restful import Resource, Api
import yaml
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
api = Api(app)

switch_id = {}

class SwitchID(Resource):

    def get(self, s_no):
        return {s_no: switch_id['s_no']}

    def put(self, s_no):
        poap_info = {}
        switch_id[s_no] = request.form['data']
        # build out the config file, based on the s_no
        # Return the following:
        #   1. Name of the config file (after creating it)
        #   2. Name of the system image
        #   3. IP address of the tftp server
        with open('podvars.yml') as fh:
            vars = yaml.load(fh)
        #_render_config(vars)
        TEMPLATE_ENVIRONMENT = Environment(
            autoescape=False,
            loader=FileSystemLoader('templates'),
            trim_blocks=False)
        
        for switch in vars['switches']:
            if s_no == switch['s_no']:
                poap_info['system_image'] = switch['details']['system_image']
                poap_info['kickstart_image'] = switch['details']['kickstart_image']
                poap_info['hostname'] = switch['details']['hostname']
                out_file = 'templates/' + switch['s_no'] + '.cfg'
                with open(out_file, 'w') as fh:
                    config = TEMPLATE_ENVIRONMENT.get_template('conf_nxv.j2').render(switch)
                    fh.write(config)
        poap_info['tftp_server'] = vars['pod']['tftp_server']
        poap_info['config_file'] = s_no + '.cfg'
        poap_info['http_server'] = vars['pod']['http_server']
        poap_info['config_protocol'] = vars['pod']['protocol']
        return(poap_info)


api.add_resource(SwitchID, '/<string:s_no>')


@app.route('/conf/<s_no>')
def return_conf(s_no):
    return render_template(s_no + '.cfg')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
