# SISTEMA DE TEMPLATES PARA PESTAÑAS

## 📋 DESCRIPCIÓN
Sistema dinámico para crear y gestionar pestañas en la interfaz web de captioning. Permite crear pestañas de forma programática sin modificar HTML hardcodeado. El sistema ha sido completamente migrado desde HTML estático a un sistema de templates dinámico y responsivo.

## 🆕 ÚLTIMAS ACTUALIZACIONES (Enero 2025)

### Mejoras Implementadas:
- ✅ **Sistema de templates completamente funcional**
- ✅ **Barra de progreso mejorada** con información detallada
- ✅ **Layout de múltiples columnas** para resultados (2-4 columnas responsivas)
- ✅ **Vista ampliada con caption** integrado
- ✅ **Altura de imágenes aumentada** (300px) para mejor visualización de fotos verticales
- ✅ **Botón "Seleccionar Imágenes"** funcional
- ✅ **Carga de modelos** corregida y optimizada
- ✅ **Endpoints de API** corregidos (/api/upload, /api/progress)
- ✅ **Sistema de eventos** completamente funcional
- ✅ **Estilos de botones unificados** (todos azules para consistencia)
- ✅ **Secciones de upload estandarizadas** en todas las pestañas
- ✅ **Drag & drop funcional** para archivos JSON
- ✅ **Navbar azul** con texto blanco consistente
- ✅ **Botones de resolución** con estilo unificado

## 🏗️ ARQUITECTURA

### Componentes Principales:
1. **`TabRegistry`** - Clase principal que gestiona todas las pestañas
2. **`TabTemplates`** - Templates predefinidos reutilizables
3. **`ExistingTabTemplates`** - Templates específicos para pestañas existentes
4. **Funciones de utilidad** - Para crear pestañas rápidamente

## 🔧 FUNCIONES DISPONIBLES

### 1. Funciones Básicas:
```javascript
// Crear pestaña personalizada
createTab({
    id: 'mi-pestaña',
    title: 'Mi Pestaña',
    icon: 'fas fa-star',
    template: () => '<div>Mi contenido</div>',
    onActivate: () => console.log('Activada'),
    onDeactivate: () => console.log('Desactivada')
});

// Crear pestaña básica
createBasicTab('id', 'Título', 'Contenido HTML', 'icono');

// Crear pestaña de carga de archivos
createFileUploadTab('id', 'Título', 'Descripción', 'accept', multiple, 'icono');

// Crear pestaña de formulario
createFormTab('id', 'Título', [campos], 'icono');
```

### 2. Funciones para Pestañas Existentes:
```javascript
// Pestañas principales del sistema
createGenerationTab();  // Pestaña de Generar Captions
createEditTab();        // Pestaña de Editar Captions
createMetadataTab();    // Pestaña de Metadatos IA
```

## 📝 TEMPLATES PREDEFINIDOS

### TabTemplates:
- **`basicCard(title, content)`** - Pestaña básica con card
- **`fileUpload(title, description, accept, multiple)`** - Carga de archivos
- **`form(title, fields)`** - Formularios dinámicos

### ExistingTabTemplates:
- **`generationTab()`** - Template completo para generación de captions
- **`editTab()`** - Template completo para edición de captions
- **`metadataTab()`** - Template completo para análisis de metadatos

## 🎯 EJEMPLOS DE USO

### Ejemplo 1: Pestaña Básica
```javascript
createBasicTab('config', 'Configuración', 
    '<p>Panel de configuración del sistema</p>',
    'fas fa-cogs'
);
```

### Ejemplo 2: Pestaña de Carga de Archivos
```javascript
createFileUploadTab('upload-docs', 'Cargar Documentos', 
    'Sube archivos PDF, Word o imágenes',
    '.pdf,.doc,.docx,image/*',
    true, // múltiples archivos
    'fas fa-upload'
);
```

