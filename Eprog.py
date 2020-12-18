# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 05:35:16 2020

@author: justi
"""

import numpy as np
import Eprog

def Calc_Grad(up,u,um,du,Grad_u):
    
    import numpy as np
    
    beta = 1.5
    a1 = beta*abs(u-um)
    #print(a1)
    b1 = beta*abs(up-u)
    #print(b1)
    c1 = 0.5*abs(up-um)
    #print(c1)
    np.seterr('ignore')
    
    if bool(up-u < 0.0) == bool(u-um < 0.0)  or bool(up-u >= 0.0) == bool( u-um >= 0.0):
        if bool(up-u < 0.0):
            const = -1.0
        else:
            const = 1.0
        
        del_u = const*min(a1,b1,c1)
    
    else:
        del_u = 0.0
        
    #print(del_u)
    uphL, uphR, umhL, umhR = Calc_halfs(up,u,um,del_u)
    
    Uph = Calc_uph(uphL,uphR)
    Umh = Calc_umh(umhL,umhR)
    
    Grad_u = (Uph-Umh)/(du)
    
    return(Grad_u)


def Calc_halfs(up,u,um,del_u):
    
    uphL = u + 0.5*del_u
    uphR = up - 0.5*del_u
    
    umhL = um + 0.5*del_u
    umhR = u - 0.5*del_u
    return(uphL, uphR, umhL, umhR)
    
def Calc_uph(uphL, uphR):
    Uph = (uphL+uphR)/2.
    return(Uph)

def Calc_umh (umhL,umhR):
    Umh = (umhL+umhR)/2.
    return(Umh)

def Calc_at_int(up,u,um, Uph, Umh):
    
    import numpy as np
    
    beta = 1.5
    a1 = beta*abs(u-um)
    b1 = beta*abs(up-u)
    c1 = 0.5*abs(up-um)
    
    if bool(up-u < 0.0) == bool(u-um < 0.0)  or bool(up-u >= 0.0) == bool( u-um >= 0.0):
        if bool(up-u < 0.0):
            const = -1.0
        else:
            const = 1.0
        del_u = const*min(a1,b1,c1)
    else:
        del_u = 0.0
        
    uphL, uphR, umhL, umhR = Calc_halfs(up,u,um,del_u)
    
    Uph = Calc_uph(uphL,uphR)
    Umh = Calc_umh(umhL,umhR)
    
    return(Uph,Umh)

def Calc_LR(up,u,um):
    
    import numpy as np
    
    beta = 1.5
    a1 = beta*abs(u-um)
    b1 = beta*abs(up-u)
    c1 = 0.5*abs(up-um)
    
    if bool(up-u < 0.0) == bool(u-um < 0.0)  or bool(up-u >= 0.0) == bool( u-um >= 0.0):        
        if bool(up-u < 0.0):
            const = -1.0
        else:
            const = 1.0
        del_u = const*min(a1,b1,c1)
    else:
        del_u = 0.0
        
    uphL, uphR, umhL, umhR = Calc_halfs(up,u,um,del_u)
    return(uphL, uphR)

def Calc_facevalues(var, varLeft, varRight,dz):
    
    import numpy as np
    
    nAlts =  503
    factor1 = 0.6250000
    factor2 = 0.0416667
    dVarLimited = np.array([0.0 for j in range(1,var.size,1)])
    #print("limit_isze = ", dVarLimited.shape)
    #print("var_size = ", var.shape)
    #print("var_left/right_size = ", varLeft.shape)
    for j in range(2,nAlts-1,1):
        
        h = 2.0/dz[j+1]
        dVarUp = h*(factor1*(var[j+1] -var[j]) - factor2*(var[j+2]-var[j-1]))
        h = 2.0/dz[j]
        dVarDown = h*(factor1*(var[j] -var[j-1]) - factor2*(var[j+1]-var[j-2]))
        
        dVarLimited[j-1] = Eprog.limiter(dVarUp, dVarDown)
        
    j = 1
    dVarUp = (var[j+1]- var[j])/dz[j+1]
    dVarDown = (var[j]-var[j-1])/dz[j]
    dVarLimited[j-1] = Eprog.limiter(dVarUp,dVarDown)
    
    j = nAlts-1
    dVarUp = (var[j+1]- var[j])/dz[j+1]
    #print("dVarUp = ", dVarUp, var[j+1], var[j], dz[j+1])
    dVarDown = (var[j]-var[j-1])/dz[j]
    dVarLimited[j-1] = Eprog.limiter(dVarUp,dVarDown)
    
    for j in range(2,nAlts,1):
        #print(j,j-2)
        varLeft[j-2] = var[j-1] + 0.5*dVarLimited[j-1]*dz[j]
        #print("var, dvarlim, dz = ", var[j-1], dVarLimited[j-1], dz[j])
        varRight[j-2] = var[j] - 0.5*dVarLimited[j]*dz[j]
    #print("varL/R = ", varLeft[0:5], varRight[0:5])
    return varLeft, varRight
        
def Calc_rusanov(var, Gradvar, DiffVar, dz, c_1d):
    
    import numpy as np
    
    varLeft = np.array([ 0.0 for j in range(1,var.size)])
    varRight = np.array([ 0.0 for j in range(1,var.size)])
    DiffFlux = np.array([ 0.0 for j in range(1,var.size)])
    
    #print(varLeft.size, varRight.size, DiffFlux.size)
    #print(varLeft[3:var.size-2].size)
    #print(varRight[3:var.size-2].size)
    #print(varLeft[2:var.size-3].size)
    #print(varRight[2:var.size-3].size)
    varLeft, varRight = Eprog.Calc_facevalues(var,varLeft,varRight, dz)
    #print('varL/R = ', varLeft[0:10], varRight[0:10])
    #print('varL-varR',  0.5*c_1d[5]*(varRight-varLeft)[0:10]/dz[2])
    #print(" ")
    #print("SIZES = ",varLeft.size, varRight.size)
    #print(Gradvar.size)
    #print(varLeft[1:501].size,varLeft[3:var.size-2].size, var.size-2, var.size-1, var.size-3 )
    #print(varRight[1:501].size)
    #print(varLeft[0:500].size)
    #print(varRight[0:500].size)
    Gradvar = 0.5*(varLeft[1:varLeft.size] + varRight[1:varRight.size] - varLeft[0:varLeft.size-1] - varRight[0:varRight.size-1])/dz[5]
    
    #print("Gradvar = ",  Gradvar)
    DiffFlux = 0.5*c_1d[1:var.size]*(varRight - varLeft)
    
    #print(DiffFlux.size, DiffFlux[1:DiffFlux.size].size, DiffFlux[0:DiffFlux.size-1].size, dz[0:dz.size-2].size )
    #print(Diff)
    
    DiffVar = (DiffFlux[1:DiffFlux.size]-DiffFlux[0:DiffFlux.size-1])/dz[1:dz.size-1]
    #print(DiffVar)
    return Gradvar, DiffVar
    
def limiter(dUp, dDown):
    
    import numpy as np
    
    beta = 1.5
    limiter_mc = 0.0
    if dUp > 0.0:
        if (dDown > 0.0):
            limiter_mc = min(beta*dUp, beta*dDown, 0.5*(dUp+dDown))
        else:
            limiter_mc = 0.0
    else:
        if dDown < 0.0:
            limiter_mc = max(beta*dUp, beta*dDown, (dUp+dDown)*0.5)
        else:
            limiter_mc = 0.0
    
    return limiter_mc

    