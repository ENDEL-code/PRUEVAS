#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime, timedelta

class ControlGastos:
    def __init__(self):
        self.archivo_datos = 'control_gastos.json'
        self.cargar_datos()
        
        # Calendario escolar SEP 2025-2026
        self.vacaciones = [
            (datetime(2025, 12, 22), datetime(2026, 1, 9)),
            (datetime(2026, 3, 30), datetime(2026, 4, 10))
        ]
        
        self.dias_festivos = [
            datetime(2025, 9, 16), datetime(2025, 11, 17), datetime(2025, 12, 25),
            datetime(2026, 1, 1), datetime(2026, 2, 2), datetime(2026, 3, 16),
            datetime(2026, 5, 1), datetime(2026, 5, 5), datetime(2026, 5, 15),
            datetime(2025, 9, 26), datetime(2025, 10, 31), datetime(2025, 11, 28),
            datetime(2026, 1, 30), datetime(2026, 2, 27), datetime(2026, 3, 27),
            datetime(2026, 5, 29), datetime(2026, 6, 26)
        ]
    
    def cargar_datos(self):
        """Carga los datos del archivo JSON"""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.deuda = datos.get('deuda', 0)
                    self.dinero_extra = datos.get('dinero_extra', 0)
                    self.total_ahorrado = datos.get('total_ahorrado', 0)
                    self.historial = datos.get('historial', [])
                    self.fecha_actual = datetime.strptime(datos.get('fecha_actual', '2025-11-10'), '%Y-%m-%d')
            except Exception as e:
                print(f"Error al cargar datos: {e}")
                self.inicializar_datos()
        else:
            self.inicializar_datos()
    
    def inicializar_datos(self):
        """Inicializa los datos por defecto"""
        self.deuda = 0
        self.dinero_extra = 0
        self.total_ahorrado = 0
        self.historial = []
        self.fecha_actual = datetime(2025, 11, 10)
    
    def guardar_datos(self):
        """Guarda los datos en el archivo JSON"""
        try:
            datos = {
                'deuda': self.deuda,
                'dinero_extra': self.dinero_extra,
                'total_ahorrado': self.total_ahorrado,
                'historial': self.historial,
                'fecha_actual': self.fecha_actual.strftime('%Y-%m-%d')
            }
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False
    
    def es_dia_vacaciones(self, fecha):
        for inicio, fin in self.vacaciones:
            if inicio <= fecha <= fin:
                return True
        return False
    
    def es_dia_festivo(self, fecha):
        return any(fecha.date() == festivo.date() for festivo in self.dias_festivos)
    
    def es_dia_clase(self, fecha):
        dia_semana = fecha.weekday()
        if 0 <= dia_semana <= 4:
            return not self.es_dia_vacaciones(fecha) and not self.es_dia_festivo(fecha)
        return False
    
    def es_sabado(self, fecha):
        return fecha.weekday() == 5
    
    def obtener_cargo_dia(self, fecha):
        if self.es_dia_vacaciones(fecha):
            return 0, 'Vacaciones'
        elif self.es_sabado(fecha):
            return 100, 'Sabado'
        elif self.es_dia_clase(fecha):
            return 50, 'Dia de clase'
        else:
            return 0, 'Sin cargo'
    
    def ya_pagado_hoy(self):
        fecha_str = self.fecha_actual.strftime('%Y-%m-%d')
        return any(h['fecha'] == fecha_str for h in self.historial)
    
    def usar_dinero_extra_para_deuda(self):
        """Usa el dinero extra para pagar la deuda"""
        if self.dinero_extra > 0 and self.deuda > 0:
            if self.dinero_extra >= self.deuda:
                self.dinero_extra -= self.deuda
                print(f"\nSe uso ${self.deuda:.2f} del dinero extra para saldar la deuda completa!")
                self.deuda = 0
            else:
                self.deuda -= self.dinero_extra
                print(f"\nSe uso todo el dinero extra (${self.dinero_extra:.2f}) para reducir la deuda!")
                self.dinero_extra = 0
            self.guardar_datos()
            return True
        elif self.deuda == 0:
            print("\nNo tienes deuda que pagar.")
            return False
        else:
            print("\nNo tienes dinero extra disponible.")
            return False
    
    def recalcular_totales(self):
        """Recalcula todos los totales desde el historial"""
        self.deuda = 0
        self.dinero_extra = 0
        self.total_ahorrado = 0
        
        for transaccion in self.historial:
            dinero_dado = transaccion['dinero_dado']
            cargo_dia = transaccion['cargo_dia']
            
            self.total_ahorrado += dinero_dado
            restante = dinero_dado
            
            # Pagar deuda existente
            if self.deuda > 0 and restante > 0:
                pago_deuda = min(restante, self.deuda)
                self.deuda -= pago_deuda
                restante -= pago_deuda
            
            # Pagar el cargo del dia
            if restante >= cargo_dia:
                restante -= cargo_dia
                self.dinero_extra += restante
            else:
                self.deuda += (cargo_dia - restante)
                restante = 0
            
            # Usar dinero extra para pagar deuda automaticamente
            if self.dinero_extra > 0 and self.deuda > 0:
                if self.dinero_extra >= self.deuda:
                    self.dinero_extra -= self.deuda
                    self.deuda = 0
                else:
                    self.deuda -= self.dinero_extra
                    self.dinero_extra = 0
            
            # Actualizar los valores en la transaccion
            transaccion['deuda_despues'] = self.deuda
            transaccion['extra_despues'] = self.dinero_extra
            transaccion['total_ahorrado_despues'] = self.total_ahorrado
        
        self.guardar_datos()
    
    def borrar_registro_historial(self, indice):
        """Borra un registro del historial y recalcula todo"""
        if 0 <= indice < len(self.historial):
            registro = self.historial[indice]
            print(f"\nBorrando registro: {registro['dia_semana']} {registro['fecha']}")
            print(f"Dinero dado: ${registro['dinero_dado']:.2f}")
            
            confirmacion = input("\nEstas seguro? (si/no): ").strip().lower()
            
            if confirmacion == 'si':
                # Eliminar el registro
                self.historial.pop(indice)
                
                # Recalcular todos los totales
                print("\nRecalculando totales...")
                self.recalcular_totales()
                
                print("\nRegistro eliminado y totales recalculados!")
                return True
            else:
                print("\nBorrado cancelado.")
                return False
        else:
            print("\nIndice invalido.")
            return False
    
    def registrar_dia(self, dinero_hoy):
        if self.ya_pagado_hoy():
            print("\nYa registraste el pago de hoy. Avanza al siguiente dia.")
            return False
        
        cargo_dia, tipo_dia = self.obtener_cargo_dia(self.fecha_actual)
        
        deuda_anterior = self.deuda
        extra_anterior = self.dinero_extra
        total_anterior = self.total_ahorrado
        
        self.total_ahorrado += dinero_hoy
        restante = dinero_hoy
        
        # Primero pagar deuda existente
        if self.deuda > 0 and restante > 0:
            pago_deuda = min(restante, self.deuda)
            self.deuda -= pago_deuda
            restante -= pago_deuda
        
        # Luego pagar el cargo del dia
        if restante >= cargo_dia:
            restante -= cargo_dia
            self.dinero_extra += restante
        else:
            self.deuda += (cargo_dia - restante)
            restante = 0
        
        # Despues de procesar, si hay dinero extra y deuda, usar el extra para pagar
        self.usar_dinero_extra_para_deuda()
        
        # Guardar en historial
        dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        transaccion = {
            'fecha': self.fecha_actual.strftime('%Y-%m-%d'),
            'dia_semana': dias_semana[self.fecha_actual.weekday()],
            'tipo_dia': tipo_dia,
            'dinero_dado': dinero_hoy,
            'cargo_dia': cargo_dia,
            'deuda_antes': deuda_anterior,
            'deuda_despues': self.deuda,
            'extra_antes': extra_anterior,
            'extra_despues': self.dinero_extra,
            'total_ahorrado_antes': total_anterior,
            'total_ahorrado_despues': self.total_ahorrado
        }
        
        self.historial.append(transaccion)
        self.guardar_datos()
        
        print(f"\nDia registrado exitosamente!")
        print(f"Tipo: {tipo_dia} | Cargo: ${cargo_dia:.2f}")
        print(f"Deuda: ${deuda_anterior:.2f} -> ${self.deuda:.2f}")
        print(f"Extra: ${extra_anterior:.2f} -> ${self.dinero_extra:.2f}")
        
        return True
    
    def siguiente_dia(self):
        self.fecha_actual += timedelta(days=1)
        self.guardar_datos()
        print(f"\nAvanzando al {self.fecha_actual.strftime('%d/%m/%Y')}")
    
    def mostrar_estado(self):
        dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        cargo_dia, tipo_dia = self.obtener_cargo_dia(self.fecha_actual)
        
        print("\n" + "="*60)
        print("           CONTROL DE GASTOS Y AHORRO SEP 2025-2026")
        print("="*60)
        print(f"\nFECHA ACTUAL: {dias_semana[self.fecha_actual.weekday()]}, {self.fecha_actual.strftime('%d/%m/%Y')}")
        print(f"Tipo: {tipo_dia} | Cargo del dia: ${cargo_dia:.2f}")
        
        if self.ya_pagado_hoy():
            print("Ya registraste el pago de hoy")
        
        print(f"\n{'-'*60}")
        print(f"TOTAL AHORRADO:    ${self.total_ahorrado:>10.2f}")
        print(f"DEUDA:             ${self.deuda:>10.2f}")
        print(f"DINERO EXTRA:      ${self.dinero_extra:>10.2f}")
        print(f"DIAS REGISTRADOS:  {len(self.historial):>10}")
        print(f"{'-'*60}")
    
    def ver_historial_con_opcion_borrar(self, ultimos=10):
        if not self.historial:
            print("\nNo hay historial aun.")
            return
        
        while True:
            limpiar_pantalla()
            print(f"\n{'='*60}")
            print(f"         HISTORIAL (ultimos {ultimos} dias)")
            print(f"{'='*60}\n")
            
            # Mostrar registros con indices
            registros_mostrados = self.historial[-ultimos:][::-1]
            indices_reales = list(range(len(self.historial) - 1, max(-1, len(self.historial) - ultimos - 1), -1))
            
            for i, (idx_real, trans) in enumerate(zip(indices_reales, registros_mostrados), 1):
                print(f"[{i}] {trans['dia_semana']} {trans['fecha']} - {trans['tipo_dia']}")
                print(f"    Dinero: ${trans['dinero_dado']:.2f} | Cargo: ${trans['cargo_dia']:.2f}")
                print(f"    Deuda: ${trans['deuda_antes']:.2f} -> ${trans['deuda_despues']:.2f}")
                print(f"    Extra: ${trans['extra_antes']:.2f} -> ${trans['extra_despues']:.2f}")
                print(f"    Total ahorrado: ${trans['total_ahorrado_despues']:.2f}")
                print()
            
            print(f"\n{'-'*60}")
            print("Opciones:")
            print("  - Escribe el numero del registro para BORRAR")
            print("  - Escribe '0' para volver al menu principal")
            print(f"{'-'*60}")
            
            opcion = input("\nOpcion: ").strip()
            
            if opcion == '0':
                break
            
            try:
                num = int(opcion)
                if 1 <= num <= len(registros_mostrados):
                    idx_real = indices_reales[num - 1]
                    if self.borrar_registro_historial(idx_real):
                        input("\nPresiona Enter para continuar...")
                else:
                    print("\nNumero invalido.")
                    input("\nPresiona Enter para continuar...")
            except ValueError:
                print("\nOpcion invalida.")
                input("\nPresiona Enter para continuar...")


