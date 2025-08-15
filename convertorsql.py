import json
import sys
from datetime import datetime

def escape_sql_identifier(identifier):
    """Escapa nomes de tabelas/colunas para MySQL"""
    return f"`{identifier.replace('`', '``')}`"

def escape_sql_value(value):
    """Escapa valores para MySQL, preservando caracteres especiais em UTF-8"""
    if value is None:
        return 'NULL'
    elif isinstance(value, bool):
        return '1' if value else '0'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'"
    else:
        # Garante que a string está em UTF-8
        if isinstance(value, str):
            try:
                # Primeiro tenta decodificar como utf-8 caso esteja em bytes
                if isinstance(value, bytes):
                    value = value.decode('utf-8')
                # Remove caracteres BOM se existirem
                if value.startswith('\ufeff'):
                    value = value[1:]
                # Escapa aspas simples e barras invertidas
                return "'" + value.replace('\\', '\\\\').replace("'", "''") + "'"
            except UnicodeError:
                # Se houver erro, tenta latin1 como fallback
                if isinstance(value, bytes):
                    value = value.decode('latin1')
                return "'" + value.replace('\\', '\\\\').replace("'", "''") + "'"
        return "'" + str(value).replace('\\', '\\\\').replace("'", "''") + "'"

def adjust_field_name(field_name, model_data):
    """Ajusta nomes de campo para ForeignKeys adicionando _id"""
    if (isinstance(model_data['fields'].get(field_name), int) and not field_name.endswith('_id')):
        return f"{field_name}_id"
    return field_name

def main():
    try:
        # Abre o arquivo JSON com tratamento especial para BOM
        with open('dados_para_migracao.json', 'rb') as f:
            content = f.read()
            if content.startswith(b'\xef\xbb\xbf'):  # Remove BOM se existir
                content = content[3:]
            data = json.loads(content.decode('utf-8'))
        
        # Abre o arquivo SQL em modo binário para garantir escrita UTF-8 correta
        with open('dados.sql', 'wb') as sql_file:
            sql_file.write(b"SET NAMES utf8mb4;\n")
            sql_file.write(b"SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            for item in data:
                try:
                    model = item['model']
                    table_name = escape_sql_identifier(model.replace('.', '_'))
                    fields = item['fields']
                    
                    adjusted_fields = {
                        adjust_field_name(f, item): v 
                        for f, v in fields.items()
                    }
                    
                    columns = [escape_sql_identifier(f) for f in adjusted_fields.keys()]
                    values = [escape_sql_value(v) for v in adjusted_fields.values()]
                    
                    # Constrói a linha SQL como bytes UTF-8
                    sql_line = (
                        f"INSERT INTO {table_name} ({', '.join(columns)})\n"
                        f"VALUES ({', '.join(values)});\n\n"
                    ).encode('utf-8')
                    
                    sql_file.write(sql_line)
                    
                except Exception as e:
                    print(f"Erro no item {item.get('pk', '?')}: {str(e)}", file=sys.stderr)
                    continue
            
            sql_file.write(b"SET FOREIGN_KEY_CHECKS = 1;\n")
        
        print("Conversão concluída! Arquivo 'dados.sql' gerado com sucesso.")
        
    except Exception as e:
        print(f"ERRO: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()