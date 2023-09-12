"""
Need to add the hook python file in the config.env.includes.settings.tk-multi-publish2.yml
"""


import os
import maya.cmds as cmds
import maya.mel as mel
import sgtk
import inspect

from tank_vendor import six

from pipelineFramework.maya.hookPublishs  import HookPublishRig

hooksPublish = HookPublishRig()

# Inherit from {self}/publish_file.py 
# Check config.env.includes.settings.tk-multi-publish2.yml
HookBaseClass = sgtk.get_hook_baseclass()


class MayaAssetRigPROXYPublishPlugin(HookBaseClass):

    def accept(self, settings, item):

        return hooksPublish.acceptLOD(
            self,
            settings,
            item,
            self.publishTemplate,
            self.propertiesPublishTemplate
        )

    def validate(self, settings, item):

        hooksPublish.validate(
            self,
            settings,
            item,
            self.propertiesPublishTemplate,
            isChild=True
        )

        # run the base class validation
        return super(MayaAssetRigPROXYPublishPlugin, self).validate(settings, item)


    def publish(self, settings, item):

        hooksPublish.publishRigLOD(
            self,
            settings,
            item,
            isChild=True
        )

        # let the base class register the publish
        super(MayaAssetRigPROXYPublishPlugin, self).publish(settings, item)

    @property
    def publishTemplate(self):
        return "Asset Rig PROXY Publish Template"

    @property
    def propertiesPublishTemplate(self):
        return "asset_rig_proxy_publish_template"

    @property
    def description(self):
        return """
        <p>This plugin publish the selected assets for the model pipeline step
        You need to select root transform of the asset.</p>
        """

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(MayaAssetRigPROXYPublishPlugin, self).settings or {}

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
        return ["maya.asset.rigPROXY"]