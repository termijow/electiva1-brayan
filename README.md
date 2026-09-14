# Demo API - Spring Boot & Java 25

API REST para la gestión de productos desarrollada con **Spring Boot** y **Java 25**.

---

## 📋 1. Requisitos Previos

Para ejecutar este proyecto necesitas tener instalado en tu sistema:

### A. Java Development Kit (JDK 25)
- Se requiere **Java 25** (ejemplo: Eclipse Temurin OpenJDK 25).
- Puedes descargarlo desde [Adoptium](https://adoptium.net/) o dejar que **IntelliJ IDEA** lo descargue automáticamente (en *Project Structure > SDKs*).

Para verificar si ya lo tienes instalado y reconocido por el sistema, abre una terminal y ejecuta:
```powershell
java -version
```
> Si te indica que no se reconoce el comando, sigue la sección [2. Configuración de Variables de Entorno](#-2-configuración-de-variables-de-entorno-windows).

### B. Gestor de Construcción (Maven)
- **No necesitas instalar Maven por separado**. El proyecto incluye el **Maven Wrapper** (`mvnw` para Linux/macOS y `mvnw.cmd` para Windows), el cual descargará automáticamente la versión exacta requerida.

---

## ⚙️ 2. Configuración de Variables de Entorno (Windows)

Si Java está instalado pero tu terminal no lo reconoce, debes configurar la variable `JAVA_HOME` y agregar la carpeta `bin` al `Path`.

### En PowerShell:
Abre PowerShell y ejecuta el siguiente comando (ajustando la ruta a tu carpeta JDK si es diferente):

```powershell
# Establecer JAVA_HOME en las variables de usuario
[System.Environment]::SetEnvironmentVariable('JAVA_HOME', 'C:\Users\Juan\.jdks\temurin-25.0.4.1', 'User')

# Agregar la carpeta bin al Path del usuario
$currentPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
if ($currentPath -notlike "*temurin-25.0.4.1\bin*") {
    $newPath = "$currentPath;C:\Users\Juan\.jdks\temurin-25.0.4.1\bin"
    [System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
}
```

> **Nota:** Abre una **nueva ventana de terminal** después de ejecutar estos comandos para que los cambios surtan efecto.

---

## 🚀 3. Paso a Paso para Levantar el Proyecto

### Opción 1: Desde la Terminal (Recomendado)

1. Abre una terminal (PowerShell o CMD) y navega a la carpeta del proyecto:
   ```powershell
   cd C:\Users\Juan\Downloads\demo\demo
   ```

2. Ejecuta la aplicación mediante Maven Wrapper:
   - **En Windows (PowerShell / CMD):**
     ```powershell
     .\mvnw.cmd spring-boot:run
     ```
   - **En Linux / macOS:**
     ```bash
     ./mvnw spring-boot:run
     ```

3. Verás en consola el banner de Spring Boot y la confirmación del puerto:
   ```text
   Tomcat initialized with port 8081 (http)
   Started DemoApplication in ... seconds
   ```

4. **Para detener la aplicación:** Presiona `Ctrl + C` en la terminal.

---

### Opción 2: Desde IntelliJ IDEA

1. Abre la carpeta del proyecto en **IntelliJ IDEA**.
2. Asegúrate de que el SDK del proyecto esté configurado en Java 25:
   - Ve a `File` > `Project Structure` > `Project` > **SDK** y selecciona `temurin-25`.
3. Navega en el explorador de archivos a:
   `src/main/java/com/example/demo/DemoApplication.java`
4. Haz clic en el ícono verde de **Play (Run)** junto a `public class DemoApplication` o en el método `main`.

---

## 🛠️ 4. Comandos Útiles de Maven Wrapper

| Acción | Comando (Windows) | Comando (Linux/macOS) |
|---|---|---|
| **Compilar el código** | `.\mvnw.cmd compile` | `./mvnw compile` |
| **Ejecutar pruebas unitarias** | `.\mvnw.cmd test` | `./mvnw test` |
| **Limpiar y compilar** | `.\mvnw.cmd clean compile` | `./mvnw clean compile` |
| **Generar el archivo JAR** | `.\mvnw.cmd clean package` | `./mvnw clean package` |
| **Ejecutar el JAR generado** | `java -jar target/demo-0.0.1-SNAPSHOT.jar` | `java -jar target/demo-0.0.1-SNAPSHOT.jar` |

---

## 🌐 5. Configuración de Red

- **Puerto:** `8081`
- **Archivo de configuración:** `src/main/resources/application.properties`
  ```properties
  spring.application.name=demo
  server.port=8081
  ```
  *(Se configuró el puerto 8081 para evitar conflictos con herramientas como Docker Desktop o WSL que suelen ocupar el puerto 8080).*

---

## 📡 6. Documentación de Endpoints y Pruebas

Con la aplicación en ejecución (`http://localhost:8081`), puedes probar los siguientes endpoints:

### 1. Listar todos los productos
- **Método:** `GET`
- **URL:** `http://localhost:8081/products` (o `http://localhost:8081/`)
- **Ejemplo en PowerShell:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8081/products"
  ```
- **Ejemplo con cURL:**
  ```bash
  curl -X GET http://localhost:8081/products
  ```

---

### 2. Crear un producto
- **Método:** `POST`
- **URL:** `http://localhost:8081/products?name={nombre}&price={precio}`
- **Parámetros:**
  - `name` (String, requerido): Nombre del producto.
  - `price` (double, requerido): Precio (debe ser mayor a 0).
- **Ejemplo en PowerShell:**
  ```powershell
  Invoke-RestMethod -Method Post -Uri "http://localhost:8081/products?name=Teclado%20Mecanico&price=250000"
  ```
- **Ejemplo con cURL:**
  ```bash
  curl -X POST "http://localhost:8081/products?name=Teclado%20Mecanico&price=250000"
  ```

---

### 3. Obtener un producto por su ID
- **Método:** `GET`
- **URL:** `http://localhost:8081/products/{id}`
- **Ejemplo en PowerShell:**
  ```powershell
  Invoke-RestMethod -Uri "http://localhost:8081/products/1"
  ```
- **Ejemplo con cURL:**
  ```bash
  curl -X GET http://localhost:8081/products/1
  ```

---

## 📁 7. Estructura del Código

```text
src/main/java/com/example/demo/
├── DemoApplication.java         # Clase principal con anotación @SpringBootApplication y main()
├── controller/
│   └── ProductController.java  # Controlador REST con endpoints GET y POST
├── service/
│   └── ProductService.java     # Lógica de negocio y validaciones
├── repository/
│   └── ProductRepository.java  # Almacenamiento en memoria (List en memoria)
└── model/
    └── Product.java            # Registro (Record) que define el modelo de datos
```
