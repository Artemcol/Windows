import json
import zlib
import bpy

def import_prisma():
    filepath = "Skybox Layer Sword.pobject"
    output_path = "Skybox_Layer_Sword.obj"
    
    # Полная очистка сцены Blender
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    print("--- Чтение бинарного файла меча... ---")
    with open(filepath, 'rb') as f:
        binary_data = f.read()
        
    # Пытаемся распаковать Zlib-поток напрямую или со сдвигом заголовка
    try:
        print("Пробуем стандартную распаковку...")
        uncompressed = zlib.decompress(binary_data).decode('utf-8', errors='ignore')
    except Exception:
        try:
            print("Обход бинарного заголовка Prisma3D (сдвиг)...")
            # Пропускаем первые байты заголовка и пробуем декомпрессию raw-потока
            uncompressed = zlib.decompress(binary_data[2:], -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
        except Exception:
            try:
                uncompressed = zlib.decompress(binary_data[3:], -zlib.MAX_WBITS).decode('utf-8', errors='ignore')
            except Exception as e:
                raise ValueError(f"Не удалось расшифровать структуру файла: {e}")
        
    start_idx = uncompressed.find('{')
    end_idx = uncompressed.rfind('}')
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError("Ошибка: Внутри расшифрованного файла не найдена структура JSON.")
        
    parsed = json.loads(uncompressed[start_idx:end_idx + 1])
    print("--- Структура успешно прочитана! Собираем 3D-модель... ---")
    
    mesh = bpy.data.meshes.new(name="Skybox_Mesh")
    obj = bpy.data.objects.new("Skybox_Layer_Sword", mesh)
    bpy.context.scene.collection.objects.link(obj)
    
    verts = []
    faces = []
    
    objects_list = parsed.get('objects', [parsed])
    for obj_data in objects_list:
        v_list = obj_data.get('vertices', [])
        f_list = obj_data.get('faces', [])
        
        offset = len(verts)
        for v in v_list:
            verts.append((v.get('x', 0), v.get('y', 0), v.get('z', 0)))
        for f in f_list:
            indices = f.get('indices', [])
            if len(indices) >= 3:
                faces.append([i + offset for i in indices])
                
    if not verts:
        for key in parsed.keys():
            if isinstance(parsed[key], dict) and 'vertices' in parsed[key]:
                v_list = parsed[key].get('vertices', [])
                f_list = parsed[key].get('faces', [])
                offset = len(verts)
                for v in v_list: verts.append((v.get('x',0), v.get('y',0), v.get('z',0)))
                for f in f_list: faces.append([i + offset for i in f.get('indices', [])])

    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    bpy.ops.wm.obj_export(filepath=output_path, export_selected=False)
    print("\n--- SUCCESS: Skybox_Layer_Sword.obj УСПЕШНО СОЗДАН! ---")

if __name__ == "__main__":
    import_prisma()
                
