"""
Need to add the hook python file in the config.env.includes.settings.tk-multi-publish2.yml
"""


import os
import maya.cmds as cmds
import maya.mel as mel
import sgtk
import inspect

from tank_vendor import six

from pipelineFramework.maya         import PublishTools

publihTools = PublishTools()

# Inherit from {self}/publish_file.py 
# Check config.env.includes.settings.tk-multi-publish2.yml
HookBaseClass = sgtk.get_hook_baseclass()


class MayaAssetMaterialXMIPublishPlugin(HookBaseClass):

    def accept(self, settings, item):

        return publihTools.hookPublishAcceptLOD(
            self,
            settings,
            item,
            self.publishTemplate,
            self.propertiesPublishTemplate,
            "MI"
        )

    def validate(self, settings, item):

        publihTools.hookPublishValidate(
            self,
            settings,
            item,
            self.propertiesPublishTemplate,
            isChild=True,
            addFields={"lod":"MI", "variant":"default"}
        )

        # run the base class validation
        return super(MayaAssetMaterialXMIPublishPlugin, self).validate(settings, item)

    def publish(self, settings, item):
        
        publihTools.hookPublishMaterialXLODPublish(
            self,
            settings,
            item,
            "MI",
            isChild=True
        )

        # let the base class register the publish
        super(MayaAssetMaterialXMIPublishPlugin, self).publish(settings, item)

    @property
    def publishTemplate(self):
        return "Asset MaterialX MI Publish Template"

    @property
    def propertiesPublishTemplate(self):
        return "asset_materialX_mi_publish_template"

    @property
    def description(self):
        return """
        <p>This plugin publish the selected assets for the model pipeline step
        You need to select root transform of the asset.</p>
        """

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(MayaAssetMaterialXMIPublishPlugin, self).settings or {}

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
        return ["maya.asset.materialXMI"]