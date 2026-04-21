import bpy

bl_info = {
    "name": "レベルエディタ",
    "author": "Hayato Abe",
    "version": (1, 0),
    "blender": (4, 4, 0),
    "location": "",
    "description": "レベルエディタ",
    "warning": "",
    "category": "Object",
}

# 有効化時
def register():
    # Blenderにクラスを登録
    for cls in classes:
        bpy.utils.register_class(cls)

    # メニューに項目を追加
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.subMenu)
    print("レベルエディタ:有効")

# 無効化時
def unregister():
    bpy.types.TOPBAR_MT_editor_menus.append(TOPBAR_MT_my_menu.subMenu)

    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタ:無効")

# テスト
if __name__ == "__main__":
    register()

# メニュー
def draw_menu_manual(self, context):
    self.layout.operator("wm.url_open_preset", text = "Manual", icon= 'HELP')

# トップバーの拡張メニュー
class TOPBAR_MT_my_menu(bpy.types.Menu):
    bl_idname = "TOPBAR_MT_my_menu"
    bl_label = "MyMenu" # 表示されるラベル
    bl_description = "拡張メニュー by " + bl_info["author"] # 説明

    # サブメニュー描画
    def draw(self, context):
        # 項目追加
        self.layout.operator("wm.url_open_preset", text= "Manual", icon= 'HELP') 

    # 既存のメニューにサブメニューを追加
    def subMenu(self, context):
        # id指定
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

# Blenderに登録するクラスリスト
classes = (
    TOPBAR_MT_my_menu,
)