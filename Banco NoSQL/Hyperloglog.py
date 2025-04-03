import redis

# Conectar ao Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Adicionar pacientes únicos que marcaram consulta
r.pfadd("pacientes_ativos", "Ana", "Carlos", "Beatriz")
r.pfadd("pacientes_ativos", "João", "Carlos", "Mariana")
r.pfadd("pacientes_ativos", "Ana", "Pedro", "Fernanda")

# Contar quantos pacientes únicos agendaram consultas
pacientes_unicos = r.pfcount("pacientes_ativos")

print(f"Total de pacientes únicos com consulta marcada: {pacientes_unicos}")

# Para testar, adicionamos mais pacientes
r.pfadd("pacientes_ativos", "Lucas", "Camila", "Gabriel")
pacientes_unicos_atualizado = r.pfcount("pacientes_ativos")

print(f"Total atualizado de pacientes únicos: {pacientes_unicos_atualizado}")