### Ejemplo 3: Pestaña de Formulario
```javascript
createFormTab('user-settings', 'Configuración de Usuario', [
    { id: 'name', label: 'Nombre', type: 'text', placeholder: 'Tu nombre' },
    { id: 'email', label: 'Email', type: 'email', placeholder: 'tu@email.com' },
    { id: 'bio', label: 'Biografía', type: 'textarea', rows: 4, placeholder: 'Cuéntanos sobre ti' }
], 'fas fa-user-cog');
```

### Ejemplo 4: Pestaña Personalizada Completa
```javascript
createTab({
    id: 'analytics',
    title: 'Analíticas',
    icon: 'fas fa-chart-bar',
    template: () => `
        <div class="row mt-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-line me-2"></i>Estadísticas</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="analyticsChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    `,
    onActivate: () => {
        // Inicializar gráfico cuando se active la pestaña
        initializeChart();
    },
    onDeactivate: () => {
        // Limpiar recursos cuando se desactive
        cleanupChart();
    }
});
```

## 🔄 FLUJO DE FUNCIONAMIENTO

1. **Inicialización**: Al cargar la página, se ejecutan las funciones de creación de pestañas
2. **Registro**: Cada pestaña se registra en `TabRegistry`
3. **Renderizado**: Se genera el HTML dinámicamente y se inserta en el DOM
4. **Event Listeners**: Se configuran automáticamente los event listeners
5. **Activación**: Al hacer clic en una pestaña, se ejecuta `onActivate()`

## 🛠️ FUNCIONES DE INICIALIZACIÓN

### Para Pestañas con Event Listeners Específicos:
```javascript
// En la función onActivate de la pestaña
onActivate: () => {
    // Re-inicializar event listeners específicos
    initializeCustomEvents();
}

// Función de inicialización
function initializeCustomEvents() {
    const button = document.getElementById('mi-boton');
    if (button) {
        button.addEventListener('click', miFuncion);
    }
}
```

## 📁 UBICACIÓN EN EL CÓDIGO

### Archivo: `templates/index.html`
- **Líneas 1418-1489**: Clase `TabRegistry`
- **Líneas 1494-1517**: `TabTemplates` (templates básicos)
- **Líneas 1524-1749**: `ExistingTabTemplates` (templates específicos)
- **Líneas 1751-1778**: Funciones de utilidad básicas
- **Líneas 1780-1799**: Funciones para pestañas existentes
- **Líneas 1801-1814**: Funciones de inicialización de eventos
- **Líneas 650-679**: Creación automática de pestañas principales
- **Líneas 930-962**: Función `displayResults` con layout de múltiples columnas
- **Líneas 1185-1214**: Función `openImageZoom` con soporte para captions

## ⚠️ CONSIDERACIONES IMPORTANTES

1. **IDs únicos**: Cada pestaña debe tener un ID único
2. **Event Listeners**: Se re-inicializan automáticamente al activar la pestaña
3. **Templates**: Pueden ser strings o funciones que retornen HTML
4. **Bootstrap**: Las pestañas usan clases de Bootstrap para funcionamiento
5. **Compatibilidad**: Funciona con el sistema de modo oscuro/claro existente

## 🚀 GUÍA PASO A PASO: CREAR NUEVA PESTAÑA

### ⚠️ IMPORTANTE: Sigue estos pasos EXACTAMENTE para mantener consistencia

### Paso 1: Decidir el tipo de pestaña
```javascript
// Para pestañas simples (solo contenido estático)
createBasicTab('id-unico', 'Título', 'Contenido HTML', 'fas fa-icono');

// Para pestañas con funcionalidad (botones, uploads, etc.)
createTab({
    id: 'id-unico',
    title: 'Título',
    icon: 'fas fa-icono',
    template: () => `HTML con estilos correctos`,
    onActivate: () => initializeTabEvents()
});
```

### Paso 2: Usar SIEMPRE los estilos correctos
```html
<!-- ✅ CORRECTO: Botones principales -->
<button class="btn btn-outline-primary">Acción</button>

<!-- ✅ CORRECTO: Botones de descarga -->
<button class="btn btn-success">Descargar</button>

<!-- ✅ CORRECTO: Botones de upload -->
<button class="btn btn-custom">Seleccionar Archivos</button>

