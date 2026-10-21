# 🗺️ Roadmap Completo del Proyecto Spring Boot + PostgreSQL
> **Basado en la guía oficial: “Parcial – Versión 1.0, Octubre de 2026”**

Este documento contiene la ruta de trabajo completa organizada en las **6 fases originales del documento**, con sus 42 pasos de verificación, los archivos involucrados y la checklist de revisión individual para que tú vayas marcando cada ítem a medida que lo revises y apruebes.

---

## 📊 Progreso General del Proyecto

- [x] **Fase 1: Configuración de PostgreSQL, corrección de errores y ejecución** *(7/7 pasos completados)*
- [x] **Fase 2: Implementación de Lombok al 100 %** *(6/6 pasos completados)*
- [x] **Fase 3: CRUD de Productos** *(7/7 pasos completados)*
- [x] **Fase 4: Módulo de Pedidos (Carrito de Compras)** *(10/10 pasos completados)*
- [x] **Fase 5: Documentación (README y Javadoc)** *(5/5 pasos completados)*
- [x] **Fase 6: Pruebas funcionales y evidencias** *(7/7 pasos completados)*

---

## 🗂️ Checklist de Archivos a Revisar Uno a Uno

Usa esta lista para auditar, humanizar y commitear cada archivo individualmente:

### 1. Configuración e Infraestructura
- [x] `application.properties` (raíz) y `src/main/resources/application.properties` *(Revisado y aprobado)*
- [x] `pom.xml`
- [x] `docker-compose.yml`
- [x] `mvnw`

### 2. Capa Modelo / Entidades (`src/main/java/com/tienda/api/model/`)
- [x] `Producto.java`
- [x] `EstadoPedido.java`
- [x] `DetallePedido.java`
- [x] `Pedido.java`

### 3. Capa DTO y Excepciones
- [x] `src/main/java/com/tienda/api/dto/ItemRequest.java`
- [x] `src/main/java/com/tienda/api/dto/PedidoRequest.java`
- [x] `src/main/java/com/tienda/api/exception/RecursoNoEncontradoException.java`
- [x] `src/main/java/com/tienda/api/exception/ManejadorGlobalExcepciones.java`

### 4. Capa Repositorio (`src/main/java/com/tienda/api/repository/`)
- [x] `ProductoRepository.java`
- [x] `PedidoRepository.java`

### 5. Capa Servicio (`src/main/java/com/tienda/api/service/`)
- [x] `ProductoService.java`
- [x] `PedidoService.java`

### 6. Capa Controlador y Main (`src/main/java/com/tienda/api/controller/`)
- [x] `ProductoController.java`
- [x] `PedidoController.java`
- [x] `src/main/java/com/tienda/api/ApiApplication.java`

### 7. Pruebas Unitarias (`src/test/java/com/tienda/api/`)
- [x] `ApiApplicationTests.java`
- [x] `service/ProductoServiceTest.java`
- [x] `service/PedidoServiceTest.java`

### 8. Documentación y Postman
- [x] `TiendaYa_API.postman_collection.json`
- [x] `README.md`
- [x] `Gomez_Brayan_Ficha2026_ActividadPedidos.docx`

---

## 🚀 Detalle Paso a Paso por Fases (42 Pasos)

### Fase 1. Configuración de PostgreSQL, corrección de errores y ejecución de la API
*Objetivo: Conseguir que el proyecto compile, se conecte a PostgreSQL y funcione antes de implementar nuevas funcionalidades.*

- [ ] **Paso 1:** Instalar y verificar PostgreSQL 15+ en el puerto 5432 (Contenedor Docker `tiendaya-db`).
- [ ] **Paso 2:** Crear la base de datos `tienda_db` mediante `CREATE DATABASE tienda_db;`.
- [ ] **Paso 3:** Configurar la dependencia del driver `org.postgresql:postgresql` en `pom.xml`.
- [x] **Paso 4:** Configurar `src/main/resources/application.properties` con `tienda_db`, puerto `8080`, usuario `postgres`.
- [ ] **Paso 5:** Compilar con `./mvnw clean install` y registrar/corregir errores:
  - Error de compilación en `ProductRequest` (`package` vs `import`).
  - Conflicto de puerto 8080 (`Port 8080 was already in use`).
- [ ] **Paso 6:** Iniciar Spring Boot y verificar inicio de Tomcat y tablas creadas por Hibernate.
- [ ] **Paso 7:** Probar endpoints preexistentes y guardar evidencias.

---

### Fase 2. Implementación de Lombok al 100 %
*Objetivo: Eliminar constructores, getters, setters y toString manuales, e implementar inyección por constructor.*

- [ ] **Paso 1:** Añadir dependencia `org.projectlombok:lombok` y `annotationProcessorPaths` en `pom.xml`.
- [ ] **Paso 2:** Revisar todas las clases y localizar código repetitivo manual.
- [ ] **Paso 3:** Migrar entidades a `@Getter`, `@Setter`, `@NoArgsConstructor`, `@AllArgsConstructor`, `@Builder`, `@Builder.Default` (evitando `@Data` en entidades JPA).
- [ ] **Paso 4:** Migrar DTOs a `@Data`, `@NoArgsConstructor`, `@AllArgsConstructor`, `@Builder`.
- [ ] **Paso 5:** Migrar servicios y controladores a inyección por constructor con `@RequiredArgsConstructor` sobre atributos `private final` (eliminando `@Autowired` en atributos).
- [ ] **Paso 6:** Validar la compilación limpia y registrar el comparativo antes/después.