def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    control = ControlGastos()
    
    while True:
        limpiar_pantalla()
        control.mostrar_estado()
        
        print("\n" + "-"*45)
        print("              MENU PRINCIPAL")
        print("-"*45)
        print("1. Registrar dinero de hoy")
        print("2. Siguiente dia")
        print("3. Ver historial (con opcion de borrar)")
        print("4. Usar dinero extra para pagar deuda")
        print("5. Salir")
        print("-"*45)
        
        opcion = input("\nElige una opcion: ").strip()
        
        if opcion == '1':
            if control.ya_pagado_hoy():
                print("\nYa registraste el pago de hoy.")
                input("\nPresiona Enter para continuar...")
            else:
                try:
                    dinero = float(input("\nCuanto dinero tienes hoy? $"))
                    if dinero < 0:
                        print("La cantidad debe ser positiva.")
                    else:
                        control.registrar_dia(dinero)
                    input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("Cantidad invalida.")
                    input("\nPresiona Enter para continuar...")
        
        elif opcion == '2':
            control.siguiente_dia()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '3':
            try:
                n = input("\nCuantos dias mostrar? (Enter para 10): ").strip()
                n = int(n) if n else 10
                control.ver_historial_con_opcion_borrar(n)
            except ValueError:
                control.ver_historial_con_opcion_borrar(10)
        
        elif opcion == '4':
            control.usar_dinero_extra_para_deuda()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == '5':
            print("\nHasta luego!")
            break
        
        else:
            print("\nOpcion invalida.")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    print("Iniciando Control de Gastos y Ahorro SEP 2025-2026...")
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\n\nError inesperado: {e}")