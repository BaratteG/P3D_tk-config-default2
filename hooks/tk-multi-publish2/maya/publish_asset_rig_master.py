"""
Need to add the hook python file in the config.env.includes.settings.tk-multi-publish2.yml
"""


import os
import maya.cmds as cmds
import maya.mel as mel
import sgtk
import inspect

from tank_vendor import six

from pipelineFramework.maya.shotgrid.publishPlugins.accepts     import Accept
from pipelineFramework.maya.shotgrid.publishPlugins.validates   import Validate
from pipelineFramework.maya.shotgrid.publishPlugins.publishes   import PublishScene

# Inherit from {self}/publish_file.py 
# Check config.env.includes.settings.tk-multi-publish2.yml
HookBaseClass = sgtk.get_hook_baseclass()


class MayaAssetRigMasterPublishPlugin(HookBaseClass):

    def accept(self, settings, item):

        acceptor = Accept(hookClass=self)
        return acceptor.accept(
            settings,
            item,
            self.publishTemplate,
            self.propertiesPublishTemplate
        )

    def validate(self, settings, item):

        validator = Validate(hookClass=self)
        validator.validate(
            item,
            self.propertiesPublishTemplate)

        # run the base class validation
        return super(MayaAssetRigMasterPublishPlugin, self).validate(settings, item)


    def publish(self, settings, item):

        publishator = PublishScene(hookClass=self)
        publishator.publish(item)

        # let the base class register the publish
        super(MayaAssetRigMasterPublishPlugin, self).publish(settings, item)

    @property
    def publishTemplate(self):
        return "Asset Rig Master Publish Template"

    @property
    def propertiesPublishTemplate(self):
        return "asset_rig_master_publish_template"

    @property
    def description(self):
        return """
        <p>This plugin publish the selected assets for the model pipeline step
        You need to select root transform of the asset.</p>
        """

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(MayaAssetRigMasterPublishPlugin, self).settings or {}

        # settings specific to this class
        maya_publish_settings = {
            self.publishTemplate : {
                "type": "template",
                "default": None,
                "description": "Template path for published work files. Should"
                "correspond to a template defined in "
                "templates.yml.",
            }
        }

        # update the base settings
        base_settings.update(maya_publish_settings)

        return base_settings

    @property
    def item_filters(self):
        return ["maya.asset.rigMaster"]