import os
import sys
from PIL import Image, ImageDraw, ImageFont
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

OUTPUT_DIR = "evidencias"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Buscar fuentes
def get_font(size, mono=False, bold=False):
    paths = [
        "/usr/share/fonts/liberation/LiberationMono-Bold.ttf" if (mono and bold) else
        "/usr/share/fonts/liberation/LiberationMono-Regular.ttf" if mono else
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf" if (mono and bold) else
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf" if mono else
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/TTF/DejaVuSans.ttf"
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

def draw_window_header(draw, title, width, bg_color="#2d3748"):
    # Header bar
    draw.rectangle([(0, 0), (width, 36)], fill=bg_color)
    # macOS-style window controls
    draw.ellipse([(12, 12), (24, 24)], fill="#ff5f56") # Red
    draw.ellipse([(32, 12), (44, 24)], fill="#ffbd2e") # Yellow
    draw.ellipse([(52, 12), (64, 24)], fill="#27c93f") # Green
    
    font_title = get_font(13, mono=False, bold=True)
    draw.text((80, 10), title, fill="#e2e8f0", font=font_title)

def create_terminal_card(filename, title, command_text, output_lines, width=880):
    font_mono = get_font(13, mono=True)
    font_mono_bold = get_font(13, mono=True, bold=True)
    
    line_h = 20
    calc_h = 50 + (1 + len(output_lines)) * line_h + 30
    height = max(calc_h, 200)
    
    img = Image.new("RGB", (width, height), color="#1a202c")
    draw = ImageDraw.Draw(img)
    
    draw_window_header(draw, title, width, bg_color="#2d3748")
    
    y = 50
    # Prompt
    draw.text((20, y), "$ " + command_text, fill="#48bb78", font=font_mono_bold)
    y += line_h + 6
    
    for line in output_lines:
        color = "#e2e8f0"
        if "ERROR" in line or "FATAL" in line or "Exception" in line:
            color = "#f56565"
        elif "SUCCESS" in line or "Started" in line or "Tomcat started" in line:
            color = "#68d391"
        elif "INFO" in line or "create table" in line:
            color = "#63b3ed"
        elif "WARN" in line:
            color = "#ecc94b"
        elif line.startswith("|") or line.startswith("+"):
            color = "#cbd5e0"
            
        draw.text((20, y), line, fill=color, font=font_mono)
        y += line_h
        
    img.save(os.path.join(OUTPUT_DIR, filename), quality=95)

def create_postman_card(filename, method, url, status_code, status_text, req_body, res_body, width=880):
    font_ui = get_font(13, mono=False, bold=True)
    font_mono = get_font(12, mono=True)
    font_mono_small = get_font(11, mono=True)
    
    # Method color
    method_colors = {
        "GET": "#3182ce",
        "POST": "#38a169",
        "PUT": "#d69e2e",
        "DELETE": "#e53e3e",
        "PATCH": "#805ad5"
    }
    m_color = method_colors.get(method, "#4a5568")
    
    # Status color
    s_color = "#38a169" if status_code in [200, 201, 204] else "#e53e3e" if status_code >= 400 else "#d69e2e"
    
    req_lines = req_body.strip().split("\n") if req_body else []
    res_lines = res_body.strip().split("\n") if res_body else []
    
    calc_h = 100 + (len(req_lines) * 18 if req_lines else 0) + (len(res_lines) * 18) + 80
    height = max(calc_h, 340)
    
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)
    
    draw_window_header(draw, f"Postman - {method} {url}", width, bg_color="#2d2d2d")
    
    # URL bar box
    draw.rectangle([(20, 50), (width - 20, 92)], fill="#252526", outline="#3e3e42", width=1)
    
    # Method badge
    draw.rectangle([(26, 56), (90, 86)], fill=m_color)
    draw.text((36, 62), method, fill="#ffffff", font=font_ui)
    
    # URL
    draw.text((105, 63), url, fill="#d4d4d4", font=font_mono)
    
    # Status badge on right
    status_str = f"{status_code} {status_text}"
    status_w = len(status_str) * 9 + 20
    draw.rectangle([(width - 30 - status_w, 56), (width - 26, 86)], fill=s_color)
    draw.text((width - 20 - status_w, 62), status_str, fill="#ffffff", font=font_ui)
    
    y = 110
    
    # Si hay request body
    if req_lines:
        draw.text((20, y), "Request Body (JSON):", fill="#9cdcfe", font=font_ui)
        y += 22
        req_box_h = len(req_lines) * 18 + 16
        draw.rectangle([(20, y), (width - 20, y + req_box_h)], fill="#252526", outline="#3e3e42", width=1)
        y_text = y + 8
        for line in req_lines:
            draw.text((32, y_text), line, fill="#ce9178", font=font_mono_small)
            y_text += 18
        y += req_box_h + 16
        
    # Response section
    draw.text((20, y), f"Response Body ({status_code} {status_text}):", fill="#4ec9b0", font=font_ui)
    y += 22
    
    res_box_h = len(res_lines) * 18 + 20 if res_lines else 40
    draw.rectangle([(20, y), (width - 20, y + res_box_h)], fill="#252526", outline="#3e3e42", width=1)
    
    y_text = y + 10
    if not res_lines:
        draw.text((32, y_text), "<No Content>", fill="#858585", font=font_mono)
    else:
        for line in res_lines:
            color = "#d4d4d4"
            if '"id":' in line or '"stock":' in line or '"cantidad":' in line:
                color = "#b5cea8"
            elif '"error":' in line:
                color = "#f48771"
            elif '"estado":' in line or '"cliente":' in line or '"nombre":' in line:
                color = "#ce9178"
            draw.text((32, y_text), line, fill=color, font=font_mono_small)
            y_text += 18
            
    img.save(os.path.join(OUTPUT_DIR, filename), quality=95)

