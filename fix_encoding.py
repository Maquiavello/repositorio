import json

print("🔧 Corrigiendo encoding del archivo JSON...")

# Leer el archivo con la codificación correcta
with open('datadump.json', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Corregir el caracter mal interpretado
fixed_content = content.replace('contrase├▒a', 'contraseña')

# Guardar el archivo corregido
with open('datadump_fixed.json', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Archivo corregido: datadump_fixed.json")
print("📝 Reemplazados: contrase├▒a → contraseña")