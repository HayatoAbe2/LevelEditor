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
    print("レベルエディタ:有効")

# 無効化時
def unregister():
    print("レベルエディタ:無効")

# テスト
if __name__ == "__main__":
    register()