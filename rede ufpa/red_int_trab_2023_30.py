import py_dss_interface
import copy
import py_dss_interface
import matplotlib.pyplot as plt
import numpy as np
from random import randint

demanda_ativa2020=6154.00
demanda_ativa2021=2877.84
demanda_ativa2023=5300.00

demanda_ativa=demanda_ativa2023
demanda_ativa_5p=demanda_ativa*1.05

print('MGS UFPA')
dss = py_dss_interface.DSSDLL()
dss_file = r"C:\Users\Gabriel Abel\Downloads\rede ufpa\RedeDeDistribuicaoUFPA_util"

pot_ativa_trifasica_ufpa=[]
menor_tensao=[]
perdas_ufpa=[]

dss.text("compile [{}]".format(dss_file))
dss.text("set number="+str(0))
dss.solution_solve()
n=144
for i in range(0,n):
    ####################################################################################################################
    #compilando
    dss.text("compile [{}]".format(dss_file))
    ####################################################################################################################

    ####################################################################################################################
    #Setando os carros carregando nos eletropostos
    dss.loads_count()
    dss.loads_first()
    for ii in range(0,dss.loads_count()):
        pot_ativa=dss.loads_read_kw()
        pot_reativa=dss.loads_read_kvar()
        dss.loads_write_kw(pot_ativa*1.3)
        dss.loads_write_kvar(pot_reativa*1.3)
        dss.loads_next()
    ####################################################################################################################

    ####################################################################################################################
    #Resolvendo o circuito
    dss.text("set number="+str(i+1))
    dss.solution_solve()
    ####################################################################################################################

    ####################################################################################################################
    # Obtenção dos dados do circuito
    potencia_ufpa = list(dss.circuit_total_power())
    pot_ativa_ufpa = abs(potencia_ufpa[0])
    pot_reativa_ufpa = abs(potencia_ufpa[1])
    tensao_ufpa = list(dss.circuit_all_bus_vmag_pu())
    loss = list(dss.circuit_losses())
    tensao_ufpa_sem_zeros=[]
    for ii in range(0, len(tensao_ufpa)):
        if tensao_ufpa[ii] < 0.4:
            pass
        else:
            tensao_ufpa_sem_zeros.append(tensao_ufpa[ii])
    del tensao_ufpa
    tensao_ufpa = copy.deepcopy(tensao_ufpa_sem_zeros)
    del tensao_ufpa_sem_zeros

    pot_ativa_trifasica_ufpa.append(pot_ativa_ufpa)
    menor_tensao.append(min(tensao_ufpa))
    perdas_ufpa.append(loss[0] / 1000)

x=np.zeros(n)
z=np.zeros(n)
w=np.zeros(n)
u=np.zeros(n)
v=np.zeros(n)
for i in range(0,n):
    x[i] = i*0.166667
    z[i] = demanda_ativa2023
    w[i] = demanda_ativa2023 * 1.05
    u[i] = 0.95
    v[i] = 1.05

y=pot_ativa_trifasica_ufpa
fig, axe = plt.subplots(figsize=(7, 6))
axe.plot(x,y,'-b', x, z, '--k', x, w, '--r')
#axe.set_title("Three-phase active power", fontsize=16)
axe.set_xlabel("Time(hours)", fontsize=12)
axe.set_ylabel("Power(kiloWatts)", fontsize=12)
plt.xticks(np.arange(0, 26, 2))
plt.yticks(np.arange(0, 7500, 500))
plt.grid(True)
plt.savefig(r"C:\Users\Gabriel Abel\Downloads\rede ufpa\resultados\three-phase active power.svg")
plt.show()

y=menor_tensao
fig5, axe5 = plt.subplots(figsize=(7, 6))
axe5.plot(x, v,'--r')
axe5.plot(x, u,'--r')
#axe5.set_title("Lower voltage", fontsize=16)
axe5.set_xlabel("Time(hours)", fontsize=12)
axe5.set_ylabel("Voltage(p.u.)", fontsize=12)
for x5, y5 in zip(x, y):
    axe5.vlines(x5, 0.9, y5, color='blue', linestyle='-', linewidth=1.5, alpha=0.75)
plt.xticks(np.arange(0, 26, 2))
plt.yticks(np.arange(0.9, 1.1, 0.025))
plt.grid(True)
plt.ylim(0.9, 1.1)
plt.savefig(r"C:\Users\Gabriel Abel\Downloads\rede ufpa\resultados\lower voltage.svg")
plt.show()

y=perdas_ufpa
fig6, axe6 = plt.subplots(figsize=(7, 6))
axe6.plot(x,y,'-b')
#axe6.set_title("Active losses", fontsize=16)
axe6.set_xlabel("Time(hours)", fontsize=12)
axe6.set_ylabel("Power(kiloWatts)", fontsize=12)
plt.xticks(np.arange(0, 26, 2))
plt.yticks(np.arange(55, 120, 5))
plt.grid(True)
plt.savefig(r"C:\Users\Gabriel Abel\Downloads\rede ufpa\resultados\active losses.svg")
plt.show()
########################################################################################################################
print('terminei')