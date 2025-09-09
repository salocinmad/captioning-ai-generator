import os
import sys
import json
import threading
import time
from flask import Flask, request, jsonify, render_template, send_file
from PIL import Image
from PIL.ExifTags import TAGS
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import onnxruntime as ort
import numpy as np
import base64
from io import BytesIO
import uuid
import zipfile
import tempfile
import time
from flask import send_file
import requests
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear config.json automáticamente si no existe
import shutil
if not os.path.exists('config.json'):
    if os.path.exists('config.example.json'):
        shutil.copy('config.example.json', 'config.json')
        print("✅ Archivo config.json creado desde config.example.json")
        print("⚠️  Recuerda editar config.json con tu API key antes de usar la aplicación")
    else:
        print("❌ Error: No se encontró config.example.json")
else:
    print("✅ Archivo config.json encontrado")

# Función para cargar configuración desde config.json
def load_config():
    """Cargar configuración desde config.json"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("✅ Configuración cargada desde config.json")
        return config
    except FileNotFoundError:
        print("⚠️ Archivo config.json no encontrado, usando configuración por defecto")
        return {
            "api_keys": {"openrouter": ""},
            "settings": {"remote_model_max_image_size": 384, "image_quality": 85, "download_image_quality": 95},
            "server": {"port": 5000, "host": "localhost", "debug_mode": True},
            "limits": {"max_files": 100, "max_file_size_mb": 200},
            "endpoints": {"openrouter_url": "https://openrouter.ai/api/v1/chat/completions"}
        }
    except Exception as e:
        print(f"⚠️ Error cargando config.json: {e}, usando configuración por defecto")
        return {
            "api_keys": {"openrouter": ""},
            "settings": {"remote_model_max_image_size": 384, "image_quality": 85, "download_image_quality": 95},
            "server": {"port": 5000, "host": "localhost", "debug_mode": True},
            "limits": {"max_files": 100, "max_file_size_mb": 200},
            "endpoints": {"openrouter_url": "https://openrouter.ai/api/v1/chat/completions"}
        }

# Cargar configuración
CONFIG = load_config()

# Configurar API key de OpenRouter
if CONFIG["api_keys"]["openrouter"]:
    os.environ['OPENROUTER_API_KEY'] = CONFIG["api_keys"]["openrouter"]
    print("✅ API key de OpenRouter configurada desde config.json")
else:
    print("⚠️ No se encontró API key de OpenRouter en config.json")

# Verificar si está en modo debug desde configuración
DEBUG_MODE = CONFIG.get("server", {}).get("debug_mode", False)

def resize_image_maintain_aspect(image, max_size=None):
    """Redimensionar imagen manteniendo aspect ratio"""
    # Usar configuración si no se especifica max_size
    if max_size is None:
        max_size = CONFIG["settings"]["remote_model_max_image_size"]
        if DEBUG_MODE:
            print(f"🔧 Usando MAX_IMAGE_SIZE desde config.json: {max_size}")
    
    width, height = image.size
    
    # Calcular el factor de escala
    if width > height:
        new_width = max_size
        new_height = int((height * max_size) / width)
    else:
        new_height = max_size
        new_width = int((width * max_size) / height)
    
    # Redimensionar
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    return resized_image

def image_to_base64(image):
    """Convertir imagen PIL a base64"""
    buffer = BytesIO()
    image.save(buffer, format='JPEG', quality=CONFIG["settings"]["image_quality"])
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def setup_cuda():
    """Configurar CUDA si está disponible"""
    if torch.cuda.is_available():
        # Verificar si CUDA_VISIBLE_DEVICES está configurado
        cuda_visible = os.environ.get('CUDA_VISIBLE_DEVICES', '')
        
        if cuda_visible:
            print(f"🔧 CUDA_VISIBLE_DEVICES configurado: {cuda_visible}")
            # Si está configurado, usar la GPU 0 visible
            device = torch.device('cuda:0')
        else:
            # Si no está configurado, usar la GPU 0 del sistema
            device = torch.device('cuda:0')
        
        print(f"🔧 CUDA disponible: {torch.cuda.get_device_name(0)}")
        print(f"💾 VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
        print(f"🎯 Usando dispositivo: {device}")
    else:
        device = torch.device('cpu')
        print("🔧 CUDA no disponible, usando CPU")
    return device

# Configurar dispositivo
device = setup_cuda()

# Configuración de Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = CONFIG["limits"]["max_file_size_mb"] * 1024 * 1024  # Límite por imagen

# Crear directorios necesarios
os.makedirs('uploads', exist_ok=True)
os.makedirs('static/captions', exist_ok=True)

# Inicializar modelos globalmente
models = {}
processors = {}
# Variables globales para modelos (WD14 eliminados)

# Variables para gestión dinámica de modelos
current_loaded_model = None
model_loading_status = {}

# Función load_wd14_tags eliminada (WD14 removido)

# Función load_single_wd14_model eliminada (WD14 removido)

# Función load_wd14_models eliminada (WD14 removido)

def initialize_models():
    """Inicializar configuración de modelos sin cargarlos"""
    global model_loading_status
    
    # Etiquetas WD14 eliminadas
    
    # Inicializar estado de modelos (sin cargar)
    model_loading_status = {
        'blip': {'loaded': False, 'available': True},
        'blip2': {'loaded': False, 'available': True},
        'llama-vision': {'loaded': False, 'available': True}
    }
    
    print("🔧 Sistema de carga dinámica de modelos inicializado")
    print("📋 Modelos disponibles (se cargarán bajo demanda):")
    for model_name, status in model_loading_status.items():
        print(f"  - {model_name}: {'✅ Disponible' if status['available'] else '❌ No disponible'}")
    
    print("💡 Los modelos se cargarán solo cuando los selecciones y se descargarán al finalizar")

# Variables globales para el progreso
progress_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Servir archivos subidos"""
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