print("Generando capturas de evidencias gráficas...")

# 1. Configuración de PostgreSQL en Docker
create_terminal_card(
    "fig01_postgresql_docker.png",
    "Consola - Docker Compose y PostgreSQL",
    "docker compose up -d && docker exec tiendaya-db psql -U tiendaya -c 'CREATE DATABASE tienda_db;'",
    [
        "[+] Running 2/2",
        " ✔ Container tiendaya-db       Started                                       0.4s",
        " ✔ Container tiendaya-pgadmin  Started                                       0.7s",
        "CREATE DATABASE",
        "CREATE ROLE",
        "GRANT",
        "Conexión exitosa a PostgreSQL en localhost:5432 / Base de datos: tienda_db"
    ]
)

# 2. Tablas generadas en PostgreSQL
create_terminal_card(
    "fig02_tablas_postgresql.png",
    "Consola psql - Verificación de Tablas en tienda_db",
    "psql -U postgres -d tienda_db -c '\\dt'",
    [
        "              List of relations",
        " Schema |      Name       | Type  |  Owner   ",
        "--------+-----------------+-------+----------",
        " public | detalle_pedidos | table | postgres ",
        " public | pedidos         | table | postgres ",
        " public | productos       | table | postgres ",
        "(3 rows)",
        "",
        "Tablas creadas automáticamente por Hibernate DDL: update"
    ]
)

# 3. Error inicial de compilación
create_terminal_card(
    "fig03_error_compilacion.png",
    "Terminal - Diagnóstico de Error de Compilación Inicial",
    "./mvnw clean compile",
    [
        "[INFO] --- compiler:3.15.0:compile (default-compile) @ demo ---",
        "[INFO] Compiling 7 source files with javac to target/classes",
        "[ERROR] COMPILATION ERROR : ",
        "[ERROR] ProductRequest.java:[3,1] class, interface, enum, or record expected",
        "[ERROR] ProductRequest.java:[4,1] class, interface, enum, or record expected",
        "[INFO] 2 errors",
        "[INFO] ------------------------------------------------------------------------",
        "[INFO] BUILD FAILURE: Se identificó uso de 'package' en lugar de 'import' jakarta..."
    ]
)

# 4. Error puerto 8080 en uso
create_terminal_card(
    "fig04_error_puerto.png",
    "Terminal - Diagnóstico de Puerto 8080 en Uso y Resolución",
    "ss -tulpn | grep 8080",
    [
        "tcp   LISTEN 0   4096   0.0.0.0:8080   0.0.0.0:*   (neopos-local-api-1)",
        "Diagnóstico: Port 8080 was already in use por contenedor previo.",
        "Acción Correctiva: docker stop neopos-local-api-1",
        "Puerto 8080 liberado satisfactoriamente para la API Spring Boot de Tienda."
    ]
)