<!-- ❌ INCORRECTO: NO usar estos estilos -->
<button class="btn btn-outline-secondary">❌ No usar</button>
<button class="btn btn-warning">❌ Solo para alertas</button>
```

### Paso 3: Estructura de upload estandarizada (OBLIGATORIA)
```html
<div class="upload-area" id="miUploadArea">
    <h5>Arrastra y suelta [tipo de archivo] aquí</h5>
    <p class="mb-3">o</p>
    <button type="button" class="btn btn-custom" id="selectMiBtn">
        Seleccionar [Tipo de Archivo]
    </button>
    <input type="file" id="miFile" accept="[tipos]" style="display: none;">
    <div id="miFileList" class="mt-3"></div>
</div>
```

### Paso 4: Función de inicialización (OBLIGATORIA)
```javascript
function initializeMiTabEvents() {
    // Event listeners para upload
    const uploadArea = document.getElementById('miUploadArea');
    const fileInput = document.getElementById('miFile');
    const selectBtn = document.getElementById('selectMiBtn');
    
    if (uploadArea && fileInput && selectBtn) {
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleMiFiles(e.dataTransfer.files);
        });
        
        // Botón de selección
        selectBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileInput.click();
        });
        
        // Cambio de archivo
        fileInput.addEventListener('change', (e) => {
            handleMiFiles(e.target.files);
        });
    }
    
    // Otros event listeners específicos de la pestaña
    const miBoton = document.getElementById('miBoton');
    if (miBoton) {
        miBoton.addEventListener('click', () => {
            // Lógica del botón
        });
    }
}

// Función para manejar archivos (OBLIGATORIA)
function handleMiFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        // Procesar archivo
        console.log('Archivo seleccionado:', file.name);
        
        // Mostrar en la lista
        const fileList = document.getElementById('miFileList');
        if (fileList) {
            fileList.innerHTML = `<div class="alert alert-success">✅ ${file.name}</div>`;
        }
    }
}
```

### Paso 5: Verificar que funciona
```javascript
// En la consola del navegador, verificar:
console.log('Pestaña creada:', window.tabRegistry.getTab('mi-pestaña'));
```

## ✅ CHECKLIST: ANTES DE DAR POR TERMINADA UNA NUEVA PESTAÑA

### Estilos y Consistencia:
- [ ] **Botones principales**: Usan `btn-outline-primary` (azul)
- [ ] **Botones de descarga**: Usan `btn-success` (verde)
- [ ] **Botones de upload**: Usan `btn-custom` (gradiente morado)
- [ ] **NO hay botones**: `btn-outline-secondary` o `btn-warning` (excepto alertas)
- [ ] **Upload area**: Sigue la estructura estándar con `upload-area`
- [ ] **IDs únicos**: Todos los elementos tienen IDs únicos y descriptivos

### Funcionalidad:
- [ ] **Event listeners**: Se inicializan en `onActivate()`
- [ ] **Drag & drop**: Funciona correctamente
- [ ] **Botón de selección**: Abre el diálogo de archivos
- [ ] **Feedback visual**: Se muestra cuando se selecciona un archivo
- [ ] **Console logs**: Para debugging (opcional pero recomendado)

### Estructura:
- [ ] **Template**: Usa función que retorna HTML
- [ ] **Bootstrap**: Usa clases de Bootstrap para layout
- [ ] **Responsive**: Funciona en móvil, tablet y desktop
- [ ] **Modo oscuro**: Compatible con el sistema de temas

### Testing:
- [ ] **Pestaña se crea**: Aparece en la lista de pestañas
- [ ] **Se activa**: Al hacer clic funciona correctamente
- [ ] **Upload funciona**: Tanto drag & drop como selección manual
- [ ] **Botones funcionan**: Todos los botones responden
- [ ] **No hay errores**: En la consola del navegador

## ⚠️ ERRORES COMUNES Y CÓMO EVITARLOS

### 1. Event Listeners No Funcionan
```javascript
// ❌ INCORRECTO: Event listeners en scope global
document.getElementById('miBoton').addEventListener('click', miFuncion);

