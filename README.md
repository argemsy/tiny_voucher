# 🧾 TinyVoucher — Microservicio de Cupones

**TinyVoucher** es un microproyecto backend construido con **FastAPI + Django ORM + PostgreSQL**, diseñado bajo principios de **arquitectura hexagonal** y **Service Layer Pattern**.  
Su propósito es ofrecer una API REST asíncrona para **gestionar, validar y redimir cupones de descuento** (vouchers) asociados a campañas promocionales.

---

## ⚙️ Características principales

- 🔄 **FastAPI asíncrono** para endpoints de alto rendimiento.  
- 🧩 **Arquitectura Hexagonal (Ports & Adapters)** — dominio independiente del framework.  
- 🧠 **Principios SOLID y Clean Code** aplicados en todas las capas.  
- 💾 **Django ORM + PostgreSQL** como infraestructura de persistencia.  
- 🧰 **Service Layer + Repository Pattern** para mantener la lógica de negocio desacoplada.  
- 🧪 **Preparado para testing** (unit, integration, e2e con `pytest`, `factory_boy`, `pytest-django`).  
- 🧱 **Docker Compose** para entorno reproducible y aislado.  
- 🧾 **Logging estructurado con structlog** y manejador de errores estándar (`error_response_handler`).

---

## 🧱 Arquitectura general

```
tiny_voucher/
├── src/
│   ├── tiny_voucher/
│   │   ├── domain/                # Entidades, interfaces y lógica de negocio pura
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   ├── infrastructure/        # Implementaciones concretas (Django ORM, APIs externas)
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   ├── application/           # Casos de uso (coordinan flujo sin lógica de negocio)
│   │   ├── presentation/          # FastAPI layer (inputs, responses, routers)
│   │   └── shared/                # Utilidades, enums, errores, mixins
│   └── config/                    # Configuración de entorno, settings, Docker, etc.
└── tests/                         # Unit, integration y e2e tests
```

### 🧩 Flujo de ejecución (ejemplo `get_voucher_admin`)
1. **FastAPI Router** recibe el request y valida input (`GetVoucherInput`).
2. **Use Case** (`GetVoucherAdminUseCase`) orquesta la operación.
3. **Service** (`VoucherServiceImpl`) aplica validaciones y obtiene entidad.
4. **Repository** (`DjangoVoucherRepositoryImpl`) consulta la base de datos.
5. Se retorna un **DTO (`VoucherDetailSchemaPayload`)** hacia la vista.

---

## 🧰 Stack técnico

| Componente | Tecnología |
|-------------|-------------|
| Framework Web | FastAPI (async) |
| ORM / Persistencia | Django ORM |
| Base de datos | PostgreSQL |
| Contenedores | Docker + Docker Compose |
| Testing | pytest, pytest-django, factory_boy |
| Lint / Format / Typing | Ruff, Black, MyPy |
| Logging | structlog |
| Arquitectura | Hexagonal + Service Layer |
| Estilo de código | PEP8 / PEP257 / Google Docstrings |

---

## 🚀 Ejecución local con Docker

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/<your-username>/tiny-voucher.git
cd tiny-voucher
```

### 2️⃣ Levantar entorno
```bash
docker-compose up --build
```

### 3️⃣ Acceder a la API
- FastAPI Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Healthcheck (próximamente): `/api/v1/health`

---

## 🧪 Testing

### Ejecutar todos los tests
```bash
pytest -v
```

### Ejecutar solo tests unitarios
```bash
pytest -m unit
```

### Ejecutar integración con DB
```bash
pytest -m integration
```

---

## 📦 Endpoint actual implementado

### `POST /api/v1/voucher`
Obtiene el detalle de un voucher por su ID.  
Internamente:
- Instancia el caso de uso `GetVoucherAdminUseCase`.
- Usa el servicio `VoucherServiceImpl` y el repositorio `DjangoVoucherRepositoryImpl`.
- Devuelve un `VoucherDetailSchemaPayload`.

**Ejemplo de request**
```json
{
  "voucher_id": "7df5e8b0-1a32-4e49-b4c1-8c1fd5a5b52d"
}
```

**Ejemplo de response**
```json
{
  "voucher": {
    "id": "7df5e8b0-1a32-4e49-b4c1-8c1fd5a5b52d",
    "code": "SUMMER2025",
    "campaign": "Summer Promo",
    "discount_type": "PERCENTAGE",
    "value": 15,
    "is_redeemed": false
  }
}
```

---

## 🧭 Próximos pasos

| Fase | Objetivo |
|------|-----------|
| 1️⃣ | Implementar `ValidateVoucherUseCase` (validación de expiración, estado y campaña). |
| 2️⃣ | Implementar `RedeemVoucherUseCase` (registro de redención y auditoría). |
| 3️⃣ | Agregar endpoints `GET /campaigns`, `POST /campaigns/{id}/vouchers`. |
| 4️⃣ | Añadir eventos de dominio para trazabilidad (`VoucherRedeemedEvent`). |
| 5️⃣ | Cobertura total de tests + GitHub Actions para CI. |

---

## 🧑‍💻 Autor

**Emperador Argenis**  
Principal / Tech Advance Engineer — Python & FastAPI  
Especialista en Arquitecturas Limpias, Hexagonales y SOLID.

---

## 🏗️ Licencia

MIT License — libre uso y distribución con atribución.
