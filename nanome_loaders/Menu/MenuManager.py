import nanome

MENU_PATH = ""
PPT_TAB_PATH = ""
IMAGE_TAB_PATH = ""

class Prefabs(object):
    tab_prefab = None
    ppt_prefab = None
    image_prefab = None

class PageTypes(nanome.util.IntEnum):
    Home = 1
    Image = 2
    PPT = 3

class MenuManager(object):
    def __init__(self, plugin):
        self.plugin = plugin
        self.ReadJsons()
        MenuManager.Page.tab_bar = self.plugin.menu.root.find_node("TabBar")
        MenuManager.Page.page_parent = self.plugin.menu.root
        MenuManager.Page.menu_manager = self

        home = self.plugin.menu.root.find_node("FilesPage")
        home_tab = self.plugin.menu.root.find_node("HomeTab")
        self.home_page = MenuManager.HomePage(home_tab, home)
        self.selected_page = self.home_page

    def ReadJsons(self):
        self.plugin.menu = nanome.ui.Menu.io.from_json(MENU_PATH)
        Prefabs.ppt_prefab = nanome.ui.LayoutNode.io.from_json(PPT_TAB_PATH).get_children()[0]
        Prefabs.image_prefab = nanome.ui.LayoutNode.io.from_json(IMAGE_TAB_PATH).get_children()[0]
        Prefabs.tab_prefab = self.plugin.menu.root.find_node("TabPrefab")
        Prefabs.tab_prefab.parent.remove_child(Prefabs.tab_prefab)

    def SwitchTab(self, page=None):
        if page==None:
            page = self.home_page
        self.selected_page.deselect()
        self.selected_page = page
        self.selected_page.select()

    def Refresh(self):
        self.plugin.menu.enable = True
        self.plugin.update_menu(self.plugin.menu)

    class Page(object):
        tab_bar = None
        page_parent = None
        menu_manager = None
        def __init__(self, tab_prefab, page_prefab):
            #setup tab
            self.tab_base = tab_prefab.clone()
            tab_prefab = None
            self.tab_button = self.tab_base.get_content()
            self.tab_label = self.tab_base.find_node("TabPrefabLabel").get_content()
            self.tab_delete_button = self.tab_base.find_node("TabPrefabDelete").get_content()

            fill = self.tab_base.find_node("Fill")
            self.tab_bar.add_child(self.tab_base)
            self.tab_bar.remove_child(fill)
            self.tab_bar.add_child(fill)

            #setup page
            self.base = page_prefab.clone()
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

        def select(self):
            self.base.enabled = True
            self.tab_base.selected = True

        def deselect(self):
            self.base.enabled = False
            self.tab_base.selected = True

    class HomePage(MenuManager.Page):
        def __init__(self, tab, page):
            self.tab_base = tab
            self.base = page
            self.type = PageTypes.Home

            def tab_pressed(button):
                self.menu_manager.SwitchTab(self)
            self.tab_button.register_pressed_callback(tab_pressed)
            self.load_button = self.base.find_node("LoadButton").get_content()
            self.instruction_label = self.base.find_node("InstructionLabel").get_content()
            self.file_list = self.base.find_node("FileList").get_content()
            #TODO: load menu logic

    class ImagePage(MenuManager.Page):
        def __init__(self, image):
            MenuManager.Page.__init__(self, Prefabs.tab_prefab, Prefabs.image_prefab)
            self.type = PageTypes.Image
            self.image = image
            self.image_content = self.base.find_node("ImageContent").add_new_image(image)

    class PPTPage(MenuManager.Page):
        def __init__(self, images):
            MenuManager.Page.__init__(self, Prefabs.tab_prefab, Prefabs.ppt_prefab)
            self.type = PageTypes.PPT
            self.images = images
            self.prev_button = self.base.find_node("PrevButton").get_content()
            self.next_button = self.base.find_node("NextButton").get_content()
            self.page_text = self.base.find_node("PageText").get_content()
            self.ppt_content = self.base.find_node("PPTContent").add_new_image()
            self.ppt_content.scaling_option = nanome.util.enums.ScalingOptions.fit
            self.current_slide = 0
            def move_next(button):
                if self.current_slide < len(self.images):
                    self.change_slide(self.current_slide+1)
            def move_prev(button):
                if self.current_slide > 0:
                    self.change_slide(self.current_slide-1)
            self.prev_button.register_pressed_callback(move_prev)
            self.next_button.register_pressed_callback(move_next)
            self.change_slide(0)

        def change_slide(self, index):
            num_slides = len(self.images)
            self.current_slide = index
            self.ppt_content.file_path = self.images[index]
            self.prev_button.unuseable = self.current_slide <= 0
            self.next_button.unuseable = self.current_slide >= num_slides
            self.page_text = str(self.current_slide) +"/" + str(num_slides)