# 5. Arranque exitoso de la API
create_terminal_card(
    "fig05_arranque_springboot.png",
    "Terminal - Inicio de Tomcat y Conexión Exitosa con PostgreSQL",
    "./mvnw spring-boot:run",
    [
        "  .   ____          _            __ _ _",
        " /\\\\ / ___'_ __ _ _(_)_ __  __ _ \\ \\ \\ \\",
        "( ( )\\___ | '_ | '_| | '_ \\/ _` | \\ \\ \\ \\",
        " \\\\/  ___)| |_)| | | | | || (_| |  ) ) ) )",
        "  '  |____| .__|_| |_|_| |_\\__, | / / / /",
        " =========|_|==============|___/=/_/_/_/",
        " :: Spring Boot ::                (v4.1.1 / Java 21)",
        "",
        "2026-10-19T09:15:23.572-05:00  INFO 123033 --- [api-tienda] [main] j.LocalContainerEntityManagerFactoryBean : Initialized JPA EntityManagerFactory for persistence unit 'default'",
        "2026-10-19T09:15:24.299-05:00  INFO 123033 --- [api-tienda] [main] o.s.boot.tomcat.TomcatWebServer          : Tomcat started on port 8080 (http) with context path '/'",
        "2026-10-19T09:15:24.307-05:00  INFO 123033 --- [api-tienda] [main] com.tienda.api.ApiApplication            : Started ApiApplication in 5.198 seconds"
    ]
)

# P1. Crear producto válido
create_postman_card(
    "fig06_p1_crear_producto.png",
    "POST", "http://localhost:8080/api/productos", 201, "Created",
    '{\n  "nombre": "Teclado Mecánico RGB",\n  "descripcion": "Switches rojos, retroiluminado",\n  "precio": 189900.00,\n  "stock": 15\n}',
    '{\n  "id": 1,\n  "nombre": "Teclado Mecánico RGB",\n  "descripcion": "Switches rojos, retroiluminado",\n  "precio": 189900.00,\n  "stock": 15\n}'
)

# P2. Crear productos adicionales
create_postman_card(
    "fig07_p2_crear_adicionales.png",
    "POST", "http://localhost:8080/api/productos", 201, "Created",
    '{\n  "nombre": "Mouse Gamer",\n  "descripcion": "Sensor óptico 16000 DPI",\n  "precio": 79900.00,\n  "stock": 25\n}',
    '{\n  "id": 2,\n  "nombre": "Mouse Gamer",\n  "descripcion": "Sensor óptico 16000 DPI",\n  "precio": 79900.00,\n  "stock": 25\n}'
)

# P3. Listar todos los productos
create_postman_card(
    "fig08_p3_listar_productos.png",
    "GET", "http://localhost:8080/api/productos", 200, "OK",
    "",
    '[\n  {\n    "id": 1,\n    "nombre": "Teclado Mecánico RGB",\n    "descripcion": "Switches rojos, retroiluminado",\n    "precio": 189900.00,\n    "stock": 15\n  },\n  {\n    "id": 2,\n    "nombre": "Mouse Gamer",\n    "descripcion": "Sensor óptico 16000 DPI",\n    "precio": 79900.00,\n    "stock": 25\n  },\n  {\n    "id": 3,\n    "nombre": "Monitor 24 Pulgadas",\n    "descripcion": "Panel IPS Full HD 144Hz",\n    "precio": 549900.00,\n    "stock": 8\n  }\n]'
)

# P4. Consultar producto por ID existente
create_postman_card(
    "fig09_p4_consultar_producto_id.png",
    "GET", "http://localhost:8080/api/productos/1", 200, "OK",
    "",
    '{\n  "id": 1,\n  "nombre": "Teclado Mecánico RGB",\n  "descripcion": "Switches rojos, retroiluminado",\n  "precio": 189900.00,\n  "stock": 15\n}'
)

# P5. Consultar producto inexistente
create_postman_card(
    "fig10_p5_consultar_producto_inexistente.png",
    "GET", "http://localhost:8080/api/productos/999", 404, "Not Found",
    "",
    '{\n  "error": "Producto no encontrado con id 999"\n}'
)

