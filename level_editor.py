import bpy
import bpy_extras
import math

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
        self.layout.operator(MYADDON_OT_stretch_vertex.bl_idname, text=MYADDON_OT_stretch_vertex.bl_label) 
        self.layout.operator(MYADDON_OT_create_ico_sphere.bl_idname, text=MYADDON_OT_create_ico_sphere.bl_label) 
        self.layout.operator(MYADDON_OT_export_scene.bl_idname, text=MYADDON_OT_export_scene.bl_label)

    # 既存のメニューにサブメニューを追加
    def subMenu(self, context):
        # id指定
        self.layout.menu(TOPBAR_MT_my_menu.bl_idname)

# オペレータ(頂点を伸ばす)
class MYADDON_OT_stretch_vertex(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_stretch_vertex"
    bl_label = "頂点を伸ばす"
    bl_description = "頂点座標を引っ張って伸ばす"
    bl_options = {'REGISTER', 'UNDO'} # redo,undo可能オプション

    # 実行時
    def execute(self, context):
        bpy.data.objects["Cube"].data.vertices[0].co.x += 1.0
        print("頂点を伸ばしました。")
        return {'FINISHED'} # オペレータの終了通知

# オペレータ(ICO球の生成)
class MYADDON_OT_create_ico_sphere(bpy.types.Operator):
    bl_idname = "myaddon.myaddon_ot_create_object"
    bl_label = "ICO球生成"
    bl_description = "ICO球を生成"
    bl_options = {'REGISTER', 'UNDO'}

    # 実行時
    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()
        print("ICO球を生成しました。")
        return {'FINISHED'}
    
# オペレータ(シーン出力)
class MYADDON_OT_export_scene(bpy.types.Operator, bpy_extras.io_utils.ExportHelper):
    bl_idname = "myaddon.myaddon_ot_export_scene"
    bl_label = "シーン出力"
    bl_description = "シーン情報をExport"
    filename_ext = ".scene" # 出力ファイル拡張子

    # 実行時
    def execute(self, context):
        print("シーン情報をExportします。")

        # 出力
        self.export()

        print("シーン情報をExportしました。")
        self.report({'INFO'}, "シーン情報をExportしました。")

        return {'FINISHED'}
    
    def export(self):
        """ファイルに出力"""

        print("シーン情報の出力開始 %r" % self.filepath)

        # ファイルオープン
        with open(self.filepath, "wt") as file:

            # シーン内の全オブジェクト
            for object in bpy.context.scene.objects:
                # 親があるものはスキップ
                if (object.parent):
                    continue

                # 深さ優先探索
                self.parse_scene_recursive(file, object, 0)

            # スコープを抜けると閉じる

    def write_and_print(self, file, str):
        print(str)

        file.write(str)
        file.write('\n')

    def parse_scene_recursive(self, file, object, level):
        """シーン解析用再帰関数"""

        # 深さ分インデント
        indent = ''
        for i in range(level):
            indent += "\t"

        # オブジェクト名書き込み
        self.write_and_print(file, indent + object.type + " - " + object.name)
        # トランスフォームを抽出
        trans, rot, scale = object.matrix_local.decompose()
        # オイラー回転に変換
        rot = rot.to_euler()
        # 度数法に変換
        rot.x = math.degrees(rot.x)
        rot.y = math.degrees(rot.y)
        rot.z = math.degrees(rot.z)
        # 表示
        self.write_and_print(file, indent + "Trans(%f,%f,%f)" % (trans.x, trans.y, trans.z))
        self.write_and_print(file, indent + "Rot  (%f,%f,%f)" % (rot.x, rot.y, rot.z))
        self.write_and_print(file, indent + "Scale(%f,%f,%f)" % (scale.x, scale.y, scale.z))
        self.write_and_print(file, '')

        # 子ノードの処理
        for child in object.children:
            self.parse_scene_recursive(file, child, level + 1)

# Blenderに登録するクラスリスト
classes = (
    MYADDON_OT_stretch_vertex,
    MYADDON_OT_create_ico_sphere,
    MYADDON_OT_export_scene,
    TOPBAR_MT_my_menu,
)

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
    bpy.types.TOPBAR_MT_editor_menus.remove(TOPBAR_MT_my_menu.subMenu)

    # Blenderからクラスを削除
    for cls in classes:
        bpy.utils.unregister_class(cls)

    print("レベルエディタ:無効")

# テスト
if __name__ == "__main__":
    register()