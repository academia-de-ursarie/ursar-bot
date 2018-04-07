import os
import imp
import inspect

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PLUGINS_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "plugins"))

class UrsarPlugin:
    '''
    Plugin base class
    '''
    is_ursar_plugin = True


class PluginManager:

    def load_plugins(self):
        '''
        Load UrsarPlugin subclasses from the modules found under PLUGINS_ROOT
        '''
        plugins = []
        plugin_modules = self.load_modules()
        for name, module in plugin_modules.items():
            try:
                for class_name, clazz in inspect.getmembers(module, predicate=inspect.isclass):
                    try:
                        if hasattr(clazz, 'is_ursar_plugin') and clazz.is_ursar_plugin and class_name != "UrsarPlugin":
                            plugins.append({
                                'name': class_name,
                                'class': clazz,
                                'module': module,
                                'full_module_name': name,
                            })
                    except Exception as e:
                        print ('Error loading %s: %s' % (class_name, e))
            except Exception as e:
                print ('Error loading %s: %s' % (name, e))

        return plugins

    def load_modules(self):
        '''
        Load plugin modules from the PLUGINS_ROOT directory
        '''
        plugin_modules = {}
        for root, dirs, files in os.walk(PLUGINS_ROOT, topdown=False):
            for file in files:
                if file[-3:] == '.py' and file != '__init__.py':
                    try:
                        module_path = os.path.join(root, file)
                        path_components = module_path.split(os.sep)
                        module_name = path_components[-1][:-3]
                        full_module_name = '.'.join(path_components)

                        plugin_modules[full_module_name] = imp.load_source(module_name, module_path)
                    except Exception as e:
                        print ("Error loading %s: %s" % (module_path, e))

        return plugin_modules