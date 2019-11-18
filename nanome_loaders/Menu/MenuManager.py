import nanome
import os
from functools import partial
dir_path = os.path.dirname(os.path.realpath(__file__))

MENU_PATH = dir_path + "/WebLoad.json"
PPT_TAB_PATH = dir_path + "/PPTTab.json"
IMAGE_TAB_PATH = dir_path + "/ImageTab.json"
LIST_ITEM_PATH = dir_path + "/ListItem.json"
UP_ICON_PATH = dir_path + "/UpIcon.png"

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

    def ClearList(self):
        self.home_page.file_list.items.clear()

    def UpdateList(self, files, folders, can_upload):
        self.home_page.upload_button.unusable = not can_upload
        self.Refresh(self.home_page.upload_button)

        old_items = set(map(lambda item: item.name, self.home_page.file_list.items))
        new_items = folders + files

        add_set = set(new_items)
        remove_items = old_items - add_set
        add_items = add_set - old_items
        changed = False

        for item in remove_items:
            self.home_page.RemoveItem(item)
            changed = True

        # iterate list to preserve ordering
        for item in new_items:
            if item not in add_items:
                continue
            self.home_page.AddItem(item, item in folders)
            changed = True

        if changed or not len(old_items):
            self.Refresh(self.home_page.file_list)

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
            self.tab_base.get_content().selected = True

        def deselect(self):
            self.base.enabled = False
            self.tab_base.get_content().selected = False

    class HomePage(Page):
        def __init__(self, tab, page, address, load_file_delegate):
            self.tab_base = tab
            self.base = page
            self.type = PageTypes.Home
            self.tab_button = self.tab_base.get_content()
            self.load_file_delegate = load_file_delegate
            self.showing_upload = False

            def tab_pressed(button):
                self.menu_manager.SwitchTab(self)
            self.tab_button.register_pressed_callback(tab_pressed)

            def open_url(button):
                self.menu_manager.plugin.open_url(address)
            url_button = self.base.find_node("URLButton").get_content()
            url_button.register_pressed_callback(open_url)

            def go_up(button):
                self.menu_manager.plugin.chdir('..')
                self.ToggleUpload(show=False)
            self.up_button = self.base.find_node("GoUpButton").get_content()
            self.up_button.register_pressed_callback(go_up)

            self.up_button.unusable = True
            self.up_button.set_all_icon(UP_ICON_PATH)
            self.up_button.icon.size = 0.5
            self.up_button.icon.color_unusable = nanome.util.Color.Grey()

            self.upload_button = self.base.find_node("UploadButton").get_content()
            self.upload_button.register_pressed_callback(self.ToggleUpload)

            self.ins_add_files = "Visit %s in browser to add files" % address
            self.ins_select_complex = "Select a structure from the workspace"

            self.instructions = self.base.find_node("InstructionLabel").get_content()
            self.instructions.text_value = self.ins_add_files
            self.breadcrumbs = self.base.find_node("Breadcrumbs").get_content()

            self.file_explorer = self.base.find_node("FileExplorer")

            ln_file_list = self.base.find_node("FileList")
            self.file_list = ln_file_list.get_content()
            self.file_list.parent = ln_file_list

            ln_file_loading = self.base.find_node("FileLoading")
            self.file_loading = ln_file_loading.get_content()
            self.file_loading.parent = ln_file_loading

            self.file_upload = self.base.find_node("FileUpload")

            # upload components
            self.panel_list = self.base.find_node("SelectComplex")
            self.panel_upload = self.base.find_node("SelectType")

            button_pdb = self.base.find_node("PDB").get_content()
            button_pdb.register_pressed_callback(partial(self.UploadComplex, "PDB"))
            button_sdf = self.base.find_node("SDF").get_content()
            button_sdf.register_pressed_callback(partial(self.UploadComplex, "SDF"))
            button_mmcif = self.base.find_node("MMCIF").get_content()
            button_mmcif.register_pressed_callback(partial(self.UploadComplex, "MMCIF"))

            self.complex_list = self.base.find_node("ComplexList").get_content()
            self.selected_complex = None

            self.select()

        def UpdateBreadcrumbs(self, path, at_root):
            self.breadcrumbs.text_value = path
            MenuManager.RefreshMenu(self.breadcrumbs)
            self.up_button.unusable = at_root
            MenuManager.RefreshMenu(self.up_button)

        def AddItem(self, name, is_folder):
            new_item = Prefabs.list_item_prefab.clone()
            new_item.name = name
            button = new_item.find_node("ButtonNode").get_content()
            button.item_name = name

            plugin = MenuManager.instance.plugin
            display_name = name.replace(plugin.account, 'account')
            label = new_item.find_node("LabelNode").get_content()
            label.text_value = display_name

            if is_folder:
                label.text_value += '/'

            def FilePressedCallback(button):
                self.file_list.parent.enabled = False
                self.file_loading.parent.enabled = True
                self.file_loading.text_value = 'loading...\n' + button.item_name
                MenuManager.RefreshMenu()

                def OnFileLoaded():
                    self.file_list.parent.enabled = True
                    self.file_loading.parent.enabled = False
                    MenuManager.RefreshMenu()

                self.load_file_delegate(button.item_name, OnFileLoaded)

            def FolderPressedCallback(button):
                MenuManager.instance.plugin.chdir(button.item_name)

            cb = FolderPressedCallback if is_folder else FilePressedCallback
            button.register_pressed_callback(cb)

            self.file_list.items.append(new_item)

        def RemoveItem(self, name):
            items = self.file_list.items
            for child in items:
                if child.name == name:
                    items.remove(child)
                    break

        def ToggleUpload(self, button=None, show=None):
            show = not self.showing_upload if show is None else show
            self.showing_upload = show
            self.file_upload.enabled = show
            self.file_explorer.enabled = not show
            self.upload_button.set_all_text('Cancel' if show else 'Upload Here')
            self.instructions.text_value = self.ins_select_complex if show else self.ins_add_files

            if show:
                plugin = MenuManager.instance.plugin
                plugin.request_complex_list(self.PopulateComplexes)
                self.panel_list.enabled = True
                self.panel_upload.enabled = False

            MenuManager.RefreshMenu()

        def PopulateComplexes(self, complexes):
            def select_complex(button):
                self.selected_complex = button.complex
                self.panel_list.enabled = False
                self.panel_upload.enabled = True
                MenuManager.RefreshMenu()

            self.complex_list.items = []
            for complex in complexes:
                item = Prefabs.list_item_prefab.clone()
                label = item.find_node("LabelNode").get_content()
                label.text_value = complex.full_name
                button = item.find_node("ButtonNode").get_content()
                button.complex = complex
                button.register_pressed_callback(select_complex)
                self.complex_list.items.append(item)

            if not complexes:
                # empty ln for spacing
                self.complex_list.items.append(nanome.ui.LayoutNode())
                ln = nanome.ui.LayoutNode()
                lbl = ln.add_new_label("no structures found in workspace")
                lbl.text_horizontal_align = lbl.HorizAlignOptions.Middle
                lbl.text_max_size = 0.4
                self.complex_list.items.append(ln)

            MenuManager.RefreshMenu(self.complex_list)

        def UploadComplex(self, save_type, button):
            plugin = MenuManager.instance.plugin
            def save_func(complexes):
                plugin.save_molecule(save_type, complexes[0])
                self.ToggleUpload(show=False)
            plugin.request_complexes([self.selected_complex.index], save_func)

    class ImagePage(Page):
        def __init__(self, image, name):
            MenuManager.Page.__init__(self, name, Prefabs.tab_prefab, Prefabs.image_prefab)
            self.type = PageTypes.Image
            self.image = image
            self.image_content = self.base.find_node("ImageContent").add_new_image(image)
            self.image_content.scaling_option = nanome.util.enums.ScalingOptions.fit

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
            self.page_text.text_value = str(self.current_slide+1) + "/" + str(num_slides)