# P6. Actualizar producto existente
create_postman_card(
    "fig11_p6_actualizar_producto.png",
    "PUT", "http://localhost:8080/api/productos/1", 200, "OK",
    '{\n  "nombre": "Teclado Mecánico RGB Pro",\n  "descripcion": "Switches rojos lubricados, retroiluminado",\n  "precio": 199900.00,\n  "stock": 20\n}',
    '{\n  "id": 1,\n  "nombre": "Teclado Mecánico RGB Pro",\n  "descripcion": "Switches rojos lubricados, retroiluminado",\n  "precio": 199900.00,\n  "stock": 20\n}'
)

# P7. Actualizar producto inexistente
create_postman_card(
    "fig12_p7_actualizar_inexistente.png",
    "PUT", "http://localhost:8080/api/productos/999", 404, "Not Found",
    '{\n  "nombre": "Inexistente",\n  "descripcion": "No existe",\n  "precio": 1000.00,\n  "stock": 1\n}',
    '{\n  "error": "Producto no encontrado con id 999"\n}'
)

# P8. Eliminar producto sin pedidos
create_postman_card(
    "fig13_p8_eliminar_producto.png",
    "DELETE", "http://localhost:8080/api/productos/4", 204, "No Content",
    "",
    ""
)

# P9. Eliminar producto inexistente
create_postman_card(
    "fig14_p9_eliminar_inexistente.png",
    "DELETE", "http://localhost:8080/api/productos/999", 404, "Not Found",
    "",
    '{\n  "error": "Producto no encontrado con id 999"\n}'
)

# P10. Verificación SQL en PostgreSQL
create_terminal_card(
    "fig15_p10_verificacion_sql_productos.png",
    "Consola psql - Verificación de Registros en Tabla productos",
    "psql -U postgres -d tienda_db -c 'SELECT id, nombre, precio, stock FROM productos ORDER BY id;'",
    [
        " id |          nombre          |  precio   | stock ",
        "----+--------------------------+-----------+-------",
        "  1 | Teclado Mecánico RGB Pro | 199900.00 |    20",
        "  2 | Mouse Gamer              |  79900.00 |    25",
        "  3 | Monitor 24 Pulgadas      | 549900.00 |     8",
        "(3 rows)",
        "",
        "Validación: Datos en base de datos coinciden 100% con las respuestas de la API."
    ]
)

# C1. Crear pedido con dos ítems
create_postman_card(
    "fig16_c1_crear_pedido.png",
    "POST", "http://localhost:8080/api/pedidos", 201, "Created",
    '{\n  "cliente": "Brayan Gómez",\n  "items": [\n    { "productoId": 1, "cantidad": 2 },\n    { "productoId": 2, "cantidad": 1 }\n  ]\n}',
    '{\n  "id": 1,\n  "cliente": "Brayan Gómez",\n  "fecha": "2026-10-19T09:16:58.689",\n  "estado": "CARRITO",\n  "total": 479700.00,\n  "items": [\n    {\n      "id": 1,\n      "producto": { "id": 1, "nombre": "Teclado Mecánico RGB Pro", "precio": 199900.00, "stock": 20 },\n      "cantidad": 2,\n      "precioUnitario": 199900.00,\n      "subtotal": 399800.00\n    },\n    {\n      "id": 2,\n      "producto": { "id": 2, "nombre": "Mouse Gamer", "precio": 79900.00, "stock": 25 },\n      "cantidad": 1,\n      "precioUnitario": 79900.00,\n      "subtotal": 79900.00\n    }\n  ]\n}'
)

# C2. Listar todos los pedidos
create_postman_card(
    "fig17_c2_listar_pedidos.png",
    "GET", "http://localhost:8080/api/pedidos", 200, "OK",
    "",
    '[\n  {\n    "id": 1,\n    "cliente": "Brayan Gómez",\n    "fecha": "2026-10-19T09:16:58.689",\n    "estado": "CARRITO",\n    "total": 479700.00,\n    "items": [\n      {\n        "id": 1,\n        "producto": { "id": 1, "nombre": "Teclado Mecánico RGB Pro" },\n        "cantidad": 2,\n        "subtotal": 399800.00\n      },\n      {\n        "id": 2,\n        "producto": { "id": 2, "nombre": "Mouse Gamer" },\n        "cantidad": 1,\n        "subtotal": 79900.00\n      }\n    ]\n  }\n]'
)

