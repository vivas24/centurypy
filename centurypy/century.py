import numpy as np
from scipy.integrate import odeint

class Century:

    ACTIVE_CONTAINER_INDEX = 3
    RESPIRATION_CONTAINER_INDEX = 5


    def __init__(self, Necromasa , LN , FraLA ,LENo ,PASo , ACTo , RESPo):
        self.Necromasa = Necromasa
        self.LN = LN
        self.FraLA = FraLA
        self.fs = 0.85 - (0.018 * self.LN)
        self.Ftex = 0.85 - (0.68 * self.FraLA)
        self.ESTo = self.Necromasa * (1 - self.fs)
        self.METo = self.Necromasa * self.fs
        self.LENo = LENo
        self.PASo = PASo
        self.ACTo = ACTo
        self.RESPo = RESPo


    def resolve(self, time, params):
        Kmet = params[0] 
        Kest = params[1]
        Kminl = params[2]
        Khumac = params[3]
        Kminp = params[4]
        ResEL = params[5]
        ResEA = params[6]
        ResMet = params[7]
        ResLA = params[8]
        ResPA = params[9]
        PartEst = params[10]
        PartLen = params[11]
        PartAct = params[12]

        y0 = self.ESTo, self.METo, self.LENo, self.ACTo, self.PASo, self.RESPo
        
        args = (self.Ftex, Kmet, Kest, Kminl, Khumac, Kminp, ResEL, ResEA, ResMet, ResLA, ResPA, PartEst, PartLen, PartAct)
        
        y = odeint(Century.ode, y0, time, args)
        
        return ([row[Century.ACTIVE_CONTAINER_INDEX] for row in y ], [row[Century.RESPIRATION_CONTAINER_INDEX] for row in y ])
    

    @staticmethod
    def ode(y, time, Ftex, Kmet, Kest, Kminl, Khumac, Kminp, ResEL, ResEA, ResMet, ResLA, ResPA, PartEst, PartLen, PartAct):
        ESTo, METo, LENTo, ACTo, PASo, RESPo = y
        
        dESTdt = -ESTo * Kest 
        
        dMETdt = -METo * Kmet 
        
        dLENTdt = ((1 - ResEL) * PartEst * ESTo * Kest)  \
                + ((1 - Ftex - PartAct) * ACTo * Khumac) \
                - (LENTo * Kminl)
        
        dACTdt =  ((1 - ResEA) * (1 -PartEst) * ESTo * Kest) \
                + ((1 - ResMet) * METo * Kmet) \
                + ((1 - ResLA - PartLen) * LENTo * Kminl) \
                + ((1 - ResPA) * PASo * Kminp) \
                - (ACTo * Khumac)
        
        dPASdt =  (PartAct * ACTo * Khumac) \
                + (PartLen * LENTo * Kminl) \
                - (PASo * Kminp) 
        
        dRESPdt = (ResEL * PartEst * ESTo * Kest) \
                + (ResEA * (1 - PartEst) * ESTo * Kest) \
                + (Ftex * ACTo * Khumac) \
                + (ResMet * METo * Kmet) \
                + (ResLA * LENTo * Kminl) \
                + (ResPA * PASo * Kminp)
        
        return (dESTdt, dMETdt, dLENTdt, dACTdt, dPASdt, dRESPdt)
