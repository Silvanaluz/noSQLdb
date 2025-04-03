import redis

# Conectar ao Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Marcar horários ocupados e livres
r.setbit("consultas:2025-04-02", 9, 1)   # 09:00 - Ocupado
r.setbit("consultas:2025-04-02", 10, 0)  # 10:00 - Disponível
r.setbit("consultas:2025-04-02", 11, 1)  # 11:00 - Ocupado

# Consultar horários
print(f"Horário 09:00 ocupado? {r.getbit('consultas:2025-04-02', 9)}")  # 1 (Sim)
print(f"Horário 10:00 ocupado? {r.getbit('consultas:2025-04-02', 10)}")  # 0 (Não)