---

### Fase 3. Implementación del CRUD completo de Productos
*Objetivo: Completar los cinco endpoints de Productos en `/api/productos` con códigos HTTP correctos.*

- [ ] **Paso 1:** Revisar endpoints existentes e identificar faltantes (PUT y DELETE).
- [ ] **Paso 2:** Organizar la estructura en `com.tienda.api` y verificar la entidad `Producto` (id, nombre, descripcion, precio con `BigDecimal`, stock con `Integer`).
- [ ] **Paso 3:** Crear `ProductoRepository` extendiendo `JpaRepository<Producto, Long>` y `RecursoNoEncontradoException`.
- [ ] **Paso 4:** Completar `ProductoService` con métodos `listarTodos()`, `buscarPorId()`, `crear()`, `actualizar()`, `eliminar()`.
- [ ] **Paso 5:** Completar `ProductoController` con anotaciones `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping`.
- [ ] **Paso 6:** Controlar respuestas HTTP: 201 (crear), 200 (consultar/actualizar), 204 (eliminar), 404 (no encontrado), 409 (conflicto llave foránea).
- [ ] **Paso 7:** Probar los 5 endpoints con Postman y validar persistencia en PostgreSQL.

---

### Fase 4. Desarrollo del módulo de Pedidos (Carrito de Compras)
*Objetivo: Implementar el carrito de compras, cálculo de subtotales y totales, validaciones y descuento de stock.*

- [ ] **Paso 1:** Definir modelo relacional: Producto 1:N DetallePedido y Pedido 1:N DetallePedido.
- [ ] **Paso 2:** Crear enum `EstadoPedido` (CARRITO, CONFIRMADO, CANCELADO) y entidades `Pedido` y `DetallePedido` con `@JsonManagedReference` y `@JsonBackReference`.
- [ ] **Paso 3:** Crear DTOs `ItemRequest` y `PedidoRequest`.
- [ ] **Paso 4:** Crear `PedidoRepository` extendiendo `JpaRepository<Pedido, Long>`.
- [ ] **Paso 5:** Implementar en `PedidoService` las operaciones de consulta (`listarTodos`, `buscarPorId`) y creación (`crear`).
- [ ] **Paso 6:** Implementar actualización (`actualizar`), adición de ítems (`agregarItem`), remoción (`quitarItem`) y cálculo de subtotales/totales en el servidor.
- [ ] **Paso 7:** Implementar confirmación de compra (`confirmar`) con `@Transactional`: validar stock suficiente, descontar inventario y cambiar estado a `CONFIRMADO` (con rollback si falla).
- [ ] **Paso 8:** Validar reglas de negocio: solo pedidos `CARRITO` se modifican, cantidad $> 0$, carrito vacío no se confirma, producto en pedido no se puede borrar (409).
- [ ] **Paso 9:** Crear `PedidoController` con los 8 endpoints solicitados.
- [ ] **Paso 10:** Crear `ManejadorGlobalExcepciones` con `@RestControllerAdvice` para capturar 404, 400 y 409.

---

### Fase 5. Documentación del Proyecto
*Objetivo: Documentar formalmente el proyecto con README y Javadoc.*

- [ ] **Paso 1:** Crear `README.md` en la raíz del proyecto.
- [ ] **Paso 2:** Documentar descripción, tecnologías y versiones (Java 21, Spring Boot, Lombok, PostgreSQL).
- [ ] **Paso 3:** Documentar instrucciones de instalación de base de datos y comandos de ejecución.
- [ ] **Paso 4:** Documentar modelo de datos, reglas de negocio y tabla de los 13 endpoints con ejemplos JSON.
- [ ] **Paso 5:** Añadir comentarios Javadoc en el 100 % de clases y métodos públicos (verificado con `./mvnw javadoc:javadoc`).

---

### Fase 6. Pruebas Funcionales y Registro de Evidencias
*Objetivo: Validar los 25 casos de prueba y consolidar el informe técnico.*

- [ ] **Paso 1:** Preparar colección Postman (`TiendaYa_API.postman_collection.json`) con carpetas `Productos` y `Pedidos`, variable `{{base_url}}` y scripts `pm.test`.
- [ ] **Paso 2:** Ejecutar pruebas P1 a P10 del módulo de Productos.
- [ ] **Paso 3:** Ejecutar pruebas C1 a C15 del módulo de Pedidos.
- [ ] **Paso 4:** Capturar y numerar mínimo 25 evidencias (generadas 32 figuras con fecha, hora y cliente "Brayan Gómez").
- [ ] **Paso 5:** Verificar registros coincidentes en PostgreSQL (`SELECT * FROM productos;`, `pedidos;`, `detalle_pedidos;`).
- [ ] **Paso 6:** Elaborar informe técnico Word con las 13 secciones obligatorias.
- [ ] **Paso 7:** Exportar colección Postman JSON y validar entregables.
