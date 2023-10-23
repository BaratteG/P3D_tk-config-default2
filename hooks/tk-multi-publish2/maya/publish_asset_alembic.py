
import os
import maya.cmds as cmds
import maya.mel as mel
import sgtk

from tank_vendor import six

from pipelineFramework.maya.shotgrid.publishPlugins.accepts        import AcceptAssetLOD
from pipelineFramework.maya.shotgrid.publishPlugins.validates      import ValidateAssetLOD
from pipelineFramework.maya.shotgrid.publishPlugins.publishes      import PublishAlembic

HookBaseClass = sgtk.get_hook_baseclass()

class MayaAssetAlembicPublishPlugin(HookBaseClass):

    def accept(self, settings, item):
        
        acceptor = AcceptAssetLOD(hookClass=self)
        return acceptor.accept(
            settings,
            item,
            self.publishTemplate,
            self.propertiesPublishTemplate
        )

    def validate(self, settings, item):

        validator = ValidateAssetLOD(hookClass=self)
        validator.validate(
            item,
            self.propertiesPublishTemplate,
            isChild=True
        )

        # run the base class validation
        return super(MayaAssetAlembicPublishPlugin, self).validate(settings, item)

    def publish(self, settings, item):

        publishator = PublishAlembic(hookClass=self)
        publishator.publish(
            item,
            isChild=True
        )

        # let the base class register the publish
        super(MayaAssetAlembicPublishPlugin, self).publish(settings, item)

    @property
    def publishTemplate(self):
        return "Asset Alembic Publish Template"

    @property
    def propertiesPublishTemplate(self):
        return "asset_alembic_publish_template"

    @property
    def description(self):
        return """
        <p>This plugin publish the selected assets for the model pipeline step
        You need to select root transform of the asset.</p>
        """

    @property
    def settings(self):
        # inherit the settings from the base publish plugin
        base_settings = super(MayaAssetAlembicPublishPlugin, self).settings or {}

        # settings specific to this class
        maya_publish_settings = {
            self.publishTemplate: {
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
        return ["maya.asset.alembic"]

def _session_path():
    """
    Return the path to the current session
    :return:
    """
    path = cmds.file(query=True, sn=True)

    if path is not None:
        path = six.ensure_str(path)

    return path


def _get_save_as_action():
    """
    Simple helper for returning a log action dict for saving the session
    """

    engine = sgtk.platform.current_engine()

    # default save callback
    callback = cmds.SaveScene

    # if workfiles2 is configured, use that for file save
    if "tk-multi-workfiles2" in engine.apps:
        app = engine.apps["tk-multi-workfiles2"]
        if hasattr(app, "show_file_save_dlg"):
            callback = app.show_file_save_dlg

    return {
        "action_button": {
            "label": "Save As...",
            "tooltip": "Save the current session",
            "callback": callback,
        }
    }