// ✅ CORRECTO: Event listeners en función de inicialización
function initializeMiTabEvents() {
    const boton = document.getElementById('miBoton');
    if (boton) {
        boton.addEventListener('click', miFuncion);
    }
}
```

### 2. Drag & Drop No Asigna Archivos
```javascript
// ❌ INCORRECTO: Solo actualizar UI
function handleFiles(files) {
    console.log('Archivo:', files[0].name);
    // Falta asignar al input
}

// ✅ CORRECTO: Asignar archivo al input
function handleFiles(files) {
    if (files.length > 0) {
        const fileInput = document.getElementById('miFile');
        if (fileInput) {
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(files[0]);
            fileInput.files = dataTransfer.files;
        }
    }
}
```

### 3. IDs Duplicados
```javascript
// ❌ INCORRECTO: IDs genéricos
<button id="btn">Botón</button>
<input id="file" type="file">

// ✅ CORRECTO: IDs únicos y descriptivos
<button id="miTabBtn">Botón</button>
<input id="miTabFile" type="file">
```

### 4. Estilos Incorrectos
```html
<!-- ❌ INCORRECTO: Estilos inconsistentes -->
<button class="btn btn-outline-secondary">Acción</button>
<button class="btn btn-warning">Limpiar</button>

<!-- ✅ CORRECTO: Estilos consistentes -->
<button class="btn btn-outline-primary">Acción</button>
<button class="btn btn-outline-primary">Limpiar</button>
```

### 5. Upload Area Mal Estructurada
```html
<!-- ❌ INCORRECTO: Estructura diferente -->
<div class="drop-zone">
    <input type="file" id="file">
</div>

<!-- ✅ CORRECTO: Estructura estándar -->
<div class="upload-area" id="miUploadArea">
    <h5>Arrastra y suelta archivos aquí</h5>
    <p class="mb-3">o</p>
    <button type="button" class="btn btn-custom" id="selectMiBtn">
        Seleccionar Archivos
    </button>
    <input type="file" id="miFile" style="display: none;">
    <div id="miFileList" class="mt-3"></div>
</div>
```

## 🎨 GUÍA DE ESTILOS Y CONSISTENCIA VISUAL

### 1. Esquema de Colores Unificado
```css
/* Colores principales del sistema */
--primary-color: #0d6efd;        /* Azul Bootstrap - Botones principales */
--success-color: #198754;        /* Verde - Botones de descarga/confirmación */
--warning-color: #ffc107;        /* Amarillo - Solo para alertas importantes */
--secondary-color: #6c757d;      /* Gris - Botones secundarios (descontinuado) */
```

### 2. Estilos de Botones Estándar
```html
<!-- Botones principales de acción -->
<button class="btn btn-outline-primary">Acción Principal</button>

<!-- Botones de descarga/confirmación -->
<button class="btn btn-success">Descargar/Confirmar</button>

<!-- Botones especiales (solo cuando sea necesario) -->
<button class="btn btn-send-to-edit">Enviar a Edición</button>

<!-- Botones de tamaño específico -->
<button class="btn btn-outline-primary btn-lg">Botón Grande</button>
<button class="btn btn-outline-primary btn-sm">Botón Pequeño</button>
```

### 3. Secciones de Upload Estandarizadas
```html
<!-- Estructura estándar para todas las pestañas -->
<div class="upload-area" id="uniqueUploadArea">
    <h5>Arrastra y suelta [tipo de archivo] aquí</h5>
    <p class="mb-3">o</p>
    <button type="button" class="btn btn-custom" id="selectFileBtn">
        Seleccionar [Tipo de Archivo]
    </button>
    <input type="file" id="fileInput" accept="[tipos]" style="display: none;">
    <div id="fileList" class="mt-3"></div>