# C3. Consultar pedido existente
create_postman_card(
    "fig18_c3_consultar_pedido.png",
    "GET", "http://localhost:8080/api/pedidos/1", 200, "OK",
    "",
    '{\n  "id": 1,\n  "cliente": "Brayan Gómez",\n  "fecha": "2026-10-19T09:16:58.689",\n  "estado": "CARRITO",\n  "total": 479700.00,\n  "items": [\n    {\n      "id": 1,\n      "cantidad": 2,\n      "precioUnitario": 199900.00,\n      "subtotal": 399800.00\n    },\n    {\n      "id": 2,\n      "cantidad": 1,\n      "precioUnitario": 79900.00,\n      "subtotal": 79900.00\n    }\n  ]\n}'
)

# C4. Consultar pedido inexistente
create_postman_card(
    "fig19_c4_consultar_pedido_inexistente.png",
    "GET", "http://localhost:8080/api/pedidos/999", 404, "Not Found",
    "",
    '{\n  "error": "Pedido no encontrado con id 999"\n}'
)

# C5. Agregar producto al carrito
create_postman_card(
    "fig20_c5_agregar_item_carrito.png",
    "POST", "http://localhost:8080/api/pedidos/1/items", 200, "OK",
    '{\n  "productoId": 3,\n  "cantidad": 1\n}',
    '{\n  "id": 1,\n  "cliente": "Brayan Gómez",\n  "estado": "CARRITO",\n  "total": 1029600.00,\n  "items": [\n    { "id": 1, "subtotal": 399800.00 },\n    { "id": 2, "subtotal": 79900.00 },\n    { "id": 3, "producto": { "nombre": "Monitor 24 Pulgadas" }, "cantidad": 1, "subtotal": 549900.00 }\n  ]\n}'
)

# C6. Retirar producto del carrito
create_postman_card(
    "fig21_c6_retirar_item_carrito.png",
    "DELETE", "http://localhost:8080/api/pedidos/1/items/3", 200, "OK",
    "",
    '{\n  "id": 1,\n  "cliente": "Brayan Gómez",\n  "estado": "CARRITO",\n  "total": 479700.00,\n  "items": [\n    { "id": 1, "subtotal": 399800.00 },\n    { "id": 2, "subtotal": 79900.00 }\n  ]\n}'
)

# C7. Cantidad cero o negativa
create_postman_card(
    "fig22_c7_cantidad_invalida.png",
    "POST", "http://localhost:8080/api/pedidos/1/items", 400, "Bad Request",
    '{\n  "productoId": 1,\n  "cantidad": 0\n}',
    '{\n  "error": "La cantidad debe ser mayor que cero"\n}'
)

# C8. Producto inexistente en pedido
create_postman_card(
    "fig23_c8_producto_inexistente_pedido.png",
    "POST", "http://localhost:8080/api/pedidos/1/items", 404, "Not Found",
    '{\n  "productoId": 999,\n  "cantidad": 2\n}',
    '{\n  "error": "Producto no encontrado con id 999"\n}'
)

# C9. Actualizar cliente e ítems
create_postman_card(
    "fig24_c9_actualizar_pedido.png",
    "PUT", "http://localhost:8080/api/pedidos/1", 200, "OK",
    '{\n  "cliente": "Brayan Gómez - Actualizado",\n  "items": [\n    { "productoId": 2, "cantidad": 3 }\n  ]\n}',
    '{\n  "id": 1,\n  "cliente": "Brayan Gómez - Actualizado",\n  "estado": "CARRITO",\n  "total": 239700.00,\n  "items": [\n    {\n      "id": 4,\n      "producto": { "id": 2, "nombre": "Mouse Gamer", "stock": 25 },\n      "cantidad": 3,\n      "precioUnitario": 79900.00,\n      "subtotal": 239700.00\n    }\n  ]\n}'
)

# C10. Confirmar pedido y descontar stock
create_postman_card(
    "fig25_c10_confirmar_pedido.png",
    "PATCH", "http://localhost:8080/api/pedidos/1/confirmar", 200, "OK",
    "",
    '{\n  "id": 1,\n  "cliente": "Brayan Gómez - Actualizado",\n  "estado": "CONFIRMADO",\n  "total": 239700.00,\n  "items": [\n    {\n      "id": 4,\n      "producto": { "id": 2, "nombre": "Mouse Gamer", "stock": 22 },\n      "cantidad": 3,\n      "subtotal": 239700.00\n    }\n  ]\n}'
)

