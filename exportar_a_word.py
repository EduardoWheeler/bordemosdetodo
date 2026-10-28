import os
from docx import Document
from docx.shared import Pt, RGBColor

def exportar_codigo_a_word(directorio_raiz, archivo_salida="Codigo_Proyecto.docx"):
    if not os.path.isdir(directorio_raiz):
        print(f"Error: El directorio '{directorio_raiz}' no existe.")
        return

    doc = Document()
    doc.add_heading('Documentación de Código Fuente', level=0)
    
    # Carpetas o archivos que ignorar para no saturar el documento
    ignorar_carpetas = {'.git', '__pycache__', 'venv', '.venv', 'build', 'dist', '.idea'}
    
    print("Procesando archivos...")
    for root, dirs, files in os.walk(directorio_raiz):
        # Filtrar carpetas ignoradas modificando la lista 'dirs' in situ
        dirs[:] = [d for d in dirs if d not in ignorar_carpetas]
        
        for file in files:
            if file.endswith(('.py', '.sql', '.html', '.css', '.js', '.json')):
                ruta_completa = os.path.join(root, file)
                ruta_relativa = os.path.relpath(ruta_completa, directorio_raiz)
                print(f"Agregando: {ruta_relativa}")
                
                doc.add_heading(f"Archivo: {ruta_relativa}", level=2)
                try:
                    with open(ruta_completa, 'r', encoding='utf-8', errors='ignore') as f:
                        contenido = f.read()
                    
                    p = doc.add_paragraph()
                    run = p.add_run(contenido)
                    run.font.name = 'Consolas'
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(40, 40, 40)
                except Exception as e:
                    doc.add_paragraph(f"[Error al leer el archivo: {e}]")
                    
    doc.save(archivo_salida)
    print(f"\n¡Listo! Documento creado exitosamente como: {archivo_salida}")

if __name__ == '__main__':
    exportar_codigo_a_word('.')