"""
Proyecto final: Sistema Urinario (Insuficiencia Renal Aguda)
    
Departamento de Ingenierí­a Eléctrica y Electrónica, Ingenierí­a Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Rivera Peñuelas Mariana, Zamora Chon Michelle Ariadna
Número de control: 22210427, 22210432
Correo institucional: l22210427@tectijuana.edu.mx, l22210432@tectijuana.edu.mx
Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerías en consola
#!pip install control
#!pip install slycot

# Librerí­as para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tF, dt, w, h = 0 , 0, 30, 1E-3, 6, 3
N = round((tF-t0)/dt)+1
t = np.linspace(t0,tF,N)
u = np.sin(m.pi/2*t) #Funcion sinusoidal, 1.5708 rad/s = 250 mHz
signal = ['Control', 'Caso']

# Componentes del circuito de control y función de transferencia
Rf= 60
Lf= 100E-3
Rp= 1E3
Cr= 250E-6
numControl = [Rp]
denControl = [Cr*Lf*Rp, Lf+Cr*Rf*Rp, Rp+Rf]
sysControl = ctrl.tf(numControl,denControl)
print(sysControl)

# Componentes del circuito del caso y función de transferencia
Rf= 600
Lf= 100E-3
Rp= 1E3
Cr= 250E-6
numCaso = [Rp]
denCaso = [Cr*Lf*Rp, Lf+Cr*Rf*Rp, Rp+Rf]
sysCaso = ctrl.tf(numCaso,denCaso)
print(sysCaso)

# Componentes del controlador
Rr = 40.3404E3  
Re = 5.0363E-3
Cr = 1E-6
Ce = 998.9458E3
numPID = [Rr*Re*Cr*Ce, Re*Ce+Rr*Cr,1]
denPID = [Re*Cr, 0]
PID = ctrl.tf(numPID,denPID)
print(PID)

#Sistema de control en lazo cerrado
X = ctrl.series(PID, sysCaso)
sysPID = ctrl.feedback(X, 1, sign = -1)
print(sysPID)
sysTratamiento = ctrl.series(sysControl, sysPID)

def plotsignals(u, sysControl, sysCaso, sysTratamiento):    
    fig = plt.figure()
    
    ts, Ve = ctrl.forced_response(sysControl, t, u, x0)
    plt.plot(t, Ve, '-', color = [252/255, 199/255, 55/255], label = '$Control$')
    
    ts, Vs = ctrl.forced_response(sysCaso, t, u, x0)
    plt.plot(t, Vs, '-', color = [231/255, 56/255, 121/255], label = '$Caso$')
    
    ts, VPID = ctrl.forced_response(sysTratamiento, t, u, x0)
    plt.plot(t,VPID,':', linewidth = 3, color = [126/255, 24/255, 145/255], label = '$Tratamiento$')
    
    plt.grid(False)
    
    plt.xlim(0, 10)
    plt.xticks(np.arange(0, 10.1, 5))
    plt.ylim(-1.1, 1.1)
    plt.yticks(np.arange(-1, 1.1, 0.25))

    plt.xlabel('$t$ $[s]$', fontsize = 11)
    plt.ylabel('$V_e(t)$ $[V]$', fontsize = 11)
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 4, fontsize = 8, frameon = False)
    plt.show()
    fig.set_size_inches(w, h)
    fig.tight_layout()
    namepng = 'python_' + 'SistemaUrinarioLC' + '.png'
    namepdf = 'python_' + 'SistemaUrinarioLC' + '.pdf'
    fig.savefig(namepng, dpi = 600, bbox_inches = 'tight')
    fig.savefig(namepdf, bbox_inches = 'tight')
    
# Respuesta del sistema en lazo abierto y en lazo cerrado
plotsignals(u, sysControl, sysCaso, sysTratamiento)
