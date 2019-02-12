#!/usr/bin/env python
import urllib.request
import urllib.parse
import json
import requests
from common.log import loggers

logger = loggers()


class SaltAPI(object):
    __token_id = ''

    def __init__(self, url, user, passwd):
        self.__url = url
        self.__user = user
        self.__password = passwd
        self.__token_id = self.get_token_id()

    def get_token_id(self):
        # user login and get token id
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        print(params)
        obj = urllib.parse.urlencode(params).encode('utf-8')
        url = str(self.__url) + '/login'
        req = urllib.request.Request(url, obj)
        try:
            opener = urllib.request.urlopen(req, timeout=60)
            content = json.loads(opener.read())
            token_id = content['return'][0]['token']
        except Exception as _:
            return ""
        return token_id

    def post_request(self, data, prefix='/', send_token=True):
        url = str(self.__url) + prefix
        if send_token:
            headers = {'X-Auth-Token': self.__token_id, 'Content-type': 'application/json'}
        else:
            headers = {'Content-type': 'application/json'}
        print("Headers: {}".format(headers))
        try:
            # 解析成json
            data = bytes(json.dumps(data), 'utf8')
            req = urllib.request.Request(url, data, headers)
            opener = urllib.request.urlopen(req, timeout=180)
            content = json.loads(opener.read())
        except Exception as e:
            print("[{}] post_request exception: {}".format(__name__, e))
            return str(e)
        return content

    def list_all_key(self):
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        content = self.post_request(params)
        if isinstance(content, dict):
            minions = content['return'][0]['data']['return']
            return minions
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def delete_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]['data']['success']
            return ret
        else:
            return {"status": False, "message": "salt api error : " + content}

    def accept_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]['data']['success']
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def reject_key(self, node_name):
        params = {'client': 'wheel', 'fun': 'key.reject', 'match': node_name}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]['data']['success']
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def remote_noarg_execution(self, tgt, fun):
        # Execute commands without parameters
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0][tgt]
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def remote_noarg_execution_notgt(self, tgt, fun):
        # Execute commands without parameters
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def remote_execution(self, tgt, fun, arg):
        # Command execution with parameters
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0][tgt]
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def remote_execution_notgt(self, tgt, fun, arg):
        # Command execution with parameters
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def shell_remote_execution(self, tgt, arg):
        # Shell command execution with parameters
        params = {'client': 'local', 'tgt': tgt, 'fun': 'cmd.run', 'arg': arg, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def grain(self, tgt, arg):
        # Grains.item
        params = {'client': 'local', 'tgt': tgt, 'fun': 'grains.item', 'arg': arg}
        content = self.post_request(params)
        if isinstance(content, dict):
            ret = content['return'][0]
            return ret
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def grains(self, tgt):
        # Grains.items
        params = {'client': 'local', 'tgt': tgt, 'fun': 'grains.items'}
        content = self.post_request(params, send_token=False)
        if isinstance(content, dict):
            ret = content['return'][0]
            logger.info("Grains data: {}".format(ret))
            return {"status": True, "message": "", "data": ret}
        else:
            return {"status": False, "message": "[GRAINS] Salt API Error : " + content}

    def target_remote_execution(self, tgt, fun, arg):
        # Use targeting for remote execution
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'nodegroup'}
        content = self.post_request(params)
        if isinstance(content, dict):
            jid = content['return'][0]['jid']
            return jid
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def deploy(self, tgt, arg):
        # Module deployment
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        content = self.post_request(params)
        return content

    def async_deploy(self, tgt, arg):
        # Asynchronously send a command to connected minions
        params = {'client': 'local_async', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg}
        content = self.post_request(params)
        if isinstance(content, dict):
            jid = content['return'][0]['jid']
            return jid
        else:
            return {"status": False, "message": "salt api error : " + content}

    def target_deploy(self, tgt, arg):
        # Based on the list forms deployment
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            try:
                return content.get("return")[0]
            except Exception as e:
                return {"status": False, "message": str(e)}
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def pillar_items(self, tgt, arg=[]):
        # Get pillar item
        if arg:
            params = {'client': 'local', 'tgt': tgt, 'fun': 'pillar.item', 'arg': arg, 'expr_form': 'list'}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': 'pillar.items', 'arg': arg, 'expr_form': 'list'}
        content = self.post_request(params)
        if isinstance(content, dict):
            try:
                return content.get("return")[0]
            except Exception as e:
                return {"status": False, "message": str(e)}
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def jobs_list(self):
        # Get Cache Jobs Default 24h '''
        url = self.__url + '/jobs/'
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, headers=headers)
        try:
            opener = urllib.request.urlopen(req)
            content = json.loads(opener.read())
        except Exception as e:
            return str(e)
        if isinstance(content, dict):
            jid = content['return'][0]
            return jid
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def jobs_info(self, arg):
        # Get Job detail info '''
        url = self.__url + '/jobs/' + arg
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, headers=headers)
        try:
            opener = urllib.request.urlopen(req)
            content = json.loads(opener.read())
        except Exception as e:
            return str(e)
        if isinstance(content, dict):
            jid = content['return'][0]
            return jid
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def stats(self):
        # Expose statistics on the running CherryPy server
        url = self.__url + '/stats'
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib.request.Request(url, headers=headers)
        try:
            opener = urllib.request.urlopen(req)
            content = json.loads(opener.read())
        except Exception as e:
            return str(e)
        if isinstance(content, dict):
            return content
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def runner_status(self, arg):
        # Return minion status
        params = {'client': 'runner', 'fun': 'manage.' + arg}
        print("[{}] params: {}".format(__name__, params))
        content = self.post_request(params)
        if isinstance(content, dict):
            jid = content['return'][0]
            return jid
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def runner(self, arg):
        # Return minion status
        params = {'client': 'runner', 'fun': arg}
        content = self.post_request(params)
        if isinstance(content, dict):
            jid = content['return'][0]
            return jid
        else:
            return {"status": False, "message": "Salt API Error : " + content}

    def events(self):
        # SSE get job info '''
        url = self.__url + '/events'
        headers = {'X-Auth-Token': self.__token_id}
        req = requests.get(url, stream=True, headers=headers)
        return req

    def hook(self, tag=""):
        # Fire an event in Salt with a custom event tag and data
        url = self.__url + '/hook/' + tag
        headers = {'X-Auth-Token': self.__token_id}
        # data = json.dumps({"gitfs": "update"})
        # data = bytes(data, 'utf8')
        req = urllib.request.Request(url, headers=headers, method="POST")
        try:
            opener = urllib.request.urlopen(req)
            content = json.loads(opener.read())
        except Exception as e:
            return str(e)
        if isinstance(content, dict):
            return content
        else:
            return {"status": False, "message": "Salt API Error : " + content}
