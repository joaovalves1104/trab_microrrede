import py_dss_interface

dss=py_dss_interface.DSSDLL()

dss_file='C:/pibic/rede/RedeDeDistribuicaoUFPA_util.dss'

dss.text("compile {}".format(dss_file))

dss.text('solve')