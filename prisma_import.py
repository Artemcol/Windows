import sys
import os
import json
import zlib
import bpy

def import_prisma(filepath, output_path):
    # Очищаем сцену Blender от куба и камеры
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    with open(filepath, 'rb') as f:
        data = f.read()
        
    # Распаковываем zlib сжатие pobject
    try:
        uncompressed = zlib.decompress(data).decode('utf-8')
    except Exception:
        uncompressed = data.decode('utf-8')
        
    parsed = json.loads(uncompressed)
    
    # Извлекаем меш (вершины, полигоны, UV)
    # Создаем базовую low-poly геометрию в Blender
    mesh = bpy.data.meshes.new(name="Skybox_Sword_Mesh")
    obj = bpy.data.objects.new("Skybox_Sword", mesh)
    
    col = bpy.context.scene.collection
    col.objects.link(obj)
    
    # Чтение геометрии из JSON структуры Призмы
    verts = []
    faces = []
    
    for v in parsed.get('vertices', []):
        verts.append((v['x'], v['y'], v['z']))
    for f in parsed.get('faces', []):
        faces.append(f['indices'])
        
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    # Экспортируем в чистый .obj
    bpy.ops.wm.obj_export(filepath=output_path, export_selected=False)
    print(f"--- SUCCESS: Model saved to {output_path} ---")

if __name__ == "__main__":
    # Получаем аргументы из консольной команды Blender
    args = sys.argv[sys.argv.index("--") + 1:]
    import_prisma(args[0], args[1])

