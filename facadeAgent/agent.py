"""
Agent documentation goes here.
"""

__docformat__ = 'reStructuredText'

import logging
import sys
from volttron.platform.agent import utils
from volttron.platform.vip.agent import Agent, Core, RPC
import sys
sys.path.append("/home/sanka/NIRE_EMS/volttron/LoadPriorityControl/LPCv1/")
import sqlite3

from Model.SmartPlug import SmartPlug
from Model.IoTDeviceGroup import IoTDeviceGroup
from Controller.SimpleControlStrategy import SimpleControlStrategy
from Controller.DeviceMonitor import DeviceMonitor
from Controller.DirectControl import DirectControl
from Controller.SheddingControl import SheddingControl
from Controller.IncrementalControl import IncrementalControl
from Controller.EMSControl import EMSControl

_log = logging.getLogger(__name__)
utils.setup_logging()
conn = sqlite3.connect('/home/sanka/NIRE_EMS/volttron/FacadeAgent/Device_configure_database.sqlite')
__version__ = "0.1"


def facadeAgent(config_path, **kwargs):
    """
    Parses the Agent configuration and returns an instance of
    the agent created using that configuration.

    :param config_path: Path to a configuration file.
    :type config_path: str
    :returns: Facadeagent
    :rtype: Facadeagent
    """
    try:
        config = utils.load_config(config_path)
    except Exception:
        config = {}

    if not config:
        _log.info("Using Agent defaults for starting configuration.")

    setting1 = int(config.get('setting1', 1))
    setting2 = config.get('setting2', "some/random/topic")

    return Facadeagent(setting1, setting2, **kwargs)


class Facadeagent(Agent):
    """
    Document agent constructor here.
    """

    def __init__(self, setting1=1, setting2="some/random/topic", **kwargs):
        super(Facadeagent, self).__init__(**kwargs)
        _log.debug("vip_identity: " + self.core.identity)

        self.setting1 = setting1
        self.setting2 = setting2

        self.default_config = {"setting1": setting1,
                               "setting2": setting2}
        # Loading parameters from the configuration database
        
        self._conn = sqlite3.connect('/home/sanka/NIRE_EMS/volttron/FacadeAgent/Device_configure_database.sqlite')
        self._cursor = self._conn.cursor()
        self._cursor.execute("SELECT * FROM devices")
        rows = self._cursor.fetchall()  
        for row in rows:
            print(row[0])
        self._cursor.close()
        self._conn.close()
        self._command ={'building540/NIRE_WeMo_CC_1/w1':1,'building540/NIRE_WeMo_CC_1/w1':0,'building540/NIRE_WeMo_CC_1/w1':1,'building540/NIRE_WeMo_CC_1/w1':0}
        self._group = IoTDeviceGroup() # Group Facade
        self._monitor = DeviceMonitor() # Monitor for smart plug update
        self._controlsimple =  SimpleControlStrategy()
        self._controldirect = DirectControl()
        self._controlshed = SheddingControl()
        self._controlincrement = IncrementalControl()
        self._emscontroller = EMSControl()
        self._emscontroller.add_Controller(self._controlsimple)
        self._emscontroller.set_Group(self._group)
        self._emscontroller.add_Controller(self._controldirect)
        self._emscontroller.add_Controller(self._controlincrement)
        self._emscontroller.add_Controller(self._controlshed)
        
        """Assign smart Plugs to the Group Facade
        """    
        self._smart_plugs={}
        for row in rows:
            plug=SmartPlug(row[0],self.vip)
            self._group.add_Device(plug)
            self._monitor.register_Observer(plug)
            self._smart_plugs[row]=plug
            
        """Updating Observers to update power consumption of each plug
        """
        
        self._monitor.set_EMS_Controller(self._emscontroller)
        
        ##
        

        # Set a default configuration to ensure that self.configure is called immediately to setup
        # the agent.
        self.vip.config.set_default("config", self.default_config)
        # Hook self.configure up to changes to the configuration file "config".
        self.vip.config.subscribe(self.configure, actions=["NEW", "UPDATE"], pattern="config")

    def configure(self, config_name, action, contents):
        """
        Called after the Agent has connected to the message bus. If a configuration exists at startup
        this will be called before onstart.

        Is called every time the configuration in the store changes.
        """
        config = self.default_config.copy()
        config.update(contents)

        _log.debug("Configuring Agent")

        try:
            setting1 = int(config["setting1"])
            setting2 = config["setting2"]
        except ValueError as e:
            _log.error("ERROR PROCESSING CONFIGURATION: {}".format(e))
            return

        self.setting1 = setting1
        self.setting2 = setting2

        for x in self.setting2:
            self._create_subscriptions(str(x))
            print(str(x))

    def _create_subscriptions(self, topic):
        """
        Unsubscribe from all pub/sub topics and create a subscription to a topic in the configuration which triggers
        the _handle_publish callback
        """
        self.vip.pubsub.unsubscribe("pubsub", None, None)

        self.vip.pubsub.subscribe(peer='pubsub',
                                  prefix=topic,
                                  callback=self._handle_publish,all_platforms=True)

    def _handle_publish(self, peer, sender, bus, topic, headers, message):
        """
        Callback triggered by the subscription setup using the topic from the agent's config file
        """
        self._monitor.process_Message({'topic':topic, 'message':message})
        
    @Core.receiver("onstart")
    def onstart(self, sender, **kwargs):
        """
        This is method is called once the Agent has successfully connected to the platform.
        This is a good place to setup subscriptions if they are not dynamic or
        do any other startup activities that require a connection to the message bus.
        Called after any configurations methods that are called at startup.

        Usually not needed if using the configuration store.
        """
        #self.vip.pubsub.publish('pubsub', "some/random/topic", message="HI!")

        # Example RPC call
        # self.vip.rpc.call("some_agent", "some_method", arg1, arg2)
        pass

    @Core.receiver("onstop")
    def onstop(self, sender, **kwargs):
        """
        This method is called when the Agent is about to shutdown, but before it disconnects from
        the message bus.
        """
        pass

    @RPC.export
    def rpc_method(self, arg1, arg2, kwarg1=None, kwarg2=None):
        """
        RPC method

        May be called from another agent via self.core.rpc.call
        """
        return self.setting1 + arg1 - arg2


def main():
    """Main method called to start the agent."""
    utils.vip_main(facadeAgent, 
                   version=__version__)


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