</div>
```

### 4. Navbar Consistente
```html
<!-- Navbar con fondo azul y texto blanco en ambos modos -->
<nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">
            <h4 class="mb-0">🤖 [Título de la Aplicación]</h4>
        </a>
        <div class="navbar-nav ms-auto">
            <button id="themeToggle" class="btn btn-outline-light btn-sm">
                🌙 Modo Oscuro
            </button>
        </div>
    </div>
</nav>
```

### 5. Botones de Resolución Unificados
```html
<!-- Botones de resolución en todas las pestañas -->
<div class="btn-group mb-4" role="group">
    <button type="button" class="btn btn-outline-primary resolution-btn" 
            data-width="512" data-height="512">512x512</button>
    <button type="button" class="btn btn-outline-primary resolution-btn" 
            data-width="768" data-height="768">768x768</button>
    <button type="button" class="btn btn-outline-primary resolution-btn" 
            data-width="1024" data-height="1024">1024x1024</button>
</div>
```

### 6. Reglas de Consistencia
- **Botones principales**: Siempre `btn-outline-primary` (azul)
- **Botones de descarga**: Siempre `btn-success` (verde)
- **Botones de resolución**: Siempre `btn-outline-primary` (azul)
- **Botones de upload**: Siempre `btn-custom` (gradiente morado)
- **Navbar**: Siempre fondo azul con texto blanco
- **Secciones de upload**: Siempre estructura `upload-area` estándar

## 🆕 NUEVAS FUNCIONALIDADES IMPLEMENTADAS

### 1. Barra de Progreso Mejorada
```javascript
// La barra de progreso ahora muestra:
// - Progreso numérico: "1/20 (5%)"
// - Texto descriptivo: "Generando captions (1 de 20) - archivo.jpg"
// - Estado del proceso: "Preparando generación...", "Finalizando..."

// Ubicación: Líneas 1609-1616 (HTML) y 710-778 (JavaScript)
```

### 2. Layout de Múltiples Columnas
```javascript
// Los resultados ahora se muestran en:
// - Móvil: 1 columna (col-12)
// - Tablet: 2 columnas (col-sm-6)
// - Desktop: 3 columnas (col-lg-4)
// - Desktop grande: 4 columnas (col-xl-3)

// Estructura de cada tarjeta:
// - Imagen arriba (300px altura)
// - Nombre del archivo como título
// - Caption como texto principal
// - Botón "Regenerar" en la parte inferior

// Ubicación: Líneas 930-962
```

### 3. Vista Ampliada con Caption
```javascript
// La vista ampliada ahora incluye:
// - Imagen con zoom y controles
// - Caption en la esquina inferior derecha
// - Badge azul con fondo semi-transparente
// - Scroll automático para captions largos

// Función actualizada:
openImageZoom(imageSrc, imageInfo, caption)

// Ubicación: Líneas 1185-1214
```

### 4. Sistema de Carga de Modelos Corregido
```javascript
// Problemas resueltos:
// - Orden de inicialización corregido
// - Elementos DOM disponibles antes de cargar modelos
// - Endpoint /api/models funcionando correctamente

// Ubicación: Líneas 683-684 (carga después de crear pestañas)
```

### 5. Endpoints de API Corregidos
```javascript
// Correcciones realizadas:
// - /upload → /api/upload
// - /progress/<id> → /api/progress/<id>
// - Archivos enviados correctamente al endpoint de generación

// Ubicación: Líneas 784, 715 (URLs corregidas)
```

### 6. Drag & Drop Funcional para Archivos JSON
```javascript
// Problema resuelto: Drag & drop no asignaba archivos al input
// Solución implementada:
function handleEditFiles(files) {
    if (files.length > 0) {
        const file = files[0];
        const fileInput = document.getElementById('captionsFile');
        
        // Asignar el archivo al input para que esté disponible
        if (fileInput) {
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
        }
    }
}

// Ubicación: Líneas 2304-2339
```

### 7. Estilos de Botones Unificados
```javascript
// Cambios realizados:
// - Todos los botones btn-outline-secondary → btn-outline-primary
// - Botón "Limpiar captions": btn-warning → btn-outline-primary
// - Botones de resolución: btn-outline-secondary → btn-outline-primary
// - Botones de prompts: btn-outline-secondary → btn-outline-primary

