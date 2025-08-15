# Corrige um arquivo já existente
with open('dados_para_migracao.json', 'rb') as f:
    content = f.read().decode('latin1')  # ou 'iso-8859-1'
    
with open('backup_bom.json', 'w', encoding='utf-8') as f:
    f.write(content)