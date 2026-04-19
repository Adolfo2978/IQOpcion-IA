# Sistema de Decisión Inteligente para Trading
# Mejora las decisiones de traders combinando:
# 1. Patrones de traders exitosos históricos
# 2. Predicciones de IA en tiempo real
# 3. Condiciones actuales del mercado
# 4. Indicadores técnicos y estrategias validadas

import json
import os
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)


class DecisionInteligenteSistema:
    """
    SISTEMA DE DECISIÓN INTELIGENTE MEJORADO
    
    Este sistema analiza y optimiza las decisiones de trading basándose en:
    
    1. 📊 APRENDIZAJE DE TRADERS EXITOSOS
       - Analiza patrones de trades históricos ganadores
       - Extrae características comunes (indicadores, timing, condiciones)
       - Crea perfiles de éxito por tipo de mercado
    
    2. 🤖 PREDICCIONES DE IA EN TIEMPO REAL
       - Integra con el motor de IA existente
       - Valida predicciones contra patrones históricos
       - Ajusta confianza basado en similitud con casos exitosos
    
    3. 📈 CONDICIONES DE MERCADO ACTUALES
       - Volatilidad, tendencia, volumen
       - Sesiones de mercado (Asia, Europa, USA)
       - Eventos económicos relevantes
    
    4. 🔍 INDICADORES TÉCNICOS VALIDADOS
       - RSI, MACD, EMA, Bandas de Bollinger
       - Patrones de velas (Wick Method, TDI)
       - Confluencia multi-timeframe
    
    5. ⚡ OPTIMIZACIÓN CONTINUA
       - Retroalimentación de cada trade
       - Actualización de pesos y umbrales
       - Detección de degradación de rendimiento
    """
    
    def __init__(self, config=None, ai_engine=None, datos_dir="Datos"):
        self.config = config
        self.ai_engine = ai_engine
        self.datos_dir = Path(datos_dir)
        self.logger = logging.getLogger(__name__)
        
        # Repositorio de decisiones exitosas
        self.trades_exitosos_path = Path("trades_exitosos.json")
        self.patrones_exitosos = []
        self.perfiles_mercado = {}
        
        # Pesos dinámicos para la decisión
        self.peso_ia = 0.35
        self.peso_patron_historico = 0.30
        self.peso_condiciones_mercado = 0.20
        self.peso_indicadores = 0.15
        
        # Estadísticas de rendimiento
        self.estadisticas = {
            'total_decisiones': 0,
            'decisiones_correctas': 0,
            'win_rate_general': 0.0,
            'win_rate_por_patron': {},
            'win_rate_por_mercado': {},
            'ultimo_reentrenamiento': None
        }
        
        # Cargar datos históricos
        self._cargar_trades_exitosos()
        self._analizar_patrones_exitosos()
        
        self.logger.info("✅ Sistema de Decisión Inteligente inicializado")
        self.logger.info(f"📊 Trades exitosos cargados: {len(self.patrones_exitosos)}")
    
    # =========================================================
    # 1. CARGA Y ANÁLISIS DE TRADERS EXITOSOS
    # =========================================================
    
    def _cargar_trades_exitosos(self):
        """Carga trades exitosos desde JSON"""
        try:
            if self.trades_exitosos_path.exists():
                with open(self.trades_exitosos_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    trades = data.get('trades', [])
                    
                    # Filtrar solo trades exitosos confirmados
                    self.trades_raw = [
                        t for t in trades 
                        if t.get('exitoso') == True and t.get('ganancia', 0) > 0
                    ]
                    
                self.logger.info(f"Cargados {len(self.trades_raw)} trades exitosos")
            else:
                self.trades_raw = []
                self.logger.warning("No se encontró archivo de trades exitosos")
        except Exception as e:
            self.logger.error(f"Error cargando trades exitosos: {e}")
            self.trades_raw = []
    
    def _analizar_patrones_exitosos(self):
        """
        Analiza patrones comunes en trades exitosos
        Extrae características clave para crear perfiles de éxito
        """
        if not self.trades_raw:
            self.logger.warning("Sin trades exitosos para analizar")
            return
        
        self.patrones_exitosos = []
        
        for trade in self.trades_raw:
            patron = self._extraer_patron_trade(trade)
            if patron:
                self.patrones_exitosos.append(patron)
        
        # Crear perfiles por tipo de mercado
        self._crear_perfiles_mercado()
        
        self.logger.info(f"Patrones exitosos identificados: {len(self.patrones_exitosos)}")
    
    def _extraer_patron_trade(self, trade: dict) -> Optional[dict]:
        """Extrae características clave de un trade exitoso"""
        try:
            indicadores = trade.get('indicadores', {})
            
            patron = {
                'simbolo': trade.get('simbolo', 'UNKNOWN'),
                'direccion': trade.get('direccion', ''),
                'timestamp': trade.get('timestamp', ''),
                'hora': self._extraer_hora(trade.get('timestamp', '')),
                'dia_semana': self._extraer_dia_semana(trade.get('timestamp', '')),
                
                # Indicadores técnicos en momento del trade
                'rsi': indicadores.get('RSI', 50),
                'macd': indicadores.get('MACD', 0),
                'stoch_k': indicadores.get('stoch_k', 50),
                'tdi_rsi': indicadores.get('TDI_rsi', 50),
                
                # Configuración del trade
                'payout': trade.get('payout', 0),
                'probabilidad_ia': trade.get('probabilidad_predicha', 0.5),
                'escenario_mercado': trade.get('escenario_mercado', 'unknown'),
                
                # Resultado
                'ganancia': trade.get('ganancia', 0),
                'exitoso': trade.get('exitoso', False)
            }
            
            # Clasificar tipo de patrón
            patron['tipo_patron'] = self._clasificar_patron(patron)
            
            return patron
        except Exception as e:
            self.logger.error(f"Error extrayendo patrón: {e}")
            return None
    
    def _clasificar_patron(self, patron: dict) -> str:
        """Clasifica el patrón basado en indicadores"""
        rsi = patron.get('rsi', 50)
        direccion = patron.get('direccion', '')
        
        # Patrones comunes
        if direccion == 'CALL':
            if rsi < 30:
                return 'SOBREVENTA_REBOTE'
            elif 45 <= rsi <= 55:
                return 'RANGO_MEDIO'
            elif rsi > 70:
                return 'MOMENTUM_FUERTE'
            else:
                return 'TENDENCIA_ALCISTA'
        elif direccion == 'PUT':
            if rsi > 70:
                return 'SOBRECOMPRA_CORRECCION'
            elif 45 <= rsi <= 55:
                return 'RANGO_MEDIO'
            elif rsi < 30:
                return 'MOMENTUM_FUERTE'
            else:
                return 'TENDENCIA_BAJISTA'
        
        return 'DESCONOCIDO'
    
    def _crear_perfiles_mercado(self):
        """Crea perfiles de éxito por tipo de mercado y condiciones"""
        self.perfiles_mercado = defaultdict(lambda: {
            'total': 0,
            'wins': 0,
            'win_rate': 0.0,
            'caracteristicas_comunes': {},
            'mejores_horas': [],
            'mejores_pares': []
        })
        
        for patron in self.patrones_exitosos:
            escenario = patron.get('escenario_mercado', 'desconocido')
            perfil = self.perfiles_mercado[escenario]
            
            perfil['total'] += 1
            if patron.get('exitoso'):
                perfil['wins'] += 1
            
            # Calcular win rate
            if perfil['total'] > 0:
                perfil['win_rate'] = (perfil['wins'] / perfil['total']) * 100
        
        self.logger.info(f"Perfiles de mercado creados: {len(self.perfiles_mercado)}")
    
    # =========================================================
    # 2. ANÁLISIS DE CONDICIONES DE MERCADO ACTUALES
    # =========================================================
    
    def analizar_condiciones_mercado(self, df: pd.DataFrame, simbolo: str) -> dict:
        """
        Analiza las condiciones actuales del mercado
        Retorna un score de favorabilidad (0-100)
        """
        condiciones = {
            'volatilidad': 0,
            'tendencia_fuerza': 0,
            'session_mercado': '',
            'score_favorabilidad': 0,
            'recomendacion': 'ESPERAR'
        }
        
        try:
            if df is None or len(df) < 20:
                return condiciones
            
            # Calcular volatilidad (ATR normalizado)
            high_low = df['high'] - df['low']
            atr = high_low.rolling(14).mean().iloc[-1]
            precio_promedio = df['close'].iloc[-20:].mean()
            volatilidad_norm = (atr / precio_promedio) * 10000
            
            # Clasificar volatilidad
            if volatilidad_norm < 5:
                condiciones['volatilidad'] = 'BAJA'
                score_vol = 40
            elif 5 <= volatilidad_norm <= 15:
                condiciones['volatilidad'] = 'MEDIA'
                score_vol = 80
            else:
                condiciones['volatilidad'] = 'ALTA'
                score_vol = 60
            
            # Determinar fuerza de tendencia
            ema_corta = df['close'].ewm(span=9).mean().iloc[-1]
            ema_larga = df['close'].ewm(span=21).mean().iloc[-1]
            diff_tendencia = abs(ema_corta - ema_larga) / ema_larga * 100
            
            if diff_tendencia > 0.5:
                condiciones['tendencia_fuerza'] = 'FUERTE'
                score_tendencia = 85
            elif diff_tendencia > 0.2:
                condiciones['tendencia_fuerza'] = 'MODERADA'
                score_tendencia = 65
            else:
                condiciones['tendencia_fuerza'] = 'LATERAL'
                score_tendencia = 45
            
            # Determinar sesión de mercado
            hora_actual = datetime.now().hour
            if 0 <= hora_actual < 8:
                condiciones['session_mercado'] = 'ASIA'
                score_sesion = 60
            elif 8 <= hora_actual < 16:
                condiciones['session_mercado'] = 'EUROPA'
                score_sesion = 85
            elif 16 <= hora_actual < 22:
                condiciones['session_mercado'] = 'USA'
                score_sesion = 90
            else:
                condiciones['session_mercado'] = 'CRUCE'
                score_sesion = 70
            
            # Score total de favorabilidad
            condiciones['score_favorabilidad'] = int(
                (score_vol * 0.35) + 
                (score_tendencia * 0.40) + 
                (score_sesion * 0.25)
            )
            
            # Recomendación basada en score
            if condiciones['score_favorabilidad'] >= 75:
                condiciones['recomendacion'] = 'OPERAR'
            elif condiciones['score_favorabilidad'] >= 55:
                condiciones['recomendacion'] = 'PRECAUCION'
            else:
                condiciones['recomendacion'] = 'ESPERAR'
            
        except Exception as e:
            self.logger.error(f"Error analizando condiciones de mercado: {e}")
            condiciones['error'] = str(e)
        
        return condiciones
    
    # =========================================================
    # 3. COMPARACIÓN CON PATRONES HISTÓRICOS
    # =========================================================
    
    def buscar_patrones_similares(self, indicadores_actuales: dict, 
                                  simbolo: str, direccion: str) -> List[dict]:
        """
        Busca patrones históricos similares a la situación actual
        Retorna los patrones más similares con sus resultados
        """
        if not self.patrones_exitosos:
            return []
        
        patrones_similares = []
        
        for patron in self.patrones_exitosos:
            # Calcular similitud
            similitud = self._calcular_similitud(indicadores_actuales, patron, direccion)
            
            if similitud > 0.6:  # Umbral mínimo de similitud
                patrones_similares.append({
                    'patron': patron,
                    'similitud': similitud,
                    'resultado': patron.get('exitoso', False),
                    'ganancia': patron.get('ganancia', 0)
                })
        
        # Ordenar por similitud
        patrones_similares.sort(key=lambda x: x['similitud'], reverse=True)
        
        return patrones_similares[:10]  # Top 10 más similares
    
    def _calcular_similitud(self, actuales: dict, historico: dict, direccion: str) -> float:
        """Calcula score de similitud entre situación actual y patrón histórico"""
        score = 0.0
        factores = 0
        
        # Mismo símbolo (20% peso)
        if actuales.get('simbolo', '') == historico.get('simbolo', ''):
            score += 0.20
        factores += 0.20
        
        # Misma dirección (25% peso)
        if direccion == historico.get('direccion', ''):
            score += 0.25
        factores += 0.25
        
        # RSI similar (15% peso)
        rsi_actual = actuales.get('rsi', 50)
        rsi_hist = historico.get('rsi', 50)
        diff_rsi = abs(rsi_actual - rsi_hist)
        if diff_rsi < 10:
            score += 0.15
        elif diff_rsi < 20:
            score += 0.08
        factores += 0.15
        
        # Hora similar (10% peso)
        hora_actual = actuales.get('hora', 12)
        hora_hist = historico.get('hora', 12)
        diff_hora = abs(hora_actual - hora_hist)
        if diff_hora <= 2:
            score += 0.10
        elif diff_hora <= 4:
            score += 0.05
        factores += 0.10
        
        # Mismo tipo de patrón (20% peso)
        tipo_actual = self._clasificar_patron({
            'rsi': rsi_actual,
            'direccion': direccion
        })
        if tipo_actual == historico.get('tipo_patron', ''):
            score += 0.20
        factores += 0.20
        
        # Mismo escenario de mercado (10% peso)
        if actuales.get('escenario', 'unknown') == historico.get('escenario_mercado', 'unknown'):
            score += 0.10
        factores += 0.10
        
        return score / factores if factores > 0 else 0.0
    
    # =========================================================
    # 4. DECISIÓN INTEGRADA FINAL
    # =========================================================
    
    def tomar_decision_optimizada(self, 
                                   df: pd.DataFrame,
                                   indicadores: dict,
                                   prediccion_ia: dict,
                                   simbolo: str) -> dict:
        """
        TOMA DE DECISIÓN ÓPTIMA
        
        Combina todos los factores para una decisión informada:
        1. Predicción de IA
        2. Patrones históricos similares
        3. Condiciones de mercado actuales
        4. Indicadores técnicos
        
        Retorna:
        {
            'accion': 'CALL' | 'PUT' | 'ESPERAR',
            'confianza': 0-100,
            'factores': {...},
            'razon': '...',
            'riesgo': 'BAJO' | 'MEDIO' | 'ALTO'
        }
        """
        decision = {
            'accion': 'ESPERAR',
            'confianza': 0.0,
            'timestamp': datetime.now().isoformat(),
            'simbolo': simbolo,
            'factores': {},
            'razon': '',
            'riesgo': 'ALTO',
            'recomendaciones': []
        }
        
        try:
            # 1. Obtener predicción de IA
            ia_confianza = prediccion_ia.get('confianza', 0)
            ia_direccion = prediccion_ia.get('direccion', None)
            
            # 2. Analizar condiciones de mercado
            condiciones_mercado = self.analizar_condiciones_mercado(df, simbolo)
            score_mercado = condiciones_mercado.get('score_favorabilidad', 0)
            
            # 3. Buscar patrones históricos similares
            indicadores_actuales = {
                'simbolo': simbolo,
                'rsi': indicadores.get('RSI', 50),
                'hora': datetime.now().hour,
                'escenario': condiciones_mercado.get('session_mercado', 'unknown')
            }
            
            patrones_similares = self.buscar_patrones_similares(
                indicadores_actuales, 
                simbolo, 
                ia_direccion
            )
            
            # Calcular score de patrones históricos
            score_patrones = 0
            if patrones_similares:
                wins_historicos = sum(1 for p in patrones_similares if p['resultado'])
                total_similares = len(patrones_similares)
                score_patrones = (wins_historicos / total_similares) * 100 if total_similares > 0 else 0
                
                # Similitud promedio
                similitud_promedio = sum(p['similitud'] for p in patrones_similares) / total_similares
                score_patrones *= similitud_promedio  # Ponderar por similitud
            
            # 4. Score de indicadores técnicos
            score_tecnicos = self._calcular_score_tecnicos(indicadores, ia_direccion)
            
            # =====================================================
            # CÁLCULO DE CONFIANZA PONDERADA
            # =====================================================
            confianzas = {
                'ia': ia_confianza,
                'patrones': score_patrones,
                'mercado': score_mercado,
                'tecnicos': score_tecnicos
            }
            
            # Aplicar pesos dinámicos
            confianza_total = (
                confianzas['ia'] * self.peso_ia +
                confianzas['patrones'] * self.peso_patron_historico +
                confianzas['mercado'] * self.peso_condiciones_mercado +
                confianzas['tecnicos'] * self.peso_indicadores
            )
            
            decision['confianza'] = round(confianza_total, 2)
            decision['factores'] = {
                'ia': confianzas['ia'],
                'patrones_historicos': score_patrones,
                'condiciones_mercado': score_mercado,
                'indicadores_tecnicos': score_tecnicos,
                'patrones_encontrados': len(patrones_similares)
            }
            
            # =====================================================
            # TOMA DE DECISIÓN FINAL
            # =====================================================
            umbral_operacion = getattr(self.config, 'UMBRAL_DECISION_INTELIGENTE', 75.0)
            
            if confianza_total >= umbral_operacion and ia_direccion in ['CALL', 'PUT']:
                decision['accion'] = ia_direccion
                
                # Determinar nivel de riesgo
                if confianza_total >= 85:
                    decision['riesgo'] = 'BAJO'
                elif confianza_total >= 70:
                    decision['riesgo'] = 'MEDIO'
                else:
                    decision['riesgo'] = 'ALTO'
                
                # Generar razón detallada
                decision['razon'] = self._generar_razon_decision(
                    ia_direccion, confianzas, condiciones_mercado, patrones_similares
                )
                
                # Recomendaciones adicionales
                decision['recomendaciones'] = self._generar_recomendaciones(
                    decision, condiciones_mercado, patrones_similares
                )
                
                self.logger.info(
                    f"✅ DECISIÓN: {decision['accion']} | "
                    f"Confianza: {decision['confianza']}% | "
                    f"Riesgo: {decision['riesgo']}"
                )
                
            else:
                decision['accion'] = 'ESPERAR'
                decision['razon'] = f"Confianza {confianza_total:.1f}% < umbral {umbral_operacion}%"
                
                if ia_direccion is None:
                    decision['razon'] += " | IA sin dirección clara"
                
                if score_mercado < 50:
                    decision['recomendaciones'].append(
                        f"Mercado desfavorable ({score_mercado}%). Esperar mejores condiciones."
                    )
                
                self.logger.info(f"⏸️ ESPERAR: {decision['razon']}")
            
            # Actualizar estadísticas
            self.estadisticas['total_decisiones'] += 1
            
        except Exception as e:
            self.logger.error(f"Error en toma de decisión optimizada: {e}", exc_info=True)
            decision['accion'] = 'ESPERAR'
            decision['razon'] = f"Error: {str(e)}"
            decision['error'] = str(e)
        
        return decision
    
    def _calcular_score_tecnicos(self, indicadores: dict, direccion: str) -> float:
        """Calcula score basado en indicadores técnicos"""
        score = 50.0  # Base neutral
        
        try:
            rsi = indicadores.get('RSI', 50)
            macd = indicadores.get('MACD', 0)
            stoch = indicadores.get('stoch_k', 50)
            
            # RSI scoring
            if direccion == 'CALL':
                if 30 <= rsi <= 70:
                    score += 15
                if rsi < 40:
                    score += 10  # Sobreventa favorable para CALL
                if rsi > 60:
                    score -= 10  # Posible sobrecompra
            elif direccion == 'PUT':
                if 30 <= rsi <= 70:
                    score += 15
                if rsi > 60:
                    score += 10  # Sobrecompra favorable para PUT
                if rsi < 40:
                    score -= 10  # Posible sobreventa
            
            # MACD scoring
            if macd > 0 and direccion == 'CALL':
                score += 10
            elif macd < 0 and direccion == 'PUT':
                score += 10
            elif (macd > 0 and direccion == 'PUT') or (macd < 0 and direccion == 'CALL'):
                score -= 15
            
            # Stochastic scoring
            if stoch < 20 and direccion == 'CALL':
                score += 8
            elif stoch > 80 and direccion == 'PUT':
                score += 8
            
            score = max(0, min(100, score))
            
        except Exception as e:
            self.logger.error(f"Error calculando score técnicos: {e}")
        
        return score
    
    def _generar_razon_decision(self, direccion: str, confianzas: dict,
                                 condiciones: dict, patrones: list) -> str:
        """Genera explicación detallada de la decisión"""
        razones = []
        
        # Razón de IA
        if confianzas['ia'] >= 80:
            razones.append(f"IA muy confiada ({confianzas['ia']:.0f}%)")
        elif confianzas['ia'] >= 60:
            razones.append(f"IA moderadamente confiada ({confianzas['ia']:.0f}%)")
        
        # Razón de patrones históricos
        if len(patrones) > 5:
            wins = sum(1 for p in patrones if p['resultado'])
            razones.append(f"{wins}/{len(patrones)} patrones similares fueron exitosos")
        
        # Razón de condiciones de mercado
        if condiciones['score_favorabilidad'] >= 75:
            razones.append(f"Condiciones de mercado favorables ({condiciones['score_favorabilidad']}%)")
            razones.append(f"Sesión {condiciones['session_mercado']} activa")
        
        # Unir razones
        return "; ".join(razones) if razones else "Decisión basada en análisis integral"
    
    def _generar_recomendaciones(self, decision: dict, condiciones: dict, 
                                  patrones: list) -> List[str]:
        """Genera recomendaciones adicionales para el trader"""
        recomendaciones = []
        
        # Basado en riesgo
        if decision['riesgo'] == 'ALTO':
            recomendaciones.append("⚠️ Considerar reducir tamaño de posición")
            recomendaciones.append("⚠️ Usar stop-loss más ajustado")
        
        # Basado en condiciones de mercado
        if condiciones['volatilidad'] == 'ALTA':
            recomendaciones.append("📊 Alta volatilidad detectada - ajustar expiración")
        elif condiciones['volatilidad'] == 'BAJA':
            recomendaciones.append("📊 Baja volatilidad - considerar esperar mayor movimiento")
        
        # Basado en patrones históricos
        if patrones:
            horas_mejores = defaultdict(int)
            for p in patrones:
                if p['resultado']:
                    horas_mejores[p['patron'].get('hora', 12)] += 1
            
            if horas_mejores:
                hora_optima = max(horas_mejores.keys(), key=lambda h: horas_mejores[h])
                recomendaciones.append(f"🕐 Históricamente mejor resultado a las {hora_optima}:00")
        
        return recomendaciones
    
    # =========================================================
    # 5. RETROALIMENTACIÓN Y MEJORA CONTINUA
    # =========================================================
    
    def registrar_resultado_trade(self, trade_info: dict):
        """
        Registra el resultado de un trade para mejorar futuras decisiones
        """
        try:
            # Agregar a lista de trades
            if not hasattr(self, 'trades_raw'):
                self.trades_raw = []
            
            self.trades_raw.append(trade_info)
            
            # Guardar en archivo
            self._guardar_trades_exitosos()
            
            # Re-analizar patrones periódicamente
            if len(self.trades_raw) % 10 == 0:
                self._analizar_patrones_exitosos()
                self.logger.info("🔄 Patrones actualizados tras 10 nuevos trades")
            
        except Exception as e:
            self.logger.error(f"Error registrando resultado de trade: {e}")
    
    def _guardar_trades_exitosos(self):
        """Guarda trades exitosos en archivo JSON"""
        try:
            data = {
                'version': '3.0',
                'ultima_actualizacion': datetime.now().isoformat(),
                'total_trades': len(self.trades_raw),
                'trades': self.trades_raw
            }
            
            with open(self.trades_exitosos_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Trades guardados: {len(self.trades_raw)}")
            
        except Exception as e:
            self.logger.error(f"Error guardando trades: {e}")
    
    def obtener_estadisticas(self) -> dict:
        """Retorna estadísticas completas del sistema"""
        return {
            'estadisticas_generales': self.estadisticas,
            'patrones_identificados': len(self.patrones_exitosos),
            'perfiles_mercado': len(self.perfiles_mercado),
            'pesos_actuales': {
                'ia': self.peso_ia,
                'patrones_historicos': self.peso_patron_historico,
                'condiciones_mercado': self.peso_condiciones_mercado,
                'indicadores_tecnicos': self.peso_indicadores
            }
        }
    
    # =========================================================
    # MÉTODOS AUXILIARES
    # =========================================================
    
    def _extraer_hora(self, timestamp: str) -> int:
        """Extrae hora de timestamp ISO"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.hour
        except:
            return 12
    
    def _extraer_dia_semana(self, timestamp: str) -> str:
        """Extrae día de la semana de timestamp"""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            return dias[dt.weekday()]
        except:
            return 'Desconocido'


# =============================================================
# EJEMPLO DE USO
# =============================================================

if __name__ == "__main__":
    # Configuración de ejemplo
    class Config:
        UMBRAL_DECISION_INTELIGENTE = 75.0
    
    # Inicializar sistema
    sistema = DecisionInteligenteSistema(config=Config())
    
    # Datos de ejemplo
    indicadores_ejemplo = {
        'RSI': 45,
        'MACD': 0.002,
        'stoch_k': 35,
        'ema_21': 1.0850,
        'ema_50': 1.0840
    }
    
    prediccion_ia = {
        'confianza': 78.5,
        'direccion': 'CALL'
    }
    
    # DataFrame simulado
    df_ejemplo = pd.DataFrame({
        'close': np.random.randn(100).cumsum() + 1.0850,
        'high': np.random.randn(100).cumsum() + 1.0860,
        'low': np.random.randn(100).cumsum() + 1.0840
    })
    
    # Tomar decisión
    decision = sistema.tomar_decision_optimizada(
        df=df_ejemplo,
        indicadores=indicadores_ejemplo,
        prediccion_ia=prediccion_ia,
        simbolo='EURUSD'
    )
    
    print("\n" + "="*60)
    print("DECISIÓN DEL SISTEMA INTELIGENTE")
    print("="*60)
    print(f"Acción: {decision['accion']}")
    print(f"Confianza: {decision['confianza']}%")
    print(f"Riesgo: {decision['riesgo']}")
    print(f"Razón: {decision['razon']}")
    print("\nFactores:")
    for factor, valor in decision['factores'].items():
        print(f"  - {factor}: {valor}")
    
    if decision['recomendaciones']:
        print("\nRecomendaciones:")
        for rec in decision['recomendaciones']:
            print(f"  {rec}")
    
    print("\nEstadísticas del sistema:")
    stats = sistema.obtener_estadisticas()
    print(f"  - Decisiones totales: {stats['estadisticas_generales']['total_decisiones']}")
    print(f"  - Patrones identificados: {stats['patrones_identificados']}")