// Resultado: Consistencia visual completa con esquema azul
```

### 8. Secciones de Upload Estandarizadas
```javascript
// Todas las pestañas ahora usan la misma estructura:
// - Pestaña Generar Captions: upload-area (múltiples imágenes)
// - Pestaña Editar Captions: upload-area (archivo JSON)
// - Pestaña Metadatos IA: upload-area (imagen única)

// Estructura estándar implementada en todas las pestañas
// Ubicación: Líneas 1728-1734, 1860-1866, 1942-1948
```

### 9. Layout y Diseño Mejorado
```javascript
// Cambios implementados para consistencia visual:

// 1. Pestaña "Editar Captions" - Layout consistente:
// - Imagen arriba (300px altura)
// - Nombre del archivo como título
// - Textarea para editar caption
// - Botones "Copiar" y "Regenerar" en la parte inferior
// - Layout responsivo: 1-4 columnas según el tamaño de pantalla

// 2. Pestaña "Metadatos IA" - Sección centrada:
// - Sección de upload centrada horizontalmente
// - Mismo tamaño que la pestaña de generación (col-md-8)
// - Resultados se muestran debajo para aprovechar el espacio

// 3. Centrado horizontal:
// - Pestaña "Editar Captions": justify-content-center
// - Pestaña "Metadatos IA": justify-content-center
// - Secciones de carga de archivos centradas para mejor apariencia

// Ubicación: Líneas 1958-2044 (editTab), 2046-2086 (metadataTab)
// Función displayEditResults: Líneas 1195-1256
```

## 🔍 DEBUGGING

### Verificar que las pestañas se crean:
```javascript
console.log('Pestañas registradas:', window.tabRegistry.tabs);
```

### Verificar que el DOM se genera:
```javascript
console.log('Contenedor de pestañas:', document.querySelector('#mainTabsContent'));
```

### Verificar event listeners:
```javascript
// En la consola del navegador
window.tabRegistry.getTab('mi-pestaña');
```

### Verificar carga de modelos:
```javascript
// Debería aparecer en consola:
// "Modelos cargados exitosamente: 3"
```

### Verificar barra de progreso:
```javascript
// Durante la generación, verificar:
// - Elemento progressContainer visible
// - Texto de progreso actualizándose
// - Porcentaje en la barra
```

## 🎯 COMPATIBILIDAD CON NUEVAS PESTAÑAS

### ✅ Todos los cambios son compatibles con el sistema de templates:
- **Barra de progreso**: Se puede usar en cualquier pestaña nueva
- **Layout de columnas**: Aplicable a cualquier contenido de pestaña
- **Vista ampliada**: Funciona con cualquier imagen en cualquier pestaña
- **Sistema de eventos**: Completamente funcional para nuevas pestañas
- **Carga de modelos**: No interfiere con nuevas funcionalidades

### 🔧 Para agregar una nueva pestaña con las mejoras:
```javascript
createTab({
    id: 'nueva-funcionalidad',
    title: 'Nueva Funcionalidad',
    template: () => `
        <!-- Sección de upload estandarizada -->
        <div class="upload-area" id="nuevaUploadArea">
            <h5>Arrastra y suelta tus archivos aquí</h5>
            <p class="mb-3">o</p>
            <button type="button" class="btn btn-custom" id="selectNuevaBtn">
                Seleccionar Archivos
            </button>
            <input type="file" id="nuevaFile" accept="*/*" style="display: none;">
            <div id="nuevaFileList" class="mt-3"></div>
        </div>
        
        <!-- Botones con estilos consistentes -->
        <div class="row mb-4">
            <div class="col-12 text-center">
                <button class="btn btn-outline-primary btn-lg me-3">
                    💾 Acción Principal
                </button>
                <button class="btn btn-outline-primary btn-lg">
                    ✏️ Otra Acción
                </button>
            </div>
        </div>
        
        <!-- Botones de resolución unificados -->
        <div class="btn-group mb-4" role="group">
            <button type="button" class="btn btn-outline-primary resolution-btn" 
                    data-width="512" data-height="512">512x512</button>
            <button type="button" class="btn btn-outline-primary resolution-btn" 
                    data-width="768" data-height="768">768x768</button>
            <button type="button" class="btn btn-outline-primary resolution-btn" 
                    data-width="1024" data-height="1024">1024x1024</button>
        </div>
        
        <!-- Layout de múltiples columnas -->
        <div class="row g-3">
            <div class="col-12 col-sm-6 col-lg-4">
                <div class="card h-100">
                    <div class="card-img-top-container" style="height: 300px;">
                        <img src="imagen.jpg" class="card-img-top" 
                             onclick="openImageZoom('imagen.jpg', 'archivo.jpg', 'caption')">
                    </div>
                    <div class="card-body">
                        <h6 class="card-title">Título</h6>
                        <p class="card-text">Contenido</p>
                        <button class="btn btn-outline-primary btn-sm">
                            🔄 Acción
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Barra de progreso mejorada -->
        <div id="progressContainer" class="mb-3" style="display: none;">
            <div class="progress mb-2">
                <div class="progress-bar" role="progressbar">0%</div>
            </div>
            <div id="progressText" class="text-center text-muted small">
                Preparando...
            </div>
        </div>
    `,
    onActivate: () => {
        // Inicializar eventos específicos
        initializeNewFunctionalityEvents();
    }
});