@app.route('/api/models', methods=['GET'])
def get_models():
    """Obtener lista de modelos disponibles"""
    try:
        models_list = [
            {'id': 'blip', 'name': 'BLIP', 'description': 'Modelo preciso para captioning detallado - Por defecto'},
            {'id': 'blip2', 'name': 'BLIP-2', 'description': 'Modelo optimizado para Stable Diffusion 1.5'},
            {'id': 'llama-vision', 'name': 'Llama 3.2 Vision', 'description': 'API remota con prompts personalizados'}
        ]
        
        # Modelos WD14 eliminados
        
        # Agregar información de estado de carga
        for model in models_list:
            model_id = model['id']
            if model_id in model_loading_status:
                model['loaded'] = model_loading_status[model_id]['loaded']
                model['available'] = model_loading_status[model_id]['available']
            else:
                model['loaded'] = False
                model['available'] = True
        
        return jsonify({
            'models': models_list,
            'current_loaded': current_loaded_model,
            'loading_system': 'dynamic'
        })
        
    except Exception as e:
        print(f"❌ Error en endpoint /api/models: {e}")
        return jsonify({'error': str(e)}), 500

# Endpoint /api/wd14/info eliminado (WD14 removido)

@app.route('/api/models/status', methods=['GET'])
def get_models_status():
    """Obtener estado detallado de todos los modelos"""
    try:
        status = {
            'current_loaded': current_loaded_model,
            'loading_system': 'dynamic',
            'device': str(device),
            'cuda_available': torch.cuda.is_available(),
            'models': {}
        }
        
        # Estado de modelos principales
        main_models = ['blip', 'blip2', 'llama-vision']
        for model_name in main_models:
            if model_name == 'llama-vision':
                # Llama Vision es siempre "disponible" ya que usa API remota
                status['models'][model_name] = {
                    'loaded': False,  # No se carga en memoria local
                    'available': True,  # Siempre disponible via API
                    'in_memory': False
                }
            else:
                status['models'][model_name] = {
                    'loaded': model_name in models and models[model_name] is not None,
                    'available': model_loading_status.get(model_name, {}).get('available', True),
                    'in_memory': model_name in models
                }
        
        # Estado de modelos WD14 eliminado
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Subir archivos para procesamiento"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No se encontraron archivos'}), 400
        
        files = request.files.getlist('files')
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No se seleccionaron archivos'}), 400
        
        # Verificar límites
        if len(files) > CONFIG["limits"]["max_files"]:
            return jsonify({'error': f'Máximo {CONFIG["limits"]["max_files"]} archivos permitidos'}), 400
        
        # Verificar tamaño total
        total_size = 0
        for file in files:
            file.seek(0, 2)  # Ir al final del archivo
            file_size = file.tell()
            file.seek(0)  # Volver al inicio
            total_size += file_size
        
        max_total_size = CONFIG["limits"]["max_files"] * CONFIG["limits"]["max_file_size_mb"] * 1024 * 1024
        if total_size > max_total_size:
            return jsonify({'error': f'Tamaño total excede {CONFIG["limits"]["max_files"] * CONFIG["limits"]["max_file_size_mb"]}MB'}), 413
        
        # Procesar archivos
        uploaded_files = []
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                uploaded_files.append(filename)
        
        return jsonify({
            'message': f'{len(uploaded_files)} archivos subidos exitosamente',
            'files': uploaded_files
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_captions():
    """Generar captions para las imágenes"""
    try:
        data = request.get_json()
        model_name = data.get('model', 'blip')
        files = data.get('files', [])
        keyword = data.get('keyword', '')
        min_words = data.get('min_words', 0)
        consistency_mode = data.get('consistency_mode', 'auto')
        custom_prompt = data.get('custom_prompt', '')
        
        if not files:
            return jsonify({'error': 'No se especificaron archivos'}), 400
        
        # Iniciar procesamiento asíncrono
        task_id = str(uuid.uuid4())
        progress_data[task_id] = {
            'status': 'processing',
            'progress': 0,
            'total': len(files),
            'current': 0,
            'results': []
        }
        
        # Procesar en hilo separado
        thread = threading.Thread(target=process_images_async, args=(files, model_name, task_id, keyword, min_words, consistency_mode, custom_prompt))
        thread.start()
        
        return jsonify({'task_id': task_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/regenerate_caption', methods=['POST'])
def regenerate_single_caption():
    """Regenerar caption para una imagen individual"""
    try:
        data = request.get_json()
        model_name = data.get('model', 'blip')
        keyword = data.get('keyword', '')
        min_words = int(data.get('min_words', 0))
        consistency_mode = data.get('consistency_mode', 'auto')
        custom_prompt = data.get('custom_prompt', '')
        filename = data.get('filename', '')
        
        if not filename:
            return jsonify({'error': 'No se especificó imagen para regenerar'}), 400
        
        # Verificar que la imagen existe
        image_path = os.path.join('uploads', filename)
        if not os.path.exists(image_path):
            return jsonify({'error': f'Imagen no encontrada: {filename}'}), 404
        
        print(f"🔄 Regenerando caption para {filename} con modelo {model_name}")
        print(f"📋 Parámetros recibidos: consistency_mode='{consistency_mode}', keyword='{keyword}', min_words={min_words}")
        print(f"🎲 Usando parámetros de aleatoriedad para generar caption diferente")
        
        # Generar nuevo caption
        new_caption = generate_caption(
            image_path=image_path,
            model_name=model_name,
            keyword=keyword,
            min_words=min_words,
            consistency_mode=consistency_mode,
            custom_prompt=custom_prompt
        )
        
        return jsonify({
            'success': True,
            'caption': new_caption,
            'model_used': model_name
        })
        
    except Exception as e:
        print(f"Error en regenerate_single_caption: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_metadata', methods=['POST'])
def analyze_metadata():
    """Analizar metadatos de imagen generada por IA"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'error': 'No se proporcionó imagen'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No se seleccionó archivo'}), 400
        
        # Abrir imagen con PIL
        image = Image.open(file.stream)
        
        # Extraer metadatos EXIF usando métodos modernos
        exif_data = {}
        
        # Método 1: Usar getexif() (método moderno)
        try:
            exif = image.getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_data[tag] = value
                print(f"EXIF encontrado con getexif(): {len(exif_data)} campos")
        except Exception as e:
            print(f"Error con getexif(): {e}")
        
        # Método 2: Usar _getexif() (método legacy)
        if not exif_data and hasattr(image, '_getexif'):
            try:
                exif = image._getexif()
                if exif is not None:
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_data[tag] = value
                    print(f"EXIF encontrado con _getexif(): {len(exif_data)} campos")
            except Exception as e:
                print(f"Error con _getexif(): {e}")
        
        # Método 3: Buscar en info del archivo
        if hasattr(image, 'info') and image.info:
            print(f"Info de imagen encontrada: {list(image.info.keys())}")
            for key, value in image.info.items():
                exif_data[f"Info_{key}"] = value
        
        print(f"Total metadatos encontrados: {len(exif_data)}")
        if exif_data:
            print(f"Campos encontrados: {list(exif_data.keys())}")
        
        # Buscar metadatos específicos de IA
        result = {
            'success': True,
            'model': None,
            'prompt': None,
            'parameters': None,
            'software': None,
            'negative_prompt': None
        }
        
        # Buscar en diferentes campos de metadatos
        metadata_fields = [
            'ImageDescription', 'UserComment', 'Software', 'Make', 'Model',
            'Artist', 'Copyright', 'ExifImageWidth', 'ExifImageHeight'
        ]
        
        # Buscar en campos Info_ (ComfyUI)
        for key, value in exif_data.items():
            if key.startswith('Info_'):
                value_str = str(value)
                
                # Buscar prompt en Info_prompt
                if key == 'Info_prompt' and not result['prompt']:
                    try:
                        import json
                        prompt_data = json.loads(value_str)
                        if '3' in prompt_data and 'inputs' in prompt_data['3'] and 'text' in prompt_data['3']['inputs']:
                            result['prompt'] = prompt_data['3']['inputs']['text']
                        if '4' in prompt_data and 'inputs' in prompt_data['4'] and 'text' in prompt_data['4']['inputs'] and prompt_data['4']['inputs']['text']:
                            result['negative_prompt'] = prompt_data['4']['inputs']['text']
                    except Exception as e:
                        print(f"Error parsing prompt: {e}")
                        pass
                
                # Buscar modelo, tamaño y LoRAs en Info_prompt (donde están realmente los datos)
                if key == 'Info_prompt':
                    try:
                        import json
                        prompt_data = json.loads(value_str)
                        
                        # Buscar modelo (campo 66)
                        if not result['model'] and '66' in prompt_data and 'inputs' in prompt_data['66'] and 'unet_name' in prompt_data['66']['inputs']:
                            result['model'] = prompt_data['66']['inputs']['unet_name']
                        
                        # Buscar tamaño (campos 54 y 55)
                        if not result['parameters']:
                            size_info = []
                            
                            # Buscar altura (campo 54)
                            if '54' in prompt_data and 'inputs' in prompt_data['54'] and 'value' in prompt_data['54']['inputs']:
                                height = prompt_data['54']['inputs']['value']
                                size_info.append(f"Altura: {height}")
                            
                            # Buscar ancho (campo 55)
                            if '55' in prompt_data and 'inputs' in prompt_data['55'] and 'value' in prompt_data['55']['inputs']:
                                width = prompt_data['55']['inputs']['value']
                                size_info.append(f"Ancho: {width}")
                            
                            if size_info:
                                result['parameters'] = " | ".join(size_info)
                        
                        # Buscar LoRAs (campo 73)
                        if '73' in prompt_data and 'inputs' in prompt_data['73']:
                            loras = []
                            inputs = prompt_data['73']['inputs']
                            
                            # Buscar todos los lora_X activos
                            for lora_key, lora_value in inputs.items():
                                if lora_key.startswith('lora_') and isinstance(lora_value, dict) and lora_value.get('on', False):
                                    lora_name = lora_value.get('lora', '')
                                    strength = lora_value.get('strength', 1.0)
                                    if lora_name:
                                        loras.append(f"{lora_name} (fuerza: {strength})")
                            
                            if loras:
                                result['lora_models'] = loras
                                
                    except Exception as e:
                        print(f"Error parsing prompt data: {e}")
                        pass
                
                # También buscar en Info_workflow por si acaso
                if key == 'Info_workflow':
                    try:
                        import json
                        workflow_data = json.loads(value_str)
                        
                        # Buscar modelo (campo 66)
                        if not result['model'] and '66' in workflow_data and 'inputs' in workflow_data['66'] and 'unet_name' in workflow_data['66']['inputs']:
                            result['model'] = workflow_data['66']['inputs']['unet_name']
                        
                        # Buscar tamaño (campos 54 y 55)
                        if not result['parameters']:
                            size_info = []
                            
                            # Buscar altura (campo 54)
                            if '54' in workflow_data and 'inputs' in workflow_data['54'] and 'value' in workflow_data['54']['inputs']:
                                height = workflow_data['54']['inputs']['value']
                                size_info.append(f"Altura: {height}")
                            
                            # Buscar ancho (campo 55)
                            if '55' in workflow_data and 'inputs' in workflow_data['55'] and 'value' in workflow_data['55']['inputs']:
                                width = workflow_data['55']['inputs']['value']
                                size_info.append(f"Ancho: {width}")
                            
                            if size_info:
                                result['parameters'] = " | ".join(size_info)
                        
                        # Buscar LoRAs (campo 73)
                        if '73' in workflow_data and 'inputs' in workflow_data['73']:
                            loras = []
                            inputs = workflow_data['73']['inputs']
                            
                            # Buscar todos los lora_X (activos e inactivos)
                            for lora_key, lora_value in inputs.items():
                                if lora_key.startswith('lora_') and isinstance(lora_value, dict):
                                    lora_name = lora_value.get('lora', '')
                                    strength = lora_value.get('strength', 1.0)
                                    is_active = lora_value.get('on', False)
                                    if lora_name:
                                        status = "✅ Activo" if is_active else "❌ Inactivo"
                                        loras.append(f"{lora_name} (fuerza: {strength}) - {status}")
                            
                            if loras:
                                result['lora_models'] = loras
                                
                    except Exception as e:
                        print(f"Error parsing workflow data: {e}")
                        pass
        
        # Buscar en campos tradicionales
        for field in metadata_fields:
            if field in exif_data:
                value = str(exif_data[field])
                
                # Buscar modelo de IA
                if not result['model']:
                    if any(keyword in value.lower() for keyword in ['stable diffusion', 'midjourney', 'dall-e', 'gpt', 'openai', 'runway', 'leonardo', 'comfyui', 'automatic1111']):
                        result['model'] = value
                
                # Buscar prompt
                if not result['prompt']:
                    if len(value) > 20 and any(keyword in value.lower() for keyword in ['prompt', 'description', 'generate', 'create']):
                        result['prompt'] = value
                
                # Buscar parámetros
                if not result['parameters']:
                    if any(keyword in value.lower() for keyword in ['steps', 'cfg', 'sampler', 'seed', 'size']):
                        result['parameters'] = value
                
                # Buscar software
                if not result['software'] and field == 'Software':
                    result['software'] = value
        
        # Buscar en UserComment que suele contener metadatos de IA
        if 'UserComment' in exif_data:
            user_comment = str(exif_data['UserComment'])
            if not result['prompt'] and len(user_comment) > 10:
                result['prompt'] = user_comment
        
        # Agregar todos los metadatos EXIF para debug
        result['all_metadata'] = exif_data
        
        # Debug: mostrar qué se está devolviendo
        print(f"Resultado final:")
        print(f"  - success: {result['success']}")
        print(f"  - model: {result['model']}")
        print(f"  - prompt: {result['prompt']}")
        print(f"  - parameters: {result['parameters']}")
        print(f"  - software: {result['software']}")
        print(f"  - lora_models: {result.get('lora_models', 'Ninguno')}")
        print(f"  - all_metadata keys: {list(exif_data.keys()) if exif_data else 'Ninguno'}")
        
        # Debug específico para Info_prompt
        if 'Info_prompt' in exif_data:
            try:
                import json
                prompt_data = json.loads(str(exif_data['Info_prompt']))
                print(f"  - Info_prompt keys: {list(prompt_data.keys())}")
                if '54' in prompt_data:
                    print(f"  - Campo 54 (altura): {prompt_data['54']}")
                if '55' in prompt_data:
                    print(f"  - Campo 55 (ancho): {prompt_data['55']}")
                if '66' in prompt_data:
                    print(f"  - Campo 66 (modelo): {prompt_data['66']}")
                if '73' in prompt_data:
                    print(f"  - Campo 73 (LoRAs): {prompt_data['73']}")
            except Exception as e:
                print(f"  - Error parsing Info_prompt: {e}")
        
        # Debug específico para Info_workflow
        if 'Info_workflow' in exif_data:
            try:
                import json
                workflow_data = json.loads(str(exif_data['Info_workflow']))
                print(f"  - Info_workflow keys: {list(workflow_data.keys())}")
                if '54' in workflow_data:
                    print(f"  - Campo 54 (altura): {workflow_data['54']}")
                if '55' in workflow_data:
                    print(f"  - Campo 55 (ancho): {workflow_data['55']}")
                if '66' in workflow_data:
                    print(f"  - Campo 66 (modelo): {workflow_data['66']}")
                if '73' in workflow_data:
                    print(f"  - Campo 73 (LoRAs): {workflow_data['73']}")
            except Exception as e:
                print(f"  - Error parsing Info_workflow: {e}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error analizando metadatos: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/progress/<task_id>', methods=['GET'])
def get_progress(task_id):
    """Obtener progreso del procesamiento"""
    if task_id not in progress_data:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    return jsonify(progress_data[task_id])

def load_model_on_demand(model_name, task_id=None):
    """Cargar modelo específico bajo demanda"""
    global current_loaded_model, models, processors, model_loading_status, progress_data
    
    # Si el modelo ya está cargado, no hacer nada
    if current_loaded_model == model_name and model_loading_status.get(model_name, {}).get('loaded', False):
        return True
    
    # Descargar modelo anterior si es diferente
    if current_loaded_model and current_loaded_model != model_name:
        unload_model(current_loaded_model)
    
    print(f"🔄 Cargando modelo {model_name}...")
    
    # Actualizar progreso si se proporciona task_id
    if task_id and task_id in progress_data:
        progress_data[task_id]['status'] = 'downloading_model'
        progress_data[task_id]['message'] = f'Descargando modelo {model_name}...'
        progress_data[task_id]['progress'] = 10
    
    try:
        if model_name == 'blip':
            models['blip'] = BlipForConditionalGeneration.from_pretrained(
                "Salesforce/blip-image-captioning-base", 
                use_safetensors=False,
                torch_dtype=torch.float16
            ).to(device)
            processors['blip'] = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
            
        elif model_name == 'blip2':
            models['blip2'] = Blip2ForConditionalGeneration.from_pretrained(
                "Salesforce/blip2-opt-2.7b", 
                torch_dtype=torch.float16,
                use_safetensors=False
            ).to(device)
            processors['blip2'] = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b", use_fast=True)
            
        
        # Modelos WD14 eliminados
        
        # Actualizar estado
        model_loading_status[model_name]['loaded'] = True
        current_loaded_model = model_name
        
        # Actualizar progreso si se proporciona task_id
        if task_id and task_id in progress_data:
            progress_data[task_id]['status'] = 'model_loaded'
            progress_data[task_id]['message'] = f'Modelo {model_name} cargado exitosamente'
            progress_data[task_id]['progress'] = 20
        
        print(f"✅ Modelo {model_name} cargado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error cargando modelo {model_name}: {e}")
        print(f"❌ Tipo de error: {type(e).__name__}")
        model_loading_status[model_name]['available'] = False
        return False

def unload_model(model_name):
    """Descargar modelo de memoria"""
    global current_loaded_model, models, processors, model_loading_status
    
    if not model_loading_status.get(model_name, {}).get('loaded', False):
        return
    
    print(f"🗑️ Descargando modelo {model_name} de memoria...")
    
    try:
        # Eliminar modelo y procesador de memoria
        if model_name in models:
            del models[model_name]
        if model_name in processors:
            del processors[model_name]
        if f'{model_name}-tokenizer' in processors:
            del processors[f'{model_name}-tokenizer']
        
        # Modelos WD14 eliminados
        
        # Limpiar cache de CUDA si está disponible
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Actualizar estado
        model_loading_status[model_name]['loaded'] = False
        
        if current_loaded_model == model_name:
            current_loaded_model = None
        
        print(f"✅ Modelo {model_name} descargado exitosamente")
        
    except Exception as e:
        print(f"❌ Error descargando modelo {model_name}: {e}")

def generate_caption(image_path, model_name='blip', keyword='', min_words=0, consistency_mode='auto', custom_prompt=''):
    """Generar caption para una imagen"""
    try:
        # Cargar imagen
        image = Image.open(image_path).convert('RGB')
        
        # Cargar modelo bajo demanda
        if not load_model_on_demand(model_name):
            return f"Error: No se pudo cargar el modelo {model_name}"
        
        # Generar caption según el modelo
        # Modelos WD14 eliminados
        if model_name == 'blip' and models.get('blip') is not None:
            caption = generate_caption_blip(image, min_words)
        elif model_name == 'blip2' and models.get('blip2') is not None:
            caption = generate_caption_blip2(image, min_words)
        elif model_name == 'llama-vision':
            # Para Llama Vision, usar prompt personalizado o uno por defecto
            prompt = custom_prompt if custom_prompt else "Describe this image in detail."
            caption = generate_caption_llama_vision(image, prompt)
        else:
            return f"Modelo {model_name} no disponible"
        
        # Aplicar reglas de consistencia para términos de personas
        caption = apply_consistency_rules(caption, consistency_mode)
        
        # Aplicar keyword si se especifica
        if keyword:
            caption = f"{keyword} {caption}"
        
        # Aplicar límites de palabras (solo para BLIP/BLIP2, no para Llama Vision)
        if model_name in ['blip', 'blip2']:
            caption = apply_word_limits(caption, min_words)
            
            # Si apply_word_limits devuelve None, significa que el caption es muy corto
            # y necesitamos regenerarlo con parámetros más largos
            if caption is None:
                # Regenerar con parámetros más largos
                if model_name == 'blip' and models.get('blip') is not None:
                    caption = generate_caption_blip(image, min_words)
                elif model_name == 'blip2' and models.get('blip2') is not None:
                    caption = generate_caption_blip2(image, min_words)
                
                # Aplicar consistencia y keyword al caption regenerado
                caption = apply_consistency_rules(caption, consistency_mode)
                if keyword:
                    caption = f"{keyword} {caption}"
        else:
            # Para Llama Vision y otros modelos, usar el caption tal como viene
            caption = caption.strip()
        
        return caption
            
    except Exception as e:
        return f"Error procesando imagen: {str(e)}"

def apply_consistency_rules(caption, consistency_mode='auto'):
    """Aplicar reglas de consistencia para términos de personas"""
    print(f"🔧 Aplicando consistencia: modo='{consistency_mode}', caption original='{caption}'")
    
    if consistency_mode == 'none':
        print("❌ Modo 'none' - no se aplica consistencia")
        return caption
    
    # Diccionario de términos de personas detectables
    person_terms = {
        # Términos femeninos
        'girl': 'girl',
        'little girl': 'little girl', 
        'young girl': 'young girl',
        'teenage girl': 'teenage girl',
        'teen girl': 'teen girl',
        'female': 'female',
        'lady': 'lady',
        'woman': 'woman',
        
        # Términos masculinos
        'boy': 'boy',
        'little boy': 'little boy',
        'young boy': 'young boy', 
        'teenage boy': 'teenage boy',
        'teen boy': 'teen boy',
        'male': 'male',
        'gentleman': 'gentleman',
        'man': 'man',
        
        # Términos neutros/plurales
        'people': 'people',
        'person': 'person',
        'persons': 'persons',
        'individual': 'individual',
        'child': 'child',
        'children': 'children',
        'kids': 'kids',
        'kid': 'kid'
    }
    
    # Si el modo es específico, usar ese término exacto
    if consistency_mode in ['woman', 'girl', 'little girl', 'young girl', 'man', 'boy', 'person']:
        target_term = consistency_mode
        print(f"✅ Modo específico: usando '{target_term}'")
    else:
        # Modo automático: detectar el término predominante
        target_term = detect_predominant_person_term(caption, person_terms)
        print(f"🤖 Modo automático: detectado '{target_term}'")
    
    # Aplicar normalización
    words = caption.lower().split()
    normalized_words = []
    
    for i, word in enumerate(words):
        # Buscar términos de 1-3 palabras
        found_replacement = False
        
        # Buscar términos de 3 palabras
        if i + 2 < len(words):
            three_word_term = f"{word} {words[i+1]} {words[i+2]}"
            if three_word_term in person_terms:
                normalized_words.append(target_term)
                # Saltar las siguientes 2 palabras
                words[i+1] = ''
                words[i+2] = ''
                found_replacement = True
        
        # Buscar términos de 2 palabras
        if not found_replacement and i + 1 < len(words):
            two_word_term = f"{word} {words[i+1]}"
            if two_word_term in person_terms:
                normalized_words.append(target_term)
                # Saltar la siguiente palabra
                words[i+1] = ''
                found_replacement = True
        
        # Buscar términos de 1 palabra
        if not found_replacement and word in person_terms:
            normalized_words.append(target_term)
            found_replacement = True
        
        # Si no se encontró reemplazo, mantener la palabra original
        if not found_replacement and word != '':
            normalized_words.append(word)
    
    result = ' '.join(normalized_words)
    print(f"📝 Resultado final: '{result}'")
    return result

def detect_predominant_person_term(caption, person_terms):
    """Detectar el término de persona predominante en el caption"""
    words = caption.lower().split()
    
    # Contar términos específicos
    term_counts = {
        'woman': 0,
        'girl': 0,
        'little girl': 0,
        'young girl': 0,
        'man': 0,
        'boy': 0,
        'person': 0
    }
    
    for i, word in enumerate(words):
        # Buscar términos de 3 palabras
        if i + 2 < len(words):
            three_word_term = f"{word} {words[i+1]} {words[i+2]}"
            if three_word_term in person_terms:
                term = person_terms[three_word_term]
                if term in term_counts:
                    term_counts[term] += 1
                # Saltar las siguientes 2 palabras
                words[i+1] = ''
                words[i+2] = ''
                continue
        
        # Buscar términos de 2 palabras
        if i + 1 < len(words):
            two_word_term = f"{word} {words[i+1]}"
            if two_word_term in person_terms:
                term = person_terms[two_word_term]
                if term in term_counts:
                    term_counts[term] += 1
                # Saltar la siguiente palabra
                words[i+1] = ''
                continue
        
        # Buscar términos de 1 palabra
        if word in person_terms:
            term = person_terms[word]
            if term in term_counts:
                term_counts[term] += 1
    
    # Determinar el término predominante
    # Priorizar términos femeninos específicos
    if term_counts['little girl'] > 0:
        return 'little girl'
    elif term_counts['young girl'] > 0:
        return 'young girl'
    elif term_counts['girl'] > 0:
        return 'girl'
    elif term_counts['woman'] > 0:
        return 'woman'
    elif term_counts['boy'] > 0:
        return 'boy'
    elif term_counts['man'] > 0:
        return 'man'
    elif term_counts['person'] > 0:
        return 'person'
    else:
        return 'person'  # Por defecto si no se detecta nada

def apply_word_limits(caption, min_words=0):
    """Aplicar límites de palabras al caption"""
    words = caption.strip().split()
    word_count = len(words)
    
    # Si no se especifican límites, usar valores por defecto
    if min_words == 0:
        min_words = 15  # Mínimo por defecto: 15 palabras
    
    # Si el caption es muy corto, intentar regenerar con parámetros más largos
    if word_count < min_words:
        # Para captions muy cortos, intentar regenerar con max_length más alto
        return None  # Indicar que se necesita regenerar
    
    return caption.strip()

def generate_caption_blip(image, min_words=0):
    """Generar caption con BLIP"""
    try:
        # Si no se especifican límites, usar valores por defecto
        if min_words == 0:
            min_words = 15  # Mínimo por defecto: 15 palabras
        
        # Calcular max_length basado en las palabras mínimas
        max_length = max(min_words * 3, 50)  # Generar suficiente para el mínimo
        
        # Intentar generar caption con diferentes parámetros hasta cumplir el mínimo
        for attempt in range(3):  # Máximo 3 intentos
            # Ajustar parámetros según el intento - SIEMPRE con aleatoriedad
            if attempt == 0:
                # Primer intento: parámetros normales con aleatoriedad
                num_beams = 7
                temperature = 1.1  # Ligeramente aleatorio
            elif attempt == 1:
                # Segundo intento: más creativo para generar más palabras
                num_beams = 5
                temperature = 1.3
                max_length = int(max_length * 1.5)
            else:
                # Tercer intento: muy creativo
                num_beams = 3
                temperature = 1.6
                max_length = int(max_length * 2)
        
        inputs = processors['blip'](image, return_tensors="pt").to(device)
        
        # Calcular min_length en tokens (aproximadamente 1.3 tokens por palabra)
        min_length_tokens = max(int(min_words * 1.3), 10)
        
        out = models['blip'].generate(
            **inputs, 
            max_length=max_length,
            min_length=min_length_tokens,  # min_length en tokens, no palabras
            num_beams=num_beams,
            temperature=temperature,
            do_sample=True,  # SIEMPRE usar muestreo para aleatoriedad
            early_stopping=True,  # Activar para BLIP
            repetition_penalty=1.2,  # Evitar repeticiones
            no_repeat_ngram_size=3   # Evitar n-gramas repetidos
        )
        caption = processors['blip'].decode(out[0], skip_special_tokens=True)
        
        # Limpiar repeticiones excesivas
        caption = clean_blip_caption(caption)
        
        # Verificar si cumple el mínimo de palabras
        word_count = len(caption.strip().split())
        if word_count >= min_words:
            return caption
        
        # Si después de 3 intentos no cumple el mínimo, devolver el mejor resultado
        return caption
        
    except Exception as e:
        return f"Error con BLIP: {str(e)}"

def clean_blip_caption(caption):
    """Limpiar caption de BLIP de repeticiones excesivas"""
    import re
    
    # Eliminar repeticiones excesivas de palabras
    caption = re.sub(r'\b(\w+)\s+\1\s+\1\b', r'\1', caption)  # Palabras repetidas 3+ veces
    caption = re.sub(r'\b(\w+)\s+\1\b', r'\1', caption)  # Palabras repetidas 2 veces
    
    # Eliminar frases repetitivas específicas
    caption = re.sub(r'\b(her right hand|her left hand|her hand)\s+(on|in|with)\s+(her right hand|her left hand|her hand)\b', 'her hand', caption, flags=re.IGNORECASE)
    
    # Eliminar repeticiones de artículos y preposiciones
    caption = re.sub(r'\b(the|a|an|and|in|on|at|to|of|with|for)\s+\1\b', r'\1', caption, flags=re.IGNORECASE)
    
    # Limpiar espacios múltiples
    caption = re.sub(r'\s+', ' ', caption)
    
    return caption.strip()

def clean_blip2_caption(caption):
    """Limpiar caption de BLIP-2 - Versión conservadora para preservar consistencia"""
    import re
    
    # Eliminar precios (ej: $44 - $45, $100, etc.)
    caption = re.sub(r'\$\d+(?:\.\d+)?(?:\s*-\s*\$\d+(?:\.\d+)?)?', '', caption)
    
    # Eliminar referencias a ciudades/países específicos
    cities_countries = [
        'marysville', 'canada', 'france', 'paris', 'london', 'new york', 'tokyo',
        'berlin', 'madrid', 'rome', 'barcelona', 'milan', 'amsterdam', 'vienna',
        'italy', 'spain', 'germany', 'japan', 'china', 'korea', 'mexico', 'brazil'
    ]
    for place in cities_countries:
        caption = re.sub(rf'\b{place}\b', '', caption, flags=re.IGNORECASE)
    
    # Eliminar texto en francés común
    french_phrases = [
        'portait une', 'vidienne', 'curle', 'boux', 'tinglers', 'cheveux', 'pantalle', 'romanes',
        'photo', 'une femme', 'jeune fille', 'avec', 'dans', 'sur', 'pour', 'avec les',
        'et une', 'les cheveux', 'romanes photo', 'une vidienne', 'curle boux'
    ]
    for phrase in french_phrases:
        caption = re.sub(rf'\b{phrase}\b', '', caption, flags=re.IGNORECASE)
    
    # Eliminar referencias a marcas/productos específicos
    brands_products = [
        'lillyhilfshsockwear', 'thermal compression', 'leggings', 'bernies 2018',
        'laurice bergmetscher', 'nelis marica', 'gr 1 4 class', 'project bernies',
        'apple tree', 'design challenge', 'annual girls', 'class project'
    ]
    for item in brands_products:
        caption = re.sub(rf'\b{re.escape(item)}\b', '', caption, flags=re.IGNORECASE)
    
    # Eliminar números de teléfono, códigos postales, etc.
    caption = re.sub(r'\b\d{3,}\b', '', caption)  # Números largos
    
    # Eliminar objetos alucinados comunes
    hallucinated_objects = [
        'toothbrush', 'knife', 'sword', 'gun', 'weapon', 'tool', 'instrument',
        'device', 'machine', 'equipment', 'apparatus', 'gadget'
    ]
    for obj in hallucinated_objects:
        caption = re.sub(rf'\b{obj}\b', '', caption, flags=re.IGNORECASE)
    
    # Eliminar repeticiones excesivas (similar a BLIP)
    caption = re.sub(r'\b(\w+)\s+\1\s+\1\b', r'\1', caption)  # Palabras repetidas 3+ veces
    caption = re.sub(r'\b(\w+)\s+\1\b', r'\1', caption)  # Palabras repetidas 2 veces
    
    # Eliminar frases repetitivas específicas
    caption = re.sub(r'\b(her right hand|her left hand|her hand)\s+(on|in|with)\s+(her right hand|her left hand|her hand)\b', 'her hand', caption, flags=re.IGNORECASE)
    
    # Eliminar repeticiones de artículos y preposiciones (similar a BLIP)
    caption = re.sub(r'\b(the|a|an|and|in|on|at|to|of|with|for)\s+\1\b', r'\1', caption, flags=re.IGNORECASE)
    
    # Limpiar espacios múltiples
    caption = re.sub(r'\s+', ' ', caption)
    
    # Limpiar caracteres extraños
    caption = re.sub(r'[^\w\s.,!?-]', '', caption)
    
    # NO eliminar palabras comunes como en la versión anterior
    # Esto preserva la estructura del caption para la consistencia
    
    return caption.strip()

def generate_caption_blip2(image, min_words=0):
    """Generar caption con BLIP-2 - Instalación limpia"""
    try:
        # Si no se especifican límites, usar valores por defecto
        if min_words == 0:
            min_words = 15  # Mínimo por defecto: 15 palabras
        
        # Configuración simple y básica
        max_length = max(min_words * 2, 50)  # Longitud máxima
        min_length_tokens = max(int(min_words * 1.3), 10)  # Mínimo en tokens
        
        # Generación con aleatoriedad para regeneración
        inputs = processors['blip2'](image, return_tensors="pt").to(device)
        out = models['blip2'].generate(
            **inputs, 
            max_length=max_length,
            min_length=min_length_tokens,
            num_beams=7,
            temperature=1.1,  # Aumentar temperatura para aleatoriedad
            do_sample=True,   # SIEMPRE usar muestreo para aleatoriedad
            early_stopping=True,
            repetition_penalty=1.2,
            no_repeat_ngram_size=3
        )
        caption = processors['blip2'].decode(out[0], skip_special_tokens=True)
        
        # Limpieza básica
        caption = clean_blip2_caption(caption)
        
        # Verificar si cumple el mínimo de palabras
        word_count = len(caption.strip().split())
        if word_count >= min_words:
            return caption
        else:
            # Si no cumple, intentar una vez más con parámetros más largos
            max_length = max(min_words * 3, 75)
            out = models['blip2'].generate(
                **inputs, 
                max_length=max_length,
                min_length=min_length_tokens,
                num_beams=5,
                temperature=1.3,  # Más aleatoriedad en el segundo intento
                do_sample=True,
                early_stopping=True,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
            caption = processors['blip2'].decode(out[0], skip_special_tokens=True)
            caption = clean_blip2_caption(caption)
            return caption
        
    except Exception as e:
        return f"Error con BLIP-2: {str(e)}"

def generate_caption_llama_vision(image, custom_prompt="Describe this image in detail."):
    """Generar caption con Llama 3.2 Vision via OpenRouter.ai"""
    try:
        # Verificar API key
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            return "Error: OPENROUTER_API_KEY no configurada. Crea un archivo .env con tu API key."
        
        # Redimensionar imagen manteniendo aspect ratio
        resized_image = resize_image_maintain_aspect(image)
        
        # Convertir a base64
        image_base64 = image_to_base64(resized_image)
        
        # Preparar payload para OpenRouter
        payload = {
            "model": CONFIG["settings"]["openrouter_model"],
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": custom_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 200,
            "temperature": 0.7
        }
        
        # Enviar petición
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            CONFIG["endpoints"]["openrouter_url"],
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                response_text = result['choices'][0]['message']['content']
                return response_text.strip()
            else:
                return "Error: Respuesta inesperada de la API"
        else:
            return f"Error API {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error con Llama 3.2 Vision: {str(e)}"

# Función generate_wd14_tags eliminada (WD14 removido)

def process_images_async(files, model_name, task_id, keyword='', min_words=0, consistency_mode='auto', custom_prompt=''):
    """Procesar imágenes de forma asíncrona"""
    try:
        # Cargar modelo bajo demanda con task_id para mostrar progreso
        if not load_model_on_demand(model_name, task_id):
            progress_data[task_id]['status'] = 'error'
            progress_data[task_id]['message'] = f'Error: No se pudo cargar el modelo {model_name}'
            return
        
        for i, filename in enumerate(files):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if os.path.exists(file_path):
                caption = generate_caption(file_path, model_name, keyword, min_words, consistency_mode, custom_prompt)
                
                progress_data[task_id]['results'].append({
                    'filename': filename,
                    'caption': caption,
                    'file_id': filename,  # Usar el nombre del archivo como ID
                    'model_used': model_name
                })
            
            # Actualizar progreso
            progress_data[task_id]['current'] = i + 1
            progress_data[task_id]['progress'] = int((i + 1) / len(files) * 100)
        
        # Completar tarea
        progress_data[task_id]['status'] = 'completed'
        
        # Descargar modelo al finalizar la generación
        print(f"🗑️ Finalizada la generación con {model_name}, descargando modelo...")
        unload_model(model_name)
        
    except Exception as e:
        progress_data[task_id]['status'] = 'error'
        progress_data[task_id]['error'] = str(e)
        
        # Descargar modelo incluso si hay error
        print(f"🗑️ Error en la generación con {model_name}, descargando modelo...")
        unload_model(model_name)

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'error': 'Archivo demasiado grande',
        'message': f'El tamaño total de los archivos excede el límite de {CONFIG["limits"]["max_files"] * CONFIG["limits"]["max_file_size_mb"]}MB. Por favor, reduce el número de archivos o su tamaño.'
    }), 413

@app.route('/api/config', methods=['GET'])
def get_config():
    """Obtener configuración actual"""
    try:
        return jsonify(CONFIG)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    """Guardar nueva configuración"""
    try:
        new_config = request.get_json()
        
        # Validar configuración
        if not new_config:
            return jsonify({'success': False, 'error': 'No se proporcionó configuración'}), 400
        
        # Guardar en archivo
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(new_config, f, indent=2, ensure_ascii=False)
        
        # Recargar configuración global
        global CONFIG
        CONFIG = new_config
        
        # Actualizar variables de entorno
        if new_config.get('api_keys', {}).get('openrouter'):
            os.environ['OPENROUTER_API_KEY'] = new_config['api_keys']['openrouter']
        
        return jsonify({'success': True, 'message': 'Configuración guardada exitosamente'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/image/<file_id>')
def get_image(file_id):
    """Obtener imagen por ID"""
    try:
        # Buscar archivo en uploads
        upload_folder = app.config['UPLOAD_FOLDER']
        
        # Primero intentar encontrar el archivo exacto
        file_path = os.path.join(upload_folder, file_id)
        if os.path.exists(file_path):
            return send_file(file_path)
        
        # Si no se encuentra, buscar por nombre parcial
        for filename in os.listdir(upload_folder):
            if file_id in filename or filename in file_id:
                file_path = os.path.join(upload_folder, filename)
                if os.path.exists(file_path):
                    return send_file(file_path)
        
        return jsonify({'error': 'Imagen no encontrada'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-zip', methods=['POST'])
def download_zip():
    """Descargar resultados como ZIP con imágenes redimensionadas"""
    try:
        data = request.get_json()
        results = data.get('results', [])
        width = data.get('width', 1024)
        height = data.get('height', 1024)
        
        if not results:
            return jsonify({'error': 'No hay resultados para descargar'}), 400
        
        print(f"Descargando ZIP con resolución: {width}x{height}")
        
        # Crear archivo ZIP temporal
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            # Crear carpeta para las imágenes
            images_folder = 'images/'
            
            # Agregar cada resultado
            for result in results:
                filename = result.get('filename', '')
                caption = result.get('caption', '')
                model_used = result.get('model_used', 'unknown')
                
                # Buscar la imagen original
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                if os.path.exists(original_path):
                    # Redimensionar imagen para el ZIP con resolución seleccionada
                    try:
                        with Image.open(original_path) as img:
                            # Convertir a RGB si es necesario
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            
                            # Calcular nuevas dimensiones manteniendo aspect ratio
                            original_width, original_height = img.size
                            
                            # Calcular el factor de escala para mantener aspect ratio
                            scale_w = width / original_width
                            scale_h = height / original_height
                            scale = min(scale_w, scale_h)  # Usar el menor para que quepa en ambas dimensiones
                            
                            # Calcular nuevas dimensiones
                            new_width = int(original_width * scale)
                            new_height = int(original_height * scale)
                            
                            print(f"Redimensionando {filename}: {original_width}x{original_height} -> {new_width}x{new_height}")
                            
                            # Redimensionar con máxima calidad
                            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                            
                            # Guardar en buffer con máxima calidad
                            img_buffer = BytesIO()
                            img_resized.save(img_buffer, format='JPEG', quality=CONFIG["settings"]["download_image_quality"], optimize=True)
                            img_buffer.seek(0)
                            
                            # Agregar imagen redimensionada a la carpeta
                            zip_file.writestr(f"{images_folder}{filename}", img_buffer.getvalue())
                            
                    except Exception as e:
                        print(f"Error procesando imagen {filename}: {e}")
                        # Si falla el redimensionado, copiar original
                        with open(original_path, 'rb') as f:
                            zip_file.writestr(f"{images_folder}{filename}", f.read())
                
                # Agregar archivo de texto con caption (solo el caption)
                caption_filename = f"{images_folder}{os.path.splitext(filename)[0]}.txt"
                zip_file.writestr(caption_filename, caption)
            
            # Crear JSON con toda la información
            json_data = {
                'metadata': {
                    'total_images': len(results),
                    'generated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'models_used': list(set(r.get('model_used', 'unknown') for r in results))
                },
                'results': results
            }
            
            # Agregar JSON a la raíz del ZIP
            zip_file.writestr('results.json', json.dumps(json_data, indent=2, ensure_ascii=False))
            
            # Agregar README
            readme_content = f"""# Resultados de Captioning IA

## Información General
- Total de imágenes: {len(results)}
- Fecha de generación: {time.strftime('%Y-%m-%d %H:%M:%S')}
- Modelos utilizados: {', '.join(set(r.get('model_used', 'unknown') for r in results))}

## Estructura del ZIP
- `images/` - Carpeta con imágenes redimensionadas y archivos TXT
- `results.json` - Archivo JSON con toda la información detallada

## Archivos por imagen
Cada imagen tiene su archivo TXT correspondiente que contiene únicamente el caption generado.

Generado por: Herramienta de Captioning IA
"""
            zip_file.writestr('README.txt', readme_content)
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'captions_{time.strftime("%Y%m%d_%H%M%S")}.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(500)
def internal_error(e):
    return jsonify({
        'error': 'Error interno del servidor',
        'message': 'Ocurrió un error inesperado. Por favor, intenta nuevamente.'
    }), 500

if __name__ == '__main__':
    print("🚀 Iniciando aplicación...")
    initialize_models()
    print("✅ Sistema de carga dinámica inicializado")
    print(f"🔧 Dispositivo disponible: {device}")
    print(f"🌐 Aplicación disponible en: http://{CONFIG['server']['host']}:{CONFIG['server']['port']}")
    print(f"📁 Límite de archivos: {CONFIG['limits']['max_files']} imágenes máximo")
    print(f"💾 Límite de tamaño: {CONFIG['limits']['max_file_size_mb']}MB por imagen")
    print(f"🐛 Modo debug: {'Activado' if DEBUG_MODE else 'Desactivado'}")
    print(f"🎨 Calidad: Máxima calidad mantenida (hasta 4096px)")
    print(f"🔄 Modo: Carga dinámica de modelos (se cargan bajo demanda)")
    app.run(debug=DEBUG_MODE, host='0.0.0.0', port=CONFIG['server']['port'])