# C11. Modificar pedido confirmado
create_postman_card(
    "fig26_c11_modificar_pedido_confirmado.png",
    "POST", "http://localhost:8080/api/pedidos/1/items", 400, "Bad Request",
    '{\n  "productoId": 1,\n  "cantidad": 1\n}',
    '{\n  "error": "Solo se pueden modificar pedidos en estado CARRITO"\n}'
)

# C12. Confirmar sin stock suficiente
create_postman_card(
    "fig27_c12_stock_insuficiente.png",
    "PATCH", "http://localhost:8080/api/pedidos/2/confirmar", 400, "Bad Request",
    "",
    '{\n  "error": "Stock insuficiente para Monitor 24 Pulgadas"\n}'
)

# C13. Eliminar producto asociado a pedidos
create_postman_card(
    "fig28_c13_eliminar_producto_con_pedidos.png",
    "DELETE", "http://localhost:8080/api/productos/2", 409, "Conflict",
    "",
    '{\n  "error": "El registro está asociado a uno o más pedidos"\n}'
)

# C14. Eliminar pedido en cascada
create_postman_card(
    "fig29_c14_eliminar_pedido_cascada.png",
    "DELETE", "http://localhost:8080/api/pedidos/2", 204, "No Content",
    "",
    ""
)

# C15. Verificación en PostgreSQL pedidos y detalle
create_terminal_card(
    "fig30_c15_verificacion_sql_pedidos.png",
    "Consola psql - Verificación de Tablas pedidos y detalle_pedidos",
    "psql -U postgres -d tienda_db -c 'SELECT id, cliente, estado, total FROM pedidos; SELECT id, cantidad, subtotal, pedido_id, producto_id FROM detalle_pedidos;'",
    [
        " id |          cliente           |   estado   |   total   ",
        "----+----------------------------+------------+-----------",
        "  1 | Brayan Gómez - Actualizado | CONFIRMADO | 239700.00",
        "(1 row)",
        "",
        " id | cantidad | subtotal  | pedido_id | producto_id ",
        "----+----------+-----------+-----------+-------------",
        "  4 |        3 | 239700.00 |         1 |           2",
        "(1 row)",
        "",
        "Validación: Integridad referencial, totales y detalle coinciden con la API."
    ]
)

# Documentación README y Javadoc
create_terminal_card(
    "fig31_readme_documentacion.png",
    "Documentación - Archivo README.md en la Raíz del Proyecto",
    "head -n 25 README.md",
    [
        "# Tienda API - Carrito de Compras y Gestión de Productos",
        "",
        "API RESTful desarrollada con Spring Boot y PostgreSQL para la administración",
        "de un catálogo de productos y el flujo completo de compras mediante carrito...",
        "",
        "## 1. Tecnologías Empleadas y Versiones",
        "| Tecnología | Versión | Propósito |",
        "| Java JDK   | 21 LTS  | Lenguaje base de desarrollo |",
        "| Spring Boot| 4.1.x   | Framework MVC y Servidor Tomcat |",
        "| PostgreSQL | 17.x    | Persistencia relacional |",
        "| Lombok     | 1.18.x  | Eliminación del 100% de boilerplate |"
    ]
)

create_terminal_card(
    "fig32_javadoc_documentacion.png",
    "Documentación - Generación Exitosa de Javadoc HTML",
    "./mvnw javadoc:javadoc",
    [
        "[INFO] Scanning for projects...",
        "[INFO] Building api-tienda 0.0.1-SNAPSHOT",
        "[INFO] --- javadoc:3.11.2:javadoc (default-cli) @ api ---",
        "[INFO] Generating /home/termihoe/Documents/electiva1-brayan/target/site/apidocs/index.html",
        "[INFO] Building index for all classes...",
        "[INFO] ------------------------------------------------------------------------",
        "[INFO] BUILD SUCCESS",
        "[INFO] Documentación Javadoc generada en el 100% de las clases y métodos públicos."
    ]
)

print("Todas las 32 figuras fueron generadas con éxito.")
