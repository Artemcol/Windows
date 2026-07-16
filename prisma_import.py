import sys
import os
import json
import zlib
import bpy

def import_prisma():
    # Имена файлов прописаны жестко, чтобы избежать ошибок консоли Blender
    filepath = "Skybox Layer Sword.pobject"
    output_path = "Skybox_Layer_Sword.obj"
    
    # Очищаем сцену Blender
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    with open(filepath, 'rb') as f:
        data = f.read()
        
    try:
        uncompressed = zlib.decompress(data).decode('utf-8')
    except Exception:
        uncompressed = data.decode('utf-8')
        
    parsed = json.loads(uncompressed)
    
    mesh = bpy.data.meshes.new(name="Skybox_Sword_Mesh")
    obj = bpy.data.objects.new("Skybox_Sword", mesh)
    
    col = bpy.context.scene.collection
    col.objects.link(obj)
    
    verts = []
    faces = []
    
    for v in parsed.get('vertices', []):
        verts.append((v['x'], v['y'], v['z']))
    for f in parsed.get('faces', []):
        faces.append(f['indices'])
        
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    # Экспортируем
    bpy.ops.wm.obj_export(filepath=output_path, export_selected=False)
    print("\n--- SUCCESS: Skybox_Layer_Sword.obj И .mtl УСПЕШНО СОЗДАНЫ! ---")

if __name__ == "__main__":
    import_prisma()
    
