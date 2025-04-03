
{$geoNear: {
  near: { type: 'Point', coordinates: [-46.6333, -23.5505] },
  distanceField: 'dist.calculate',
  maxDistance: 1000,
  query: { "especialista.especialidade": "Cardiologista",
    "data_consulta": { "$gte": ISODate("2025-04-01")} },
  spherical:true}}