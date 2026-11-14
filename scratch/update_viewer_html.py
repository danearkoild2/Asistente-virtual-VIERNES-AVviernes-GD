import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

viewer_path = r'c:\Users\DanearKoild\Desktop\Mark-LV-main\core\live2d\viewer.html'
bak_path = r'c:\Users\DanearKoild\Desktop\Mark-LV-main\core\live2d\viewer.html.bak'

with open(bak_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. New classes to insert before EdithLive2DApp
new_classes = '''
    // ══════════════════════════════════════════════════════════════════════════
    // 4. CONTROLADOR DE FLOTACIÓN HOLOGRÁFICA (HolographicFloatController)
    // ══════════════════════════════════════════════════════════════════════════
    class HolographicFloatController {
      constructor() {
        this.phase = 0.0;
        this.currentMode = 'IDLE';
        this.speed = 1.0;
        this.amplitudeMultiplier = 1.0;
        this.enabled = true;

        // Salidas suavizadas
        this.floatY = 0.0;
        this.floatX = 0.0;
        this.floatScale = 1.0;
        this.bodyTiltZ = 0.0;
        this.chestTiltZ = 0.0;
        this.hipTiltZ = 0.0;

        // Parámetros de transición por estado
        this.targetBaseElevation = 0.0;
        this.currentBaseElevation = 0.0;
        this.targetAmpY = 13.5;
        this.currentAmpY = 13.5;
        this.targetSpeed = 0.85;
        this.currentSpeed = 0.85;
      }

      setMode(mode) {
        this.currentMode = String(mode || 'IDLE').toUpperCase();
        switch (this.currentMode) {
          case 'SLEEPING':
            this.targetAmpY = 5.0;
            this.targetSpeed = 0.45;
            this.targetBaseElevation = 4.0;
            break;
          case 'LISTENING':
            this.targetAmpY = 7.5;
            this.targetSpeed = 0.80;
            this.targetBaseElevation = -2.0;
            break;
          case 'THINKING':
          case 'SEARCHING':
          case 'ANALYZING':
            this.targetAmpY = 11.0;
            this.targetSpeed = 1.25;
            this.targetBaseElevation = -13.0; // Elevación ascendente sutil al computar
            break;
          case 'SPEAKING':
            this.targetAmpY = 8.5;
            this.targetSpeed = 0.95;
            this.targetBaseElevation = -5.0;
            break;
          case 'CELEBRATE':
            this.targetAmpY = 18.0;
            this.targetSpeed = 1.60;
            this.targetBaseElevation = -18.0;
            break;
          case 'ERROR':
            this.targetAmpY = 6.0;
            this.targetSpeed = 0.70;
            this.targetBaseElevation = 2.0;
            break;
          default: // IDLE
            this.targetAmpY = 13.5;
            this.targetSpeed = 0.85;
            this.targetBaseElevation = 0.0;
            break;
        }
      }

      update(dt, state, isSpeaking) {
        if (!this.enabled) {
          this.floatY = 0.0;
          this.floatX = 0.0;
          this.floatScale = 1.0;
          this.bodyTiltZ = 0.0;
          this.chestTiltZ = 0.0;
          this.hipTiltZ = 0.0;
          return;
        }

        const effectiveState = isSpeaking ? 'SPEAKING' : state;
        if (effectiveState !== this.currentMode && this.currentMode !== 'CELEBRATE') {
          this.setMode(effectiveState);
        }

        // Interpolación gradual de estado
        this.currentAmpY += (this.targetAmpY * this.amplitudeMultiplier - this.currentAmpY) * Math.min(1.0, dt * 2.5);
        this.currentSpeed += (this.targetSpeed * this.speed - this.currentSpeed) * Math.min(1.0, dt * 2.5);
        this.currentBaseElevation += (this.targetBaseElevation - this.currentBaseElevation) * Math.min(1.0, dt * 3.0);

        // Fase continua e ininterrumpida
        this.phase += dt * (1.55 * this.currentSpeed);

        // Oscilación vertical multi-armónica (Y)
        const sin1 = Math.sin(this.phase);
        const sin2 = Math.sin(this.phase * 0.48 + 1.15);
        this.floatY = this.currentBaseElevation + (sin1 * 0.78 + sin2 * 0.22) * this.currentAmpY;

        // Deriva horizontal lenta (X)
        this.floatX = Math.sin(this.phase * 0.52 + 0.8) * (this.currentAmpY * 0.26);

        // Pulsación sutil de profundidad 3D (0.35%)
        this.floatScale = 1.0 + (sin1 * 0.0035);

        // Micro-torsión física en columna y cadera
        this.bodyTiltZ = sin1 * 1.35;
        this.chestTiltZ = sin2 * 0.85;
        this.hipTiltZ = -sin1 * 1.10;
      }
    }

    // ══════════════════════════════════════════════════════════════════════════
    // 5. BIBLIOTECA Y CONTROLADOR DE GESTOS SEMÁNTICOS (GestureController)
    // ══════════════════════════════════════════════════════════════════════════
    class GestureController {
      constructor(app) {
        this.app = app;
        this.activeGesture = null;
        this.gestureName = '';
        this.elapsed = 0.0;
        this.duration = 0.0;
        this.attackTime = 0.45;
        this.releaseTime = 0.65;
        this.intensity = 1.0;

        // Memoria de alternancia de brazos durante el habla
        this.lastArmUsed = 'right';
        this.speechSegmentCount = 0;

        // Parámetros de articulación corporal y de mangas
        this.offsets = {
          shoulderL: 0.0,
          shoulderR: 0.0,
          armL: 0.0,
          armR: 0.0,
          armBL: 0.0,
          armBR: 0.0,
          sleeveL: 0.0,
          sleeveR: 0.0,
          sleeveLL: 0.0,
          sleeveLR: 0.0,
          chestZ: 0.0,
          hipZ: 0.0,
          bodyAngleX: 0.0,
          bodyAngleY: 0.0,
          bodyAngleZ: 0.0,
          posZ: 0.0,
          posX: 0.0,
          posY: 0.0,
          headAngleX: 0.0,
          headAngleY: 0.0,
          headAngleZ: 0.0
        };

        this.definitions = this.buildGestureLibrary();
      }

      buildGestureLibrary() {
        return {
          // ── Explicación con alternancia natural de brazos ─────────────────
          EXPLAIN_LEFT: {
            duration: 3.4, attack: 0.45, release: 0.65,
            params: {
              shoulderL: 0.65, armL: 0.55, armBL: 0.45, sleeveL: 0.60, sleeveLL: 0.65,
              shoulderR: -0.15, armR: -0.10, armBR: -0.05, sleeveR: -0.10, sleeveLR: 0.0,
              chestZ: -0.45, bodyAngleX: 3.5, bodyAngleZ: -2.5, posZ: 0.25,
              headAngleX: -2.5, headAngleY: 2.0, headAngleZ: -3.5
            },
            emotion: 'neutral', emotionIntensity: 0.70
          },
          EXPLAIN_RIGHT: {
            duration: 3.4, attack: 0.45, release: 0.65,
            params: {
              shoulderR: 0.65, armR: 0.55, armBR: 0.45, sleeveR: 0.60, sleeveLR: 0.65,
              shoulderL: -0.15, armL: -0.10, armBL: -0.05, sleeveL: -0.10, sleeveLL: 0.0,
              chestZ: 0.45, bodyAngleX: -3.5, bodyAngleZ: 2.5, posZ: 0.25,
              headAngleX: 2.5, headAngleY: 2.0, headAngleZ: 3.5
            },
            emotion: 'neutral', emotionIntensity: 0.70
          },
          EXPLAIN_BOTH: {
            duration: 3.8, attack: 0.50, release: 0.70,
            params: {
              shoulderL: 0.50, armL: 0.45, armBL: 0.35, sleeveL: 0.50, sleeveLL: 0.55,
              shoulderR: 0.50, armR: 0.45, armBR: 0.35, sleeveR: 0.50, sleeveLR: 0.55,
              chestZ: 0.0, bodyAngleX: 0.0, bodyAngleY: 2.5, bodyAngleZ: 0.0, posZ: 0.45,
              headAngleX: 0.0, headAngleY: 3.0, headAngleZ: 0.0
            },
            emotion: 'happy', emotionIntensity: 0.65
          },

          // ── Énfasis en conclusiones o datos cruciales ─────────────────────
          EMPHASIZE: {
            duration: 2.6, attack: 0.25, release: 0.55,
            params: {
              shoulderL: 0.60, shoulderR: 0.60,
              armL: 0.30, armR: 0.30, armBL: 0.40, armBR: 0.40,
              sleeveL: 0.45, sleeveR: 0.45, sleeveLL: 0.40, sleeveLR: 0.40,
              chestZ: 0.0, bodyAngleX: 0.0, bodyAngleY: -2.0, bodyAngleZ: 0.0, posZ: 0.75,
              headAngleX: 0.0, headAngleY: -4.5, headAngleZ: 0.0
            },
            emotion: 'enthusiastic', emotionIntensity: 0.85
          },

          // ── Presentación de opciones o resultados ─────────────────────────
          PRESENT_LEFT: {
            duration: 4.2, attack: 0.50, release: 0.75,
            params: {
              shoulderL: 0.80, armL: 0.70, armBL: 0.60, sleeveL: 0.75, sleeveLL: 0.85,
              shoulderR: -0.20, armR: -0.15, armBR: -0.10, sleeveR: -0.15, sleeveLR: 0.0,
              chestZ: -0.65, bodyAngleX: -7.5, bodyAngleY: 1.5, bodyAngleZ: -4.0, posZ: 0.20,
              headAngleX: -6.0, headAngleY: -1.0, headAngleZ: -5.0, posX: -12.0
            },
            emotion: 'curious', emotionIntensity: 0.80
          },
          PRESENT_RIGHT: {
            duration: 4.2, attack: 0.50, release: 0.75,
            params: {
              shoulderR: 0.80, armR: 0.70, armBR: 0.60, sleeveR: 0.75, sleeveLR: 0.85,
              shoulderL: -0.20, armL: -0.15, armBL: -0.10, sleeveL: -0.15, sleeveLL: 0.0,
              chestZ: 0.65, bodyAngleX: 7.5, bodyAngleY: 1.5, bodyAngleZ: 4.0, posZ: 0.20,
              headAngleX: 6.0, headAngleY: -1.0, headAngleZ: 5.0, posX: 12.0
            },
            emotion: 'curious', emotionIntensity: 0.80
          },

          // ── Confirmación / Asentimiento ───────────────────────────────────
          CONFIRM: {
            duration: 2.8, attack: 0.35, release: 0.50,
            params: {
              shoulderL: 0.20, shoulderR: 0.20,
              armL: 0.15, armR: 0.15, armBL: 0.15, armBR: 0.15,
              sleeveL: 0.20, sleeveR: 0.20, sleeveLL: 0.20, sleeveLR: 0.20,
              chestZ: 0.0, bodyAngleX: 0.0, bodyAngleY: -1.5, bodyAngleZ: 0.0, posZ: 0.30,
              headAngleX: 0.0, headAngleY: -6.0, headAngleZ: 0.0
            },
            emotion: 'happy', emotionIntensity: 0.80
          },

          // ── Búsqueda / Reflexión / Análisis ───────────────────────────────
          THINK_ANALYZE: {
            duration: 3.5, attack: 0.55, release: 0.65,
            params: {
              shoulderL: 0.45, armL: 0.35, armBL: 0.30, sleeveL: 0.35, sleeveLL: 0.40,
              shoulderR: -0.10, armR: 0.0, armBR: 0.0, sleeveR: 0.0, sleeveLR: 0.0,
              chestZ: -0.35, bodyAngleX: -2.5, bodyAngleY: 3.0, bodyAngleZ: -3.0, posZ: -0.15,
              headAngleX: 4.5, headAngleY: 5.5, headAngleZ: 7.5
            },
            emotion: 'curious', emotionIntensity: 0.85
          },

          // ── Advertencia / Cuidado ─────────────────────────────────────────
          WARN_CAUTION: {
            duration: 3.0, attack: 0.30, release: 0.60,
            params: {
              shoulderL: 0.45, shoulderR: 0.45,
              armL: 0.10, armR: 0.10, armBL: 0.20, armBR: 0.20,
              sleeveL: 0.25, sleeveR: 0.25, sleeveLL: 0.25, sleeveLR: 0.25,
              chestZ: 0.0, bodyAngleX: 0.0, bodyAngleY: 0.0, bodyAngleZ: 0.0, posZ: -0.55,
              headAngleX: 0.0, headAngleY: -2.0, headAngleZ: 0.0
            },
            emotion: 'surprised', emotionIntensity: 0.75
          },

          // ── Disculpa ──────────────────────────────────────────────────────
          APOLOGIZE: {
            duration: 3.2, attack: 0.40, release: 0.60,
            params: {
              shoulderL: -0.25, shoulderR: -0.25,
              armL: -0.15, armR: -0.15, armBL: -0.10, armBR: -0.10,
              sleeveL: -0.15, sleeveR: -0.15, sleeveLL: -0.10, sleeveLR: -0.10,
              chestZ: 0.0, bodyAngleX: 0.0, bodyAngleY: -3.0, bodyAngleZ: 0.0, posZ: -0.20,
              headAngleX: 0.0, headAngleY: -7.5, headAngleZ: 2.0
            },
            emotion: 'sad', emotionIntensity: 0.65
          },

          // ── Descubrimiento / Eureka ───────────────────────────────────────
          DISCOVER: {
            duration: 3.2, attack: 0.28, release: 0.60,
            params: {
              shoulderL: 0.70, shoulderR: 0.70,
              armL: 0.60, armR: 0.60, armBL: 0.50, armBR: 0.50,
              sleeveL: 0.65, sleeveR: 0.65, sleeveLL: 0.70, sleeveLR: 0.70,
              chestZ: 0.0, bodyAngleX: 0.0, bodyAngleY: 2.0, bodyAngleZ: 0.0, posZ: 0.50,
              headAngleX: 0.0, headAngleY: 4.0, headAngleZ: 0.0, posY: 10.0
            },
            emotion: 'enthusiastic', emotionIntensity: 0.95
          },

          // ── Saludo / Bienvenida ───────────────────────────────────────────
          GREETING: {
            duration: 3.2, attack: 0.40, release: 0.65,
            params: {
              shoulderR: 0.75, armR: 0.65, armBR: 0.55, sleeveR: 0.70, sleeveLR: 0.75,
              shoulderL: 0.10, armL: 0.05, armBL: 0.0, sleeveL: 0.05, sleeveLL: 0.0,
              chestZ: 0.35, bodyAngleX: 3.0, bodyAngleY: 1.0, bodyAngleZ: 2.0, posZ: 0.25,
              headAngleX: 2.0, headAngleY: -2.0, headAngleZ: 3.5
            },
            emotion: 'happy', emotionIntensity: 0.85
          },

          // ── Despedida ─────────────────────────────────────────────────────
          FAREWELL: {
            duration: 3.4, attack: 0.45, release: 0.70,
            params: {
              shoulderR: 0.65, armR: 0.55, armBR: 0.45, sleeveR: 0.60, sleeveLR: 0.65,
              shoulderL: -0.10, armL: -0.05, armBL: 0.0, sleeveL: 0.0, sleeveLL: 0.0,
              chestZ: 0.25, bodyAngleX: 2.0, bodyAngleY: -1.0, bodyAngleZ: 1.5, posZ: 0.15,
              headAngleX: 1.0, headAngleY: -3.0, headAngleZ: 2.5
            },
            emotion: 'happy', emotionIntensity: 0.75
          }
        };
      }

      setSemanticIntent(intent, metadata) {
        intent = String(intent || 'neutral').toLowerCase().trim();
        metadata = metadata || {};

        let gestureKey = '';
        switch (intent) {
          case 'explain':
          case 'explaining':
            this.speechSegmentCount++;
            if (this.speechSegmentCount % 3 === 0) {
              gestureKey = 'EXPLAIN_BOTH';
            } else if (this.lastArmUsed === 'left') {
              gestureKey = 'EXPLAIN_RIGHT';
              this.lastArmUsed = 'right';
            } else {
              gestureKey = 'EXPLAIN_LEFT';
              this.lastArmUsed = 'left';
            }
            break;

          case 'emphasize':
          case 'emphasis':
          case 'important':
            gestureKey = 'EMPHASIZE';
            break;

          case 'present':
          case 'presentation':
          case 'options':
            gestureKey = (metadata.side === 'right') ? 'PRESENT_RIGHT' : 'PRESENT_LEFT';
            break;

          case 'confirm':
          case 'confirmed':
          case 'agree':
            gestureKey = 'CONFIRM';
            break;

          case 'think':
          case 'search':
          case 'searching':
          case 'analyze':
          case 'analyzing':
            gestureKey = 'THINK_ANALYZE';
            break;

          case 'warn':
          case 'warning':
          case 'caution':
            gestureKey = 'WARN_CAUTION';
            break;

          case 'apologize':
          case 'sorry':
            gestureKey = 'APOLOGIZE';
            break;

          case 'discover':
          case 'discovery':
          case 'celebrate':
            gestureKey = 'DISCOVER';
            break;

          case 'greet':
          case 'greeting':
          case 'hello':
            gestureKey = 'GREETING';
            break;

          case 'farewell':
          case 'bye':
            gestureKey = 'FAREWELL';
            break;

          case 'idle':
          case 'neutral':
          default:
            return;
        }

        if (gestureKey) {
          const intensity = Number(metadata.intensity) || 1.0;
          const duration = Number(metadata.duration) || 0.0;
          this.triggerGesture(gestureKey, duration, intensity);
        }
      }

      triggerGesture(name, duration = 0.0, intensity = 1.0) {
        name = String(name || '').toUpperCase().trim();
        const def = this.definitions[name];
        if (!def) {
          console.warn("[GestureController] Gesto no reconocido:", name);
          return false;
        }

        this.activeGesture = def;
        this.gestureName = name;
        this.elapsed = 0.0;
        this.duration = (duration > 0.0) ? duration : def.duration;
        this.attackTime = def.attack || 0.45;
        this.releaseTime = def.release || 0.65;
        this.intensity = Math.max(0.2, Math.min(1.5, Number(intensity) || 1.0));

        if (def.emotion && this.app && this.app.emotions) {
          this.app.emotions.setEmotion(def.emotion, (def.emotionIntensity || 0.8) * this.intensity, this.duration);
        }

        return true;
      }

      interrupt() {
        if (this.activeGesture) {
          // Recuperación acelerada a neutral en 0.22 s
          this.releaseTime = 0.22;
          this.elapsed = Math.max(this.elapsed, this.duration - this.releaseTime);
        }
      }

      update(dt, state, isSpeaking) {
        if (!this.activeGesture) {
          for (const k in this.offsets) {
            this.offsets[k] += (0.0 - this.offsets[k]) * Math.min(1.0, dt * 5.5);
          }
          return;
        }

        this.elapsed += dt;
        if (this.elapsed >= this.duration) {
          this.activeGesture = null;
          this.gestureName = '';
          return;
        }

        let weight = 0.0;
        const t = this.elapsed;
        const dur = this.duration;
        const att = this.attackTime;
        const rel = this.releaseTime;

        if (t < att) {
          const p = t / att;
          weight = p * p * (3.0 - 2.0 * p);
        } else if (t < (dur - rel)) {
          const sustainPhase = (t - att) * 2.2;
          weight = 1.0 + Math.sin(sustainPhase) * 0.04;
        } else {
          const p = (dur - t) / rel;
          weight = p * p * (3.0 - 2.0 * p);
        }

        weight = Math.max(0.0, Math.min(1.0, weight)) * this.intensity;

        const pMap = this.activeGesture.params || {};
        for (const k in this.offsets) {
          const target = (pMap[k] !== undefined) ? (pMap[k] * weight) : 0.0;
          this.offsets[k] += (target - this.offsets[k]) * Math.min(1.0, dt * 14.0);
        }
      }
    }
'''

# Check if target marker exists
marker = '    // 4. APLICACIÓN PRINCIPAL EDITH LIVE2D PRO (EdithLive2DApp)'
if marker not in content:
    print(f"ERROR: Could not find marker: {marker}")
    sys.exit(1)

content = content.replace(marker, new_classes + '\n' + '    // 6. APLICACIÓN PRINCIPAL EDITH LIVE2D PRO (EdithLive2DApp)')

# In EdithLive2DApp constructor, add floater and gestures initialization
init_marker = 'this.spontaneous = new EdithSpontaneousEngine(this);'
new_init = '''this.spontaneous = new EdithSpontaneousEngine(this);
        this.floater = new HolographicFloatController();
        this.gestures = new GestureController(this);'''

if init_marker not in content:
    print(f"ERROR: Could not find init_marker: {init_marker}")
    sys.exit(1)

content = content.replace(init_marker, new_init)

# In EdithLive2DApp public API methods, add new methods
api_marker = '      setPresentationMode(active) {'
new_api = '''      setSemanticIntent(intent, metadata) {
        if (this.gestures) {
          this.gestures.setSemanticIntent(intent, metadata);
        }
      }

      triggerGesture(name, duration = 0.0, intensity = 1.0) {
        if (this.gestures) {
          return this.gestures.triggerGesture(name, duration, intensity);
        }
        return false;
      }

      interruptGestures() {
        if (this.gestures) this.gestures.interrupt();
        if (this.spontaneous) this.spontaneous.interruptAction();
      }

      setFloatMode(mode) {
        if (this.floater) this.floater.setMode(mode);
      }

      setFloatParams(speed, amp) {
        if (this.floater) {
          if (speed !== undefined) this.floater.speed = Number(speed) || 1.0;
          if (amp !== undefined) this.floater.amplitudeMultiplier = Number(amp) || 1.0;
        }
      }

      setPresentationMode(active) {'''

if api_marker not in content:
    print(f"ERROR: Could not find api_marker: {api_marker}")
    sys.exit(1)

content = content.replace(api_marker, new_api)

# In getStatus(), add gesture and floater data
status_marker = 'activeAction: this.spontaneous.activeAction,'
new_status = '''activeAction: this.spontaneous.activeAction,
          activeGesture: this.gestures ? this.gestures.gestureName : '',
          floatElevation: this.floater ? (this.floater.floatY).toFixed(1) : 0,'''

if status_marker not in content:
    print(f"ERROR: Could not find status_marker: {status_marker}")
    sys.exit(1)

content = content.replace(status_marker, new_status)

# In onTick(), update floater and gestures, and apply parameters to core!
sub_update_marker = '''        this.emotions.update(dt);
        this.gaze.update(dt, this.state, isSleep);
        this.spontaneous.update(dt, this.state, isSleep);

        const emo = this.emotions.current;
        const act = this.spontaneous.offsets;'''

new_sub_update = '''        this.emotions.update(dt);
        this.gaze.update(dt, this.state, isSleep);
        this.spontaneous.update(dt, this.state, isSleep);
        this.floater.update(dt, this.state, this.speaking);
        this.gestures.update(dt, this.state, this.speaking);

        const emo = this.emotions.current;
        const act = this.spontaneous.offsets;
        const flt = this.floater;
        const gst = this.gestures.offsets;'''

if sub_update_marker not in content:
    print(f"ERROR: Could not find sub_update_marker: {sub_update_marker}")
    sys.exit(1)

content = content.replace(sub_update_marker, new_sub_update)

# Update head, neck, body angles, shoulders, arms, sleeves, depth and position
head_angles_marker = '''          const speakNod = isSpeaking ? (Math.sin(now * 12.0) * this.smoothedAmp * 4.2) : 0.0;
          const totalAngleX = Math.max(-30.0, Math.min(30.0, this.gaze.headCurrent.x + act.angleX));
          const totalAngleY = Math.max(-30.0, Math.min(30.0, this.gaze.headCurrent.y + emo.headPitchOffset + act.angleY - speakNod));
          const totalAngleZ = Math.max(-30.0, Math.min(30.0, this.gaze.headCurrent.z + emo.headTiltOffset + act.angleZ));

          core.setParameterValueById('ParamAngleX', totalAngleX);
          core.setParameterValueById('ParamAngleY', totalAngleY);
          core.setParameterValueById('ParamAngleZ', totalAngleZ);

          // Cuerpo y Postura
          const totalBodyX = Math.max(-10.0, Math.min(10.0, (this.gaze.currentGaze.x * 9.0) + act.bodyX));
          const totalBodyY = Math.max(-10.0, Math.min(10.0, (this.gaze.currentGaze.y * 6.0) + act.bodyY));
          const totalBodyZ = Math.max(-10.0, Math.min(10.0, (this.gaze.currentGaze.x * -4.0) + act.bodyZ));

          core.setParameterValueById('ParamBodyAngleX', totalBodyX);
          core.setParameterValueById('ParamBodyAngleY', totalBodyY);
          core.setParameterValueById('ParamBodyAngleZ', totalBodyZ);

          // Inclinación hacia adelante / profundidad
          core.setParameterValueById('ParamPosition_Z', Math.max(-1.0, Math.min(1.0, emo.bodyLeanOffset + act.posZ)));
        }

        // Posición general del modelo con desplazamiento de presentación fluido
        this.currentPresentationOffset += (this.targetPresentationOffset - this.currentPresentationOffset) * Math.min(1.0, dt * 5.0);
        this.model.x = this.baseX + this.currentPresentationOffset + act.posX;
        this.model.y = this.baseY - act.posY;'''

new_head_angles = '''          const speakNod = isSpeaking ? (Math.sin(now * 12.0) * this.smoothedAmp * 4.2) : 0.0;
          const totalAngleX = Math.max(-30.0, Math.min(30.0, this.gaze.headCurrent.x + act.angleX + gst.headAngleX));
          const totalAngleY = Math.max(-30.0, Math.min(30.0, this.gaze.headCurrent.y + emo.headPitchOffset + act.angleY + gst.headAngleY - speakNod));
          const totalAngleZ = Math.max(-30.0, Math.min(30.0, this.gaze.headCurrent.z + emo.headTiltOffset + act.angleZ + gst.headAngleZ));

          core.setParameterValueById('ParamAngleX', totalAngleX);
          core.setParameterValueById('ParamAngleY', totalAngleY);
          core.setParameterValueById('ParamAngleZ', totalAngleZ);

          // Cuerpo y Postura Articulada
          const totalBodyX = Math.max(-10.0, Math.min(10.0, (this.gaze.currentGaze.x * 9.0) + act.bodyX + gst.bodyAngleX));
          const totalBodyY = Math.max(-10.0, Math.min(10.0, (this.gaze.currentGaze.y * 6.0) + act.bodyY + gst.bodyAngleY));
          const totalBodyZ = Math.max(-10.0, Math.min(10.0, (this.gaze.currentGaze.x * -4.0) + act.bodyZ + flt.bodyTiltZ + gst.bodyAngleZ));

          core.setParameterValueById('ParamBodyAngleX', totalBodyX);
          core.setParameterValueById('ParamBodyAngleY', totalBodyY);
          core.setParameterValueById('ParamBodyAngleZ', totalBodyZ);

          // Inclinación hacia adelante / profundidad
          core.setParameterValueById('ParamPosition_Z', Math.max(-1.0, Math.min(1.0, emo.bodyLeanOffset + act.posZ + gst.posZ)));
        }

        // Hombros y Brazos (Gesticulación Semántica Expresiva)
        core.setParameterValueById('ParamAngle_ShoulderL', gst.shoulderL);
        core.setParameterValueById('ParamAngle_ShoulderR', gst.shoulderR);

        // Física y Deformación Dinámica de Brazos
        core.setParameterValueById('ParamArmPhysics_L1', gst.armL);
        core.setParameterValueById('ParamArmPhysics_L2', gst.armL * 0.85);
        core.setParameterValueById('ParamArmPhysics_L3', gst.armL * 0.65);
        core.setParameterValueById('ParamArmPhysics_R1', gst.armR);
        core.setParameterValueById('ParamArmPhysics_R2', gst.armR * 0.85);
        core.setParameterValueById('ParamArmPhysics_R3', gst.armR * 0.65);

        core.setParameterValueById('ParamArmBPhysics_L1', gst.armBL);
        core.setParameterValueById('ParamArmBPhysics_L2', gst.armBL * 0.80);
        core.setParameterValueById('ParamArmBPhysics_R1', gst.armBR);
        core.setParameterValueById('ParamArmBPhysics_R2', gst.armBR * 0.80);

        // Dinámica y Amplitud de Mangas
        core.setParameterValueById('ParamSleevePhysics_L1', gst.sleeveL);
        core.setParameterValueById('ParamSleevePhysics_L2', gst.sleeveL * 0.85);
        core.setParameterValueById('ParamSleevePhysics_R1', gst.sleeveR);
        core.setParameterValueById('ParamSleevePhysics_R2', gst.sleeveR * 0.85);
        core.setParameterValueById('ParamSleeveLPhysics_L1', gst.sleeveLL);
        core.setParameterValueById('ParamSleeveLPhysics_R1', gst.sleeveLR);

        // Torsión y Articulación de Pecho, Caderas y Columna
        core.setParameterValueById('ParamAngle_ChestZ', flt.chestTiltZ + gst.chestZ);
        core.setParameterValueById('ParamAngle_HipZ', flt.hipTiltZ + gst.hipZ);

        // Posición general del modelo con desplazamiento de presentación y flotación holográfica continua
        this.currentPresentationOffset += (this.targetPresentationOffset - this.currentPresentationOffset) * Math.min(1.0, dt * 5.0);
        this.model.x = this.baseX + this.currentPresentationOffset + act.posX + flt.floatX + gst.posX;
        this.model.y = this.baseY - act.posY + flt.floatY + gst.posY;
        this.model.scale.set(this.baseScale * flt.floatScale);'''

if head_angles_marker not in content:
    print(f"ERROR: Could not find head_angles_marker")
    sys.exit(1)

content = content.replace(head_angles_marker, new_head_angles)

# Update debug HUD template
debug_marker = '<b>Action:</b> ${st.activeAction || \'NONE\'}<br>'
new_debug = '''<b>Action:</b> ${st.activeAction || \'NONE\'} | <b>Gesture:</b> ${st.activeGesture || \'NONE\'}<br>
          <b>Float:</b> ${st.floatElevation}px<br>'''

if debug_marker not in content:
    print("Warning: debug_marker not found, skipping HUD text modification")
else:
    content = content.replace(debug_marker, new_debug)

with open(viewer_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: viewer.html updated successfully with HolographicFloatController and GestureController!")
