import nanome
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

MENU_PATH = dir_path + "/WebLoad.json"
PPT_TAB_PATH = dir_path + "/PPTTab.json"
IMAGE_TAB_PATH = dir_path + "/ImageTab.json"
LIST_ITEM_PATH = dir_path + "/ListItem.json"

class Prefabs(object):
    tab_prefab = None
    ppt_prefab = None
    image_prefab = None
    list_item_prefab = None

class PageTypes(nanome.util.IntEnum):
    Home = 1
    Image = 2
    PPT = 3

#Singleton class.
class MenuManager(object):
    def __init__(self, plugin, address, load_file_delegate):
        MenuManager.instance = self
        self.plugin = plugin
        self.ReadJsons()
        MenuManager.Page.tab_bar = self.plugin.menu.root.find_node("TabBar")
        MenuManager.Page.page_parent = self.plugin.menu.root.find_node("Pages")
        MenuManager.Page.menu_manager = self

        home = self.plugin.menu.root.find_node("FilesPage")
        home_tab = self.plugin.menu.root.find_node("HomeTab")
        self.home_page = MenuManager.HomePage(home_tab, home, address, load_file_delegate)
        self.selected_page = self.home_page
        self.uploaded = False
        self.Refresh()

    def ReadJsons(self):
        self.plugin.menu = nanome.ui.Menu.io.from_json(MENU_PATH)
        Prefabs.ppt_prefab = nanome.ui.LayoutNode.io.from_json(PPT_TAB_PATH).get_children()[0]
        Prefabs.image_prefab = nanome.ui.LayoutNode.io.from_json(IMAGE_TAB_PATH).get_children()[0]
        Prefabs.list_item_prefab = nanome.ui.LayoutNode.io.from_json(LIST_ITEM_PATH)
        Prefabs.tab_prefab = self.plugin.menu.root.find_node("TabPrefab")
        Prefabs.tab_prefab.parent.remove_child(Prefabs.tab_prefab)

    def SwitchTab(self, page=None):
        if page==None:
            page = self.home_page
        self.selected_page.deselect()
        self.selected_page = page
        self.selected_page.select()
        MenuManager.RefreshMenu()

    def OpenPage(self, type, data, name):
        if type == PageTypes.Image:
            MenuManager.ImagePage(data, name)
        if type == PageTypes.PPT:
            MenuManager.PPTPage(data, name)
        self.Refresh()

    @classmethod
    def RefreshMenu(cls, content = None):
        MenuManager.instance.Refresh(content)

    def Refresh(self, content = None):
        if content and self.uploaded:
            self.plugin.update_content(content)
        else:
            self.uploaded = True
            self.plugin.menu.enable = True
            self.plugin.update_menu(self.plugin.menu)

    def AddFile(self, name):
        self.home_page.AddFile(name)
        self.Refresh()

    def RemoveFile(self, name):
        self.home_page.RemoveFile(name)
        self.Refresh()

    def UpdateFiles(self, names):
        file_names = set(map(lambda item: item.name, self.home_page.file_list.items))
        add_set = set(names)
        remove_files = file_names - add_set
        changed = False

        for file in remove_files:
            self.home_page.RemoveFile(file)
            changed = True

        add_files = add_set - file_names
        for file in add_files:
            self.home_page.AddFile(file)
            changed = True
        if changed:
            self.Refresh()

    def GetFiles(self):
        return list(map(lambda item: item.name, self.home_page.file_list.items))

    def GetOpenFiles(self):
        return list(map(lambda item: item.name, MenuManager.Page.page_parent.get_children()))

    class Page(object):
        tab_bar = None
        page_parent = None
        menu_manager = None
        def __init__(self, name, tab_prefab, page_prefab):
            #setup tab
            self.tab_base = tab_prefab.clone()
            tab_prefab = None
            self.tab_button = self.tab_base.get_content()
            self.tab_label = self.tab_base.find_node("TabPrefabLabel").get_content()
            self.tab_delete_button = self.tab_base.find_node("TabPrefabDelete").get_content()

            base_name = os.path.basename(name)
            base_name = os.path.splitext(base_name)[0]
            tab_name = base_name[:6]
            self.tab_label.text_value = tab_name

            fill = self.tab_bar.find_node("Fill")
            self.tab_bar.add_child(self.tab_base)
            self.tab_bar.remove_child(fill)
            self.tab_bar.add_child(fill)

            #setup page
            self.base = page_prefab.clone()
            self.base.name = base_name
            page_prefab = None
            self.page_parent.add_child(self.base)

            #setup buttons
            def tab_delete(button):
                self.page_parent.remove_child(self.base)
                self.tab_bar.remove_child(self.tab_base)
                self.menu_manager.SwitchTab()
            self.tab_delete_button.register_pressed_callback(tab_delete)

            def tab_pressed(button):
                self.menu_manager.SwitchTab(self)
            self.tab_button.register_pressed_callback(tab_pressed)

            self.menu_manager.SwitchTab(self)

        def select(self):
            self.base.enabled = True
            self.tab_base.selected = True

        def deselect(self):
            self.base.enabled = False
            self.tab_base.selected = True

    class HomePage(Page):
        def __init__(self, tab, page, address, load_file_delegate):
            self.tab_base = tab
            self.base = page
            self.type = PageTypes.Home
            self.tab_button = self.tab_base.get_content()

            def tab_pressed(button):
                self.menu_manager.SwitchTab(self)
            self.tab_button.register_pressed_callback(tab_pressed)
            self.load_button = self.base.find_node("LoadButton").get_content()
            instruction_label = self.base.find_node("InstructionLabel").get_content()
            instruction_label.text_value = "Add files by visiting " + address + " in your browser"
            self.file_list = self.base.find_node("FileList").get_content()

            self.selected_file = None

            def load_file(button):
                if self.selected_file == None:
                    return
                load_file_delegate(self.selected_file.file_name)

            self.load_button.unuseable = True
            self.load_button.register_pressed_callback(load_file)

        def AddFile(self, name):
            new_file = Prefabs.list_item_prefab.clone()
            new_file.name = name
            button = new_file.find_node("ButtonNode").get_content()
            label = new_file.find_node("LabelNode").get_content()
            label.text_value = name
            button.file_name = name

            def FilePressedCallback(button):
                if not self.selected_file is None:
                    self.selected_file.selected = False
                    MenuManager.RefreshMenu(self.selected_file)
                self.selected_file = button
                self.selected_file.selected = True
                self.load_button.unuseable = False
                MenuManager.RefreshMenu(self.selected_file)
            button.register_pressed_callback(FilePressedCallback)

            self.file_list.items.append(new_file)

        def RemoveFile(self, name):
            if self.selected_file.file_name == name:
                self.selected_file = None
                self.load_button.unuseable = True
            files = self.file_list.items
            deleted_file = None
            for child in files:
                if child.name == name:
                    deleted_file = child
                    break
            if deleted_file == None:
                nanome.util.Logs.debug("Cannot delete file " + name + ". File not found.")
            else:
                files.remove(deleted_file)

    class ImagePage(Page):
        def __init__(self, image, name):
            MenuManager.Page.__init__(self, name, Prefabs.tab_prefab, Prefabs.image_prefab)
            self.type = PageTypes.Image
            self.image = image
            self.image_content = self.base.find_node("ImageContent").add_new_image(image)

    class PPTPage(Page):
        def __init__(self, images, name):
            MenuManager.Page.__init__(self, name, Prefabs.tab_prefab, Prefabs.ppt_prefab)
            self.type = PageTypes.PPT
            self.images = images
            self.prev_button = self.base.find_node("PrevButton").get_content()
            self.next_button = self.base.find_node("NextButton").get_content()
            self.page_text = self.base.find_node("PageText").get_content()
            self.ppt_content = self.base.find_node("PPTContent").add_new_image()
            self.ppt_content.scaling_option = nanome.util.enums.ScalingOptions.fit

            self.current_slide = 0
            def move_next(button):
                next_slide = (self.current_slide+1) % len(self.images)
                self.change_slide(next_slide)
                MenuManager.RefreshMenu(self.ppt_content)
                MenuManager.RefreshMenu(self.page_text)
            def move_prev(button):
                next_slide = (self.current_slide-1) % len(self.images)
                self.change_slide(next_slide)
                MenuManager.RefreshMenu(self.ppt_content)
                MenuManager.RefreshMenu(self.page_text)
            self.prev_button.register_pressed_callback(move_prev)
            self.next_button.register_pressed_callback(move_next)
            self.change_slide(0)

        def change_slide(self, index):
            num_slides = len(self.images)
            self.current_slide = index
            self.ppt_content.file_path = self.images[index]
            self.page_text.text_value = str(self.current_slide+1) +"/" + str(num_slides)