// Función de inicialización con estilos consistentes
function initializeNewFunctionalityEvents() {
    // Event listeners para upload estandarizado
    const uploadArea = document.getElementById('nuevaUploadArea');
    const fileInput = document.getElementById('nuevaFile');
    const selectBtn = document.getElementById('selectNuevaBtn');
    
    if (uploadArea && fileInput && selectBtn) {
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            handleNuevaFiles(e.dataTransfer.files);
        });
        
        // Botón de selección
        selectBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fileInput.click();
        });
        
        // Cambio de archivo
        fileInput.addEventListener('change', (e) => {
            handleNuevaFiles(e.target.files);
        });
    }
    
    // Botones de resolución
    document.querySelectorAll('.resolution-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.resolution-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}
```

---

**Última actualización**: Enero 2025  
**Versión del sistema**: 2.1  
**Compatibilidad**: Bootstrap 5, Font Awesome 6  
**Estado**: Sistema completamente funcional, optimizado y con estilos unificados

## 📋 RESUMEN DE CAMBIOS EN VERSIÓN 2.1

### ✅ Estilos y Consistencia Visual:
- **Botones unificados**: Todos los botones principales usan `btn-outline-primary` (azul)
- **Navbar consistente**: Fondo azul con texto blanco en ambos modos
- **Secciones de upload estandarizadas**: Misma estructura en todas las pestañas
- **Botones de resolución unificados**: Estilo azul consistente
- **Drag & drop funcional**: Corregido para archivos JSON

### ✅ Funcionalidades Mejoradas:
- **Carga de captions**: Funciona tanto con drag & drop como con selección manual
- **Botón "Limpiar captions"**: Cambiado de amarillo a azul para consistencia
- **Event listeners**: Inicialización correcta en todas las pestañas
- **Feedback visual**: Logs de debugging para mejor mantenimiento

### ✅ Guía de Estilos:
- **Esquema de colores documentado**
- **Reglas de consistencia establecidas**
- **Templates estandarizados para nuevas pestañas**
- **Ejemplos completos de implementación**

### ✅ Layout y Diseño Mejorado:
- **Pestaña "Editar Captions"**: Layout consistente con "Generar Captions" (imagen arriba, contenido abajo)
- **Pestaña "Metadatos IA"**: Sección de upload centrada y del mismo tamaño
- **Centrado horizontal**: Secciones de carga de archivos centradas en pestañas de edición y metadatos
- **Layout responsivo**: Imágenes se cargan abajo para aprovechar mejor el espacio de edición
- **Consistencia visual**: Todas las pestañas siguen el mismo patrón de diseño

