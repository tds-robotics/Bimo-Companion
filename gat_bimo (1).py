from gpiozero import AngularServo
import time
import threading

class GatBimo:
    def __init__(self, pin_pan=17, pin_tilt=13):
       
        self.servo_pan = AngularServo(pin_pan, min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0024)
        self.servo_tilt = AngularServo(pin_tilt, min_angle=-90, max_angle=90, min_pulse_width=0.0005, max_pulse_width=0.0024)
        
        
        self.PAN_CENTRU = 20.0
        self.TILT_CENTRU = 45.0 
        
        
        self.servo_pan.angle = self.PAN_CENTRU
        self.servo_tilt.angle = self.TILT_CENTRU
        time.sleep(0.5)
        self._elibereaza_motoare()
        
        self.in_miscare = False 

    def _elibereaza_motoare(self):
        
        self.servo_pan.detach()
        self.servo_tilt.detach()
    def homing(self):
       
        if self.in_miscare: return
        self.in_miscare = True
        
        
        
        
        self._miscare_lina(self.servo_pan, self.PAN_CENTRU, 30, 0.005)
        self._miscare_lina(self.servo_pan, 30, -30, 0.005)
        self._miscare_lina(self.servo_pan, -30, self.PAN_CENTRU, 0.005)
        
       
        self._miscare_lina(self.servo_tilt, self.TILT_CENTRU, 70, 0.005) # "Sus" (mai puțin înclinat)
        self._miscare_lina(self.servo_tilt, 70, self.TILT_CENTRU, 0.005) # Revine la repaus
        
        
        self.servo_pan.angle = self.PAN_CENTRU
        self.servo_tilt.angle = self.TILT_CENTRU
        
        
        self._elibereaza_motoare()
        self.in_miscare = False
    def _miscare_lina(self, servo, unghi_start, unghi_final, intarziere=0.005):
        
        
        
        if servo == self.servo_tilt and unghi_final > 90:
            unghi_final = 90
            
        pasi = range(int(unghi_start), int(unghi_final) + 1, 1) if unghi_start < unghi_final else range(int(unghi_start), int(unghi_final) - 1, -1)
        
        for unghi in pasi:
           
            unghi_sigur = max(-90, min(90, unghi))
            servo.angle = unghi_sigur
            time.sleep(intarziere)

   
    
    def salut(self):
       
        if self.in_miscare: return
        self.in_miscare = True
        
        
        self._miscare_lina(self.servo_pan, self.PAN_CENTRU, 20, 0.004)
        self._miscare_lina(self.servo_pan, 20, -20, 0.004)
        self._miscare_lina(self.servo_pan, -20, self.PAN_CENTRU, 0.004)
        
       
        self._miscare_lina(self.servo_tilt, self.TILT_CENTRU, 70, 0.004)
        self._miscare_lina(self.servo_tilt, 70, self.TILT_CENTRU, 0.004)
        
        self._elibereaza_motoare()
        self.in_miscare = False

    def reactie_stres(self):
       
        if self.in_miscare: return
        self.in_miscare = True
        
        
        self._miscare_lina(self.servo_tilt, self.TILT_CENTRU, 55, 0.015) 
        time.sleep(2.5) 
        self._miscare_lina(self.servo_tilt, 55, self.TILT_CENTRU, 0.01) # Revine mai vioi
        
        self._elibereaza_motoare()
        self.in_miscare = False

    def aprobare(self):
       
        if self.in_miscare: return
        self.in_miscare = True
        
        for _ in range(2):
            self._miscare_lina(self.servo_tilt, self.TILT_CENTRU, 65, 0.005)
            self._miscare_lina(self.servo_tilt, 65, self.TILT_CENTRU, 0.005)
            
        self._elibereaza_motoare()
        self.in_miscare = False

    def dezaprobare(self):
       
        if self.in_miscare: return
        self.in_miscare = True
        
        self._miscare_lina(self.servo_pan, self.PAN_CENTRU, 25, 0.005)
        self._miscare_lina(self.servo_pan, 25, -25, 0.005)
        self._miscare_lina(self.servo_pan, -25, self.PAN_CENTRU, 0.005)
        
        self._elibereaza_motoare()
        self.in_miscare = False